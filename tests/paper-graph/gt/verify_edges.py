#!/usr/bin/env python3
"""Verify GT edges: dst must cite src (S2 references, ID then title fallback);
chronology from arXiv YYMM prefix. Incremental cache -> safe to re-run/resume."""
import json
import os
import pathlib
import re
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).parent
KEY = os.environ['S2_API_KEY']
Q = json.loads((HERE / 'queries.json').read_text())
TITLES = json.loads((HERE / 'id_titles_s2.json').read_text())
TITLES['2202.00512'] = 'Progressive Distillation for Fast Sampling of Diffusion Models'
CACHE_P = HERE / 'refs_cache.json'
CACHE = json.loads(CACHE_P.read_text()) if CACHE_P.exists() else {}


def norm(t):
    return re.sub(r'[^a-z0-9 ]', '', (t or '').lower().replace('-', ' '))


def refs_of(aid):
    if aid in CACHE:
        return CACHE[aid]
    url = (f'https://api.semanticscholar.org/graph/v1/paper/arXiv:{aid}/references'
           f'?fields=title,externalIds&limit=1000')
    req = urllib.request.Request(url, headers={'x-api-key': KEY})
    out = 'PENDING'
    for attempt in range(5):
        try:
            data = json.loads(urllib.request.urlopen(req, timeout=40).read())
            out = [[((r.get('citedPaper') or {}).get('externalIds') or {}).get('ArXiv'),
                    (r.get('citedPaper') or {}).get('title')] for r in data.get('data', [])]
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                out = None
                break
            time.sleep(3 + 3 * attempt)
        except Exception:
            time.sleep(3 + 3 * attempt)
    if out != 'PENDING':
        CACHE[aid] = out
        CACHE_P.write_text(json.dumps(CACHE))
    time.sleep(1.2)
    return CACHE.get(aid, 'FETCH_FAILED')


edges, seen = [], set()
for q in Q['queries']:
    for s, d in q['edges']:
        if (s, d) not in seen:
            seen.add((s, d))
            edges.append((q['qid'], s, d))

results = []
for qid, s, d in edges:
    chrono = d[:4] >= s[:4]
    refs = refs_of(d)
    if refs in (None, 'FETCH_FAILED'):
        cited = 'S2_NO_RECORD' if refs is None else 'FETCH_FAILED'
    else:
        ids = {r[0] for r in refs if r[0]}
        if s in ids:
            cited = 'YES_BY_ID'
        else:
            tn = norm(TITLES.get(s, ''))
            hit = tn and any(
                (tn in norm(r[1]) or norm(r[1]) in tn)
                for r in refs if r[1] and len(norm(r[1])) > 20)
            cited = 'YES_BY_TITLE' if hit else 'NOT_FOUND'
    results.append({'qid': qid, 'src': s, 'dst': d, 'cited': cited, 'chrono_ok': chrono})
    print(f"{s} -> {d}  cited={cited} chrono={'ok' if chrono else 'BAD'}"
          + ('' if cited.startswith('YES') and chrono else '   <<< CHECK'), flush=True)

(HERE / 'edge_verification.json').write_text(json.dumps(results, indent=1))
bad = [r for r in results if not r['cited'].startswith('YES') or not r['chrono_ok']]
print(f"\nTOTAL {len(results)} edges, problems: {len(bad)}")
for r in bad:
    print('  PROBLEM:', r)

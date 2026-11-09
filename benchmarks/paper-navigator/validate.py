#!/usr/bin/env python3
"""离线检查70题、参考答案、引用表、历史报告及文件校验值的一致性。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

FIELDS = [
    "id",
    "problem_type",
    "intent_type",
    "paper_query_explicitness",
    "industry_domain",
    "topic_area",
    "time_scope",
    "evidence_requirement",
    "expected_output",
    "source_pattern",
    "query",
]
IDS = [f"Q{i:03d}" for i in range(1, 71)]
REVIEW_STATUS = "candidate_pending_human_review"
VERDICTS = {
    "OK": 2748,
    "DOI_RESOLVES": 19,
    "NEAR": 3,
    "MISMATCH": 2,
    "PDF_OK": 1,
    "EXISTS_ONLY": 1,
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


def normalized_title(text: str) -> str:
    return "".join(
        char
        for char in unicodedata.normalize("NFKC", text).casefold()
        if char.isalnum()
    )


def inline_indices(text: str) -> set[int]:
    indices = set()
    for label in re.findall(r"\[([\d\s,，、\-–—]+)\]", text):
        for token in re.split(r"[,，、\s]+", label):
            span = re.fullmatch(r"(\d+)[\-–—](\d+)", token)
            if span:
                indices.update(range(int(span[1]), int(span[2]) + 1))
            elif token.isdigit():
                indices.add(int(token))
    return indices


def validate(root: Path) -> dict:
    errors, notices = [], []

    def check(condition, message):
        if not condition:
            errors.append(message)

    manifest = read_json(root / "asset_manifest.json")
    check(manifest["review_status"] == REVIEW_STATUS, "manifest: GT状态不一致")
    paths = [entry["path"] for entry in manifest["files"]]
    check(len(paths) == len(set(paths)), "manifest: 文件路径重复")
    expected_paths = {"question_queries_70_same_discipline.csv", "cases.jsonl"}
    expected_paths.update(f"gt/answers/{qid}.md" for qid in IDS)
    expected_paths.update(f"gt/cited/{qid}.json" for qid in IDS)
    expected_paths.update(
        f"gt/{name}"
        for name in [
            "文献表_70题.csv",
            "verify_report.json",
            "trace_stats.json",
            "final_report.md",
            "pilot_report.md",
            "collection_notes.md",
            "doubao_overlap_report.json",
            "豆包检索_70题.xlsx",
        ]
    )
    check(set(paths) == expected_paths, "manifest: 数据资产清单不完整或有额外条目")
    for entry in manifest["files"]:
        path = (root / entry["path"]).resolve()
        if root not in path.parents or not path.is_file():
            errors.append(f"manifest: 文件缺失或路径越界: {entry['path']}")
            continue
        raw = path.read_bytes()
        check(len(raw) == entry["bytes"], f"文件大小变化: {entry['path']}")
        check(
            hashlib.sha256(raw).hexdigest() == entry["sha256"],
            f"SHA-256不一致: {entry['path']}",
        )

    fields, queries = read_csv(root / "question_queries_70_same_discipline.csv")
    check(fields == FIELDS, "题集字段不一致")
    check([row["id"] for row in queries] == IDS, "题号必须为连续唯一的Q001–Q070")
    check(len({row["query"] for row in queries}) == 70, "查询文本缺失或重复")
    check(
        all(set(row) == set(FIELDS) and all(row.values()) for row in queries),
        "题集字段缺失或为空",
    )
    check(len({row["industry_domain"] for row in queries}) == 10, "行业域数量不符")
    check(len({row["problem_type"] for row in queries}) == 9, "问题类型数量不符")
    check(
        Counter(row["paper_query_explicitness"] for row in queries)
        == {"显性": 38, "隐性": 32},
        "显性/隐性分布不符",
    )
    cases = [
        json.loads(line)
        for line in (root / "cases.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    check([case["id"] for case in cases] == IDS, "逐题索引的题号不符")
    by_case = {case["id"]: case for case in cases}

    gt = root / "gt"
    for folder, suffix in [("answers", ".md"), ("cited", ".json")]:
        check(
            {path.name for path in (gt / folder).glob(f"*{suffix}")}
            == {qid + suffix for qid in IDS},
            f"{folder}: 应恰好包含70份逐题文件",
        )
    table_fields, table = read_csv(gt / "文献表_70题.csv")
    check(
        table_fields == ["问题编号", "问题主题", "问题原文", "文献标题", "链接/来源"],
        "文献表字段不符",
    )
    grouped = defaultdict(list)
    for row in table:
        grouped[row["问题编号"]].append(row)
    check(set(grouped) == set(IDS), "文献表题号不符")
    verification = read_json(gt / "verify_report.json")
    verified = {(row["qid"], row["index"]): row for row in verification}
    check(len(verified) == len(verification) == 2774, "核验条目缺失或重复")
    check(
        Counter(row["verdict"] for row in verification) == VERDICTS, "核验分类计数不符"
    )
    corrections = {
        (row["qid"], row["index"]): row
        for row in manifest["known_verification_title_corrections"]
    }
    observed_corrections, reference_keys = set(), set()
    citation_counts = {}
    for query in queries:
        qid = query["id"]
        case = by_case[qid]
        check(
            all(case.get(key) == value for key, value in query.items()),
            f"{qid}: 索引元数据不同",
        )
        check(case["review_status"] == REVIEW_STATUS, f"{qid}: 索引GT状态不同")
        check(
            case["reference_answer"] == f"gt/answers/{qid}.md", f"{qid}: 答案路径不同"
        )
        check(
            case["reference_papers"] == f"gt/cited/{qid}.json", f"{qid}: 引用路径不同"
        )
        cited = read_json(gt / "cited" / f"{qid}.json")
        expected = set(range(1, len(cited) + 1))
        check(
            [row["index"] for row in cited] == sorted(expected),
            f"{qid}: 引用编号不连续",
        )
        check(case["reference_count"] == len(cited), f"{qid}: 索引引用数不同")
        check(len(grouped[qid]) == len(cited), f"{qid}: 文献表引用数不同")
        citation_counts[qid] = len(cited)
        answer = (gt / "answers" / f"{qid}.md").read_text(encoding="utf-8")
        headings = list(
            re.finditer(r"^#{1,6}\s*.*(?:参考文献|References).*$", answer, re.M | re.I)
        )
        if not headings:
            errors.append(f"{qid}: 未找到参考文献章节")
            continue
        body, bibliography = (
            answer[: headings[-1].start()],
            answer[headings[-1].end() :],
        )
        listed = {
            int(value) for value in re.findall(r"^\s*\[(\d+)\]", bibliography, re.M)
        }
        check(listed == expected, f"{qid}: 文末引用编号与结构化引用不同")
        check(inline_indices(body) == expected, f"{qid}: 正文引用存在缺失或越界")
        for ref, row in zip(cited, grouped[qid]):
            key = (qid, ref["index"])
            reference_keys.add(key)
            check(
                (ref["title"], ref["url"]) == (row["文献标题"], row["链接/来源"]),
                f"{key}: 文献表不一致",
            )
            check(
                (row["问题主题"], row["问题原文"])
                == (query["topic_area"], query["query"]),
                f"{key}: 题面不一致",
            )
            url = urlsplit(ref["url"])
            check(
                url.scheme in {"http", "https"} and bool(url.netloc),
                f"{key}: URL格式无效",
            )
            check(ref["url"] in bibliography, f"{key}: 文末缺少引用链接")
            check(
                normalized_title(ref["title"]) in normalized_title(bibliography),
                f"{key}: 文末缺少论文标题",
            )
            historical = verified.get(key)
            if historical is None:
                errors.append(f"{key}: 缺少历史核验记录")
                continue
            check(historical["url"] == ref["url"], f"{key}: 核验链接不一致")
            if historical["title"] != ref["title"]:
                correction = corrections.get(key, {})
                check(
                    correction.get("historical_title") == historical["title"]
                    and correction.get("current_title") == ref["title"]
                    and correction.get("url") == ref["url"]
                    and historical["official_title"] == ref["title"],
                    f"{key}: 未记录的历史标题差异",
                )
                observed_corrections.add(key)
                notices.append(
                    {
                        "qid": qid,
                        "index": ref["index"],
                        "reason": correction.get("reason", "未记录"),
                    }
                )
    check(sum(citation_counts.values()) == len(table) == 2774, "总引用数不符")
    check(reference_keys == set(verified), "引用与核验报告的条目集合不同")
    check(observed_corrections == set(corrections), "历史标题订正清单不一致")

    traces = read_json(gt / "trace_stats.json")
    check(set(traces) == set(IDS), "检索统计题号不符")
    check(sum(row["searches"] for row in traces.values()) == 3719, "历史检索次数不符")
    check(
        all(row["bad_lines"] == 0 for row in traces.values()),
        "历史统计含无法解析的日志行",
    )
    overlap = read_json(gt / "doubao_overlap_report.json")
    check(
        overlap["query_alignment"]
        == {"checked": 70, "identical": 70, "mismatched": []},
        "豆包题面对齐记录不符",
    )
    check({row["qid"] for row in overlap["per_query"]} == set(IDS), "豆包报告题号不符")
    check(
        all(row["gt"] == citation_counts[row["qid"]] for row in overlap["per_query"]),
        "豆包报告GT计数不符",
    )
    for key, value in [
        ("doubao_papers", 421),
        ("doubao_matched_in_gt", 103),
        ("doubao_only", 318),
    ]:
        check(overlap["overall"][key] == value, f"豆包总计不符: {key}")
    check(len(overlap["doubao_only_papers"]) == 318, "豆包补充候选数量不符")
    check(len(overlap["per_query"]) == 70, "豆包逐题报告存在重复或缺失")
    for key, total in [("doubao", 421), ("matched", 103), ("doubao_only", 318)]:
        check(
            sum(row[key] for row in overlap["per_query"]) == total,
            f"豆包逐题计数与总计不符: {key}",
        )
    with zipfile.ZipFile(gt / "豆包检索_70题.xlsx") as workbook:
        check(workbook.testzip() is None, "豆包工作簿ZIP校验失败")

    return {
        "schema_version": 1,
        "status": "failed"
        if errors
        else "passed_with_notices"
        if notices
        else "passed",
        "scope": "离线文件完整性和跨文件一致性；未重新联网检索或核验论文内容。",
        "reference_review_status": REVIEW_STATUS,
        "summary": {
            "manifested_files": len(paths),
            "queries": len(queries),
            "reference_answers": len(citation_counts),
            "citations": len(table),
            "verification_verdicts": dict(
                Counter(row["verdict"] for row in verification)
            ),
            "historical_searches": sum(row["searches"] for row in traces.values()),
            "doubao_papers": overlap["overall"]["doubao_papers"],
            "doubao_matched": overlap["overall"]["doubao_matched_in_gt"],
            "doubao_only": overlap["overall"]["doubao_only"],
        },
        "notices": notices,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument(
        "--report", type=Path, help="可选：将本次离线检查报告写入JSON文件"
    )
    args = parser.parse_args()
    try:
        report = validate(args.root.resolve())
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        report = {"status": "failed", "errors": [str(exc)]}
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.write_text(output, encoding="utf-8")
    print(output, end="")
    return int(report["status"] == "failed")


if __name__ == "__main__":
    raise SystemExit(main())

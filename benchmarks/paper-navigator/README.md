# Paper Navigator: 70 Academic Search Queries

This dataset contains 70 Chinese academic-search queries (`Q001`–`Q070`) for evaluating `paper-navigator` across 10 industry domains and 9 task categories. It includes 38 queries that explicitly request papers and 32 queries with an implicit need for academic evidence.

## Files and format

- [`question_queries_70_same_discipline.csv`](question_queries_70_same_discipline.csv): the query set and its task metadata, preserved from the existing benchmark snapshot.
- Encoding: UTF-8 with BOM and CRLF line endings; one header row and 70 data rows. Use `encoding="utf-8-sig"` when reading it with Python. The local `.gitattributes` preserves the original line endings in Git.
- SHA-256: `8bfdf453a68a7ba53e3249bb133dd09a0cad3e87540eddf6d5b314b6573bf2d1`.

| Column | Meaning |
|---|---|
| `id` | Stable query identifier |
| `problem_type` | Task category |
| `intent_type` | User intent |
| `paper_query_explicitness` | Explicit (`显性`) or implicit (`隐性`) literature request |
| `industry_domain` | Industry domain |
| `topic_area` | Research topic |
| `time_scope` | Requested time range |
| `evidence_requirement` | Evidence needed to answer the query |
| `expected_output` | Expected answer format or content |
| `source_pattern` | Suggested sources for the topic |
| `query` | Original user-facing query text |

## Coverage

The categories below describe the distribution of these 70 queries; this is not a full factorial combination of domains and tasks.

| Industry domain | Queries |
|---|---:|
| AI/软件工程 | 7 |
| 医疗健康 | 8 |
| 金融保险 | 8 |
| 交通/自动驾驶/低空经济 | 7 |
| 能源/矿业/油气 | 6 |
| 制造/工业互联网/机器人 | 6 |
| 农业/生态/环境 | 7 |
| 教育/文化/传媒 | 7 |
| 零售/物流/供应链 | 6 |
| 建筑/城市治理/应急安全 | 8 |
| **Total** | **70** |

| Task category | Queries |
|---|---:|
| 最新论文/SOTA/综述检索 | 10 |
| 原始论文/奠基出处追溯 | 6 |
| 方法对比评估 | 8 |
| 机制原理解释 | 8 |
| 证据/benchmark/数据核验 | 6 |
| 行业应用/治理分析 | 15 |
| 跨学科文献脉络梳理 | 3 |
| 同学科脉络梳理 | 4 |
| 综合分析 | 10 |
| **Total** | **70** |

## Using the queries

Submit the `query` text as the user prompt and use `id` to associate each system output with its evaluation record. The other columns provide evaluator context. If an experiment also supplies these annotations to the system, report that input choice explicitly so comparisons use the same conditions.

Keep the query wording and time constraints intact when comparing systems. Record the evaluation date, model and skill version, available tools, and search budget alongside the outputs; live search results and time-sensitive requests can change over time.

This release contains queries and task metadata. Paper relevance labels, reference answers, and a scoring harness are separate evaluation assets. The metadata describes intended evidence and output requirements; it does not establish answer correctness or define an automatic score.

## Provenance

The file is imported byte-for-byte from the existing 70-query `paper-navigator` benchmark snapshot first committed on 2026-08-06. The original query-authoring prompts and any user-log sampling records are not documented in this snapshot, so it should not be described as a verified sample of production traffic.

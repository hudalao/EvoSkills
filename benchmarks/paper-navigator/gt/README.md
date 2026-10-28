# 70 题参考答案与核验材料

**状态：参考答案候选，整体人工复核待完成。** 本目录保存既有构建记录与数据快照；本次入库进行了离线完整性和跨文件一致性检查，没有重新执行联网检索、论文内容核验或模型评测。

## 材料入口

| 文件 | 内容 |
|---|---|
| `answers/Q001.md`–`answers/Q070.md` | 70 份中文参考答案，含正文编号引用及文末参考文献 |
| `cited/Q001.json`–`cited/Q070.json` | 70 份结构化引用表，每项包含 `index`、`title`、`url` |
| [文献表_70题.csv](文献表_70题.csv) | 2,774 行引用记录，含问题编号、主题、原文、文献标题和链接；引用数包含跨题重复 |
| [verify_report.json](verify_report.json) | 2,774 条历史引用核验记录，按 `qid` 与 `index` 对齐结构化引用 |
| [trace_stats.json](trace_stats.json) | 70 题历史检索次数、工具分布、轮次及饱和曲线统计 |
| [doubao_overlap_report.json](doubao_overlap_report.json) | 豆包独立检索与参考集合的逐题比对、匹配计数及补充候选 |
| [豆包检索_70题.xlsx](豆包检索_70题.xlsx) | 对同 70 题独立检索的工作簿，含 421 条论文结果及查询统计 |
| [collection_notes.md](collection_notes.md) | 原始采集说明，记录候选状态、采集方式、核验与已知边界 |
| [pilot_report.md](pilot_report.md) | 6 题试点报告，记录 15 轮预算实验及正式批调整依据 |
| [final_report.md](final_report.md) | 全量采集与核验报告，含待人工复核重点 |

三份 Markdown 历史报告保留原文，其中运行目录、工具路径和“后续”步骤反映当时的项目状态。当前文件位置以本页、[题集说明](../README.md)和[逐题索引](../cases.jsonl)为准；原始逐次检索日志及采集执行器未包含在本次快照中。

## 如何对齐一题

以 Q001 为例：从主 CSV 或 `cases.jsonl` 获取题面，在 `answers/Q001.md` 查看参考论述，在 `cited/Q001.json` 查看引用列表。正文 `[n]`、文末 `[n]` 和 JSON 的 `index=n` 对应同一条文献；文献表按题号、引用编号顺序展开。历史核验报告使用 `(qid, index)` 定位同一引用。

个别答案正文保留了 `[n](主题说明)` 等原始记法，Markdown 阅读器可能将其显示为相对链接。定位真实文献时，以引用编号、文末参考文献及 `cited/` 中的 URL 为准。

`verify_report.json` 记录的是历史的标题、链接和存在性检查，其 `verdict` 不是论文对题目相关性的分级标签。自动核验通过也不能替代对答案论断、数字、实验条件和引文支持的复核。

## 已知的历史快照差异

**Q021，第 32 条引用**：历史核验报告中的 `title` 保留订正前的转述式标题；答案、结构化引用和文献表已使用官方标题。报告的 `official_title` 与当前引用标题相同，DOI 均为 `10.1016/j.petlm.2020.12.001`。本次保留原报告字节，在 [asset_manifest.json](../asset_manifest.json) 中记录这一订正，离线检查将其作为已知提示展示。

## 离线检查

在仓库根目录执行：

```bash
python3 benchmarks/paper-navigator/validate.py
```

该命令只用 Python 标准库，不需要 API key。它检查文件 SHA-256、70 题对齐、正文与文末引用编号、标题及链接、文献表、历史核验记录和统计计数，并检查豆包工作簿的文件完整性。已提交的 [validation_report.json](../validation_report.json) 记录本次结果。

成功状态为 `passed_with_notices`，当前唯一已知提示为上述 Q021 标题订正；发现缺文件、篡改或未记录的不一致时返回非零退出码。该结果仅表示离线材料一致，参考答案仍保持待人工复核状态。

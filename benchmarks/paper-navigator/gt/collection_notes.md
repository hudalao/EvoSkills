# paper-navigator GT(参考答案集)

**状态:GT 候选,等人工核对**。核对通过前不要当作定稿基准使用。

采集于 2026-08-06:70 题各派一个 Opus 5(effort max)agent 自由深检索(**刻意不按 SKILL.md 流程** —— 该技能是被测对象,GT 必须高于它的天花板),18 轮上限 + 连续两轮零新增即停,S2 Graph API + 网页检索双通道。

## 目录

| 路径 | 内容 |
|---|---|
| `文献表_70题.csv` | **主表**。2774 行 × 5 列(问题编号/问题主题/问题原文/文献标题/链接来源),utf-8-sig |
| `answers/Q0xx.md` | 各题中文答案:正文 [n] 引用标注 + 文末参考文献表。主表每行的**依据**在这里 |
| `cited/Q0xx.json` | 结构化引用表 `[{index,title,url}]`,主表的唯一数据源 |
| `traces/Q0xx.jsonl` | 逐次检索日志(共 3719 次),每行含 round / tool / query / results / new_relevant_count |
| `verify_report.json` | 2774 条链接逐条核验明细 |
| `trace_stats.json` | 各题检索次数、轮数、饱和曲线 |
| `final_report.md` / `pilot_report.md` | 总报告 / 试点阶段报告(含轮次预算实验结论) |
| `豆包检索_70题.xlsx` | **外部补充验证源**。豆包(独立引擎)对同 70 题的检索结果:论文 421 行 + Query 统计 + 标识符分布(3 sheet) |
| `doubao_overlap_report.json` | 豆包结果 vs GT 引用逐题交叉比对(命中/佐证/doubao_only),由 `../harness/gt_doubao_overlap.py` 确定性生成 |

题面来自 `../question_queries_70_same_discipline.csv`(70 题 × 10 行业 × 9 问题类型)。

## 核验结论(详见 `final_report.md` 第四节)

2774 条引用机核通过 **99.06%**;其余为出版方拒绝脚本读标题(DOI 可解析)、中英双语标题、PDF 无 title 等可解释情形,已逐条人工确认。采集中修掉 3 处真实缺陷(整站宕机的中文刊链接换 DOI、agent 转述的标题订正为官方写法、未注册的印刷 DOI 换刊物官网页)。

## 豆包交叉验证(补充验证,2026-09-08)

外部用豆包对**同 70 题**(与 `../question_queries_70_same_discipline.csv` 逐字一致,70/70)独立检索,每题约 5-6 篇、共 421 篇;标识符覆盖:arXiv 30.9% / DOI 25.7% / ACL 5.5% / PubMed 0.2% / 其他 22.6% / 未提供 15.2%。

- **103/421(24.5%)命中 GT**(标识符 53 + 标题精确 47 + 标题模糊 3),对应 GT 侧佐证率 103/2774(3.7%)。豆包每题只取 5-6 篇、GT 每题均约 40 篇,重叠低是结构性结果——**豆包未检到不构成对 GT 条目的否证,命中才计佐证**(仅作正向参考)。
- **318 篇 doubao_only**(豆包检到、GT 未收录)全列于 `doubao_overlap_report.json`,是 GT 完备性的增补候选,供人工核对时参考,不直接并入 GT。其中 Q009(医疗大模型合规治理)整题 0 重合,与下文"中文文献是系统性弱项"边界互相印证。
- 比对可复现:`../harness/gt_doubao_overlap.py`(确定性脚本,无网络调用)。

## 复现与再采集

工具在 `../harness/`:`gt_batch_workflow.js`(全 70 题内嵌,按 `args.ids` 选题)、`gt_progress.py`(进度盘点/清半成品)、`gt_verify_citations.py`(链接核验,`--recheck` 增量复核)、`gt_build_csv.py`(汇总主表)、`gt_trace_stats.py`(饱和统计);流程见 `../harness/GT_RUNBOOK.md`。

原始运行目录(含 agent 中间产物,共 265MB)按仓库惯例不入库,只保留这里的 11MB 交付集。

## 已知边界(设计打分规则时要考虑)

- **中文文献是系统性弱项**:S2 对中文期刊索引极差,各题中文文献靠网页检索救回;多题 notes 写明"中文检索只找到博客/政策文件,未达引用门槛"。
- **未穷尽**:62/70 题打满 18 轮仍有新获,只有 7 题自然停。GT 的完备性上限在**检索模态编排**(bulk 扫库 + 引文图占 25% 检索、贡献最大单轮收获),不在轮数。
- **负结论是高价值锚点**:Q012(无同数据集 GNN vs 序列 Transformer 正面对比)、Q018(无榜单排名 vs 实路排名对比)、Q031(无季节轴 benchmark)、Q036(无 Assmann 理论 KG 本体)—— 技能若为这些点编造文献,可直接判错。

# paper-graph 评测 GT

## queries.json

8 个查询：topic ×4（q1 高效注意力 / q2 扩散采样加速 / q3 RAG / q4 test-time 推理）、
seed ×2（q5 LoRA / q6 FlashAttention）、hybrid ×2（q7 偏好优化+DPO / q8 VLM+CLIP）。
**刻意排除 speech-SSL 域**：SKILL.md 自带 BEST-RQ 示例，属于"训练样例"，用它评测会高估。

每个查询三层 GT：

- `anchors[]` — 必现论文（arXiv ID 级比对报告 appendix，`expect` 仅为构建期人工核验用的标题片段，不参与打分）。
  58 个唯一 ID 已全部核验（2026-07-16）：57 个经 S2 API 标题比对，1 个（2202.00512
  Progressive Distillation）S2 无索引、经 arXiv abs 页确认。
- `edges[]` — 经典演化边 `[src, dst]`（dst evolves-from src）。计边召回：报告中存在同向
  paper-to-paper 边即命中。42 条全部为"dst 明确以 src 为改进对象"的强边（构建者人工判定），
  concurrent/平行工作一律不入 GT 边。
  **引用+时序已全量联网核验（2026-07-17，见 edge_verification.json）**：41 条唯一边中
  37 条经 S2 references 按 ID 命中，4 条因 S2 数据缺陷（缺记录/引用列表不全）改用 dst PDF
  参考文献 grep 直查命中；时序 41/41 合法。注意"dst 引用 src"是演化关系的必要条件，
  "以 src 为改进对象"的语义层仍是构建者专家判断。
- `taxonomy_hint` — judge 软评 taxonomy 时的锚（不是唯一正确答案，是"合理分类应覆盖的分支"）。

## 已知坑（评分实现时必须处理）

1. **S2 索引缺口**：2202.00512 在 S2 无记录。引用一致性检查（B cites A）遇到无法解析的
   ID 时按"标题模糊匹配 references 列表"降级，仍失败记 `unverifiable` 而非 `fail`。
   该论文同时是 q2 检索覆盖率的天然难点——技能 fetch 走 S2 找不到它属于真实发现，不是 GT 错误。
2. **锚点召回口径**：以报告 appendix 的 arXiv ID 集合算；无 ID 的条目回退标题模糊匹配
   （去连字符、小写、80% 相似度）。
3. **边方向**：时序检查 year(dst) ≥ year(src) 对全部 42 条 GT 边成立；报告边若反向，
   记方向错误而非未命中。

## 待建（顺序）

- [x] audit_edge 微基准（2026-07-17 建成）：`../edge_bench/` — 40 对（20 真边全部取自已验证
  集 + 20 难负例：同域并行 10、错轴归因 5、时序反向 2、跨域哨底 2、并发伪谱系 2 —— 真实分布
  见 pairs.json 的 category），prompt 用技能自带 audit_edge.md 模板组装，材料 S2 batch +
  PD 本地 PDF 提取。运行：`edge_bench/run_edge_bench.sh <model>`（40 次一发调用，可断点续跑，
  自动打分）。指标：真边存活率（≠REJECT）+ 假边拒绝率（=REJECT）+ 分 category 混淆。
- [x] 检索冻结（2026-07-17）：`../fixtures/<qid>/` 8/8 齐（parse 层为 harness 中立、Fable 产出并
  程序化校验约束）。**头条发现：锚点召回 9/61 = 14.8%（q1/q4 为零）**，n=30 敏感性探针证明是
  S2 相关性排序问题而非预算，详见 anchor_recall_frozen.json（含 16.4%→14.8% 的匹配器缺陷更正记录）。
- [x] check_graph.py（2026-07-17，harness/ 下）：按渲染器真实语法解析（`_P{src} -->|Gap...| _P{dst}`、
  appendix `**({i}) [title](url)**`）；结构/lint（mmdc 编译为 auto 降级模式）/幻觉编号/引用一致性
  （S2-ID→标题→unverifiable 降级链，fixture 的 `arxiv_id` 字段+url 兜底解析）/时序/锚点边召回/
  伪造压力（噪声-噪声边及其引用失败率）。合成报告冒烟通过：四类故障模式全部检出。
- [ ] e2e 执行器设计（下一阶段）：SUT 从 fixture（步骤 6）起跑 runbook 至 13，需 Bash 白名单 +
  uv 环境；产物交 check_graph.py + judge 侧 taxonomy 软评/边语义抽查（prompt 须区别于技能自带
  audit_edge 模板）。

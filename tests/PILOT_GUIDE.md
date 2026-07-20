# paper-rebuttal 评测 Pilot 运行指南

3 个 ICLR 2026 真实 case，双臂对照（skill-on vs skill-off），Claude Code headless 执行。
本目录整体在 .gitignore 里，所有产物只落本地。

---

## 0. 一次性准备

**登录 CLI**（二选一）：

```bash
claude /login          # 浏览器授权一次
```

或者在 `tests/.env` 里加一行（runner 会自动加载）：

```
ANTHROPIC_API_KEY=sk-ant-...
```

**验证**（应输出 OK 而不是 Not logged in）：

```bash
claude -p "reply with exactly: OK" --model claude-sonnet-5
```

其他依赖：只需系统 python3（≥3.9，纯标准库）。S2 key 这轮用不到。

---

## 1. 跑整个矩阵（推荐）

```bash
cd ~/Developer/evoskill
caffeinate -i tests/harness/run_matrix.sh claude-sonnet-5
```

- 3 case × 2 臂 = 6 次运行，串行，预计 **15–40 分钟**。
- 费用量级：单次运行输入 4–10 万 token（case 03 论文最长），全程大约 **几美元、不超过 $10**。
- `caffeinate -i` 防止 Mac 睡眠，可省略。
- 结果目录默认 `tests/harness/runs/<时间戳>/`，跑完自动打印汇总表。

只想先试单个（比如最便宜的 case 02 基线臂）：

```bash
tests/harness/run_case.sh tests/paper-rebuttal/cases/02-reject-compute-teacher base claude-sonnet-5 /tmp/pilot-试跑
python3 tests/harness/check_rebuttal.py tests/paper-rebuttal/cases/02-reject-compute-teacher /tmp/pilot-试跑/ws --meta /tmp/pilot-试跑/meta.json
```

---

## 2. 每次运行发生了什么

`run_case.sh` 为每次运行建隔离工作区：

```
runs/<ts>/<case>-<arm>/
├── ws/                  # SUT 的工作区
│   ├── input/           #   paper.md + reviews.json（评论已预编号 R1.W2 式）
│   ├── output/          #   SUT 应产出 analysis.json + rebuttal.md
│   └── .claude/skills/  #   仅 skill 臂：拷入 paper-rebuttal 技能
├── transcript.jsonl     # 完整事件流（工具调用、token 用量都在里面）
├── meta.json            # 臂/耗时/退出码/技能是否被触发
├── metrics.json         # checker 的全部确定性指标
└── stderr.log
```

要点：

- 双臂 **prompt 完全相同**（`cases/<id>/prompt.txt`），唯一差异是技能在不在工作区。
- 工具白名单只有 Read/Write/Edit/Glob/Grep/Skill，**无法联网**——这很重要，因为这三篇的真实 rebuttal 和结局就挂在 OpenReview 上。
- skill 臂拷贝技能时会删掉 frontmatter 的 `allowed-tools` 行（那些是 EvoScientist 家的工具名，Claude Code 不认识会锁死工具集）。这是宿主适配，不改技能内容。

---

## 3. 读结果

汇总表列含义（`summarize.py` 随时可重跑：`python3 tests/harness/summarize.py tests/harness/runs/<ts>`）：

| 列 | 含义 | 期望 |
|---|---|---|
| ok | 两个输出文件都产出且可解析 | Y |
| champ | 最友好审稿人判对（03 判 R1 或 R4 都算对） | Y |
| prioP / prioR | high 优先级 vs GT 分数驱动项的精确率/召回率 | 越高越好，重点看双臂差 |
| cons | 共识主题检出数 / GT 总数（跨审稿人同类意见归并） | 3/3 或 4/4 |
| cov | rebuttal 对全部评论 ID 的覆盖率 | 1.0 |
| hi% | 回应字数花在高优先级意见上的占比 | 技能教 60%，看双臂差 |
| fab | 疑似编造数字候选数（**候选≠实锤**，终判留给后续 judge 环节） | 越少越好 |
| skill | 技能是否真被触发（base 臂恒为 n） | skill 臂应为 Y |
| sec | 运行耗时 | — |

深挖单次运行：`metrics.json` 有逐项明细（漏了哪几个高优先级 ID、哪个共识主题没检出、编造候选的上下文片段）；`ws/output/rebuttal.md` 值得人工读一两份。

---

## 4. 常见问题

- **Not logged in**：第 0 步没完成，或 .env 里 key 名写错。
- **exit_code 非 0 且 output/ 为空**：看 `stderr.log` 和 `transcript.jsonl` 最后几行；若是 max-turns 打满（默认 60），记下 case 名。
- **skill 臂 skill=n**（技能没触发）：这本身就是重要发现（技能 description 触发失败），不要重跑抹掉，保留该目录。
- **checker 报 analysis_parse_error**：SUT 没按 schema 输出，也是有效发现，metrics.json 里会记录。
- 某次运行想重打分（不重跑模型）：单独执行 `check_rebuttal.py`（命令见第 1 节）。

## 5. 先别下的结论

这轮是 n=1 的 pilot：没有重复运行、judge 侧指标（误报判定、说服力盲评）还没上、fab 列只是候选。**目的是验证管线 + 看方向性信号**，不是出结论。

## 5.5 Judge 环节（矩阵跑完后，同样在你本地跑）

一条命令跑全部三类 judge（编造裁决 / 回应质量 / 双臂盲评×2 轮位置交换）：

```bash
tests/harness/judge_all.sh tests/harness/runs/<你的runs目录> <judge模型>
# 例如： tests/harness/judge_all.sh tests/harness/runs/glm52-20260716-070215 zhipu-coding/glm-5.2
```

- judge 模型传你 CLI 能用的任意模型名；有 Anthropic 侧账号时建议换 opus/fable 复判一遍。
- 所有判定强制附带**逐字引文**并被脚本核验（`quote_verified: false` 的判定视为作废）。
- 盲评做两轮 A/B 位置交换，两轮不一致记 tie，防位置偏好。
- 产物写回每个 run 目录：`judge_fab.json` / `judge_quality.json` / `judge_pairwise.json`，脚本最后打印汇总。
- 费用：约 15 次小型调用，比矩阵便宜一个量级。
- 已知局限：GLM 判 GLM 有自评偏好风险——引文核验 + 同模型对称盲评已部分缓解，最终结论建议用第二家模型复判。

## 5.8 rebuttal 正式集（n=10 全量）

case 04–10 已建好并完成 GT 标注（04↔05 同分带配对、06/07 split-reject、08 全正分、09/10 oral-mixed）。跑法与 pilot 完全一致，直接全量：

```bash
# 不带 case 参数 = 跑全部 10 个 case × 2 臂 = 20 次运行，串行约 5-6 小时，建议过夜
caffeinate -i tests/harness/run_matrix.sh zhipu-coding/glm-5.2 tests/harness/runs/formal-glm52
```

- 20 次里包含重跑 pilot 3 个 case——这是特意保留的：同条件重跑给出 run-to-run 方差估计，补上 pilot "n=1" 的口径缺陷。只想跑 7 个新 case（14 次）的话，把 `tests/paper-rebuttal/cases/0[4-9]-* tests/paper-rebuttal/cases/10-*` 追加到命令末尾。
- 跑完 judge 环节由我起子 agent 做（同 pilot：盲评封印映射 + 引文核验），你不用跑 judge_all。
- 注意 07 的论文输入较大（多图 CV 论文），单次运行可能偏慢，属正常。

## 5.9 paper-review 矩阵（第二个技能，样本已建好）

15 个 case（5 篇 ICLR 2026 录用论文 × V0 干净对照 / V1 中等 4 雷 / V2 高难 5 雷），每个 case 双臂。埋雷明细在各 `cases/<paper>-<variant>/gt/defects.json`（对 SUT 不可见）。

```bash
# 先冒烟：单篇论文的 3 个变体（6 次运行）
SKILL_NAME=paper-review tests/harness/run_matrix.sh <模型> \
  tests/harness/runs/review-smoke \
  tests/paper-review/cases/cocomix-v0 tests/paper-review/cases/cocomix-v1 tests/paper-review/cases/cocomix-v2

# 全量：15 case × 2 臂 = 30 次运行（串行约 4-6 小时，建议过夜跑）
SKILL_NAME=paper-review tests/harness/run_matrix.sh <模型> tests/harness/runs/review-full
```

- 输入是 LaTeX 全文（67–222KB），单次运行成本与 rebuttal 同量级。
- checker 只出结构指标（findings.json 合规、major/minor 计数）；埋雷命中率由 `judge.py review-match` 产出、误报率由 `judge.py review-fp` 产出（**顺序：先 match 后 fp**）。
- V0 对照臂的发现数是误报基线的原料，别跳过。
- 汇总表 review 行的列语义：`ok`=产出且可解析、`prioP`=埋雷严格召回（judge match 后才有值）、`prioR`=宽松召回（含 PARTIAL）、`cons`=major/minor 发现数、`cov`=major 发现的误报率（judge fp 后才有值）、`fab`=判为不实的发现数、`skill`=技能是否触发。

## 5.95 paper-graph e2e 矩阵（第三个技能）

8 个查询 case（检索已冻结进 `cases/<qid>/input/`，SUT 从 classify 步起跑），双臂同 prompt（含输出契约，checker 对两臂通用）。**graph 臂特殊点**：允许 Bash（skill 的 uv CLI 需要）、max-turns 150、S2 key 注入假值（防重抓=构造性密封）。

```bash
# 先导航试跑：1 topic + 1 seed × 2 臂 = 4 次（单次可能 20-50 分钟，比 rebuttal 慢）
SKILL_NAME=paper-graph tests/harness/run_matrix.sh zhipu-coding/glm-5.2 \
  tests/harness/runs/graph-pilot \
  tests/paper-graph/cases/q2-diffusion-sampling tests/paper-graph/cases/q5-seed-lora

# 全量：8 case × 2 臂 = 16 次，务必过夜
SKILL_NAME=paper-graph tests/harness/run_matrix.sh zhipu-coding/glm-5.2 tests/harness/runs/graph-full
```

- 汇总表 graph 行的列语义不同：`prioP`=锚点召回、`prioR`=GT边召回、`cons`=引用验证边/总边、`cov`=时序违规数、`hi%`=噪声-噪声边中引用失败数、`fab`=幻觉编号数。
- 注意：锚点召回的天花板是检索冻结层的 14.8%——这列低不是 SUT 的锅，看的是双臂差和边质量列。
- skill 臂已知风险（属评测对象）：SKILL.md 里 CLI 路径写死 `EvoScientist/skills/...` 前缀，与挂载路径不符，看 SUT 能否自行定位——这是真实的可移植性考点，勿提前修。
- 深挖单次运行：`metrics.json` 里有逐边引用/时序判定；judge 侧（taxonomy 软评、边语义抽查）等矩阵跑完我起子 agent 做。

## 6. 跑完之后

把汇总表贴给我，或直接告诉我 runs 目录路径，我来做逐项分析（含双臂 diff、transcript 里的技能遵从度检查），然后我们定下一步：补 judge、扩到 10 case、还是先修 prompt/技能。

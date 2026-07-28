# 人工盲评表操作手册（实习生版）

本手册教你**准备一张人工盲评表**：把同一批 case 在两个臂（例：无技能基线 vs 某技能版本）下的产出配对、匿名成 A/B，交给人类评委逐 case 填胜负，再回收进持久台账 `ledger.csv`。协议设计与统计口径以英文版 [README.md](README.md) 为准；本文只管操作。

**什么时候做**：矩阵执行（见 [../INTERN_RUNBOOK.md](../INTERN_RUNBOOK.md)）跑完、`tests/harness/runs/<目录>` 里已有成对的 `{case}-{tag}` 产物之后。

**前置**：只需系统 python3（纯标准库，无需装依赖）。

## 1. 生成盲评工作区

在 `tests/human-eval/` 目录下执行（以 paper-graph、无技能 vs v0.1.1 为例）：

```bash
python3 blind_prep.py --skill paper-graph \
  --runs ../harness/runs/graph-full \
  --baseline-tag base --baseline-ref no-skill \
  --candidate-tag skill --candidate-ref v0.1.1 \
  --artifact ws/output/report.md --extra ws/input/query.txt \
  --sut <SUT模型字符串> --out judge_ws/graph-<模型简称>-base-vs-v011
```

参数含义：

| 参数 | 填什么 |
|---|---|
| `--runs` | 矩阵产物目录（内含 `{case}-{tag}` 子目录） |
| `--baseline-tag` / `--candidate-tag` | 子目录名的臂后缀（run_matrix.sh 产出即 `base` / `skill`） |
| `--baseline-ref` / `--candidate-ref` | 记入台账的版本号；无技能臂固定写 `no-skill`，技能臂写版本 tag（如 `v0.1.1`） |
| `--artifact` | 被评的交付物在 run 目录内的路径（见下表） |
| `--extra` | 评委需要看的上下文文件，可重复多次；原样复制、不匿名 |
| `--sut` | 跑矩阵用的模型字符串，与运行时完全一致 |
| `--out` | 工作区输出目录，建议 `judge_ws/<技能>-<模型简称>-<基线>-vs-<候选>` |

各技能的 `--artifact` / `--extra` 对照：

| 技能 | `--artifact` | `--extra`（评委上下文） |
|---|---|---|
| paper-graph | `ws/output/report.md` | `ws/input/query.txt` |
| paper-rebuttal | `ws/output/rebuttal.md` | `ws/input/paper.md`、`ws/input/reviews.json` |
| paper-review | `ws/output/self_review.md` | `ws/input/main_flat.tex` |

成功时打印 `N blinded cases -> ...（candidate as A in k/N; mapping sealed）`。A/B 位置按 case 自动均衡且可复现，不由人挑选。若提示某 case 只在一个臂存在，会跳过该 case——正常（对应臂跑失败时会这样），回传时说明即可。

**两个技能版本对比（v0.1.0 vs v0.1.1）**：两个版本各跑一遍矩阵后，臂后缀都叫 `-skill`、分居两个 runs 目录，需要先做一个软链合并目录再喂给 `--runs`：

```bash
mkdir -p ../harness/runs/graph-v010-vs-v011
for d in ../harness/runs/graph-full-v010/*-skill; do
  c=$(basename "$d" -skill); ln -s "$(cd "$d" && pwd)" "../harness/runs/graph-v010-vs-v011/$c-v010"
done
for d in ../harness/runs/graph-full-v011/*-skill; do
  c=$(basename "$d" -skill); ln -s "$(cd "$d" && pwd)" "../harness/runs/graph-v010-vs-v011/$c-v011"
done
```

然后 `--runs ../harness/runs/graph-v010-vs-v011 --baseline-tag v010 --candidate-tag v011 --baseline-ref v0.1.0 --candidate-ref v0.1.1`。

## 2. 表长什么样、评委怎么填

工作区结构：

```
judge_ws/<名字>/
  README.md            # 评审规则（自动生成，英文）
  verdicts.tsv         # ← 评委要填的表
  .mapping.json        # A/B 与臂的对应，封存：判决收齐前任何人不得打开
  <case-1>/
    query.txt          # 上下文（未匿名）
    report_A.md        # 匿名产出 A
    report_B.md        # 匿名产出 B
  <case-2>/ ...
```

`verdicts.tsv` 每行一个 case，制表符分隔，填三列：

| 列 | 填法 |
|---|---|
| `winner` | `A` / `B` / `tie` |
| `margin` | 非平局必填 `clear`（明显）或 `slight`（略胜）；平局必须留空 |
| `reason` | 非平局必填一行理由；文字里不要出现制表符 |

评审纪律（对评委逐条讲清）：

1. 判决收齐前**不得打开** `.mapping.json`、runs 目录、旧的 judge/tally 报告。
2. 逐 case 读 `query.txt`（或对应上下文）+ `report_A.md` + `report_B.md` 再下判断；每行都要填，不能跳。
3. 评「用户拿到手的交付物质量」：正确性、是否忠实回应输入、结构与可用性——**不评排版口味**。
4. 用能保留制表符的编辑器填表（VS Code 正常；勿让编辑器把 tab 转成空格，否则回收时整行报错）。

## 3. 回收进台账

评委填完后：

```bash
python3 tally.py ingest judge_ws/<名字> --judge <评委姓名缩写>
```

该命令会校验表格完整性→解封 mapping→把 A/B 还原成 candidate/baseline→追加进 `ledger.csv`→打印本组胜率。校验不过时 mapping 保持封存，按报错逐行改（常见：winner 拼写不对、平局带了 margin、非平局缺 reason、tab 被转成了空格导致整行读不出）。

同一（技能 × case × 版本对 × 评委）重复回收会被拒收；确要覆盖旧判决加 `--force`。LLM 评委的判决也能进同一台账（`--judge <模型名> --judge-type llm`），人机一致率会在报告里自动算出。

## 4. 看汇总

```bash
python3 tally.py report              # 全部
python3 tally.py report --skill paper-graph
```

输出各版本对的 W/T/L、去平局胜率、符号检验 p 值。注意：单对 case 数太少时只有一边倒的结果才显著（协议目标是每技能 ~20 个 case；8 个 case 时几乎全胜才算数）——解读交给负责人，你只需保证数据如实回收。

## 5. 回传什么

`judge_ws/` 与 runs 均不进 git；**`ledger.csv` 是唯一持久记录**。每轮评完回传：

1. `ledger.csv`（必须）；
2. 整个 `judge_ws/<名字>/` 打包（建议，便于抽查）：`tar czf <名字>.tgz -C judge_ws <名字>/`。

## 6. 红线（Do NOT）

1. 不要在判决收齐前打开 `.mapping.json`——盲评作废，整轮重来。
2. 不要手改 `ledger.csv`——只能经 `tally.py ingest` 写入。
3. 不要挑着 case 评或重跑产出去「修」难看的结果；产出是什么就评什么。
4. 不要把 runs 产物、judge_ws、ledger 上传到公开仓库/网盘。

拿不准的：**停下来问**，不要自行发挥。

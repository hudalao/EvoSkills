# 评测执行手册（实习生版）

本手册覆盖**矩阵执行**（SUT 运行与产物回传）这一段的操作细节；judge 环节同样可以自己跑（`judge.py` 各模式 + `blind_prep.py`，见方法参考 §3 与附录 B）。唯一的请求：评测集与 GT（`cases/`、`gt/`、`fixtures/`）先保持原样跑出第一批可比数据，之后要怎么演进由你们决定。

## 0. 环境准备（新机器从零开始，约 15 分钟）

前置：macOS/Linux，python3 ≥ 3.9，能访问 arXiv/S2 的网络。

```bash
# 1) claude CLI（如未装）并完成登录/配置——用负责人指定的账号与模型代理
npm install -g @anthropic-ai/claude-code   # 或按公司内部方式安装
claude -p "reply with exactly: OK" --model <指定的SUT模型>   # 必须输出 OK 才继续

# 2) uv（paper-graph 的技能 CLI 需要）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3) node（mermaid 编译需要；首跑会自动下载 chromium，属正常）
curl -so- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh" && nvm install --lts

# 4) harness 的 python 依赖
cd tests/harness && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# 5) （可选）tests/.env 里填 S2_API_KEY=<负责人提供或你自己申请的key>
#    没有它 SUT 运行不受影响，只是 graph checker 的引用一致性列会显示 unverifiable，
#    分析阶段会在负责人侧重打，无需担心。
```

**SUT 模型**：全程使用负责人指定的同一个模型字符串（例：`zhipu-coding/glm-5.2`）。中途换模型会毁掉可比性。

## 1. 三条独立任务（无先后依赖，任意顺序）

三个技能的评测**互相之间没有任何依赖**——A/B/C 可以按任意顺序跑、分几天跑、在不同机器上并行跑（同一账号同时跑两个矩阵会互抢限速，单机建议串行）。全部命令在**仓库根目录**执行，建议都套 `caffeinate -i`（Mac 防休眠）。

```bash
# A. rebuttal 全量：10 case × 2 臂 = 20 次，约 5-6 小时
caffeinate -i tests/harness/run_matrix.sh <模型> tests/harness/runs/formal-<模型简称>

# B. review 全量：15 case × 2 臂 = 30 次，约 5-6 小时
SKILL_NAME=paper-review caffeinate -i tests/harness/run_matrix.sh <模型> tests/harness/runs/review-full

# C. graph（内部分两步，这是唯一的顺序要求）
# C1 先导：2 case × 2 臂 = 4 次，单次 20-50 分钟
SKILL_NAME=paper-graph caffeinate -i tests/harness/run_matrix.sh <模型> \
  tests/harness/runs/graph-pilot \
  tests/paper-graph/cases/q2-diffusion-sampling tests/paper-graph/cases/q5-seed-lora
# → 回传 graph-pilot 等负责人确认后再跑 C2。
#   说明：这道检查点是成本保险而非正确性要求——graph 执行链是首次真跑，
#   先用 4 次探雷，避免万一有环境问题时浪费整批 16 次。
# C2 全量：8 case × 2 臂 = 16 次，务必过夜
SKILL_NAME=paper-graph caffeinate -i tests/harness/run_matrix.sh <模型> tests/harness/runs/graph-full
```

每条命令结束会自动打印汇总表——**你不需要解读它**，原样回传即可。

## 2. 回传什么

每批跑完，把对应的 `tests/harness/runs/<目录>` 整个打包发回：

```bash
cd tests/harness/runs && tar czf <目录>.tgz <目录>/
```

包里已含全部所需（transcript.jsonl / meta.json / metrics.json / ws 产物），不要删减。

## 3. 铁律（Do NOT）

1. **不要改** `tests/*/cases/`、`tests/*/gt/`、`tests/paper-graph/fixtures/` 下的任何文件——GT 和冻结输入动一个字节，整批数据作废。
2. **不要重跑**已完成的 run 去"修"看起来不好的结果。失败/异常的 run 保留原样回传——异常本身就是数据（比如 skill 列 = n 是重要发现，不是故障）。
3. 某个 case 中断（断网/机器重启）：整个 case-臂目录删掉重跑**这一个**即可（runner 幂等，其他不受影响），并在回传时说明哪些重跑过。
4. 不要在运行期间用同一账号并行干别的重活（限速会拖慢矩阵）。
5. 不要把 tests/.env、runs 产物或本目录任何内容上传到公开仓库/网盘。

## 4. 快速排障

| 症状 | 处理 |
|---|---|
| `Not logged in` | 第 0 步的 CLI 登录没完成 |
| 某 run exit_code≠0 且 output 为空 | 看该目录 stderr.log 最后几行；记下 case 名，继续跑后面的，回传时说明 |
| `CHECK INCOMPLETE: ...` | checker 没打上分，不影响 SUT 产物，照常回传 |
| graph 臂跑得极慢（>90 分钟/次） | 正常范围外——中止该 run，记录，问负责人 |
| mmdc/chromium 下载卡住 | 网络问题；graph checker 会自动降级，不阻塞 |

有任何拿不准的：**停下来问**，不要自行发挥。

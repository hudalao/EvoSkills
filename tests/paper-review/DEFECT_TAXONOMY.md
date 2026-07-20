# paper-review 评测：缺陷注入分类法 v1

每个变体注入 4–6 个缺陷 + 每篇一个零注入对照。缺陷必须满足三条：
(1) **自然**——像真实作者会犯的错，不是荒诞改写;
(2) **可判定**——detection criteria 写成"review 中出现 X 类批评且指向该位置/该 claim 即算命中"，judge 不需要品味判断;
(3) **局部**——单个 patch 尽量只动一处，互相不纠缠，保证按缺陷计召回。

对应 SKILL.md 的 5 aspects + claims 检查 + limitation/图表规范。每类给出注入配方与判定标准模板。

| ID | 类别（aspect） | 注入配方 | 判定标准（命中条件） |
|----|----|----|----|
| D1 | 无支撑强 claim（Claims/A1） | 在 abstract 或 intro 加一句超出实验范围的强断言（如 "consistently outperforms all baselines across every setting"，而某表存在输/平项），或把既有 claim 的限定词删掉（"in most settings"→删） | 指出该 claim 缺乏/超出实验支撑，或要求弱化措辞；须点名该句或其位置 |
| D2 | 模块动机缺失（A2 写作） | 删除 Method 中某模块的动机段（"why"句），只留"what" | 指出该模块缺少动机/理由说明；点名该模块 |
| D3 | 术语不一致（A2 写作） | 从第 N 节起把一个核心术语换成同义新名（如 "anchor model"→"reference policy"），全文两名混用 | 指出术语混用/前后不一致；两个名字至少出现一个 |
| D4 | 复现细节缺失（A2 写作） | 删除关键超参/实现细节句（学习率、数据规模、判据阈值），若在表中则删表行 | 指出缺少可复现细节；指向该实验/设置 |
| D5 | 边际提升夸大（A3 结果） | 把正文对某表的解读从如实改为夸大（"comparable"→"substantially better"），表内数字不动 | 指出正文解读与表格数字不符/夸大；点名该表或该句 |
| D6 | 消融缺失（A4 完备性） | 删除某核心组件的消融行+对应正文句；正文其他处仍宣称该组件必要 | 指出该组件缺少消融支撑；点名组件 |
| D7 | 基线缺失叙述矛盾（A4 完备性） | 在 related work 承认某直接可比方法，但实验表无该基线且无解释 | 指出该基线未比较/未解释；点名方法 |
| D8 | 不现实假设（A5 方法设计） | 在方法或设置里插入一条强假设句（如 "we assume validation labels are available at test time"），下游不再提及 | 指出该假设不现实/未讨论其影响；点名假设 |
| D9 | limitation 章节删除（结论检查） | 整节删除（若原文有）；或删掉其中实质性条目只留客套 | 指出缺少 limitation 讨论 |
| D10 | 引用断链（提交卫生） | 把 2–3 处 \cite 键改错 → 编译后出现 [?]；LaTeX 场景直接留错误键 | 指出引用缺失/[?]/bib 不完整 |
| D11 | \todo 残留（提交卫生） | 在 appendix 或正文角落留一条 `\todo{fix this}` / `% TODO` 可见注释 | 指出残留 TODO 标记 |
| D12 | 图表规范违例（图表检查） | 表 caption 移到表下方 + 去掉 booktabs 换 \hline+竖线；或去掉最优加粗与 ↑↓ 指示 | 指出表格格式问题（caption 位置/竖线/未标注方向任一即可） |
| D13 | 摘要-结论承诺失配（A1/结构） | 摘要承诺三个贡献，结论只总结两个（删结论中一条） | 指出结论未覆盖摘要承诺的贡献；点名缺失项 |
| D14 | 数据泄漏式设置（A5 方法设计，高难雷） | 在实验设置里埋一句训练/测试重叠的描述（如 "hyperparameters tuned on the test split"） | 指出评测协议受污染/不公平；点名该句 |

## 变体组合规则

- 每篇 2 个变体：**V1 = 中等难度**（D9-D12 类表面雷 2 个 + D1/D5/D6 类实质雷 2 个）；**V2 = 高难度**（D2/D8/D13/D14 类隐蔽雷 4 个 + 表面雷 1 个），另加 **V0 = 干净对照**。
- 同一变体内的雷分散在不同章节，两两无语义关联。
- 每个雷记录进 `gt/defects.json`：`{id, type, aspect, location_anchor(节名+邻近原文短语), patch_file, detection_criteria, severity(major|minor), notes}`。
- patch 以 unified diff 存 `patches/<variant>/<defect_id>.patch`，构建脚本按序应用；任何 patch 应用失败即构建中止（防漂移）。

## 验证者检查单（workflow Verify 阶段用）

1. patch 干净应用且只改动预期行数;
2. 注入后 LaTeX 仍可编译（或至少无新增致命语法错）;
3. 雷"自然"：改动读起来像作者疏忽，不像故意破坏（长度、语域一致）;
4. **原文冲突检查**：确认原文没有本来就存在的同类问题会与判定标准混淆（如原文本就没有该模块的消融→D6 不成立须换目标）;
5. 判定标准可机判：一个不了解注入过程的人拿着 criteria 能对任意 review 给出 yes/no。

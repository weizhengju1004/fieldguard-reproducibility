# FieldGuard 方法说明与模拟演示材料

仓库地址：[https://github.com/weizhengju1004/fieldguard-reproducibility](https://github.com/weizhengju1004/fieldguard-reproducibility)

**模拟演示：八条示例中的 evidence、报告、反馈、标注和评分标签均为手工构造；没有运行 CLIP 或 Qwen，也没有生成真人评分记录。实际公开状态及核实后的仓库地址记录在 `manifest.json`。**

本包依据 2026-10-11 的“投稿稿修订_三图文字统一”稿件制作，用于展示字段格式、方法约束、安全门和指标计数。它不能复现或证明论文表一、表二的性能。论文原文件和三张图不在本包内，篇幅不受本包影响。

## 包含内容

| 文件或目录 | 用途 |
|---|---|
| `docs/evidence_format.md`、`schemas/evidence.schema.json` | evidence 的候选 JSON 表示、字段类型、单位、空掩膜与坐标约定 |
| `prompts/` | 初稿 p0、针对性修订 p1 和通用修订对照模板 |
| `docs/audit_rules.md` | 字段提取说明、在线审计、触发、接纳、回退和人工复核规则 |
| `docs/metric_definitions.md` | 七项判据、ACPR、TRR、CDR，以及分母和舍入规则 |
| `examples/reports_readable.md` | 八条示例的中文说明和完整英文报告，可直接阅读 |
| `examples/evidence/`、`trajectories.jsonl` | 每条示例的 E、R0、F、R1、审计标签与选用版本 |
| `examples/offline_annotations.jsonl`、`labels.csv` | 独立保存的构造离线标注和逐报告评价标签 |
| `scripts/`、`run_demo.py`、`tests/` | 本地格式检查、安全门重放、指标汇总及计数回归检查 |
| `demo_output/` | 实际运行上述本地脚本得到的模拟示例计算结果 |
| `manifest.json`、`VERIFICATION.json`、`SHA256SUMS.txt` | 材料状态、核验范围及文件校验值 |

这里的 schema 是按论文字段定义整理的候选公开接口，不宣称恢复了某次真实实验的序列化格式。提示词是方法模板，也不是从实际模型调用中恢复的历史提示词。

## 本地运行

使用 Python 3.9 或更新版本；已用本机 Python 3.9.13 核验。演示、汇总和测试仅使用 Python 标准库，不需要 GPU、模型权重或网络。先在终端进入解压后的材料包目录：

```powershell
python -B run_demo.py
python -B -m unittest discover -s tests -v
```

如果 `python` 没有指向已安装的 Python，可以改用本机解释器的完整路径。脚本只会更新包内 `demo_output/` 的三个结果 JSON。

也可以单独执行汇总：

```powershell
python -B scripts/metric_summary.py examples/labels.csv --output demo_output/metric_summary.json
python -B scripts/gate_demo.py examples/trajectories.jsonl --output demo_output/gate_decisions.json
```

## 如何看结果

这组示例有 `N=8`、`N_T=6`。最终三个报告七项同时通过，所以 ACPR 为 `3/8=37.5%`；四条触发记录至少修复一项初始错误，所以 TRR 为 `4/6=66.7%`；一条触发记录新增错误，所以 CDR 为 `1/6=16.7%`。这些只是说明公式的演示数字。

- `demo-002` 修复位置；`demo-003` 同时修复分数和面积，但 TRR 的分子只加一。
- `demo-004` 修复位置却新增分数错误，安全门回退 R0；按最终选用文本计数，TRR/CDR 均不加一。
- `demo-005` 仍有关键违规，转人工复核。没有对外接纳的报告；评价列使用明确指定的交接前 R0，记录仍留在两个分母中。
- `demo-006` 修复遗漏分数并通过在线审计，但保留了错误 evidence 的位置，离线 LPR 仍失败。
- `demo-007` 沿用错误的正常判定，未触发修订；离线 DPR/LPR/CPR 失败。
- `demo-008` 刻意设置一次在线语义漏判：补齐影响陈述，却引入无依据的确定性原因；离线 TRR 和 CDR 同时计数。这是规则风险的构造演示，不是测得的漏判案例或发生率。

## 核验边界

`online_audit` 是预先手工指定的 q 标签，`labels.csv` 是预先手工指定的离线 y 标签。脚本重放安全门并计算已有标签，没有自动从自然语言提取七项判据，也没有完成真实的语义评审。关键词出现本身不能证明 CPR 或 EBR 通过。

离线标注与参考信息不能进入在线反馈。本包单独保存离线文件，并检查反馈目标和字段、错误 evidence 示例中的真值位置隔离。E 的字节指纹在 R0/R1 中复用；由于不含实际照片和热图，这项检查只证明示例引用了同一份结构化 E。

本包的复现范围是方法说明、给定审计标签下的安全门重放和给定离线标签下的指标汇总。论文性能表的实证复现仍需要真实输入、模型执行记录及独立获取的评价标签。

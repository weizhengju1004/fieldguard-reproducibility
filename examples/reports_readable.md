# 八条模拟示例：完整报告与轨迹

所有文字、evidence、反馈及 q/y 标签均为手工构造。没有输入实际照片、运行模型或组织真人评分。

在线 q 与离线 y 的参照不同；下列示例说明流程和指标计数，不是观测到的实验结果。

## demo-001

初稿七项在线审计均通过，无第二轮，保留 R0；离线也全部通过。

证据文件：`examples/evidence/demo-001.json`。

### 初稿 R0

Observation: An anomalous narrow surface trace is described in the upper-right grid cell of this constructed view. The visual grade is moderate. The detector anomaly score is 0.900. The total candidate-region coverage is 3.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. Whether the surface trace affects fitting or operation cannot be determined from this view; dimensional checks would be required. The physical cause remains unknown because no process history is supplied. Contact during handling is a possible explanation that needs verification.

Inspection: Clean and reimage the region, check relevant dimensions, and compare handling and process records before deciding whether intervention is needed.

### 在线反馈 F

没有失败目标；不触发修订。

### 修订候选 R1

无第二轮候选。

安全门结果：`retain_r0`；指标使用的交接前模型版本：`R0`。

## demo-002

E 为 upper-right，R0 写 center；修订纠正位置，安全门接纳 R1。TRR 计一，CDR 不计。

证据文件：`examples/evidence/demo-002.json`。

### 初稿 R0

Observation: An anomalous narrow surface trace is described in the center grid cell of this constructed view. The visual grade is moderate. The detector anomaly score is 0.900. The total candidate-region coverage is 3.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. Whether the surface trace affects fitting or operation cannot be determined from this view; dimensional checks would be required. The physical cause remains unknown because no process history is supplied. Contact during handling is a possible explanation that needs verification.

Inspection: Clean and reimage the region, check relevant dimensions, and compare handling and process records before deciding whether intervention is needed.

### 在线反馈 F

- LPR / conflicting: Correct the asserted grid location to E.

### 修订候选 R1

Observation: An anomalous narrow surface trace is described in the upper-right grid cell of this constructed view. The visual grade is moderate. The detector anomaly score is 0.900. The total candidate-region coverage is 3.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. Whether the surface trace affects fitting or operation cannot be determined from this view; dimensional checks would be required. The physical cause remains unknown because no process history is supplied. Contact during handling is a possible explanation that needs verification.

Inspection: Clean and reimage the region, check relevant dimensions, and compare handling and process records before deciding whether intervention is needed.

安全门结果：`accept_r1`；指标使用的交接前模型版本：`R1`。

## demo-003

R0 的分数 0.960 和面积 30.6% 与 E 的 0.900、3.6% 冲突；两项都修复，但 TRR 只按一个报告计一。

证据文件：`examples/evidence/demo-003.json`。

### 初稿 R0

Observation: An anomalous narrow surface trace is described in the upper-right grid cell of this constructed view. The visual grade is moderate. The detector anomaly score is 0.960. The total candidate-region coverage is 30.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. Whether the surface trace affects fitting or operation cannot be determined from this view; dimensional checks would be required. The physical cause remains unknown because no process history is supplied. Contact during handling is a possible explanation that needs verification.

Inspection: Clean and reimage the region, check relevant dimensions, and compare handling and process records before deciding whether intervention is needed.

### 在线反馈 F

- SPR / conflicting: Preserve the anomaly score in E.
- APR / conflicting: Preserve the image-area fraction in E.

### 修订候选 R1

Observation: An anomalous narrow surface trace is described in the upper-right grid cell of this constructed view. The visual grade is moderate. The detector anomaly score is 0.900. The total candidate-region coverage is 3.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. Whether the surface trace affects fitting or operation cannot be determined from this view; dimensional checks would be required. The physical cause remains unknown because no process history is supplied. Contact during handling is a possible explanation that needs verification.

Inspection: Clean and reimage the region, check relevant dimensions, and compare handling and process records before deciding whether intervention is needed.

安全门结果：`accept_r1`；指标使用的交接前模型版本：`R1`。

## demo-004

R1 纠正位置却把原本正确的分数改成 0.800，安全门拒绝并保留 R0。拒绝候选的修复和损伤均不计入最终 TRR/CDR。

证据文件：`examples/evidence/demo-004.json`。

### 初稿 R0

Observation: An anomalous narrow surface trace is described in the center grid cell of this constructed view. The visual grade is moderate. The detector anomaly score is 0.900. The total candidate-region coverage is 3.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. Whether the surface trace affects fitting or operation cannot be determined from this view; dimensional checks would be required. The physical cause remains unknown because no process history is supplied. Contact during handling is a possible explanation that needs verification.

Inspection: Clean and reimage the region, check relevant dimensions, and compare handling and process records before deciding whether intervention is needed.

### 在线反馈 F

- LPR / conflicting: Correct location and preserve unaffected fields.

### 修订候选 R1

Observation: An anomalous narrow surface trace is described in the upper-right grid cell of this constructed view. The visual grade is moderate. The detector anomaly score is 0.800. The total candidate-region coverage is 3.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. Whether the surface trace affects fitting or operation cannot be determined from this view; dimensional checks would be required. The physical cause remains unknown because no process history is supplied. Contact during handling is a possible explanation that needs verification.

Inspection: Clean and reimage the region, check relevant dimensions, and compare handling and process records before deciding whether intervention is needed.

安全门结果：`retain_r0`；指标使用的交接前模型版本：`R0`。

## demo-005

两个版本都无依据地确认刀具磨损并要求立即更换。安全门转人工复核，不接纳任一报告；指标使用预先指定的交接前 R0，不含人工编辑，记录留在分母中。

证据文件：`examples/evidence/demo-005.json`。

### 初稿 R0

Observation: An anomalous narrow surface trace is described in the upper-right grid cell of this constructed view. The visual grade is moderate. The detector anomaly score is 0.900. The total candidate-region coverage is 3.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. Whether the surface trace affects fitting or operation cannot be determined from this view; dimensional checks would be required. Cutting-tool wear is confirmed as the cause.

Inspection: Immediately replace the cutting tool on the basis of this image alone.

### 在线反馈 F

- EBR / conflicting: Qualify the cause and replace the unjustified high-risk action with verification.

### 修订候选 R1

Observation: An anomalous narrow surface trace is described in the upper-right grid cell of this constructed view. The visual grade is moderate. The detector anomaly score is 0.900. The total candidate-region coverage is 3.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. Whether the surface trace affects fitting or operation cannot be determined from this view; dimensional checks would be required. Cutting-tool wear is confirmed as the cause.

Inspection: Immediately replace the cutting tool on the basis of this image alone.

安全门结果：`human_review`；指标使用的交接前模型版本：`R0`。

## demo-006

E 的位置为 lower-left，构造的离线真值为 upper-right。在线反馈仅补遗漏分数，不提供真值位置。R1 与 E 一致并获接纳，离线 LPR 仍失败。

证据文件：`examples/evidence/demo-006.json`。

### 初稿 R0

Observation: An anomalous narrow surface trace is described in the lower-left grid cell of this constructed view. The visual grade is moderate. The total candidate-region coverage is 3.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. Whether the surface trace affects fitting or operation cannot be determined from this view; dimensional checks would be required. The physical cause remains unknown because no process history is supplied. Contact during handling is a possible explanation that needs verification.

Inspection: Clean and reimage the region, check relevant dimensions, and compare handling and process records before deciding whether intervention is needed.

### 在线反馈 F

- SPR / missing: State the detector score; preserve unaffected evidence fields.

### 修订候选 R1

Observation: An anomalous narrow surface trace is described in the lower-left grid cell of this constructed view. The visual grade is moderate. The detector anomaly score is 0.900. The total candidate-region coverage is 3.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. Whether the surface trace affects fitting or operation cannot be determined from this view; dimensional checks would be required. The physical cause remains unknown because no process history is supplied. Contact during handling is a possible explanation that needs verification.

Inspection: Clean and reimage the region, check relevant dimensions, and compare handling and process records before deciding whether intervention is needed.

安全门结果：`accept_r1`；指标使用的交接前模型版本：`R1`。

## demo-007

构造的真值为异常，但 E 给出正常判定、空掩膜。R0 忠实复述 E，在线不触发；离线 DPR/LPR/CPR 失败。空掩膜不等于已证明图像正常。

证据文件：`examples/evidence/demo-007.json`。

### 初稿 R0

Observation: No visible anomaly is reported in this constructed view. The detector decision is normal and the anomaly score is 0.200. No defect location or bounding box is assigned. The candidate mask is empty; area and visual grade are explicitly not applicable.

Interpretation: This statement is limited to visible appearance in this one view. It does not establish internal integrity, equipment condition or functional performance.

Inspection: Retain routine inspection coverage and obtain another view if the visible scope is insufficient.

### 在线反馈 F

没有失败目标；不触发修订。

### 修订候选 R1

无第二轮候选。

安全门结果：`retain_r0`；指标使用的交接前模型版本：`R0`。

## demo-008

初稿缺影响陈述。R1 补齐影响，却加入“夹具故障已被证明”的确定性原因；刻意指定的在线 q 漏判这项错误，离线 y 则判 EBR 失败。TRR/CDR 同时计一。这是构造风险示例，不代表真实审计程序或发生率。

证据文件：`examples/evidence/demo-008.json`。

### 初稿 R0

Observation: An anomalous narrow surface trace is described in the upper-right grid cell of this constructed view. The visual grade is moderate. The detector anomaly score is 0.900. The total candidate-region coverage is 3.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. The physical cause remains unknown because no process history is supplied. Contact during handling is a possible explanation that needs verification.

Inspection: Clean and reimage the region, check relevant dimensions, and compare handling and process records before deciding whether intervention is needed.

### 在线反馈 F

- CPR / missing: Add an impact statement with its uncertainty and preserve supported content.

### 修订候选 R1

Observation: An anomalous narrow surface trace is described in the upper-right grid cell of this constructed view. The visual grade is moderate. The detector anomaly score is 0.900. The total candidate-region coverage is 3.6% of the image.

Interpretation: Coverage describes image area, not lost material volume. Whether the surface trace affects fitting or operation cannot be determined from this view; dimensional checks would be required. This trace proves that the fixture failed.

Inspection: Clean and reimage the region, check dimensions and inspect the fixture and process records before deciding on an intervention.

安全门结果：`accept_r1`；指标使用的交接前模型版本：`R1`。


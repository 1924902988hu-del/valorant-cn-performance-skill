# Source inventory

本项目的一手资料清单与适用限制位于：

`skills/valorant-cn-performance/references/sources.md`

刷新日期：2026-07-22。

本轮关键修正：

1. 不再写“国服 ACE 必须关闭内存完整性/Hyper-V”；腾讯页面只把这些列为特定 CPU 虚拟化弹框在 BIOS 设置后仍存在时的条件排查。
2. 不再写“国际服 VBS/HVCI 随便关”；Riot 的可选 Vanguard On-Demand 需要 Windows 11 25H2、VBS/HVCI、IOMMU 等前置条件。
3. Raw Input Buffer 的移除来自 11.06，不与 UE5 迁移混为一谈。
4. 更新 AMD 路径：12.09 已加入游戏内 Anti-Lag 2。
5. WMI 内存频率不再被当作 XMP/EXPO 或双通道的确定证据。

# 诊断方案

## 结论与置信度

**选 Vanguard On-Demand，就保留 VBS 和“内存完整性”（HVCI）；不要为了未经验证的 FPS 收益关闭它们。置信度：高。**

Windows 11 25H2 只是条件之一。On-Demand 还要求 UEFI Secure Boot、TPM 2.0、VBS、HVCI、IOMMU 等安全能力。关闭 VBS/HVCI 会降低系统防护，并直接失去 On-Demand 资格。

## 已知 / 缺失

- 已知：港服、Windows 11 25H2、希望使用 Vanguard On-Demand。
- 已知：“内存完整性”即 HVCI，依赖 VBS，并不是两个互不相关的 FPS 开关。
- 缺失：CPU、GPU、内存、当前 FPS/1% low、帧时间，以及其他 On-Demand 前置条件是否通过。
- 未进行本机检测，因此不能断言你的电脑存在 VBS/HVCI 性能问题。

## 症状分类

目前属于**反作弊资格与系统安全配置选择**，不是已证实的客户端 FPS 瓶颈。没有 A/B 数据，不能把朋友的建议当作针对你电脑的性能结论。

## 优先动作

1. **保持 VBS、内存完整性、Secure Boot 和 TPM 开启。**  
   依据等级：Riot/Microsoft 官方一手。  
   适用条件：你仍想使用 On-Demand。  
   预期观察：VBS/HVCI 不会成为 Pre-Check 的失败项。  
   回滚：没有改动则无需回滚；若当前已关闭，记录原值后再按官方路径逐项恢复并重启验证。

2. **运行 Riot 提供的 On-Demand Pre-Check。**  
   依据等级：Riot 官方一手。  
   适用条件：该可选模式已对你的客户端开放。  
   预期观察：明确显示 25H2、VBS、HVCI、IOMMU、Secure Boot、TPM 等条件的通过/失败状态。  
   回滚：这是检查动作，无需回滚。

3. **先在当前安全配置下建立性能基线。**  
   依据等级：可重复测量方法。  
   适用条件：你确实遇到低 FPS、卡顿或 1% low 较差。  
   预期观察：同一地图、画质、帧率上限和后台环境下，连续三轮记录 avg FPS、1% low 与帧时间。  
   回滚：无系统改动，无需回滚。

4. **若确有性能问题，先检查低风险项目。**  
   依据等级：Microsoft、Riot及 GPU 厂商一手。  
   适用条件：基线确认存在客户端性能问题。  
   预期观察：确认 Windows 刷新率、目标 GPU、电源、温度/功耗、后台录制和覆盖层；NVIDIA 可单独 A/B 游戏内 Reflex，兼容 AMD 可测试 Anti-Lag 2。  
   回滚：恢复游戏或后台应用原值。

## 暂不建议

- 不建议为“可能多几帧”关闭 VBS/HVCI：Riot 已确认它们是 On-Demand 前置条件，而你的实际 FPS 收益没有数据支持。
- 不建议关闭 Secure Boot、TPM、驱动签名或 Vanguard 服务。
- 不建议使用注册表优化包、`bcdedit` 脚本或所谓 Vanguard 关闭器。
- 如果未来决定放弃 On-Demand，也不能默认关闭 VBS/HVCI一定更快；应先评估安全代价，并进行单变量、可回滚的三轮 A/B 测试。

## 复测协议

固定同一游戏补丁、地图/模式、分辨率、画质、帧率上限、电源状态和后台程序；热身后各测三轮，比较：

- avg FPS
- 1% low
- 帧时间尖峰及波动
- 若有网络症状，再记录 RTT 和丢包

没有稳定、可重复的收益，就不要牺牲安全功能。

## 来源与日期

- [Riot：Vanguard On-Demand](https://www.riotgames.com/en/news/vanguard-on-demand)，2026-06-24。
- [Microsoft：VBS/HVCI 硬件辅助安全](https://learn.microsoft.com/en-us/windows/security/book/hardware-security-silicon-assisted-security)。
- [Microsoft：内存完整性/HVCI 配置](https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity)。

本 Skill 证据刷新至 **2026-07-22**；On-Demand 的具体开放范围和 Pre-Check 结果仍以你当前 Riot Client 为准。
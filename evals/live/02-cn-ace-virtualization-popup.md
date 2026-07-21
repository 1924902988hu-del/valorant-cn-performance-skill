# 诊断方案

## 结论与置信度

最可能是 Windows 的 VBS/HVCI/Hyper-V/WSL2/Docker 虚拟化链路与国服 ACE 冲突，而不是 BIOS 没开启；置信度：中。

你平时依赖 WSL2 和 Docker，因此不建议永久关闭虚拟化。先做无损区分实验，再决定是否短暂切换。

## 已知 / 缺失

- 用户确认：国服、弹框原文匹配、Windows 11、BIOS 已开启 SVM 和 IOMMU、需要 WSL2 与 Docker。
- 脚本观察：无；目前没有读取你的电脑状态。
- 仍缺：Windows 具体 build、`msinfo32` 中 VBS/虚拟机监控程序状态、内存完整性状态、已启用的 Windows 虚拟化组件。

## 症状分类

反作弊启动兼容问题，不是 FPS 或网络问题。

## 优先动作

1. **先读取当前虚拟化状态，不改设置**

   - 操作：打开 `msinfo32`，记录“基于虚拟化的安全性”状态，以及是否显示“已检测到虚拟机监控程序”；同时查看 Windows 安全中心 → 设备安全性 → 内核隔离 → “内存完整性”当前状态。
   - 依据等级：官方/一手。
   - 适用条件：所有情况。
   - 预期观察：确认是仅有 BIOS 虚拟化，还是 Windows 的 VBS/HVCI/Hyper-V 已实际占用虚拟化能力。
   - 回滚：只读，无需回滚。

2. **先做不破坏 WSL2 配置的运行态测试**

   - 完全退出 Docker Desktop。
   - 在终端运行：`wsl --shutdown`
   - 确认 Docker 没有随即重新启动，然后重新启动国服客户端。
   - 依据等级：条件诊断；WSL2、Docker、Hyper-V 均属于腾讯弹框路径中的冲突候选。
   - 预期观察：
     - 弹框消失：更像是正在运行的 WSL/Docker 虚拟机造成冲突。
     - 仍弹框：更像是 Windows 启动时加载的 VBS/HVCI/Hyper-V 平台冲突；单纯退出 Docker 不够。
   - 回滚：重新启动 Docker Desktop或再次运行 WSL 即可。

3. **如果仍弹，优先向腾讯支持提交兼容问题**

   提供弹框截图、Windows build、主板型号、SVM/IOMMU 状态，以及 `msinfo32` 中上述两项状态，并明确说明必须使用 WSL2/Docker。腾讯官方将这条报错单独列为 CPU 虚拟化占用问题；这是最适合确认当前 ACE 版本是否支持共存的渠道。

   - 依据等级：腾讯官方/一手。
   - 预期观察：获得针对当前 ACE 版本和系统状态的处理方案。
   - 回滚：无系统改动。

4. **仅在你接受暂时降低安全保护时，单独 A/B 测试“内存完整性”**

   先截图原值；一次只关闭“内存完整性”，重启后测试 ACE。不要同时关闭其他组件。

   - 依据等级：官方/一手、条件执行。
   - 适用条件：退出 WSL/Docker无效，并且你明确接受测试期间 HVCI 内核保护降低。
   - 预期观察：若弹框消失，可确认 HVCI/VBS 链路相关；若无变化，立即恢复原值。
   - 回滚：恢复“内存完整性”为原状态并重启。
   - 风险：降低 Windows 内核安全保护；还可能受企业策略或驱动兼容状态影响。

5. **最后才测试 Hyper-V/虚拟机平台**

   如果内存完整性测试无效，才考虑临时关闭 Windows 功能中的“虚拟机平台”、Hyper-V、Windows 虚拟机监控程序平台或 Sandbox。必须先逐项截图记录，并一次只测试一类。

   - 依据等级：腾讯官方路径＋Microsoft 一手安全说明。
   - 适用条件：你接受 WSL2/Docker 在测试期间不可用。
   - 预期观察：重启后 ACE 是否恢复启动。
   - 回滚：重新启用原组件并重启。
   - 重要限制：这不是长期优化方案。若确认只有关闭这些组件才能运行，实际选择就是“游戏时关闭虚拟化栈”或等待/请求 ACE 提供兼容修复，不能同时承诺 WSL2/Docker 正常工作。

## 暂不建议

- 不要关闭 BIOS 的 SVM、IOMMU；ACE 官方路径本身要求确认这些功能已开启。
- 不要一次性关闭 HVCI、VBS、Hyper-V、WSL2 和所有安全功能，否则无法判断真正冲突项。
- 不要复制网上来源不明的 `bcdedit`、注册表脚本或“一键关闭虚拟化”工具。
- 不要结束、删除或屏蔽 ACE 服务。
- 不建议为了这个弹框永久关闭内存完整性；它不是 FPS 优化项。

## 复测协议

每一轮只改变一个条件，重启要求保持一致，并记录：

1. Docker/WSL 是否运行；
2. 内存完整性与 Windows 虚拟化组件原值；
3. 是否仍出现同一弹框；
4. ACE 是否能正常启动；
5. 测试完成后是否成功恢复 WSL2、Docker及原安全设置。

这次主要指标是“弹框是否消失”，avg FPS、1% low、帧时间、RTT和丢包暂不适用。

## 来源与日期

- [腾讯游戏安全：CPU 虚拟化功能弹框处理](https://gamesafe.qq.com/article/1181.shtml)，2026-01-04；只适用于该特定弹框。
- [Microsoft：VBS/HVCI 与硬件辅助安全](https://learn.microsoft.com/en-us/windows/security/book/hardware-security-silicon-assisted-security)。
- [Microsoft：内存完整性/HVCI 配置说明](https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity)。

证据刷新至 2026-07-22；尚未读取你电脑的实际状态，因此这是诊断方案，不是“问题已解决”。
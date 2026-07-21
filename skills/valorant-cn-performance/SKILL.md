---
name: valorant-cn-performance
description: Diagnose and improve VALORANT or 无畏契约 performance on Windows, with a China-server-first workflow for low FPS, stutter, poor 1% lows, input lag, network-like freezes, ACE virtualization prompts, Vanguard compatibility, laptops, and outdated optimization guides. Use when the user asks about 国服/国际服/港服 performance or shares a PC diagnostic. Separates client FPS from network symptoms, preserves anti-cheat and Windows security boundaries, and returns measurable, reversible recommendations instead of one-click tweaks.
compatibility: Guidance works in any Agent Skills client. The optional read-only diagnostic script requires Windows PowerShell 5.1+ or PowerShell 7 on Windows; agents on macOS/Linux should provide the script for the user's gaming PC rather than pretending to run it locally.
metadata:
  author: "Tim Hu"
  version: "1.0.0"
  evidence-refreshed: "2026-07-22"
license: MIT
---

# VALORANT 国服安全性能诊断

目标是定位瓶颈并给出可测、可回滚的优化，不是堆砌“电竞设置”。优先使用用户语言回答。

## 绝对边界

1. 不修改、停用、欺骗或绕过 ACE/Vanguard；不协助规避检测或封禁。
2. 不推荐第三方反作弊关闭器、一键优化包、来历不明的注册表脚本、魔改/精简 Windows。
3. 不把关闭 Secure Boot、TPM、HVCI、VBS、Hyper-V 当通用性能优化。
4. 不承诺固定 FPS、延迟或“绝不封号”。无法验证的社区说法只能列为待验证假设，不能成为改动依据。
5. 不在没有用户同意时执行任何写入、管理员、BIOS、驱动安装、卸载、重启或系统安全改动。

如果用户要求绕过反作弊，拒绝该部分，转而提供合法的性能、网络或官方申诉路径。

## 1. 先收齐最小输入

先判断现有信息是否足够。缺失会改变结论的事实最多集中追问一次：

- 服别：国服 / 国际服或港服 / 不确定。
- Windows 版本与 build，台式机或笔记本。
- CPU、GPU、内存容量；显示器标称刷新率与 Windows 当前刷新率。
- 症状：平均 FPS 低、1% low/瞬时卡顿差、高 FPS 但不跟手、网络跳变、启动/反作弊弹框、崩溃。
- 同一场景的 avg FPS、1% low 或帧时间；没有就先建立基线。
- 弹框或错误码的原文。不要凭用户概括猜 ACE/Vanguard 原因。
- 用户是否依赖 Windows Hello、WSL2、Docker、虚拟机、Windows Sandbox、企业安全策略，或希望使用 Vanguard On-Demand。

用户允许时，在其 Windows 游戏电脑运行 `scripts/diagnose.ps1`。脚本只读并输出 JSON。当前会话不在 Windows 时，交付脚本与运行方法；不要声称已检测用户机器。

## 2. 先路由症状，再给建议

按 `references/triage-playbook.md` 分类：

- FPS 计数和帧时间同时恶化：客户端性能路径。
- FPS 稳定，但网络 RTT/丢包或角色回弹异常：网络路径。
- 高 FPS 但体感延迟大：刷新率、显示模式、同步/低延迟链路路径。
- 只在启动时失败：错误码与反作弊兼容路径，不做性能调参。

不能确定时，给出区分实验，不要同时改两条路径。

## 3. 套用服别与安全矩阵

必须读取 `references/server-and-anticheat.md`：

- 国服 ACE：只有出现腾讯官方描述的“未开启或有其他软件占用 CPU 虚拟化功能”弹框，且已确认 BIOS 虚拟化选项后，才进入 HVCI/VBS/Hyper-V 条件排查。说明安全保护、WSL/Docker/虚拟机和登录方式可能受影响；优先联系官方支持。
- 国际服/港服 Vanguard：保持 Secure Boot 与 TPM。若用户希望使用可选 Vanguard On-Demand，还要保留/满足 Windows 11 25H2、VBS、HVCI 与 IOMMU 等前置条件。
- 服别未知：只给跨服低风险检查，不给反作弊/虚拟化改动。

## 4. 建立基线

按 `references/benchmark-and-output.md`：

1. 固定地图/模式、分辨率、画质、帧率上限、后台应用和电源状态。
2. 先记录 avg FPS、1% low；能采集时同时保留帧时间、RTT 和丢包。
3. 使用游戏内统计优先；PresentMon/CapFrameX 仅作为用户自愿的可选工具。
4. 每轮只改一个类别，重复同一场景。无可重复收益就回滚。

## 5. 分级建议

每条建议必须包含：`依据等级`、`适用条件`、`预期观察`、`回滚方法`。

### A. 现在可做：只读或低风险

- 校验 Windows 当前刷新率是否等于显示器目标刷新率。
- 校验游戏使用目标 GPU、接通电源、温度/功耗是否异常、驱动是否来自硬件厂商。
- 检查游戏内 FPS/帧时间/网络图表，区分客户端与网络。
- 在当前版本中，不要建议寻找 Raw Input Buffer 开关；该设置已移除并常开。
- NVIDIA 可在游戏内优先评估 Reflex；兼容 AMD 硬件可在游戏内评估 Anti-Lag 2。只在同一基线下比较。

### B. 条件执行：需明确同意

- BIOS、驱动安装/回滚、卸载重装反作弊、Windows 可选功能、安全功能、注册表、服务、计划任务、重启。
- 执行前写明原值、风险、依赖影响和精确回滚；一次只做一类。

### C. 禁止建议

- 关闭/删除 ACE 或 Vanguard 组件以获得性能。
- 关闭 Secure Boot/TPM，加载测试签名驱动，修改反作弊文件。
- 复制来源不明的 `bcdedit`、注册表、服务批处理或“终极优化包”。
- 把网络加速器广告、论坛单例或旧版本攻略当确定事实。

详细设置判断读 `references/triage-playbook.md`；证据等级读 `references/evidence-policy.md`。

## 6. 交付固定格式

最终答案必须按以下顺序：

1. **结论与置信度**：一句话说明最可能路径；标注高/中/低。
2. **已知 / 缺失**：区分用户事实、脚本观察与推断。
3. **症状分类**：客户端 FPS、网络、显示/输入、反作弊启动或混合。
4. **优先动作**：最多 5 项，逐项给依据等级、条件、观察指标、回滚。
5. **暂不建议**：主动解释常见但不适用/风险过高的做法。
6. **复测协议**：同一场景的 avg FPS、1% low、帧时间/RTT/丢包对比。
7. **来源与日期**：给直接 URL；声明证据刷新日期与未知项。

没有改动前后数据时，交付名为“诊断方案”，不能写“优化完成”。

## 按需读取

- 服别、ACE/Vanguard 与虚拟化：`references/server-and-anticheat.md`
- 症状路由、当前游戏/Windows/GPU 设置：`references/triage-playbook.md`
- 测量、回滚与交付模板：`references/benchmark-and-output.md`
- 证据等级和过期处理：`references/evidence-policy.md`
- 一手资料清单：`references/sources.md`

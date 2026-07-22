# OKX.AI Genesis 提交清单

刷新时间：2026-07-22（Asia/Shanghai）。

## 官方时间与入口

- 官方活动页：<https://web3.okx.com/xlayer/build-x-series>
- HackQuest 英文活动页：<https://www.hackquest.io/hackathons/OKXAI-Genesis-Hackathon>
- OKX.AI ASP 指南：<https://www.okx.ai/tutorial/asp>
- ASP 注册文档：<https://web3.okx.com/zh-hans/onchainos/dev-docs/okxai/registerasp>
- OKX.AI Agent 市场：<https://www.okx.ai/agents>
- 最终表单：<https://docs.google.com/forms/d/e/1FAIpQLSfIAgP_WmMGtZ5qyW_LnKZonsjyfOYwV3bduRwiuN4oBmcqjQ/viewform>

官方英文主页面与 HackQuest 英文页当前均写明截止时间为 `2026-07-27 23:59 UTC`，即北京时间 `2026-07-28 07:59`。部分中文、日文镜像仍残留 `2026-07-17`，属于页面同步冲突；以当前英文官方主页面、开放中的英文 HackQuest 页面和可访问表单为操作依据，同时保留风险说明。

## 参赛硬门槛

1. 构建一个解决明确现实问题的 ASP；不要求必须是加密项目。
2. ASP 必须通过 OKX.AI 内部审核并公开上线；未获批或无法上线的提交无效。
3. 在 X 发布带 `#OKXAI` 的参赛帖，介绍 ASP、用途并包含清晰演示；演示不超过 90 秒。
4. 截止前提交 Google 表单，包含 ASP 资料和 X 参赛帖链接。

官方 ASP 指南称审核通常在 24 小时内完成；这不是保证，因此必须尽早创建并激活。

## 奖金

总奖池：100,000 USDT。所有获奖者还可能获得 OKX 官方 PR 与合作机会。

| 奖项 | 名额 | 奖金 |
|---|---:|---:|
| Best Product | 3 | 10,000 / 6,000 / 4,000 USDT |
| Creative Genius | 3 | 10,000 / 6,000 / 4,000 USDT |
| Revenue Rocket | 3 | 10,000 / 6,000 / 4,000 USDT |
| Finance Copilot | 3 | 每名 2,500 USDT |
| Software Utility | 3 | 每名 2,500 USDT |
| Lifestyle Companion | 3 | 每名 2,500 USDT |
| Artistic Excellence | 3 | 每名 2,500 USDT |
| Social Buzz | 10 | 每名 1,000 USDT |

FrameGuard CN 的主攻顺序：`Software Utility` → `Best Product` → `Social Buzz`。免费 A2A 没有活动期收入，不把 `Revenue Rocket` 作为主要目标。

## 表单实际必填字段

2026-07-22 直接读取开放表单所得字段：

1. ASP Name
2. Agent ID（ASP 上架后得到的 ID）
3. ASP Description
4. ASP Type（A2A / A2MCP）
5. X Account Handle
6. X Participation Post (Link)
7. Telegram Handle

其中 Agent ID、X 帖子链接尚未产生；Telegram Handle 必须由 Tim 提供，不能推测。

## 当前证据与状态

| 项目 | 状态 | 证据 |
|---|---|---|
| 标准 Agent Skill | 已完成 | `skills/valorant-cn-performance/` |
| 公开仓库 | 已完成 | <https://github.com/1924902988hu-del/valorant-cn-performance-skill> |
| v1.0.0 安装包 | 已完成 | GitHub Release，SHA-256 `d99a837e30aa3bff399da23b5a1c70e320206898d8d6380ef2433745271b6b3f` |
| 真实 Agent 回归 | 已完成 | 6 个输出，`212/212` 检查通过 |
| Windows 真机诊断 | 未完成 | 不宣称真机兼容或 FPS 增益 |
| ASP 身份/服务资料 | 已准备 | 质量检查通过，等待最终链上确认 |
| Agent ID | 未产生 | 链上创建后读取真实回执 |
| OKX.AI 审核/上线 | 未开始 | 创建并激活后等待结果 |
| 90 秒内演示 | 开发中 | `docs/demo-script-90s.md` 与 `docs/demo-storyboard.html` |
| X 参赛帖 | 未发布 | 发布动作前展示最终文案并确认 |
| Google 表单 | 未提交 | 最终提交动作前确认 |

## 不能跨越的证明边界

- 公开仓库、Release 和回归测试不能替代 OKX.AI 审核上线。
- Agent ID 不能从钱包地址或预检查结果推断，只能取链上创建回执。
- 模型回归不等于 Windows 真机 FPS 提升。
- X 草稿不等于已发布；表单已填写不等于已提交；必须保留公开链接或提交回执。

# VALORANT CN Performance Skill

面向《无畏契约》国服的安全性能诊断 Agent Skill。它把“先分清客户端 FPS 与网络问题、先测量、每次只改一类、复测、无收益即回滚”固化为可复用工作流，并对 ACE、Vanguard 与 Windows 安全设置设置严格边界。

## 安装

通过 Agent Skills CLI：

```bash
npx skills add 1924902988hu-del/valorant-cn-performance-skill --skill valorant-cn-performance
```

或把 `skills/valorant-cn-performance/` 复制到兼容客户端的 skills 目录。

## 内容

- `skills/valorant-cn-performance/`：可移植的 Agent Skill
- `evals/cases/`：6 个固定回归用例
- `evals/fixtures/`：用于校验评测器的样例交付
- `evals/live/`：6 个由 `gpt-5.6-sol` 生成的真实 Skill 回归输出
- `tests/validate.py`：零第三方依赖的结构、脚本安全与评测契约校验
- `docs/okx-a2a-listing-draft.md`：OKX.AI A2A 服务登记草案
- `docs/demo-script-90s.md`：90 秒演示脚本
- `docs/source-inventory.md`：一手资料清单与刷新日期
- `docs/genesis-submission-checklist.md`：OKX.AI Genesis 规则、奖金、表单字段与当前提交状态
- `docs/demo-storyboard.html`：可直接录屏的 80 秒中文演示分镜

## 本地验证

```bash
python3 tests/validate.py
python3 tests/validate.py --outputs evals/live
```

Windows 诊断脚本只读，不写文件、不改注册表、不改服务：

```powershell
powershell -NoProfile -File .\skills\valorant-cn-performance\scripts\diagnose.ps1
```

如果本机执行策略阻止脚本，优先复制执行所需的只读查询，或使用组织允许的签名流程；不要永久降低系统执行策略。

## 当前边界

- 本包是诊断与建议 Skill，不是远程控制器，也不承诺固定 FPS 提升。
- 不修改、终止或绕过 ACE/Vanguard，不推荐“反作弊关闭器”、魔改系统或一键优化包。
- 关闭 HVCI/VBS/Hyper-V 不是通用性能建议，只能在腾讯官方所述的特定虚拟化弹框路径里，解释安全与开发环境代价后由用户决定。
- OKX.AI 身份与服务资料已经过上架格式检查，但尚未得到最终链上创建确认，因此还没有 Agent ID、未进入审核、未上线、未发 X、未提交黑客松。

## 已验证状态

- Agent Skills 官方参考校验器：`Valid skill`
- 6 个真实 Agent 回归：`212/212` 契约检查通过
- PowerShell：完成静态只读检查；尚未在 Windows 真机执行，因此不声明真机兼容或性能收益

## 公开发布

- 仓库：<https://github.com/1924902988hu-del/valorant-cn-performance-skill>
- v1.0.0：<https://github.com/1924902988hu-del/valorant-cn-performance-skill/releases/tag/v1.0.0>
- 安装包：<https://github.com/1924902988hu-del/valorant-cn-performance-skill/releases/download/v1.0.0/valorant-cn-performance.skill>
- 安装包 SHA-256：`d99a837e30aa3bff399da23b5a1c70e320206898d8d6380ef2433745271b6b3f`
- 主分支发布提交：`935ce19eac9f7a74e680f6504edc0469b98ea31a`

Evidence refreshed: 2026-07-22.

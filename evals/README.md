# 固定回归评测

`cases/` 包含 6 个不可随意改写的输入，用来防止 Skill 在迭代中重新出现危险或过时建议。

## 两层验证

1. `python3 tests/validate.py`：校验包结构、frontmatter、引用、只读脚本禁用词、用例 schema，并用 `fixtures/` 验证断言器自身。
2. 真实 Agent 回归：在启用本 Skill 的 Agent 中逐条发送 `prompt`，把完整回答保存为同名 `.md`，再运行：

```bash
python3 tests/validate.py --outputs /path/to/agent-outputs
```

评测器检查每个输出的 `required` 和 `forbidden` 片段。它只能证明关键安全/内容契约是否出现，不能替代人工判断、Windows 真机基准或用户验收。

`fixtures/` 是断言器的样例交付，不是声称来自真实模型/真机的成绩。

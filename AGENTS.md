# luca · 启动协议（Codex / 其它 agent CLI 入口）

> 这扇门唤醒 luca，协议对所有 AI 一致。进来**按顺序读这两篇，再回应**：

1. **[SOUL.md](SOUL.md)** —— 我的**人格**（我是谁、怎么待你、信什么、什么脾气）。
2. **[CLAUDE.md](CLAUDE.md)** —— 我**怎么运作**（身体目录 / 怎么记 / 进项目第一动作）。里面 `@SOUL.md` 那行 = 第 1 步已读，跳过即可。

## Room 实效性

`projects/` 下 TODO、BUG、PRD、EXP 等账本发生新增、修改、状态迁移或删除时，必须在同一轮同步重渲染 `projects/room/` 中受影响的页面和详情页，并校验统计、状态、导航与本地链接一致。账本仍是唯一事实源，`room/` 只做展示，不得反向写回账本。

## Git 提交规范

本节是 AgentOS 项目域唯一的通用 Git 提交规范；各子仓库只补充自身验证要求，不重复定义或改写本节。

1. 单次 commit 只包含一个逻辑主题，禁止混入无关修改。
2. 仅在用户直接要求提交，或当前工作流明确包含 commit 时提交；一次授权只覆盖当前一轮修改。
3. 提交前确认必要验证已通过、无未决冲突、diff 范围清楚且处于可提交状态。
4. 提交前执行 `git pull --rebase`；工作区存在未提交修改时使用 `--autostash`；没有 upstream 时跳过同步。
5. commit 与 push 分别授权；允许 commit 不代表允许 push。
6. 涉及多个 Git root 时，每个仓库分别检查、同步、暂存、提交和汇报。

Commit message 必须使用 Conventional Commits：

```text
<feat|fix|refactor|docs|chore|test|ci|perf>(scope): 中文 subject
```

- type 必填，使用以上标准类型。
- scope 可省略；填写时必须对应实际模块或子系统。
- subject 使用中文，简洁明确，不超过 50 字，禁止模糊描述。
- “使用中文”只约束 subject，不得省略 type 或使用“修复：”“功能：”等中文前缀代替 type。
- 必要时补充 body，说明变更原因、变更方式和验证步骤。

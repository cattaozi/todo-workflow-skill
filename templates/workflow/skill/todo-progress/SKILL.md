# todo-progress — 推进 TODO 的 SOP

> 任何 AI 助手在**推进** TODO 状态之前，先按本文件作为运行时合约。
> 配对 SOP：[`../todo-create/SKILL.md`](../todo-create/SKILL.md)（创建 TODO 时用）。
> 用户可以随时问"你刚才那条操作走的是哪条规则？"——AI 必须答得上。

## 文件位置

- 索引：`.workflow/todo/index.md`（活跃表 + 搁置表 + 归档表）
- 单条详情：`.workflow/todo/TODO_NNN_<短描述>.md`
- **结构约定**：[`../../todo/README.md`](../../todo/README.md) —— 修改 index.md 前**首次本 session** 必读，定义了列序 / 列格式 / 修改规则。不要现编。

## 状态全景

| 状态 | emoji | 含义 |
|---|---|---|
| `todo` | ⚪ | 未开始（可拾取） |
| `in_progress` | 🟡 | 在做 |
| `on_hold` | ⏸️ | 搁置——已成形但现在不具备条件，主动泊车，等复活条件 |
| `done` | 🟢 | 完成 |
| `abandoned` | ⚫ | 放弃 |

合法转换：

```
   todo ⇄ on_hold ──→ in_progress ──→ done
     └───────┴────────────┴────────→ abandoned
```

> `in_progress` 做到一半遇阻，也可退回 `on_hold`。
> **`on_hold` 不是垃圾场**：进它必须有 DoD + **复活条件**（"等什么才能继续"）。写不出复活条件 → 要么是 EXP（还没想清，回灵感池），要么老实 `abandoned`。

## DoD vs AC 的区别（**推进时必须查 AC**）

| | 完成定义 (DoD) | 验收条件 (AC) |
|---|---|---|
| **形态** | 一两句话目标态 | 可勾选清单 |
| **谁用** | 工程师对照自己说"做完了" | 任何人（含未来的你）拿来逐条核对 |
| **特征** | 抽象、隐含 | 具体、可观测、布尔 |

**状态门槛靠 AC 判定，不是靠"觉得做完了"**。

## 状态转换

### todo → in_progress（开始做）

**门槛：AC 必须已写好**

- AC 仍是 TBD / 不存在 → **拒绝开始**，回头走 [todo-create](../todo-create/SKILL.md) 让 PM 补 AC
- AC 已写齐：
  - 更新详情文件 frontmatter `status: in_progress`
  - 更新 `index.md` 状态列 → 🟡

### in_progress → done（完成）

**门槛 1：AC 全部勾完**（严格——任何一条 `[ ]` 都不能转 done）

**门槛 2：验证通过**（项目相关，按下面 checklist 跑完）

- [ ] 后端动了：`<test-cmd>` / `<lint-cmd>` / `<type-cmd>` 通过
- [ ] 前端动了：`<type-check-cmd>` / `<lint-cmd>` / `<build-cmd>` 通过
- [ ] 涉及用户可见改动：**如果需要重启服务才能让用户验收，必须实际重启**（不能假设代码改了就跑通；user 拍板那一刻看到的必须是新代码）
- [ ] 涉及 API：curl 端到端跑通主路径（不止单测）
- [ ] 不因「工作量大」放弃以上任何一条（见 bootstrap §Step 0）

全部通过后：

- 更新 frontmatter `status: done` + `completed: <YYYY-MM-DD>`
- 移到 `index.md` 归档表（含完成日期）
- 详情文件可选加 `## 关键决策`，**仅在出现非显然决策时**（比如换了选型 / 撤销了 PRD 写的方案 / 踩了非常规坑）；常规执行不需要赘述，commit message 已经记够了

### → on_hold（搁置）/ on_hold → 唤回

**门槛：有 DoD + 明确复活条件**（不要求 AC——AC 是"开做"的门槛，搁置还没开做）

搁置（`todo` 或 `in_progress` → `on_hold`）：

- 更新 frontmatter `status: on_hold`
- `note` 必须写**为什么搁置 + 复活条件**（如"等 #064 落地"、"等并行场景出现"、"等产品拍板"）
- `index.md`：从活跃表移到**搁置表**，**原因列**填 note
- 复活条件写不出 → 不该搁置：回 EXP（还没想清）或 `abandoned`（确定不做）

唤回（`on_hold` → `todo` / `in_progress`）：

- 复活条件满足后，`status` 改回 `todo`（回池待排）或 `in_progress`（直接开做，**仍走 AC 门槛**）
- `index.md`：从搁置表移回活跃表

### todo / in_progress / on_hold → abandoned

- 更新 frontmatter `status: abandoned` + `completed` 日期（用放弃日期）
- `note` 必须写**为什么放弃**（一句话）
- 移到 `index.md` 归档表，**原因列**填放弃理由

## 推进完成的 AC（**元 AC** —— 推进动作本身的验收）

每次状态转换后核对：

- [ ] 详情文件 frontmatter status / completed 字段已更新
- [ ] `index.md` 中该条目移到了正确分区（活跃 / 搁置 / 归档）
- [ ] (on_hold / abandoned) **原因列已填**（搁置含复活条件 / 放弃含理由）
- [ ] (done) 验证 checklist 全过（见上）

> **不再要求 count 字段同步** —— index.md 的总数靠现场数表格行得到，不存 frontmatter。

## 红线

- **没有 AC 不能转 in_progress** —— AC 是 PM 责任，缺了就回头走 [todo-create](../todo-create/SKILL.md)
- **没勾完 AC 不能转 done** —— 工程师不能自己说"差不多了"
- **AC 不能临场放水** —— 如果一条 AC 实际做不了或语义不对，**改 AC 内容**（甚至拆出新 TODO），**不能编理由打勾**
- **不要跨级跳** —— 只允许上图列出的合法转换；不要 todo → done 跳过 in_progress
- **`on_hold` 必须带复活条件** —— 搁置不是软放弃；说不出"等什么才能继续"就别搁置（回 EXP 或 abandon）
- **搁置 / 放弃必须写原因** —— index 原因列空着的 `on_hold` / `abandoned` 不算合法状态
- **不要重排编号** —— done / abandoned 的也保留原编号
- **不要自动提交 commit** —— TODO 完成只更新文件；git commit 永远等用户拍板
- **「工作量大」不能让你少跑验证** —— 见 bootstrap §Step 0；如果 pytest fixture 麻烦就修 fixture，不是绕过

---
name: todo-progress
description: 推进 / 开始 / 关闭 TODO，含状态门槛。当用户要"做/开始 #NN"、"#NN 做完了/完成/关闭/收工/搞定/done"、搁置/放弃 TODO、或"推进 Epic"时用。需当前项目已有 .workflow/。
argument-hint: "[#编号 + 操作，如 '开始 #12' / '#12 做完了' / '搁置 #12' / '推进 Epic：<名>']"
---

# /tf:todo-progress — 推进 TODO 的 SOP

> 本技能即"推进 TODO"的运行时合约。操作**当前项目**的 `.workflow/todo/`。配对：`/tf:todo-create`。
> 用户输入：$ARGUMENTS。前置：当前项目**没有 `.workflow/`** → 提示先 `/tf:init`，停。

## 文件位置

- 索引：`.workflow/todo/index.md`（活跃表 + 专项表 + 搁置表 + 已完结专项 + 归档表）
- 单条详情：`.workflow/todo/TODO_NNN_<短描述>.md`
- **索引格式（列序 / 列格式 / 排序 / 修改规则）**：见 `/tf:todo-create` §索引格式（那是权威 schema）。改 index 前照它，不要现编。下面只列推进时高频用到的迁表/排序要点。

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
> **`on_hold` 不是垃圾场**：进它必须有 DoD + **复活条件**（"等什么才能继续"）。写不出复活条件 → 要么是 EXP（回灵感池），要么老实 `abandoned`。

## DoD vs AC 的区别（**推进时必须查 AC**）

| | 完成定义 (DoD) | 验收条件 (AC) |
|---|---|---|
| **形态** | 一两句话目标态 | 可勾选清单 |
| **谁用** | 工程师对照自己说"做完了" | 任何人拿来逐条核对 |
| **特征** | 抽象、隐含 | 具体、可观测、布尔 |

**状态门槛靠 AC 判定，不是靠"觉得做完了"**。

## 状态转换

### todo → in_progress（开始做）

**门槛：AC 必须已写好**

- AC 仍是 TBD / 不存在 → **拒绝开始**，回头走 `/tf:todo-create` 让 PM 补 AC
- AC 已写齐：更新详情 frontmatter `status: in_progress`；更新 `index.md` 状态列 → 🟡

### in_progress → done（完成）

**门槛 1：AC 全部勾完**（严格——任何一条 `[ ]` 都不能转 done）

**门槛 2：验证通过**（项目相关，按下面 checklist 跑完）

- [ ] 后端动了：`<test-cmd>` / `<lint-cmd>` / `<type-cmd>` 通过
- [ ] 前端动了：`<type-check-cmd>` / `<lint-cmd>` / `<build-cmd>` 通过
- [ ] 涉及用户可见改动：**需要重启服务才能让用户验收的，必须实际重启**（user 拍板那刻看到的必须是新代码）
- [ ] 涉及 API：curl 端到端跑通主路径（不止单测）
- [ ] 不因「工作量大」放弃以上任何一条（见 bootstrap §Step 0）

全部通过后：

- 更新 frontmatter `status: done` + `completed: <YYYY-MM-DD>`
- 移到 `index.md` 归档表（含完成日期），**按完成日期降序插到正确位置**（见 `/tf:todo-create` §索引格式·排序规则）
- 若执行中冒出**非显然决策**，补进 `## 关键决策 / 方案`（长存的设计理由）

### → on_hold（搁置）/ on_hold → 唤回

**门槛：有 DoD + 明确复活条件**（不要求 AC）

搁置：`status: on_hold`；`note` 写**为什么搁置 + 复活条件**；`index.md` 从活跃表移到**搁置表**，**原因列**填 note。复活条件写不出 → 回 EXP 或 `abandoned`。

唤回：`status` 改回 `todo` / `in_progress`（直接开做**仍走 AC 门槛**）；从搁置表移回活跃表。

### todo / in_progress / on_hold → abandoned

- `status: abandoned` + `completed` 日期（用放弃日期）；`note` 写**为什么放弃**；移到归档表，**原因列**填理由

> **Epic 成员是例外：成员不拆散**。上面"迁到归档 / 搁置"只对**散户 TODO**。**Epic 成员**任何状态都留在自己的 `### Epic：<名>` 表，**原行改 emoji + 填 `完成`（done/abandoned 填日期）+ `原因/备注` 列**（🟢 选填产出 / ⚫ 必填放弃理由 / ⏸️ 必填复活条件）。
>
> **但整张 Epic 表会随完结而搬家**：当**最后一个成员**转 🟢/⚫，把**整个 Epic 块从 `## 专项` 迁到 `## 已完结专项`**（在 `## 归档` 之前，成员行不拆）。目的：`## 专项` 只留在做的。详见 `/tf:todo-create` §索引格式。

## 推进整个 Epic（专项）

用户说"**推进 Epic：<名>**"时：

1. **读 index** `## 专项` 下 `### Epic：<名>` 表，取成员清单（行序 = 推进顺序）。
2. **算就绪顺序**：跳过 `依赖` 列里还没 done 的前置项；先推无未完成依赖的成员。
3. **逐个推**：每个就绪成员走标准转换（`todo → in_progress → done`），**每步门槛照常**。
4. **遇阻即停、不硬推**：缺 AC / 撞到需用户拍板 / 验证不过 → **停在那条，报告**进度，等用户。
5. **每完成一个就更新 index**：done 成员**原行**改 🟢 + 填 `完成` + `原因/备注`（**成员不拆**）。
6. **全部 🟢/⚫** → **把整个 Epic 块从 ## 专项 迁到 ## 已完结专项**（成员不拆），报告 Epic 收尾。

> 红线：推 Epic 是"**带顺序的批量驱动**"，不是"降低单条门槛"。

## 推进完成的 AC（**元 AC**）

- [ ] 详情 frontmatter status / completed 已更新
- [ ] `index.md` 位置正确：散户 TODO 迁到对应分区；Epic 成员**原地**改状态 + 填 `完成` + `原因/备注`
- [ ] (Epic 末位成员完结) 整块 Epic 已从 `## 专项` 迁到 `## 已完结专项`
- [ ] (on_hold / abandoned) **原因列已填**
- [ ] (done) 验证 checklist 全过

## 红线

- **没有 AC 不能转 in_progress** —— 缺了回头走 `/tf:todo-create`
- **没勾完 AC 不能转 done** —— 不能自己说"差不多了"
- **AC 不能临场放水** —— 改 AC 内容（甚至拆新 TODO），不能编理由打勾
- **不要跨级跳** —— 不要 todo → done 跳过 in_progress
- **`on_hold` 必须带复活条件**；**搁置 / 放弃必须写原因**
- **不要重排编号**；**不要自动提交 commit**
- **「工作量大」不能让你少跑验证** —— 见 bootstrap §Step 0

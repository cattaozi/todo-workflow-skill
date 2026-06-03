# todo-create — 创建 TODO 的 SOP

> 任何 AI 助手在**创建** TODO 之前，按本文件作为运行时合约。
> 配对 SOP：[`../todo-progress/SKILL.md`](../todo-progress/SKILL.md)（推进 TODO 状态时用）。
> 用户可以随时问"你刚才那条操作走的是哪条规则？"——AI 必须答得上。
>
> 同目录还有 [`TEMPLATE.md`](TEMPLATE.md) —— 创建新 TODO 时复制它当起点。

## TODO 的边界（**先想清这条再开**）

TODO 是**计划级**轨道——一件值得"开始 → 推进 → 验收"流程的事。

- ✅ "实现登录后端"、"接入 markdown 编辑器"、"做图片 EXIF 解析"
- ❌ "改个变量名"、"调下 padding"、"修个 typo"——直接做，不走流程
- ❌ "整理一下代码"——目标太虚

判定标准：**说不出 DoD 就不该开 TODO**。说得出 DoD 但目标 < 半天 → 也不开（直接做 + commit）。

## 触发场景

- **从 PRD 拆**：PRD §四 phase 拆出可交付单元（最常见）
- **从 EXP promote**：`EXP_NNN` status: `seed → promoted`，对应转出一条或多条 TODO
- **临时新需求**：用户反馈、设计变更、新发现的子问题
- **interrupt**：做 TODO_A 时发现独立的 TODO_B 该做（见 bootstrap §中途冒出新任务）

## 文件位置

- 索引：`.workflow/todo/index.md`（汇总视图，一行一条）
- 单条详情：`.workflow/todo/TODO_NNN_<短描述>.md`（**每条 TODO 都必须有**）

## 单条 frontmatter

```yaml
---
id: NN
title: "<标题>"
status: todo
added: "YYYY-MM-DD"
completed: null         # done / abandoned 时填日期
prd: "PRD_001"          # 可选，从哪个 PRD 拆来
explore: "EXP_001"      # 可选，从哪个预研转来
phase: "A"              # 可选，phase 归属
priority: P0 | P1 | P2  # 可选
note: "一句话当前进展"
---
```

## 详情文件结构（**强制章节**）

完整模板见同目录 [`TEMPLATE.md`](TEMPLATE.md)。创建 TODO 时**复制它当起点**，按方括号 / 注释填空。

最小**强制章节**：

- `## 背景 / Why`
- `## 任务`（checkbox 列表）
- `## 完成定义（DoD）`
- `## 验收条件（AC）`（可暂留 TBD）
- `## 关联`

## DoD vs AC 的区别（**写 TODO 时不能混**）

| | 完成定义 (DoD) | 验收条件 (AC) |
|---|---|---|
| **形态** | 一两句话目标态 | 可勾选清单 |
| **谁用** | 工程师对照自己说"做完了" | 任何人（含未来的你）拿来逐条核对 |
| **特征** | 抽象、隐含 | 具体、可观测、布尔 |
| **示例（坏 AC）** | "组件能用、视觉对" | —— |
| **示例（好 AC）** | —— | "Button 三个变体都能渲染；hover 时主按钮上浮 2px + 阴影；`pnpm build` 0 error" |

## 创建步骤

1. **粒度自检**（详见 §粒度判断）：能不能 0.5-2 天干完？不能 → 先拆分，**不要硬塞**
2. **分配编号**：上一个 + 1，**永不复用**（done / abandoned 的也不能复用）
3. **创建详情文件** `TODO_NNN_<短描述>.md`：
   - 完整 frontmatter（含 `prd` / `phase` / `priority` 关联字段）
   - **至少**写齐这 3 节：`背景 / Why`、`任务`、`完成定义 (DoD)`
   - `验收条件 (AC)` 可暂留 TBD（PM 责任，必须在 todo-progress 推进到 in_progress 之前补）
4. **在 `index.md` 加一行**——首次本 session 操作 index 前，**先 Read [`../../todo/README.md`](../../todo/README.md) §index.md schema**，按那里规定的列序 + 列格式写。不要现编。

## 创建完成的 AC（**元 AC** —— 创建动作本身的验收）

- [ ] 详情文件 frontmatter 完整（id / title / status: todo / added / 关联字段）
- [ ] 详情文件至少 3 节：背景 + 任务 + DoD
- [ ] `index.md` 活跃项加了行（含状态 emoji、添加日期）

> **不再要求 count 字段同步** —— index.md frontmatter 不存 count；要数总数现场数表格行即可。

## 粒度判断

一条 TODO 应满足：

- ✅ **0.5 - 2 天**能干完
- ✅ 有明确的 DoD（AC 可暂留 TBD）
- ✅ 可独立 commit、独立 demo
- ❌ 不是"一周的工程"或"一个 phase"
- ❌ 不是"未来某个想法"（那是 EXP）
- ❌ 不是"5 分钟的改动"（直接做）

## 红线

- **不要批量创建一堆但都不完整** —— 宁可一条条做实，每条至少有背景 + DoD
- **不要为"将来可能要做"的事开 TODO** —— 那是 EXP（status: seed）。但**用户明确说"开 TODO"时听用户**
- **不要为 5 分钟的改动开 TODO** —— TODO 是计划级；零碎改直接做 + commit
- **不要省 DoD** —— 创建时连"完成态长什么样"都说不清，就该回去拆需求 / 写 PRD，而不是开 TODO
- **不要重排编号** —— 永不复用，包括 done / abandoned 的
- **AC 拖延有限度** —— 创建时可以 TBD，但**不能进 in_progress 仍 TBD**（这是 todo-progress 的门槛）

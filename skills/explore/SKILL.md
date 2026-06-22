---
name: explore
description: 把半生不熟的想法登记/推进为预研（EXP）。当用户说"我有个想法 / 预研一下 / 探索 X / 能不能用 X 做"时用。需当前项目已有 .workflow/ 且启用 EXP 域。
argument-hint: "[想法一句话，或 EXP 编号]"
---

# /tf:explore — 预研推进 SOP

> 灵感池。"我想试试..." / "如果用 X 来做..." 这种半生不熟的想法先进这里。
> 用户输入：$ARGUMENTS。前置：当前项目**没有 `.workflow/`** → 提示先 `/tf:init`；项目**没有 EXP 域** → 告知未启用 EXP，停。

## 状态

| 状态 | 含义 |
|---|---|
| `seed` | 刚记下，没动 |
| `exploring` | 在调研、做 spike |
| `promoted` | 成熟了，转 TODO 或 PRD |
| `dropped` | 想清楚了不做，记原因 |

## 登记 EXP（动作）

> 按统一骨架读：**触发 → 门槛 → 状态写入 → index 迁移 → 必填项**（与 `/tf:todo-create`、`/tf:todo-progress` 各动作同构）。

- **触发**：用户说"我有个想法 / 预研一下 / 探索 X / 能不能用 X 做"。
- **门槛**：无——灵感池就是低门槛入口（但别把 seed 直接当 TODO 做，见 §红线）。
- **状态写入**：新建 `EXP_NNN_<短描述>.md`（编号 3 位，**永不复用**），frontmatter `status: seed` + 正文六段：**背景 / 起源**、**核心想法**（一句话）、**价值假设**、**风险与未知**、**下一步**。
- **index 迁移**：按 §索引格式·修改规则，活跃表加行。不要现编。
- **必填项**：扫 `.workflow/prd/index.md` 与 `.workflow/todo/index.md`，**标关联、避免重复**。

## 推进 EXP（状态转换）

> 用户说"推进 EXP #N"进入。每个动作仍按上面五栏骨架读。

### seed → exploring（开始调研）

- **触发**：用户要深入这条 EXP。
- **门槛**：无。
- **状态写入**：frontmatter `status: exploring`；文档追加调研记录 / 链接 / 代码片段。
- **index 迁移**：状态列 → 🟡（留活跃表）。
- **必填项**：无。

### → promoted（转 TODO / PRD）

- **触发**：想法成熟、能说清要做什么。
- **门槛**：小功能 → 转 TODO（走 `/tf:todo-create`）；大功能 → 转 PRD。
- **状态写入**：frontmatter `status: promoted` + `promoted_to: "TODO #NN"` / `"PRD_NNN"`。
- **index 迁移**：删活跃行、归档表加行，备注写 `promoted_to`。
- **必填项**：`promoted_to` 已填。

### → dropped（想清不做）

- **触发**：想清楚了不做。
- **门槛**：无。
- **状态写入**：frontmatter `status: dropped` + `note` 写原因。
- **index 迁移**：归档表加行（⚫）。
- **必填项**：备注 / 原因已填。

## 红线

- **不要把 seed 直接当 TODO 做**——先想清楚再动
- **定期清池**：seed 超过 30 天没动的，review 还有没有价值

---

## 索引格式（`.workflow/explore/index.md` 的权威 schema —— 写之前照这个）

Frontmatter 只一行 `type: explore`，**禁存** count 类字段。两段：`## 活跃项` + `## 归档`。

- **活跃表列序**：`编号 | 标题 | 状态 | 添加 | 下一步`
- **归档表列序**：`编号 | 标题 | 状态 | 添加 | 完成 | 备注`
- 列内：编号 = `[EXP_NNN](EXP_NNN_xxx.md)`；状态 emoji ⚪seed/🟡exploring/🟢promoted/⚫dropped；添加·完成 = `MM-DD`；下一步 = 一句话 next-action（≤30 字）；备注（仅归档）= promote 到哪 / dropped 原因。
- **修改规则**：新 EXP → 活跃表加行；`seed→exploring` 改 🟡；`→promoted`（转 TODO/PRD）删活跃行+归档加行（备注写 promoted_to）；`→dropped` 归档 ⚫ + 备注写原因。
- **不要做的事**：改列序 / 把 promoted·dropped 留活跃表 / frontmatter 加 count。

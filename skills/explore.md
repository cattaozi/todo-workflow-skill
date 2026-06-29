# skills/explore —— 半生不熟的想法怎么进、怎么推

> 灵感池在当前项目间的 `explore/`。"我想试试…" / "如果用 X 来做…" 这种没想清的想法先进这里，**别直接当 TODO 做**。

## 登记 EXP（seed）

- **触发**：你说"有个想法 / 预研一下 / 探索 X / 能不能用 X 做"。
- **门槛**：无——低门槛入口。
- **建** `explore/EXP_NNN_<短描述>.md`（`status: seed`），正文六段：背景 / 起源 · 核心想法（一句话）· 价值假设 · 风险与未知 · 下一步。
- **落账**：`explore/index.md` 活跃表加行。
- **必带**：扫 `prd/` 和 `todo/` 账本，标关联、避免重复。

## 推进 EXP

- **seed → exploring**（开始调研）：`status: exploring`；文档追加调研记录 / 链接 / 代码片段；状态列 → 🟡。
- **→ promoted**（成熟，转 TODO / PRD）：小功能 → 走 `skills/todo.md`；大功能 → 走 `skills/prd.md`。`status: promoted` + `promoted_to`；删活跃行、归档加行（备注写转去哪）。
- **→ dropped**（想清不做）：`status: dropped` + note 写原因；归档（⚫）。

## 红线

- 不把 seed 直接当 TODO 做——先想清再动。
- 定期清池：seed 超 30 天没动的，review 还有没有价值。

# Explore — 预研推进 SOP

> 灵感池。"我想试试..." / "如果让 AI 给宝宝..." / "能不能用 LangGraph 做..." 这种半生不熟的想法先进这里。

## 触发

用户说"我有个想法" / "预研一下" / "探索 X" / "能不能..."

## 状态

| 状态 | 含义 |
|---|---|
| `seed` | 刚记下，没动 |
| `exploring` | 在调研、做 spike |
| `promoted` | 成熟了，转 TODO 或 PRD |
| `dropped` | 想清楚了不做，记原因 |

## 流程

### Step 1：结构化

创建 `.workflow/explore/EXP_NNN_<短描述>.md`：

```yaml
---
id: NNN
title: "xxx"
status: seed
added: "YYYY-MM-DD"
promoted_to: null
note: "一句话当前状态"
---
```

正文段落：

- **背景 / 起源**：为什么想到这个
- **核心想法**：一句话说清楚
- **价值假设**：如果做了，对家 / 对宝宝 / 对研究有什么价值
- **风险与未知**：不确定的点
- **下一步**：具体可以试什么，或者再放一放

### Step 2：关联

扫 `.workflow/prd/index.md` 和 `.workflow/todo/index.md`，避免重复，标关联。

### Step 3：归位

- 存入 `.workflow/explore/`
- 更新 `.workflow/explore/index.md` —— 首次本 session 操作 index 前，**先 Read [`../../explore/README.md`](../../explore/README.md) §index.md schema**，按列序 / 列格式写。不要现编。

## 推进

- 用户说"推进 EXP #N" → 在文档里追加调研记录、链接、代码片段
- 成熟后：
  - 小功能 → 转 TODO（status: `promoted`, `promoted_to: "TODO #NN"`）
  - 大功能 → 转 PRD（status: `promoted`, `promoted_to: "PRD_NNN"`）
- 想清楚不做 → status: `dropped` + note 写原因

## 红线

- **不要把 seed 直接当 TODO 做**——seed 没想清楚，先想清楚再动
- **定期清池**：seed 超过 30 天没动的，review 一下还有没有价值

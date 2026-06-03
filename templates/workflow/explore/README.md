# .workflow/explore/

预研 / 灵感池目录。每个 EXP 是独立文件（`EXP_NNN_*.md`），所有 EXP 通过 `index.md` 汇总。

> **何时读本文件**
> - 第一次往 `index.md` 写入之前（新建 EXP / 状态变更）
> - 跨项目移植本工作流之前
>
> 单纯**读** index.md 内容不需要先读本文件。

---

## 文件命名

```
EXP_<3位数字>_<英文短描述（连字符）>.md
```

- 例：`EXP_001_ai_family_steward.md`、`EXP_002_passkey_for_doorbell.md`
- 编号永不复用

## EXP 详情文件格式

见 [`../skill/explore/SKILL.md`](../skill/explore/SKILL.md) §Step 1 模板。

## index.md 结构约定（**写之前必读**）

### Frontmatter

只 `type` 一行：

```yaml
---
type: explore
---
```

**不存** count / seed_count / last_updated 等统计字段。

### 正文模板

````markdown
---
type: explore
---

<!-- 格式约定见 ./README.md -->

# 预研索引

> 状态：⚪ seed · 🟡 exploring · 🟢 promoted · ⚫ dropped
> 流程详见 [`../skill/explore/SKILL.md`](../skill/explore/SKILL.md)。

## 活跃项

| 编号 | 标题 | 状态 | 添加 | 下一步 |
|---|---|---|---|---|
| [EXP_001](EXP_001_ai_family_steward.md) | AI 家庭管家 | ⚪ | 06-03 | 等 MVP 上线再推进 |

## 归档

| 编号 | 标题 | 状态 | 添加 | 完成 | 备注 |
|---|---|---|---|---|---|
````

### 列序（钉死，禁改）

**活跃表**：`编号 | 标题 | 状态 | 添加 | 下一步`

**归档表**：`编号 | 标题 | 状态 | 添加 | 完成 | 备注`

### 列内格式约定

| 列 | 格式 | 例 |
|---|---|---|
| **编号** | markdown link `[EXP_NNN](EXP_NNN_xxx.md)` | `[EXP_001](EXP_001_ai_family_steward.md)` |
| **状态** | emoji：⚪ seed / 🟡 exploring / 🟢 promoted / ⚫ dropped | `⚪` |
| **添加 / 完成** | `MM-DD`（跨年 `YYYY-MM-DD`） | `06-03` |
| **下一步** | 一句话当前 next-action（不超 30 中文字符） | `跑通 py-webauthn demo + iPad Safari 实测` |
| **备注**（仅归档） | 一句话总结：promote 到哪 / dropped 原因 | `promoted → TODO #033` 或 `dropped: 性能瓶颈不可解` |

### 修改规则

| 触发动作 | 改什么 | 触发 SOP |
|---|---|---|
| 新 EXP（"我有个想法"）| 活跃表加一行 | [explore](../skill/explore/SKILL.md) §Step 1 |
| `seed → exploring`（在做 spike） | 状态 emoji 改 🟡 | 同上 §推进 |
| `→ promoted`（成熟，转 TODO 或 PRD） | 删活跃行，归档加一行（备注写 promoted_to） | 同上 |
| `→ dropped`（想清不做） | 同上，状态 ⚫，备注写原因 | 同上 |

### 不要做的事

- ❌ 改列序
- ❌ 把 promoted / dropped 留在活跃表
- ❌ 在 frontmatter 加 count 字段

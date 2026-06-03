# .workflow/prd/

产品需求文档目录。每个 PRD 是独立文件（`PRD_NNN_*.md`），所有 PRD 通过 `index.md` 汇总。

> **何时读本文件**
> - 第一次往 `index.md` 写入之前（新建 PRD / 状态变更）
> - 跨项目移植本工作流之前
>
> 单纯**读** index.md 内容不需要先读本文件。

---

## 文件命名

```
PRD_<3位数字>_<英文短描述（连字符）>.md
```

- 例：`PRD_001_mvp.md`、`PRD_002_user_dashboard.md`
- 编号永不复用

## PRD 详情文件格式

由用户自己写。工程的 AI 负责 review，流程见 [`../skill/prd-review/SKILL.md`](../skill/prd-review/SKILL.md)。

## index.md 结构约定（**写之前必读**）

### Frontmatter

只 `type` 一行：

```yaml
---
type: prd
---
```

**不存** count / draft_count / shipped_count / last_updated 等统计字段。

### 正文模板

````markdown
---
type: prd
---

<!-- 格式约定见 ./README.md -->

# PRD 索引

> 状态：⚪ draft · 🟡 ready · 🟢 shipped · ⚫ archived
> 流程详见 [`../skill/prd-review/SKILL.md`](../skill/prd-review/SKILL.md)。

## 活跃项

| 编号 | 标题 | 状态 | 添加 | 澄清(R) | 关联 TODO |
|---|---|---|---|---|---|
| [PRD_001](PRD_001_mvp.md) | 产品 MVP | ⚪ | 06-03 | 0 | #009-#032 |

## 归档

| 编号 | 标题 | 状态 | 添加 | 完成 | 备注 |
|---|---|---|---|---|---|
````

### 列序（钉死，禁改）

**活跃表**：`编号 | 标题 | 状态 | 添加 | 澄清(R) | 关联 TODO`

**归档表**：`编号 | 标题 | 状态 | 添加 | 完成 | 备注`

### 列内格式约定

| 列 | 格式 | 例 |
|---|---|---|
| **编号** | markdown link `[PRD_NNN](PRD_NNN_xxx.md)` | `[PRD_001](PRD_001_mvp.md)` |
| **状态** | emoji：⚪ draft / 🟡 ready / 🟢 shipped / ⚫ archived | `⚪` |
| **添加 / 完成** | `MM-DD`（跨年 `YYYY-MM-DD`） | `06-03` |
| **澄清(R)** | 工程 review 待澄清项数；`0` 表示无 | `3` |
| **关联 TODO** | 从本 PRD 拆出的 TODO 编号范围 | `#009-#032` |
| **备注**（仅归档） | 一句话总结 | `MVP 上线；6 房间 + 鉴权 + 上传` |

### 修改规则

| 触发动作 | 改什么 | 触发 SOP |
|---|---|---|
| 新 PRD draft | 活跃表加一行 | 用户自己写文件；AI 顺手加索引行 |
| 工程 review 找出待澄清项 | 改"澄清(R)"列计数 | [prd-review](../skill/prd-review/SKILL.md) |
| `draft → ready`（review 完成、所有澄清项解决） | 状态 emoji 改 🟡 | 同上 |
| `ready → shipped`（PRD 拆的 TODO 全部 done） | 删活跃行，归档加一行 | 同上 |
| `→ archived`（决定不做） | 同上，状态 ⚫，备注写原因 | 同上 |

### 不要做的事

- ❌ 改列序
- ❌ 把 shipped / archived 留在活跃表
- ❌ 在 frontmatter 加 count 字段

# .workflow/todo/

行动项目录。每条 TODO 是独立文件（`TODO_NNN_*.md`），所有 TODO 通过 `index.md` 汇总。

> **何时读本文件**
> - 第一次往 `index.md` 写入之前（创建 TODO / 状态变更）
> - 设计新的 TODO 分组方式
> - 跨项目移植本工作流之前
>
> 单纯**读** index.md 内容不需要先读本文件。

---

## 文件命名

```
TODO_<3位数字>_<英文短描述（连字符）>.md
```

- 例：`TODO_016_backend_auth.md`、`TODO_028_notes_reading_and_yard.md`
- 编号**永不复用**（done / abandoned 也保留原号）
- 短描述用英文连字符（snake-case），便于跨平台、命令行友好

## TODO 详情文件格式

见 [`../skill/todo-create/TEMPLATE.md`](../skill/todo-create/TEMPLATE.md)。

## index.md 结构约定（**写之前必读**）

### Frontmatter

只保留 `type` 一行，**禁止**存 count / done_count / active_count / last_updated 等统计字段（这些手工同步是 bug 工厂；要数总数靠数表格行）。

```yaml
---
type: todo
---
```

### 正文模板（严格按这个顺序）

````markdown
---
type: todo
---

<!-- 格式约定见 ./README.md。frontmatter 不存 count；分组依据见下方 §分组约定 -->

# TODO 索引

> 状态：⚪ 未开始 · 🟡 进行中 · 🟢 完成 · ⚫ 放弃
> 操作规则：创建走 [`../skill/todo-create/SKILL.md`](../skill/todo-create/SKILL.md)；推进走 [`../skill/todo-progress/SKILL.md`](../skill/todo-progress/SKILL.md)。
> 注：分组依据见本目录 README §分组约定。

## 活跃项

### <分组名 1>（如 Phase A · 静态家）

| 编号 | 标题 | 状态 | 添加 | 优先级 | 依赖 |
|---|---|---|---|---|---|
| [#016](TODO_016_backend_auth.md) | 后端鉴权 | 🟡 | 06-03 | P0 | —— |

### <分组名 2>

...

## 归档

| 编号 | 标题 | 状态 | 添加 | 完成 | 备注 |
|---|---|---|---|---|---|
| [#009](TODO_009_visual_foundation.md) | 视觉基础设施 | 🟢 | 06-03 | 06-03 | 8 公共组件 + 6 路由通 |
````

### 列序（**钉死，禁改**）

**活跃表**：`编号 | 标题 | 状态 | 添加 | 优先级 | 依赖`

**归档表**：`编号 | 标题 | 状态 | 添加 | 完成 | 备注`

### 列内格式约定

| 列 | 格式 | 例 |
|---|---|---|
| **编号** | markdown link `[#NNN](TODO_NNN_xxx.md)` | `[#016](TODO_016_backend_auth.md)` |
| **标题** | 一句话，不超 30 中文字符 | `后端鉴权（users + 登录 API + JWT）` |
| **状态** | emoji 单字符：⚪ todo / 🟡 in_progress / 🟢 done / ⚫ abandoned | `🟢` |
| **添加 / 完成** | `MM-DD`（年隐含；跨年时改 `YYYY-MM-DD`） | `06-03` |
| **优先级** | `P0` / `P1` / `P2`，无优先级留 `——`（中文破折号） | `P1` |
| **依赖** | 逗号分隔 `#NNN`；无依赖 `——` | `#016, #019` |
| **备注**（仅归档） | 一句话总结：关键产出 / 选型 / 决策提示 | `bcrypt 直调 + JWT 30 天；5 用例验证全通` |

### 分组约定（**项目级选择，项目内固定**）

活跃项分组方式按项目复杂度选一种：

| 项目类型 | 分组方式 | 示例 |
|---|---|---|
| 有 PRD 的产品项目 | **按 PRD phase** | `### Phase A · 静态家` |
| 无 PRD 的工具项目 | **按主题** | `### 鉴权` / `### 缓存` |
| 时间驱动项目 | **按月份** | `### 2026-06` |

选定后项目内保持一致，**不要混用**。

### 修改规则（什么时候改、由谁触发）

| 触发动作 | 改什么 | 由哪个 SOP 触发 |
|---|---|---|
| 创建新 TODO | 活跃项相应分组加一行 | [todo-create](../skill/todo-create/SKILL.md) §创建步骤 |
| `todo → in_progress` | 该行状态 emoji 改 🟡 | [todo-progress](../skill/todo-progress/SKILL.md) §状态转换 |
| `in_progress → done` | **删活跃行**，归档表加一行（含完成日期 + 备注） | 同上 |
| `→ abandoned` | 同 done，状态用 ⚫，备注写为什么放弃 | 同上 |
| 分组重命名 | 改 `### 标题`；行不动 | 谨慎操作；改完通知 user |

### 不要做的事

- ❌ 改列序
- ❌ 加新列（除非走"改 schema"流程，更新本 README）
- ❌ 把 done / abandoned 留在活跃表
- ❌ 用 `2026.06.03` 这种非 ISO 格式（点号易跟版本号混）
- ❌ 在 frontmatter 加 count 字段（看现状即可）

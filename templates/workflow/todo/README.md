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

> 状态：⚪ 未开始 · 🟡 进行中 · ⏸️ 搁置 · 🟢 完成 · ⚫ 放弃
> 操作规则：创建走 [`../skill/todo-create/SKILL.md`](../skill/todo-create/SKILL.md)；推进走 [`../skill/todo-progress/SKILL.md`](../skill/todo-progress/SKILL.md)。
> 注：分组依据见本目录 README §分组约定；专项（Epic）见 §专项约定。

## 专项（Epic）

> 一个 Epic = "同一件事拆出来的多个 TODO"。成员住这里**而不是** ## 活跃项；表结构和活跃表完全一致。
> 成员 `done`/`abandoned` 照常迁出到 ## 归档、`on_hold` 迁到 ## 搁置（靠 `epic:` 标签保留归属）——所以本区只显示**在做/待做**的活跃成员。

### Epic：Space 个人化模型落地

> 把 Space 改造成 opt-in 个人化成员模型；顺序：BE 迁移 → FE 重组 → 平台收口。

| 编号 | 标题 | 状态 | 添加 | 优先级 | 依赖 |
|---|---|---|---|---|---|
| [#080](TODO_080_platform_page.md) | 平台管理独立页 | 🟡 | 06-02 | P0 | #079 |
| [#081](TODO_081_idp_consume.md) | 接入 idp 消费侧 | ⚪ | 06-02 | P1 | #079 |

## 活跃项

### <分组名 1>（如 Phase A · 静态家）

| 编号 | 标题 | 状态 | 添加 | 优先级 | 依赖 |
|---|---|---|---|---|---|
| [#016](TODO_016_backend_auth.md) | 后端鉴权 | 🟡 | 06-03 | P0 | —— |

### <分组名 2>

...

## 搁置

| 编号 | 标题 | 状态 | 添加 | 原因（含复活条件） |
|---|---|---|---|---|
| [#042](TODO_042_parallel_clarify.md) | 并行节点澄清绑定 | ⏸️ | 05-18 | 等真实并行场景出现再做；当前链路触发不到 |

## 归档

| 编号 | 标题 | 状态 | 添加 | 完成 | 原因 |
|---|---|---|---|---|---|
| [#009](TODO_009_visual_foundation.md) | 视觉基础设施 | 🟢 | 06-03 | 06-03 | 8 公共组件 + 6 路由通 |
| [#064](TODO_064_evidence_rule.md) | evidence_rule 赋值 | ⚫ | 05-27 | 05-28 | PRD 信息塌方，强落=死代码；等产品对齐 |
````

### 列序（**钉死，禁改**）

**活跃表 / 专项表**：`编号 | 标题 | 状态 | 添加 | 优先级 | 依赖`（两者同构）

**搁置表**：`编号 | 标题 | 状态 | 添加 | 原因（含复活条件）`

**归档表**：`编号 | 标题 | 状态 | 添加 | 完成 | 原因`

### 列内格式约定

| 列 | 格式 | 例 |
|---|---|---|
| **编号** | markdown link `[#NNN](TODO_NNN_xxx.md)` | `[#016](TODO_016_backend_auth.md)` |
| **标题** | 一句话，不超 30 中文字符 | `后端鉴权（users + 登录 API + JWT）` |
| **状态** | emoji 单字符：⚪ todo / 🟡 in_progress / ⏸️ on_hold / 🟢 done / ⚫ abandoned | `🟢` |
| **添加 / 完成** | `MM-DD`（年隐含；跨年时改 `YYYY-MM-DD`） | `06-03` |
| **优先级** | `P0` / `P1` / `P2`，无优先级留 `——`（中文破折号） | `P1` |
| **依赖** | 逗号分隔 `#NNN`；无依赖 `——` | `#016, #019` |
| **原因**（搁置表） | **为什么搁置 + 复活条件**，必填，不能空 | `等 #064 落地；当前依赖未通` |
| **原因**（归档表） | `abandoned` 写**为什么放弃**（必填）；`done` 写关键产出 / 选型一句话（选填，可 `——`） | `PRD 塌方，强落=死代码` |

### 分组约定（**项目级选择，项目内固定**）

活跃项分组方式按项目复杂度选一种：

| 项目类型 | 分组方式 | 示例 |
|---|---|---|
| 有 PRD 的产品项目 | **按 PRD phase** | `### Phase A · 静态家` |
| 无 PRD 的工具项目 | **按主题** | `### 鉴权` / `### 缓存` |
| 时间驱动项目 | **按月份** | `### 2026-06` |

选定后项目内保持一致，**不要混用**。

### 专项约定（Epic）

| 规则 | 说明 |
|---|---|
| **何时用** | 一件事拆出 **≥3 个** TODO、且需要按序推进时，开一个 Epic。少于 3 个或松散相关 → 别开 |
| **vs PRD** | Epic 是**没有 PRD 的工程性倡议**（重构 / 迁移）。**有 PRD 就别再套 Epic**——PRD 的"关联 TODO"本来就是分组器 |
| **vs phase** | 一个 TODO 只有一个家：要么在某 Epic 表，要么在活跃项的某 phase 分组，不并存 |
| **成员标记** | 成员 frontmatter 加 `epic: "<名>"`，值 = 本区 `### Epic：` 后的名字，**逐字一致** |
| **成员迁移** | 成员状态流转和活跃项**完全一样**：done/abandoned → 归档、on_hold → 搁置（都保留 `epic:` 标）。本区只留活跃成员 |
| **Epic 完结** | 全部成员都 done/abandoned 后，删掉本区该 `### Epic：` 子段（成员留在归档、仍带标可追溯） |
| **顺序** | 成员行按推进顺序排；跨成员依赖写在各自 `依赖` 列。"推进整个 Epic" 走 [todo-progress](../skill/todo-progress/SKILL.md) §推进整个 Epic |

### 修改规则（什么时候改、由谁触发）

| 触发动作 | 改什么 | 由哪个 SOP 触发 |
|---|---|---|
| 创建新 TODO | 活跃项相应分组加一行；**属于 Epic 的** → 加到对应 `### Epic：` 表 | [todo-create](../skill/todo-create/SKILL.md) §创建步骤 |
| `todo → in_progress` | 该行状态 emoji 改 🟡（行在哪张表就改哪张） | [todo-progress](../skill/todo-progress/SKILL.md) §状态转换 |
| `→ on_hold`（搁置） | **删活跃/专项行**，搁置表加一行（状态 ⏸️ + **原因含复活条件**） | 同上 |
| `on_hold → 唤回` | **删搁置行**，移回原表（活跃项 or 对应 Epic）（状态 ⚪/🟡） | 同上 |
| `in_progress → done` | **删活跃/专项行**，归档表加一行（含完成日期 + 原因/产出） | 同上 |
| `→ abandoned` | **删活跃/专项/搁置行**，归档表加一行，状态 ⚫，**原因列写为什么放弃** | 同上 |
| 开 / 关 Epic | 加 / 删 `## 专项` 下的 `### Epic：<名>` 子段 | [todo-create](../skill/todo-create/SKILL.md) / [todo-progress](../skill/todo-progress/SKILL.md) |
| 分组重命名 | 改 `### 标题`；行不动 | 谨慎操作；改完通知 user |

### 不要做的事

- ❌ 改列序
- ❌ 加新列（除非走"改 schema"流程，更新本 README）
- ❌ 把 on_hold 留在活跃表（搁置的进搁置表）；把 done / abandoned 留在活跃表（进归档表）
- ❌ 搁置表 / 归档表的**原因列留空**
- ❌ 同一个 TODO 同时出现在 Epic 表和活跃项（一个 TODO 只有一个家）
- ❌ 给 < 3 个 TODO 或有 PRD 的需求硬开 Epic
- ❌ 用 `2026.06.03` 这种非 ISO 格式（点号易跟版本号混）
- ❌ 在 frontmatter 加 count 字段（看现状即可）

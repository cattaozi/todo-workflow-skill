# skills/room —— 我怎么把状态渲染给人看

> `room/` 是给用户看的项目房间。它把项目域和当前事项渲染成可浏览页面，但不成为新的事实源；luca 自身能力属于本体，不作为项目内容展示。

## 适用

- 用户想看 luca 当前管着什么。
- 用户要一个 dashboard、状态页、可视化汇报或项目域总览页面。
- 需要把 `projects/` 的账本、总览和记忆入口整理成面向人的阅读视图。

## 负责

- 生成或更新 `projects/room/` 下的多页面状态展示。
- 从本体文件和项目域事实中提炼给人看的当前状态。
- 让用户先从总览判断整体状态，再按主题进入当前事项、缺陷、需求 / 调研和记忆页面。

## 不负责

- 不把 `room/` 当事实源。
- 不从 `room/` 读回状态。
- 不在 dashboard 里创造新事实。
- 不替代 `projects/README.md`、BUG / TODO / PRD / EXP index 或 `memory/`。

## 页面文件

固定入口与专题页：

```text
projects/room/dashboard.html
projects/room/todo.html
projects/room/bugs.html
projects/room/product.html
projects/room/memory.html
projects/room/room.css
projects/room/room.js
projects/room/todo/TODO_NNNN.html
```

设计规范：

```text
skills/reference/design.md
```

事实来源：

- `CLAUDE.md`：项目域边界、记忆规则、协作规则。
- `projects/README.md`：外部资源、服务定义、协作约定、待确认事项。
- `projects/bug/index.md`：待修复和已修复 Bug。
- `projects/todo/index.md`：当前 TODO 和 Epic 状态。
- `projects/prd/index.md`：PRD 和产品建议稿状态。
- `projects/explore/index.md`：EXP 状态。
- `projects/memory/README.md`：长期记忆入口和防复发经验。

缺少某个来源时，不编造内容；对应区域显示为空、未初始化或待补充。

## 页面结构

`dashboard.html` 只做总览入口，包含：

1. **关键状态**：开放事项、Bug、PRD、EXP 和资源的摘要数字；事项统计采用 TODO 与 EPIC 同层的顶层口径。开放事项摘要下方固定展示按创建顺序最新的三个 TODO，不按状态过滤。
2. **项目域**：外部资源、远程 Git、服务定义和启动入口。外部资源表只显示“名称 / 简介 / 操作”三列；“简介”把 `projects/README.md` 中的“功能”和“一句话理解”合并在同一单元格呈现，不丢失任一事实。表格提供“移除”操作，但按钮只复制一段遵守 `skills/project.md` 移出协议的模型指令，不直接变更文件或删除资源。
3. **更新时间与来源**。专题页面只通过顶部 Tab 进入，不在总览正文重复生成入口卡。

专题内容分别进入：

- `todo.html`：TODO 与 EPIC 统一作为顶层事项参与列表和看板；EPIC 是含子 TODO 的特殊事项，只占一个顶层位置，子 TODO 默认折叠。EPIC 不占 TODO 数字编号，编号列和看板标识只显示 `EPIC`，并直接链接到对应的 `projects/todo/epic/<slug>.md` 说明文件；界面不展示 slug，也不得临时编造数字。TODO 列表统一使用“编号 / 事项 / 状态 / 操作”四列，不再单设“摘要”列；事项标题作为较大、较重的第一行，原摘要作为弱化的第二行。该两行结构同时适用于普通 TODO、EPIC 顶层和展开后的子 TODO；EPIC 的分段进度条就是标题下的第二行摘要。EPIC 列表标题末尾用低强调小字显示从 `projects/todo/index.md` 实时计算的 `N 个 TODO` 总数；只补总数，不恢复“开放 / 完成 / 废弃”文字汇总。四列表格必须使用统一的固定列轨：编号 `82px`、状态 `92px`、操作 `116px`，事项占据剩余宽度；普通 TODO、EPIC 跨列内部网格、展开后的子 TODO 都复用相同的状态和操作轨道，表头与每一行的状态徽标必须严格左对齐。操作列保留宽度，但表头不显示“操作”文字，只通过无障碍名称保留列语义。列表中的 EPIC 从“事项”列开始跨越状态和操作列：折叠内容在跨列区域内保持事项 / 状态 / 操作的对齐，展开后的子 TODO 表使用整段跨列宽度，不得被限制在事项单列。EPIC 进度条展示子 TODO 的进行中、可推进、等待依赖、搁置、已完成与已废弃构成，分段和计数必须从账本实时计算；EPIC 标题下不再重复显示“子 TODO / 开放 / 完成 / 废弃”文字汇总。列表和看板中的每个 TODO、EPIC 都提供“施工”“聊聊”两个复制按钮：TODO 的“施工”要求先评估可实施性并按 `skills/todo.md` 的“实施 TODO”协议生成开工简报，EPIC 的“施工”要求按“推进 Epic”协议生成推进简报，两者都必须等待用户拍板；“聊聊”分别复制带真实 TODO 编号或 Epic 标题与 slug 的状态讨论指令。操作按钮默认不显示，只在对应事项行或卡片被鼠标悬停、或其内部控件获得键盘焦点时显示；不支持悬停的触屏设备必须保留可操作的显示兜底。按钮不得直接修改账本、状态或代码。看板按进行中、可推进、等待依赖、搁置分列，依赖判断只依据账本显式状态；已完成与已废弃顶层事项放在页面末尾并默认折叠。每个 `TODO_NNNN` 从总览、列表、看板和 EPIC 子项统一进入 `projects/room/todo/TODO_NNNN.html` 详情页。
- `bugs.html`：待修复 Bug 与近期已修复摘要。
- `product.html`：PRD、产品建议稿和 EXP。
- `memory.html`：协作约定、长期记忆入口和待确认事项。

所有页面复用同一顶部 Tab 导航；项目域固定呈现在总览，其余主题只在自己的页面呈现完整明细。顶部 Tab 是唯一专题导航，不在总览正文重复入口。总览不展示 luca 自我介绍。room 内凡是包含两条及以上数据行的表格，都必须为整行提供统一、轻量的悬停底色反馈，并在行内控件获得键盘焦点时提供同等反馈；表头、空表和单行信息表不添加该效果。

## 生成规则

1. 确保 `projects/room/` 存在。
2. 读取 `skills/reference/design.md`，按它约束视觉、布局和 HTML 形态。
3. 按事实来源读取必要文件；读不到就标记缺失，不阻塞整体页面。
4. 生成可直接从本地文件打开的 HTML，复用本地 `room.css`，不依赖外网资源。默认不使用 JavaScript；用户明确要求复制、切换等本地交互时，使用最小本地 `room.js`，不得让页面直接执行账本迁移、外部资源移除或其它项目状态变更。
5. 页面只展示当前可确认事实；推测必须标明。
6. 每次生成都完整重渲染总览、四个专题页、全部 `TODO_NNNN` 详情页和共享样式，不把旧页面当历史记录；不得生成能力 Tab 或能力专题页。TODO 详情页的状态、日期、依赖与 Epic 归属以 `todo/index.md` 为准，正文以对应 `todo/TODO_NNNN.md` 为准；YAML front matter 只用于顶部元数据卡，不得渲染进正文，源文件的首个 H1 与页面标题重复时也从正文省略。正文阅读层必须使用统一内边距、深色标题层级、可读正文颜色、标准列表缩进，以及一致的代码、引用和表格间距；必须保留事实源链接。保留 `domain.html` 时只能作为跳转总览项目域区域的兼容入口，不得恢复导航 Tab 或复制项目域内容。
7. 生成后优先用 Codex preview / in-app browser 打开验证页面可读性、布局和关键内容；无法预览时说明原因。
8. 完成后报告总览入口、专题页、读取来源和缺失区域。

## 更新时机

- 用户要求查看 luca 或项目域 dashboard。
- 外部资源、服务定义、BUG / TODO / PRD / EXP 或记忆入口发生明显变化。
- 新 luca 实例初始化后，需要让用户快速理解当前状态。

## 触发方式

触发靠语义，不靠口令。用户表达想看见、刷新或重新生成 luca 当前状态页时，我就更新 `projects/room/` 多页面展示。

触发后先读取当前事实来源，再完整重渲染页面；不要在旧 HTML 上局部猜改。

视觉、排版或页面信息架构要调整时，优先修改 `skills/reference/design.md`，再按新规范重渲染全部页面。

## 红线

- dashboard 不是账本，不承载状态迁移。
- dashboard 不是记忆，不沉淀经验。
- dashboard 不是计划，不替用户拍板。
- dashboard 不展示 `ABILITY.md` 能力集；能力是 luca 本体，不是项目状态。
- dashboard 过期时直接重新渲染，不手工修补局部事实。

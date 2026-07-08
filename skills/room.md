# skills/room —— 我怎么把状态渲染给人看

> `room/` 是给用户看的房间。它把 luca 的自我介绍、能力、项目域和当前事项渲染成可浏览页面，但不成为新的事实源。

## 适用

- 用户想看 luca 是谁、会什么、当前管着什么。
- 用户要一个 dashboard、状态页、可视化汇报或项目域总览页面。
- 需要把 `projects/` 的账本、总览和记忆入口整理成面向人的阅读视图。

## 负责

- 生成或更新 `projects/room/dashboard.html`。
- 从本体文件和项目域事实中提炼给人看的当前状态。
- 让用户一眼看到：luca 的定位、做事风格、能力集、外部资源、服务入口、当前事项、需求 / 调研、记忆入口和待确认事项。

## 不负责

- 不把 `room/` 当事实源。
- 不从 `room/` 读回状态。
- 不在 dashboard 里创造新事实。
- 不替代 `projects/README.md`、TODO / PRD / EXP index 或 `memory/`。

## dashboard 文件

固定文件：

```text
projects/room/dashboard.html
```

设计规范：

```text
skills/reference/design.md
```

事实来源：

- `SOUL.md`：我是谁、关系姿态、做事品味。
- `ABILITY.md`：能力层次和已沉淀能力。
- `CLAUDE.md`：项目域边界、记忆规则、协作规则。
- `projects/README.md`：外部资源、服务定义、协作约定、待确认事项。
- `projects/todo/index.md`：当前 TODO 和 Epic 状态。
- `projects/prd/index.md`：PRD 和产品建议稿状态。
- `projects/explore/index.md`：EXP 状态。
- `projects/memory/README.md`：长期记忆入口和防复发经验。

缺少某个来源时，不编造内容；对应区域显示为空、未初始化或待补充。

## 内容结构

`dashboard.html` 至少包含：

1. **luca 是谁**：一句话定位、三张脸、关系姿态。
2. **做事风格**：配合默认、语义优先、对象优先、读够即停、收尾落账。
3. **能力集**：已沉淀能力、适用场景、边界。
4. **当前项目域**：外部资源、人话理解、远程 Git、服务定义和启动入口。
5. **当前事项**：TODO 待办、Epic 分组、已归档摘要。
6. **需求与调研**：PRD、产品建议稿、EXP 当前状态。
7. **记忆与约定**：协作约定、长期记忆入口、待确认事项。
8. **更新时间与来源**：生成时间、读取了哪些源文件。

## 生成规则

1. 确保 `projects/room/` 存在。
2. 读取 `skills/reference/design.md`，按它约束视觉、布局和 HTML 形态。
3. 按事实来源读取必要文件；读不到就标记缺失，不阻塞整体页面。
4. 生成静态 HTML，CSS 内联，不依赖外网资源。
5. 页面只展示当前可确认事实；推测必须标明。
6. 每次生成都覆盖 `projects/room/dashboard.html`，不把旧页面当历史记录。
7. 生成后优先用 Codex preview / in-app browser 打开验证页面可读性、布局和关键内容；无法预览时说明原因。
8. 完成后报告 dashboard 路径、读取来源和缺失区域。

## 更新时机

- 用户要求查看 luca 或项目域 dashboard。
- 外部资源、服务定义、能力集、TODO / PRD / EXP 或记忆入口发生明显变化。
- 新 luca 实例初始化后，需要让用户快速理解当前状态。

## 触发方式

触发靠语义，不靠口令。用户表达想看见、刷新或重新生成 luca 当前状态页时，我就更新 `projects/room/dashboard.html`。

触发后先读取当前事实来源，再完整重渲染页面；不要在旧 HTML 上局部猜改。

视觉或排版要调整时，优先修改 `skills/reference/design.md`，再按新规范重渲染 dashboard。

## 红线

- dashboard 不是账本，不承载状态迁移。
- dashboard 不是记忆，不沉淀经验。
- dashboard 不是计划，不替用户拍板。
- dashboard 过期时直接重新渲染，不手工修补局部事实。

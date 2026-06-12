---
name: init
description: 在当前项目从零创建 .workflow/ 工作流框架（初始化）。当用户说"搭建工作流/初始化工作流/init workflow/克隆工作流"时用。
argument-hint: "（过程中会问你几个项目问题）"
---

# /tf:init — 初始化 tf 工作流到当前项目

把"文件驱动的产品/工程工作流"装进当前项目。**本技能自包含**——要写的内容都在下面，不读任何外部模板、不依赖软链。

> 已有 `.workflow/`？→ **别重装**：提示用户"看状态用 `/tf:status`、升级用 `/tf:update`"，停。
> （`/tf:update` 也会调用本技能的"刷新模式"：只重写 bootstrap 等代码文件，保留数据。）

## Step A：探查项目（秒级，不打扰用户）

`ls -la` 根目录；看 `package.json`/`pyproject.toml`/`Cargo.toml`/`go.mod` 推断技术栈；看 git 状态。**不要 grep 整个代码库。**

## Step B：问用户 4 件事（一次问完，等回答再动手）

1. 项目一句话简介？
2. 主要技术栈（我探查到 <…>，要补充/修正吗）？
3. 项目类型？(a) 业务/产品 → 带 PRD + EXP；(b) 工具/库 → 只带 TODO；(c) 研究 → 带 EXP 不带 PRD
4. CLAUDE.md：<已存在/不存在>。已存在则：(a) 末尾追加工作流段 / (b) 备份后重写

## Step C：生成 `.workflow/` 文件

按项目类型决定 prd/explore 要不要建。**所有内容用下面「## 内嵌内容」里的原文**，原样写出（projects.md 需填一行）。

- 所有：`.workflow/skill/bootstrap/SKILL.md`、`.workflow/todo/index.md`、`.workflow/projects.md`、`.workflow/README.md`
- 业务/产品：`.workflow/prd/index.md`
- 业务/研究：`.workflow/explore/index.md`

> **注意**：不写任何 `*/README.md` schema 文件——索引格式由 `/tf:todo-create`、`/tf:prd-review`、`/tf:explore` 各自定义（写 index 时照那里的格式）。`.workflow/` 只存数据 + bootstrap。

## Step D：CLAUDE.md / AGENTS.md

把下面「## 内嵌内容 · CLAUDE.md 工作流段」追加到 CLAUDE.md 末尾（无则新建含该段的 CLAUDE.md）。已有 `@.workflow/skill/bootstrap` → 报冲突，不覆盖。

## Step E：自检 + 报告

```bash
ls -la .workflow/ .workflow/skill/ .workflow/todo/
test -f .workflow/skill/bootstrap/SKILL.md && echo "bootstrap OK"
grep "@.workflow/skill/bootstrap" CLAUDE.md && echo "注入 OK"
grep -q "{{" .workflow/projects.md && echo "⚠️ projects.md 占位未填" || echo "projects.md OK"
```

报告：生成了哪些文件 / 项目类型 / 让用户**新开会话**说"在吗"试 bootstrap 汇报、或 `/tf:todo-create <标题>` 建第一条。

---

# 内嵌内容（以下原文写入项目）

## `.workflow/skill/bootstrap/SKILL.md`

````markdown
# Bootstrap — 启动协议（tf 工作流）

> AI 进入本项目，**先按此协议执行，再回应用户**。本项目用 tf 工作流：数据在 `.workflow/`，操作由 `/tf:*` 技能负责（自然语言会自动触发，斜杠可显式调）。

## Step 0：内化原则（所有操作都受约束）

- **「工作量大」不是妥协理由**：做不做靠**正确/合理**，不靠嫌麻烦；工作量只影响排期。冒出"不值得 / 留到以后 / 太复杂"时停一下自查：真技术判断，还是工作量逃避？
- **修 bug 不许只治标**：根因没定位、没消除不算修完——`if` 绕过、`catch` 吞异常、调大 timeout 遮症状都不算。顺手修的小 bug 也守。

## Step 1：扫一眼状态

只读这些的表格（不读详情文件，省 token）：`.workflow/projects.md`（不存在就跳过）、`todo/index.md`、`prd/index.md`、`explore/index.md`。

## Step 2：要不要主动汇报

- 用户已派**具体任务**（"加个 X"、"#3 做完了"）→ 跳过汇报，直接干。
- 开场含糊（"在吗"、"今天做什么"）→ 输出汇报（≤6 行）：🟡在做 / ⚪待开始 / 🟢已完成 / 📋PRD / 🌱EXP + 一句"想推哪个？"。

## Step 3：工作流操作 → 走 `/tf:*` 技能

创建 TODO、推进/关闭 TODO、review PRD、预研、升级——交给对应 `/tf:*` 技能（自然语言自动触发，也可斜杠）。**各技能自带门槛**（AC 不齐不开工、AC 没勾完+验证没过不准 done、搁置/放弃必写原因等），bootstrap 不重复。意图不明 → 列 `/tf:*` 让用户选，不要猜。

## 红线

- **「工作量」不是妥协理由**（最高优先级，见 Step 0）
- **不凭记忆操作工作流** —— 交给 `/tf:*` 技能，按它的门槛走
- **用户具体任务优先于流程装饰** —— SOP 是路径不是关卡
- **小修不进 TODO** —— 改 typo / 调 CSS 直接做 + commit；TODO 是计划级（半天起）
- **不自动 commit、不自动 push** —— 平时只改文件；用户说"收工/提交"才提交（仅当下这轮），push 永远等用户。多仓库的提交编排见 `/tf:todo-progress` §收工
````

## `.workflow/todo/index.md`

````markdown
---
type: todo
---

# TODO 索引

> 状态：⚪ 未开始 · 🟡 进行中 · ⏸️ 搁置 · 🟢 完成 · ⚫ 放弃
> 操作：创建走 `/tf:todo-create`，推进走 `/tf:todo-progress`（索引格式由它们定义）。
> 区段顺序（钉死）：活跃项 → 专项(进行中) → 搁置 → 已完结专项 → 归档。

## 活跃项

| 编号 | 标题 | 状态 | 添加 | 优先级 | 依赖 |
|---|---|---|---|---|---|

## 专项（Epic）

（暂无）

## 搁置

| 编号 | 标题 | 状态 | 添加 | 原因（含复活条件） |
|---|---|---|---|---|

## 已完结专项

（暂无）

## 归档

| 编号 | 标题 | 状态 | 添加 | 完成 | 原因 |
|---|---|---|---|---|---|
````

## `.workflow/prd/index.md`（仅业务/产品）

````markdown
---
type: prd
---

# PRD 索引

> 操作走 `/tf:prd-review`（格式由它定义）。状态：draft / ready / shipped / archived。

| 编号 | 标题 | 状态 | 添加 | 澄清(R) | 关联 TODO |
|---|---|---|---|---|---|
````

## `.workflow/explore/index.md`（仅业务/研究）

````markdown
---
type: explore
---

# EXP 索引

> 操作走 `/tf:explore`（格式由它定义）。状态：seed / exploring / promoted / dropped。

| 编号 | 标题 | 状态 | 添加 | 下一步 |
|---|---|---|---|---|
````

## `.workflow/projects.md`

复制下面内容，把 `{{PROJECTS_TABLE}}` 换成一行（单仓项目 = 本仓本体）：项目 | 角色 | 一句话职责 | 技术栈 | 仓库边界。

````markdown
# 工作区项目拓扑

> 本工作区受管项目清单。三件正交的事：**我在管什么**→本文件；**怎么干活**→根 `CLAUDE.md`；**按什么流程**→ tf 插件的 `/tf:*`。

## 受管项目

| 项目 | 角色 | 一句话职责 | 技术栈 | 仓库边界 |
|---|---|---|---|---|
{{PROJECTS_TABLE}}

> 单仓项目就一行（本仓本体），留着别删——它是 bootstrap 定位"我在管什么"的依据。
````

## `.workflow/README.md`

````markdown
# .workflow/ — 工作流数据目录

本目录只存**业务数据**（TODO / PRD / EXP 内容 + 索引 + 项目拓扑）和一个常驻的 `bootstrap`。
**流程（SOP）不在这里**——它们是 `tf` 插件的 `/tf:*` 技能。

- 看状态：`/tf:status`　建 TODO：`/tf:todo-create`　推进：`/tf:todo-progress`
- review PRD：`/tf:prd-review`　预研：`/tf:explore`　升级：`/tf:update`
- 自然语言（"加个 TODO"）也会自动触发对应技能。

> 工作流代码升级走 `/plugin update tf`；本目录数据的迁移走 `/tf:update`。
````

## 内嵌内容 · CLAUDE.md 工作流段

````markdown

---

## 工作流（tf 插件）

> **启动协议**：下方 `@` 导入的 bootstrap 是本 session 的运行时合约。进项目先扫一眼 `.workflow/` 状态，再回应；具体任务优先于汇报。

@.workflow/skill/bootstrap/SKILL.md

> 工作流操作是 `tf` 插件的 `/tf:*` 技能（todo-create / todo-progress / prd-review / explore / status / update），自然语言会自动触发，也可斜杠显式调。`.workflow/` 只存数据。
````

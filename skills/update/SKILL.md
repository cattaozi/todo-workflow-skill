---
name: update
description: 把本项目的 .workflow/ 数据/结构对齐到最新工作流，并出"心智简报"。当用户说"更新/升级/同步工作流、update workflow、检查工作流更新"时用。需当前项目已有 .workflow/。
argument-hint: "（无参数=对齐+迁移；'check'=只检查差异不改）"
---

# /tf:update — 升级工作流

> 升级分两件事：**代码（SOP/命令）走 `/plugin update tf`**（Claude Code 原生，不归本技能管）；**本项目 `.workflow/` 的结构对齐 + 数据迁移**归本技能。
> 前置：项目**没有 `.workflow/`** → 提示先 `/tf:init`，停。随时可发，长任务中也能跑（独立动作，完事回原任务）。

## Step 0：旧布局迁移（首次从"`.workflow/skill` 版"升级时，**只跑一次**）

**检测**：项目里存在 `.workflow/skill/todo-create/`（或其它 per-op SOP 目录），或 `.workflow/todo/README.md` 等 schema 文件 → 这是插件化之前的老布局，先做一次性清理：

- **删冗余代码文件**（已被 `tf` 插件取代）：`.workflow/skill/todo-create/`、`todo-progress/`、`prd-review/`、`explore/` 整目录；`.workflow/todo/README.md`、`prd/README.md`、`explore/README.md`。
- **保留 `.workflow/skill/bootstrap/`**，但**刷新它的内容**（见 Step 4）——旧 bootstrap 带路由表/版本自查，已过时。
- **`.workflow/EVOLUTION.md`**：方法论已归插件，项目这份留着无害（是项目自己的历史），不必删。
- ⚠️ **绝不碰数据**：`*/index.md`、`TODO_*.md`、`PRD_*.md`、`EXP_*.md`、`projects.md` 一个不动。
- 删完进 Step 2 继续（对齐索引结构）。

> 判据：**只删被插件取代的 SOP/schema（代码），带编号的资产和索引内容（数据）全留。** 拿不准的文件 → 留着 + 问用户，绝不删。

## 步骤

1. **先拿最新代码**：提示用户（或确认已）运行 `/plugin update tf`。插件更新后，`/tf:*` 技能即最新版；本技能下面据此对齐项目数据。

2. **算差异**（`check` 模式走到这步停、只报告）：把本项目各 `.workflow/*/index.md` 的**结构**（区段、列序）跟最新的权威格式比对——
   - TODO 索引 vs `/tf:todo-create` §索引格式
   - PRD 索引 vs `/tf:prd-review` §索引格式
   - EXP 索引 vs `/tf:explore` §索引格式
   差异通常是：缺了某列 / 缺了某区段 / 排序规则变了。列出来报给用户。

3. **迁移数据**（`check` 模式不做）：按差异把 index **结构**改成最新格式——**只动结构，绝不动行内容**：
   - 加列（如给 Epic 表补 `完成` 列，旧行该列填 ——）
   - 加 / 拆区段（如新增 `## 已完结专项`，把全绿的 Epic 块下沉过去）
   - 按新排序规则重排
   - ⚠️ **绝不删条目、不改 TODO/PRD/EXP 的实际内容、不用空模板覆盖** —— 这是最大事故源。

4. **刷新 bootstrap**：`.workflow/skill/bootstrap/SKILL.md` 是项目里唯一的"代码文件"，可能随版本变。**调用 `/tf:init` 的刷新模式**（它检测到已有 `.workflow/` 时，只重写 bootstrap 等代码文件、保留你的数据）来更新它。

5. **心智简报（本次升级真正的产出）**：逐条讲——
   - **变了什么**（一句话）
   - **对你日常的影响**：从现在起要开始/停止/改变做什么
   - **你的数据被怎么动了**：动了哪张表/加了什么列/分区，**原内容一字未改**
   收尾问一句"这些跟你的习惯有冲突吗、认可吗"。**只同步文件不出简报 = 没升级完。**

## 红线

- **旧布局清理只删"已知被插件取代的 SOP/schema"** —— 即 `.workflow/skill/{todo-create,todo-progress,prd-review,explore}/` 和 `.workflow/*/README.md`；**其余一律不删**，尤其任何带编号的 `TODO_*/PRD_*/EXP_*` 和各 `index.md`
- **绝不用空模板覆盖项目 `index.md`** —— 会清空你的 TODO/PRD/EXP，最大事故源
- **数据迁移只改结构不改语义** —— 加列/分区/重排可以，删条目/改内容不行
- **不自动 commit** —— 改完等用户 diff 审过再拍板
- **拿不准某处怎么迁 → 停下问用户**，不猜着改数据

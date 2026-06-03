---
name: todo-workflow
description: |
  Bootstrap a file-driven product/engineering workflow in the current project.
  Use when the user wants to "set up todo workflow", "init workflow", "克隆工作流",
  "搭建工作流", "用 todo-workflow", or kick off a new project and wants planning
  structure. Creates a `.workflow/` directory with SOPs, indexes, templates, and
  EVOLUTION log, then configures CLAUDE.md (or AGENTS.md) for `@`-injection.
  Adapts to project type: business product / tool library / research.
---

# todo-workflow — 工作流初始化

把一套"文件驱动的产品/工程管理工作流"克隆到当前项目。完成后项目拥有：

- `.workflow/` 目录（SOP / 索引 / 模板 / 项目拓扑 / 历史日志）
- `CLAUDE.md`（或 `AGENTS.md`）配置好 bootstrap `@` 注入

未来任何 AI 进入项目，bootstrap 自动注入，按工作流走，**不再依赖 AI 自律**。

---

## 灵魂（5 条原则，你必须内化，不是机械执行）

### 1. SOP 是运行时合约，不是参考文档
触发对应意图时**必须 Read 对应 SKILL.md**（本 session 首次时）。不能凭记忆操作。这是反"AI 长 session 记忆漂移"的机制。

### 2. DoD vs AC 不是文字游戏
- **DoD（完成定义）** = 一句话目标态（工程师对照自己说"做完了"）
- **AC（验收条件）** = 可勾选清单（任何人逐条核对）

状态门槛靠 AC 判定，不是"觉得做完了"。

### 3. 「工作量大」不是技术判断
"嫌麻烦"包装成"不值得"是 AI 自欺最常见入口。工作量**影响排期**，**不影响决策**。每次冒出"留给以后 / 不值得 / 太复杂"念头时，停一下问自己：这是真技术判断，还是工作量逃避？

### 4. 数据产物有 schema，不能现编
`index.md` 这种"被多个 SOP 修改的产物"必须有同目录 `README.md` 定义结构。AI 写入前 Read schema；纯读不用。**避免不同 AI / 不同 session 把同样的 index 写出不同形态**。

### 5. 用户的具体任务优先于 SOP 装饰流程
SOP 是**路径**不是**关卡**。用户说"先干这个再说"就先干，不要僵在流程里。

---

## 执行流程

### Step 1: 探查项目现状（不打扰用户）

逐个看，秒级完成：

1. `ls -la` 看根目录
2. 检查是否已有：`CLAUDE.md`、`AGENTS.md`、`.workflow/`、`README.md`
3. 看包管理 / 配置文件推断技术栈：`package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` 等
4. 看 git 状态

**不要 grep 整个代码库**，只看根目录元数据。

### Step 2: 跟用户确认 5 个问题（一次性问完）

```
我准备克隆 todo-workflow 到当前项目，先确认 5 件事：

1. 【项目一句话简介】这个项目是做什么的？
   （例："家庭网站 × AI 试验田"、"内部数据 ETL"、"开源 OAuth library"）

2. 【主要技术栈】我探查到：<根据 Step 1 结果填>
   有需要补充 / 修正的吗？

3. 【项目类型】哪种？这决定要不要带 PRD / EXP 体系：
   (a) 业务/产品项目 → **带 PRD + EXP**（全套）
   (b) 工具/库项目  → **只带 TODO**（精简）
   (c) 研究/试验项目 → **带 EXP，不带 PRD**

4. 【工作区项目拓扑】这个工作区管着哪些项目 / 仓库？各自什么角色？
   （单仓项目 → 就它自己，一行即可；多仓工作台 → 列出如"前端仓 / 后端仓 / SDK / 原型·真相源"）

5. 【CLAUDE.md 处理】我探查到：<已存在 / 不存在>
   如已存在：(a) 在末尾追加工作流段落 / (b) 备份后重写

我会等你回答后再开始动手。
```

**注意**：5 件事一件不能少；不要假设答案默默执行。

### Step 3: 生成 `.workflow/` 文件

按下面映射表，对每条目：
1. `Read` 本 Skill 的 template 文件（路径相对本 SKILL.md）
2. `Write` 到目标路径（项目根的对应位置）
3. 内容**原样复制**，不做 placeholder 替换（这些是工作流的 SOP 文档，跟项目无关）

| 项目类型 | 目标路径（项目内） | 模板源（本 Skill 内） |
|---|---|---|
| 所有 | `.workflow/README.md` | `templates/workflow/README.md` |
| 所有 | `.workflow/EVOLUTION.md` | `templates/workflow/EVOLUTION.md` |
| 所有 | `.workflow/projects.md` | `templates/workflow/projects.md` |
| 所有 | `.workflow/skill/bootstrap/SKILL.md` | `templates/workflow/skill/bootstrap/SKILL.md` |
| 所有 | `.workflow/skill/todo-create/SKILL.md` | `templates/workflow/skill/todo-create/SKILL.md` |
| 所有 | `.workflow/skill/todo-create/TEMPLATE.md` | `templates/workflow/skill/todo-create/TEMPLATE.md` |
| 所有 | `.workflow/skill/todo-progress/SKILL.md` | `templates/workflow/skill/todo-progress/SKILL.md` |
| 所有 | `.workflow/todo/README.md` | `templates/workflow/todo/README.md` |
| 所有 | `.workflow/todo/index.md` | `templates/workflow/todo/index.md` |
| 业务/产品 | `.workflow/skill/prd-review/SKILL.md` | `templates/workflow/skill/prd-review/SKILL.md` |
| 业务/产品 | `.workflow/prd/README.md` | `templates/workflow/prd/README.md` |
| 业务/产品 | `.workflow/prd/index.md` | `templates/workflow/prd/index.md` |
| 业务/研究 | `.workflow/skill/explore/SKILL.md` | `templates/workflow/skill/explore/SKILL.md` |
| 业务/研究 | `.workflow/explore/README.md` | `templates/workflow/explore/README.md` |
| 业务/研究 | `.workflow/explore/index.md` | `templates/workflow/explore/index.md` |

**工具/库项目**：跳过所有 PRD / EXP 行。`.workflow/README.md` 中提到 PRD/EXP 的内容也要相应注释或删除（**或保留作为提示**——告知"未来要不要带"）。

> **不要" cherry pick "改 SKILL 内容**——所有 Skill 文件原样复制。后续用户自己改是项目演化的事。
>
> **唯一例外：`projects.md` 要填充内容**（其它 `.workflow/` 文件都原样复制）。复制后把 `{{PROJECTS_TABLE}}` 换成 Step 2 第 4 题的项目清单：一项目一行，按文件内 schema 列序（项目 \| 角色 \| 一句话职责 \| 技术栈 \| 仓库边界）。单仓项目填一行即可。

### Step 4: CLAUDE.md / AGENTS.md 处理

读 `templates/claude-md/new.md.tmpl` 或 `templates/claude-md/append.md.tmpl`，做 placeholder 替换。

**占位符语法**：`{{PLACEHOLDER}}`（Mustache 风格）

**需要替换的占位符**（来自用户 Step 2 回答）：

| 占位 | 来源 |
|---|---|
| `{{PROJECT_NAME}}` | 项目名（从 git remote / 目录名 / 用户提供） |
| `{{PROJECT_TAGLINE}}` | 用户回答的"一句话简介" |
| `{{PROJECT_DESCRIPTION}}` | 你根据探查 + 简介展开 2-3 行 |
| `{{TECH_STACK_BLOCK}}` | 把用户确认的技术栈写成 markdown bullet 列表 |
| `{{DEV_COMMANDS}}` | 根据语言/框架给典型启动命令（如 `npm run dev` / `cargo run`） |
| `{{DEPENDENCY_NOTES}}` | 一句话约定包管理器（如 "使用 pnpm（不要 npm/yarn）"） |
| `{{VERIFY_CHECKLIST_HINT}}` | 一句话提示典型验证（如 "ruff/mypy/pytest 全过；前端 type-check/lint/build 全过"） |
| `{{LANGUAGE_SPECIFIC_CONVENTIONS}}` | 1-2 节项目语言/框架的编码约定。猜不准时**空着**，让用户后续自补 |

**三种情况分支：**

| 情况 | 处理 |
|---|---|
| **A) 无 CLAUDE.md 也无 AGENTS.md** | Read `templates/claude-md/new.md.tmpl` → 替换 placeholder → Write 到 `CLAUDE.md` |
| **B) 有 CLAUDE.md 但无 `@.workflow/skill/bootstrap` 注入** | 用户选 (a) 追加 → Read `templates/claude-md/append.md.tmpl` → 替换（无 placeholder，可直接写）→ 追加到 `CLAUDE.md` 末尾；用户选 (b) 备份重写 → `mv CLAUDE.md CLAUDE.md.backup.<date>` → 走 A 流程 |
| **C) 只有 AGENTS.md 无 CLAUDE.md** | 追加 `append.md.tmpl` 到 `AGENTS.md` 末尾。`@` 注入对 Codex 老版本不生效但不破坏；最坏情况手动让 AI Read bootstrap |

**已有 `@.workflow/skill/bootstrap`**：说明已经装过，**报告冲突让用户决定**，不要自作主张覆盖。

### Step 5: 自检（必跑）

```bash
# 1. 目录结构齐
ls -la .workflow/
ls -la .workflow/skill/
ls -la .workflow/todo/      # 至少有 README.md + index.md

# 2. README 的 schema 链接对得上
grep -l "见 ./README.md" .workflow/todo/index.md

# 3. SKILL 引用 README 正确
grep "todo/README.md" .workflow/skill/todo-create/SKILL.md
grep "todo/README.md" .workflow/skill/todo-progress/SKILL.md

# 4. CLAUDE.md / AGENTS.md 含 @ 注入
grep "@.workflow/skill/bootstrap" CLAUDE.md   # 或 AGENTS.md

# 5. projects.md 占位已替换（不能残留 {{ }}）
grep -q "{{" .workflow/projects.md && echo "⚠️ projects.md 占位未填充" || echo "projects.md OK"
```

任何一条不通 → 修复后再下一步。**不要因为"差不多了"放过**（这是 §灵魂 #3）。

### Step 6: 给用户报告

用模板：

```
✅ 工作流已就位。

## 生成的文件（共 N 个）

[列出来]

## CLAUDE.md 处理

<新建 / 追加 / 备份后重写到 CLAUDE.md.backup.YYYY-MM-DD>

## 项目类型

<a) 业务/产品 (全套) / b) 工具/库 (精简) / c) 研究 (带 EXP)>

## 现在试试

1. 新开一个对话说"在吗" → AI 按 bootstrap 协议汇报状态（空）
2. 新对话说"我想加一个 TODO：<标题>" → AI 走 todo-create SOP
3. 修改完代码 git 提交前永远等你说"提交"

## 没做的事（你后续可以做）

- 把现成的需求文档扔进 PRD 走 prd-review 流程（仅业务/产品项目）
- 把"半生不熟的想法"开 EXP（业务/研究项目）

## 文档入口

- `.workflow/README.md` —— 工作流总入口
- `.workflow/projects.md` —— 工作区管哪些项目（bootstrap 启动读它定位）
- `.workflow/EVOLUTION.md` —— 方法论沉淀
- 各 `<domain>/README.md` —— index.md schema
```

报告完成后 **stop**，等用户测试。

---

## 故障 / 边界情况

| 情况 | 处理 |
|---|---|
| 项目已有完整 `.workflow/`（已装过本 Skill） | **报告冲突，不覆盖**。问用户是要"升级"（diff 应用差异）还是"跳过" |
| Template 文件 Read 失败 | Skill 安装可能损坏。提示用户重新 `git pull` 或 clone Skill |
| 项目根不可写 | 报错给用户，不静默失败 |
| 用户拒绝回答 Step 2 问题 | 不强推；说"我等你回答完再开始"，挂起 |

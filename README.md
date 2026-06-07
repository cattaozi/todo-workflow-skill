# todo-workflow-skill

> 一个 Anthropic Skill —— 把"文件驱动的产品/工程管理工作流"一键克隆到任何项目。

**为什么需要**：单人/小团队项目里，AI 容易"想到哪做到哪"——任务没规划 / 状态散 / 决策回头查不到。这个 Skill 把一套经过实战的工作流（TODO / PRD / EXP / SOP / 历史沉淀）打包好，AI 调用一次就把骨架搭起来。

**适用于**：

- ✅ Claude Code（一等公民，`@` 注入自动生效）
- ✅ 其他能读写文件的 AI 工具（Cursor / Aider 等），通过手工提示 AI 加载本 Skill 也能用
- ❌ 仅对话不能写文件的 AI（如纯 ChatGPT 网页版无 Code Interpreter）—— 那种情况看本仓库 `docs/INVOKE_FALLBACK.md`（如有）

---

## 安装

### Claude Code（推荐）

```bash
# 安装到用户级 Skill 目录
git clone https://github.com/cattaozi/todo-workflow-skill ~/.claude/skills/todo-workflow

# 验证：新开 Claude Code 会话，问 AI "list available skills"，应能看到 todo-workflow
```

### 项目级（仅当前项目用）

```bash
cd <your-project>
git clone https://github.com/cattaozi/todo-workflow-skill .claude/skills/todo-workflow
```

### 其他 AI 工具（手工模式）

```bash
# 1. clone 仓库到任意位置
git clone https://github.com/cattaozi/todo-workflow-skill ~/skills/todo-workflow

# 2. 用 AI 时，告诉它路径
"请按 ~/skills/todo-workflow/SKILL.md 的指令，把工作流克隆到当前项目"
```

---

## 用法

安装好后，在 AI 对话框说**任意触发短语**：

- "init workflow"
- "set up todo workflow"
- "用 todo-workflow"
- "搭建工作流"
- "克隆工作流"

AI 会：

1. **探查**项目（不打扰你）
2. **问你 4 个问题**（项目简介 / 技术栈确认 / 项目类型 / CLAUDE.md 处理）
3. **生成所有文件**（按项目类型自适应）
4. **自检 + 报告**

完成后，新开对话里你会看到 AI 按 bootstrap 协议主动汇报状态——证明 `@` 注入生效。

---

## 你拿到什么

工作流装好后，项目根多了：

```
your-project/
├── .workflow/
│   ├── README.md                       # 入口
│   ├── EVOLUTION.md                    # 方法论沉淀 + 演进日志
│   ├── skill/                          # 5 个 SOP (bootstrap + todo + prd + explore)
│   ├── todo/                           # 行动项目录 + README schema + 空 index
│   ├── prd/                            # 产品文档目录 (仅业务/产品项目)
│   └── explore/                        # 灵感池目录 (业务/研究项目)
└── CLAUDE.md                           # 含 @ 注入 bootstrap
```

详细的"工作流是怎么工作的"见 [`docs/HOW_IT_WORKS.md`](docs/HOW_IT_WORKS.md)。
设计哲学见 [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md)。

---

## 核心概念（30 秒理解）

| 概念 | 是什么 |
|---|---|
| **PRD** | 产品需求文档。你写，AI review，拆 TODO |
| **TODO** | 行动项（一个 0.5-2 天能干完的事）。状态机 `todo → in_progress → done`，AC 卡门槛 |
| **EXP** | "我有个想法"。半生不熟的预研，成熟了 promote 成 TODO 或 PRD |
| **SOP** | `.workflow/skill/<name>/SKILL.md` —— 操作规则。AI 操作前必须 Read |
| **index.md** | 每个 domain 的汇总表 |
| **README.md**（在 domain 目录下） | 该 domain 的 `index.md` schema 定义 |
| **EVOLUTION.md** | 工作流自身的演进日志 + 方法论沉淀 |

---

## 设计哲学（一段就懂）

**SOP 不是给人看的文档，是给 AI 的运行时合约。** 普通 markdown 文档 AI 看了"觉得知道了"，长 session 后会漂移。Skill / `@` 注入 / "操作前必须 Read"的强制约束，让 AI 没机会偷懒。

**DoD vs AC 不是修辞**。DoD 是"做完了"的目标态描述（一句话）；AC 是可勾选的布尔清单。状态门槛靠 AC 判定——"觉得做完了"不算数。

**「工作量大」不是技术判断**。AI 容易把"嫌麻烦"包装成"不值得"。本 Skill 把"工作量影响排期不影响决策"写进 bootstrap 红线。

**渐进披露**。bootstrap 自动注入（必常驻）；其它 SOP 按意图 Read（不污染上下文）；数据 schema 在写入前 Read（不污染读取）。

---

## 工作流的演进

这套工作流不是设计出来的，是真实项目跑出来的。源自一个真实产品项目的 35 个 TODO + 3 个 EXP + 1 个 PRD 的实战。

每次踩坑后的沉淀都写在 `.workflow/EVOLUTION.md`（包括本 Skill 安装到新项目后）。下游项目积累的新洞察可以反馈回本 Skill 上游。

---

## 让已落地的项目保持最新

本仓库（你正在维护的这个工作区）就是**真相源，始终最新**。已经装了工作流的其它项目怎么跟上？**本地目录对比，不走远程 git。**

**一次性设置**：把约定路径软链到本工作区，这样所有项目都从一个稳定路径读到你的最新版：

```bash
# 若该路径之前 clone 过（是真实目录），先删掉，否则 ln 会建到目录内部
rm -rf ~/.claude/skills/todo-workflow
ln -sfn /Users/liangliang/IdeaProjects/ai_project/todo-workflow-skill ~/.claude/skills/todo-workflow
```

> 之后你在本工作区改了什么，`~/.claude/skills/todo-workflow` 立刻就是最新——零同步动作。
> （维护者用软链，不要再 clone-install；上面"安装"段的 clone 是给纯使用者的。）

**升级某个项目**：在那个项目里对 AI 说一句 **"更新工作流"**（或 "update workflow" / "同步工作流"）即可——AI 按 `.workflow/README.md` §升级 执行：

1. **定位本地真相源** `~/.claude/skills/todo-workflow/templates/workflow/`（只读本地，无网络）
2. 用 `EVOLUTION.md` 的方法论编号算版本差
3. **覆盖代码层**（所有 `README.md` + 整个 `skill/` 树），**保留数据层**（`index.md` + 带编号的 TODO/PRD/EXP 详情 + `projects.md`）
4. 按新增的 EVOLUTION 条目迁移已有数据（如加列、加分区）
5. **出「心智简报」**——逐条讲"变了什么 / 对你日常的影响 / 你的数据被怎么动"，并问用户是否认可，再等拍板提交

> 重点不是同步文件，是**更新使用者的心智**：升级完用户得知道"从现在起怎么用得不一样"，否则这次升级等于没做。

> 完整步骤与红线（**绝不用空 index 覆盖项目数据**等）见每个项目内的 `.workflow/README.md` §升级——那是给项目里的 AI 看的权威 SOP，本仓库的 [`templates/workflow/README.md`](templates/workflow/README.md) 是它的模板源。

---

## 贡献

发现工作流缺陷、想加新 SOP、改进模板：

1. Open Issue 描述问题 / 想法
2. 或直接 PR（建议先 Issue 讨论）
3. 改动**必须同步更新** `templates/workflow/EVOLUTION.md`（沉淀理由）

---

## License

MIT

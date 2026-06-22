# tf — 文件驱动的产品/工程工作流（Claude Code 插件）

> 把一套经过实战的工作流装进 Claude Code，让单人 / 小团队 + AI 协作时**有章可循、状态留痕、决策可追**——而不是 AI 想到哪做到哪。

**为什么需要**：项目里 AI 容易"想到哪做到哪"——任务没规划、状态散、决策回头查不到、修 bug 只治标。`tf` 把 TODO / PRD / EXP 的管理流程做成带**质量门槛**的运行时合约，AI 走标准流程、不偷懒漂移。

---

## 安装

```
/plugin marketplace add cattaozi/todo-workflow-skill
/plugin install tf@todo-workflow
```

新开一个会话，输 `/tf:` 应能补全出全套命令。更新：`/plugin update tf`。

> 标准 Claude Code 插件——一键装、原生更新，**不需要 clone、不需要建软链、不需要任何手动步骤**。

---

## 核心思想：代码与数据分离

- **插件 = 流程（代码）**：所有 SOP（怎么建 TODO、怎么推进、怎么 review PRD、怎么升级）是插件里自包含的 `/tf:*` 技能。
- **你的项目 = 数据**：项目里只有一个 `.workflow/` 目录，存你真实的 TODO / PRD / EXP 内容 + 索引 + 项目拓扑，外加一个常驻的 `bootstrap`（启动协议）。
- 一句话：**流程归插件，数据归项目。** 流程升级走 `/plugin update`，绝不动你的数据。

---

## 命令（统一前缀 `/tf:`）

| 命令 | 干什么 |
|---|---|
| `/tf:init` | 在当前项目从零建出 `.workflow/` 框架 |
| `/tf:status` | 看当前在做什么 / 待办 / PRD / EXP 概览 |
| `/tf:todo-create` | 建一个 TODO（带粒度自检、DoD/AC 门槛） |
| `/tf:todo-progress` | 推进 / 关闭 TODO（AC 没勾完 + 验证没过不准 done） |
| `/tf:prd-create` | 把"有空白、没理清"的需求拷问 + 结构化成 PRD 草稿 |
| `/tf:prd-review` | 以工程视角 review PRD、找澄清项、拆 TODO |
| `/tf:explore` | 把半生不熟的想法登记为预研（EXP） |
| `/tf:update` | 把项目里的 `.workflow/` 对齐到最新工作流 |

> 也支持自然语言——"加个 TODO""这个做完了""我有个想法"会自动触发对应技能，不必非打斜杠。

---

## 灵魂：SOP 是"运行时合约"，不是参考文档

和普通待办清单的区别——每个环节都有**卡门槛的护栏**：

- AC 没写齐不准开工；AC 没勾完 + 验证没过不准 done
- 修 bug 根因不消除不算完（不许 `if` 绕过 / `catch` 吞掉遮症状）
- 「工作量大」不是妥协理由——只影响排期，不影响"做不做"
- Epic 完结自动下沉，不挡日常预览；搁置/放弃必写原因

让模型走标准流程、且**不偷懒、不漂移**。

---

## 你拿到什么

```
your-project/
├── .workflow/                       # 只有数据 + 一个常驻 bootstrap
│   ├── skill/bootstrap/SKILL.md     #   @ 注入的启动协议（唯一"代码文件"）
│   ├── todo/index.md + TODO_*.md    #   你的 TODO 数据
│   ├── prd/ · explore/              #   （按项目类型）
│   ├── projects.md                  #   工作区项目拓扑
│   └── README.md                    #   一句话指引
└── CLAUDE.md                        # 含 @ 注入 bootstrap

# 流程 SOP 都在 tf 插件里（/tf:* 技能），不写进你的项目。
```

---

## 设计沉淀

这套工作流不是设计出来的，是真实项目跑出来的，每条结构性演进 + 可复用 insight 沉淀在 [`EVOLUTION.md`](EVOLUTION.md)。

## License

MIT

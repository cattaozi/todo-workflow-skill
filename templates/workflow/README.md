# .workflow/ — 工作流环境

文件驱动的产品 / 工程管理。**新 session 入口**：[`skill/bootstrap/SKILL.md`](skill/bootstrap/SKILL.md)。

## 目录

| 目录 / 文件 | 内容 |
|---|---|
| [`prd/`](prd/index.md) | 产品需求文档（你自己写，工程的你 review）—— 子目录 [`README.md`](prd/README.md) 定义 `index.md` schema |
| [`todo/`](todo/index.md) | 行动项 —— 子目录 [`README.md`](todo/README.md) 定义 `index.md` schema |
| [`explore/`](explore/index.md) | 灵感池 / 预研 —— 子目录 [`README.md`](explore/README.md) 定义 `index.md` schema |
| `skill/` | 工作流 SOP（每个 Skill 一个 folder，主文件 `SKILL.md`） |
| [`EVOLUTION.md`](EVOLUTION.md) | **工作流演进日志 + 方法论沉淀**——每次对工作流做结构性改动后在这里记一条 |

## Skill 列表

| Skill | 主文件 | 职责 |
|---|---|---|
| **bootstrap** | [`skill/bootstrap/SKILL.md`](skill/bootstrap/SKILL.md) | 启动协议 + 意图路由表 |
| **prd-review** | [`skill/prd-review/SKILL.md`](skill/prd-review/SKILL.md) | PRD 工程 review 流程 |
| **todo-create** | [`skill/todo-create/SKILL.md`](skill/todo-create/SKILL.md) | 创建 TODO（+ TEMPLATE.md） |
| **todo-progress** | [`skill/todo-progress/SKILL.md`](skill/todo-progress/SKILL.md) | 推进 TODO 状态（含门槛） |
| **explore** | [`skill/explore/SKILL.md`](skill/explore/SKILL.md) | 预研推进流程 |

## Skill 文件结构约定

每个 Skill 是一个独立目录：

```
skill/<skill-name>/
├── SKILL.md        ← 主文件（必有）。Bootstrap 加载它。
├── TEMPLATE.md     ← 可选：使用时复制的模板
├── EXAMPLES.md     ← 可选：示例
└── ...             ← 其它资源（脚本、参考、checklist）
```

匹配 Anthropic Skills / Cursor Rules 等业界 Skill 体系约定，便于未来复用。

## 设计原则

1. **文件驱动**：所有状态在文件里，不在脑子里
2. **渐进披露**：AI 先读 index 再读详情，省 token
3. **SOP 作为运行时合约**：操作前必须 Read 对应 SKILL.md，不能凭记忆（详见 bootstrap）
4. **PM ↔ 工程师**：一个人戴两顶帽子，PRD 与 PRD-R 强迫切换视角
5. **永不复用编号**：done / abandoned 的 ID 也保留，方便追溯
6. **永不静默改状态**：所有变更同步 `last_updated`
7. **工作流本身要演进**：每次对工作流的结构性改动后，在 [`EVOLUTION.md`](EVOLUTION.md) 加一条——不只是 changelog，更是方法论沉淀

## Skill 加载模型（重要）

这些 SKILL.md **不是** Anthropic Skills 系统的真 Skill（不会出现在 Claude Code 的 `available skills` 里）。它们是结构化成 Skill 形态的 SOP。加载分三层：

```
Layer 1 — 真常驻（每次请求自动注入）
└── CLAUDE.md
    └── @.workflow/skill/bootstrap/SKILL.md   ← Claude Code 的 @ 导入语法，bootstrap 内容被内联

Layer 2 — 按意图 Read（bootstrap 路由表指挥）
├── todo-create/SKILL.md
├── todo-progress/SKILL.md
├── prd-review/SKILL.md
└── explore/SKILL.md

Layer 3 — Skill 内部资源
└── todo-create/TEMPLATE.md  等
```

**为什么只 `@` 导入 bootstrap，不 `@` 其它 Skill**：
- bootstrap 是路由器，必须时刻在
- 其它 Skill 是功能模块，按需读取，避免每次请求都把全部 SOP 塞进上下文
- 这就是"渐进披露"原则的落地

**对其它 AI 工具的兼容**：Codex 等不识别 `@` 语法的工具，会把 `@.workflow/...` 当字面文本看到——通常会被识别为"该读这个文件"的暗示，最坏情况手动 Read 即可，功能不破。

## 不做的事

- 不做仪表盘（UI 给团队看用的；单人项目不需要）
- 不接 TAPD 等外部任务系统
- 不为复用 PRD 而提前抽象（YAGNI）

# todo-workflow 是怎么工作的

读这篇，给你 5 分钟搞明白整套工作流的运转。**给人看，也给新接手的 AI 看。**

---

## 三层加载模型

工作流的所有"规则"和"产物"分三层加载，避免 AI 上下文爆炸：

```
Layer 1 — 常驻（每次请求自动注入）
└── CLAUDE.md
    └── @.workflow/skill/bootstrap/SKILL.md   ← Claude Code @ 导入

Layer 2 — 操作 SOP = tf 插件技能（斜杠显式 / bootstrap 路由自然语言）
├── /tf:todo-create     ← "加 TODO"
├── /tf:todo-progress    ← "做 #NN"
├── /tf:prd-review       ← review PRD
└── /tf:explore          ← "我有个想法"
   （住插件 skills/<名>/SKILL.md；自然语言时读 ~/.claude/skills/todo-workflow/skills/<名>/SKILL.md）

Layer 3 — 数据产物 schema（写入前 Read，住项目 .workflow/）
├── .workflow/todo/README.md      ← 改 todo/index.md 前 Read
├── .workflow/prd/README.md
└── .workflow/explore/README.md
```

**为什么这样分层？**

- Layer 1 永远在 = AI 进来就知道"有套路"
- Layer 2 在插件 = 代码与数据分离，更新走 `/plugin update`；斜杠显式调或自然语言路由
- Layer 3 写前读 = 防止 AI 凭记忆把 index 写成不同形态；schema 住项目让数据自描述

---

## 状态机（TODO 视角）

```
[创建] ──→ ⚪ todo  ⇄  ⏸️ on_hold ──→ 🟡 in_progress ──→ 🟢 done
              └──────────┴────────────────┴──────────→ ⚫ abandoned
```

**门槛：**

- `todo → in_progress`：AC（验收条件）必须已写齐
- `in_progress → done`：AC 全部勾完 + 验证通过（lint / test / 端到端）
- `→ on_hold`（搁置）：有 DoD + **复活条件**（不要求 AC）；`in_progress` 遇阻也可退回搁置

AC 是"可勾选清单"，DoD 是"一句话目标态"。两者都要写但用途不同（详见 todo-create SKILL）。

**`on_hold`（搁置）**="已成形但现在不具备条件"——既非可拾取的 `todo`，也非 `abandoned`。它单列**搁置表**移出可拾取池；进它必须写**原因 + 复活条件**，否则回 EXP 或 abandon。`abandoned` / `on_hold` 在索引都要填**原因列**。

---

## 一个 TODO 的完整生命周期（示例）

### 1. 创建

用户："加个 TODO：用户登录"

AI（按 todo-create SOP）：
- 检查粒度（0.5-2 天能干完？）
- 分配编号（如 #042，永不复用）
- Read `todo/README.md` 看 index 怎么写
- 创建 `TODO_042_user_login.md`（含背景 / 任务 / DoD，AC 可暂留 TBD）
- 在 `todo/index.md` 活跃表加一行

### 2. 推进

用户："做 #042"

AI（按 todo-progress SOP）：
- 检查 AC 是否已写（没写 → 拒绝开始，让 PM 补 AC）
- 改 frontmatter `status: in_progress` + index 状态列 🟡
- 真做事（写代码 / 改 schema / 加测试）

### 3. 完成

用户："#042 做完了"

AI：
- 核对 AC 全部勾完？没勾完 → 拒绝标 done
- 跑验证 checklist（lint / test / 重启服务等）
- 改 frontmatter `status: done`
- 移到 index.md 归档表（含完成日期 + 备注）
- **不自动 commit**（等用户拍板）

---

## 文件位置对照

```
# 项目里（数据 + schema + bootstrap）
.workflow/
├── README.md              ← 工作流总入口 + 升级 SOP
├── EVOLUTION.md           ← 方法论沉淀 + 演进日志
├── skill/bootstrap/SKILL.md  ← 唯一住项目的 SOP（@ 注入，常驻）
├── todo/
│   ├── README.md          ← todo/index.md schema 定义
│   ├── index.md           ← 全部 TODO 汇总
│   └── TODO_NNN_*.md      ← 单条 TODO（按需）
├── prd/                   ← 同上结构
└── explore/               ← 同上结构

# tf 插件里（操作 SOP，通过 /tf:* 调用，不写进项目）
tf/skills/
├── init/ · status/ · update/         ← 生命周期命令
├── todo-create/SKILL.md + TEMPLATE.md
├── todo-progress/SKILL.md
├── prd-review/SKILL.md
└── explore/SKILL.md
```

---

## 关键约定

### 编号

- TODO 用 `#NNN`（3 位数字）
- PRD 用 `PRD_NNN`
- EXP 用 `EXP_NNN`
- **永不复用**（done / abandoned 都保留原号；新建是最大已用 + 1）

### 日期

- ISO 风格 `MM-DD`（年隐含）；跨年时改 `YYYY-MM-DD`
- **不要** `2026.06.03` 这种点号格式（容易跟版本号混）

### 状态 emoji

| domain | ⚪ | 🟡 | ⏸️ | 🟢 | ⚫ |
|---|---|---|---|---|---|
| TODO | 未开始 | 进行中 | 搁置 | 完成 | 放弃 |
| PRD | draft | ready | —— | shipped | archived |
| EXP | seed | exploring | —— | promoted | dropped |

### index.md 列序（钉死禁改）

| domain | 活跃表 | 搁置表（仅 TODO） | 归档表 |
|---|---|---|---|
| TODO | 编号 / 标题 / 状态 / 添加 / 优先级 / 依赖 | 编号 / 标题 / 状态 / 添加 / **原因(含复活条件)** | + 完成 + **原因** |
| PRD | 编号 / 标题 / 状态 / 添加 / 澄清(R) / 关联 TODO | —— | + 完成 + 备注 |
| EXP | 编号 / 标题 / 状态 / 添加 / 下一步 | —— | + 完成 + 备注 |

**活跃项 = 扁平待办池**：不按 phase / 主题 / 月份分组，一堆松散 TODO 平铺即可。散户 TODO 完成/搁置时迁到 ## 归档 / ## 搁置。

**专项（Epic）= 活跃项之外唯一的分组**：把"同一件事拆出的多个 TODO"归到 `## 专项` 下 `### Epic：<名>` 表（列 = 活跃表 + `完成` + `原因/备注`）。**成员不拆散**——done/abandoned/on_hold 都在原行改状态 emoji、填 `完成` 日期、`原因/备注` 列记产出/理由/复活条件，所以 Epic 表是这件事的**完整台账**，回顾一眼看全。说"推进 Epic：<名>"，AI 按依赖序逐个推成员、每条门槛照常。**Epic 全完结**（成员全 🟢/⚫）→ 整块从 `## 专项` 迁到 `## 已完结专项`（在 `## 归档` 前），让 `## 专项` 只剩在做的、日常预览不被绿表淹没。区段顺序：活跃项 → 专项 → 搁置 → 已完结专项 → 归档。

详细列格式见各 domain 的 `README.md`。

---

## 红线（永远不要）

- ❌ AI 自动 git commit（等用户说）
- ❌ index.md frontmatter 存 count（手算 = bug 工厂）
- ❌ 把 on_hold 留在活跃表（进搁置表）；把 done/abandoned 留在活跃表（进归档表）
- ❌ 搁置 / 放弃不写原因（index 原因列空着）
- ❌ on_hold 没有复活条件（那是软放弃——回 EXP 或老实 abandon）
- ❌ 5 分钟修复也开 TODO（直接做 + commit）
- ❌ 状态跳级（todo → done 必须经过 in_progress）
- ❌ AC 没勾完标 done（"差不多了"不算）
- ❌ 「工作量大」当借口（详见 PHILOSOPHY）

---

## 进阶

- **interrupt 处理**（中途冒出新任务）：见 bootstrap §中途冒出新任务
- **EXP promote** 到 TODO/PRD：见 explore SKILL
- **PRD review 找澄清项**：见 prd-review SKILL
- **演进工作流本身**：在 `EVOLUTION.md` 加一条记录

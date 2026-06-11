---
name: prd-review
description: 对 PRD 做工程视角 review、找澄清项、拆 TODO。当用户丢入 PRD 文件、说"review 这个 PRD / 分析需求 / 拆 PRD"时用。需当前项目已有 .workflow/ 且启用 PRD 域。
argument-hint: "[PRD 文件路径或 PRD 编号]"
---

# /tf:prd-review — PRD 工程 review SOP

> 单人项目里，PM 的你写完 PRD，工程的你 review。目的：在动键盘前找出 PRD 里说不清楚 / 跟现状矛盾 / 实现成本被低估的地方。
> 用户输入：$ARGUMENTS。前置：当前项目**没有 `.workflow/`** → 提示先 `/tf:init`；项目**没有 PRD 域**（工具/库项目）→ 告知未启用 PRD，停。

## 流程

### Step 1：归位

- 新 PRD 存入 `.workflow/prd/PRD_NNN_<短描述>.md`（编号 3 位，永不复用）
- 更新 `.workflow/prd/index.md` 加条目 —— 按本技能 §索引格式 写，不要现编。

### Step 2：扫结构性问题

逐章节看，至少检查：

1. **可落地性**：每个字段 / 协议 / 组件，当前技术栈能不能做？
2. **依赖通路**：要的数据 / 外部服务 / 模型 / API，是否就绪？
3. **与现状冲突**：跟项目既有架构文档、`CLAUDE.md` 里的铁律、技术栈约定有没有矛盾？
4. **维度混淆**：同一份数据是否在不同地方有不同结构、不同生命周期？
5. **自指依赖**：A 依赖 B，B 又依赖 A？
6. **关键约束边界**：新需求是否触碰核心约束（安全 / 隐私 / 权限默认值）？与既定铁律冲突就挑出来让 PM 拍板。

### Step 3：产出 PRD-R 澄清文档（如有必要）

文件名：`PRD_NNN_RMMM_<主题>.md`（PRD_001 的第一个澄清 = `PRD_001_R001_xxx.md`）

```yaml
---
id: PRD_001_R001
title: "<澄清主题>"
prd: "PRD_001"
status: pending | accepted | rejected
date: "YYYY-MM-DD"
related_todo: "#NN, #MM"
---
```

正文段落：**背景**（哪段引起疑问）/ **问题**（具体说不清的是什么）/ **选项**（每个列代价）/ **推荐**（哪种、为什么）/ **决策**（user 填：最终选择 + 一行理由）。

### Step 4：拆 TODO

- 没阻塞 → `/tf:todo-create` 新建 TODO（`status: todo`），frontmatter 标 `prd: "PRD_NNN"`，进活跃表
- 硬阻塞 → 新建 TODO **直接建 `status: on_hold`**，note 写"等 PRD_NNN_R00M 决策"，进**搁置表**
  - 前提仍是**说得出 DoD**；连完成态都说不清 → 别建 TODO，回 EXP 或留在 PRD-R 决策清单

### Step 5：更新索引

- `.workflow/prd/index.md` —— 按本技能 §索引格式
- `.workflow/todo/index.md` —— 按 `/tf:todo-create` §索引格式
- 给用户简短摘要

## 红线

- **不要默认 PRD 写得对**——你的工作就是找漏洞
- **不要静默重写 PRD**——把问题写进 PRD-R，让 PM 的用户拍板
- **项目核心约束不可妥协**——任何 PRD 暗示要突破安全 / 隐私 / 权限铁律，都要在 PRD-R 里挑出来

---

## 索引格式（`.workflow/prd/index.md` 的权威 schema —— 写之前照这个）

Frontmatter 只一行 `type: prd`，**禁存** count 类字段。两段：`## 活跃项` + `## 归档`。

- **活跃表列序**：`编号 | 标题 | 状态 | 添加 | 澄清(R) | 关联 TODO`
- **归档表列序**：`编号 | 标题 | 状态 | 添加 | 完成 | 备注`
- 列内：编号 = `[PRD_NNN](PRD_NNN_xxx.md)`；状态 emoji ⚪draft/🟡ready/🟢shipped/⚫archived；添加·完成 = `MM-DD`；澄清(R) = 工程 review 待澄清项数（0 表无）；关联 TODO = 拆出的编号范围（如 `#009-#032`）；备注（仅归档）一句话总结。
- **修改规则**：新 draft → 活跃表加行；找出澄清项 → 改"澄清(R)"计数；`draft→ready`（澄清全解决）改 🟡；`ready→shipped`（拆的 TODO 全 done）删活跃行+归档加行；`→archived`（不做）归档 ⚫ + 备注写原因。
- **不要做的事**：改列序 / 把 shipped·archived 留活跃表 / frontmatter 加 count。

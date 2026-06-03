# PRD Review — PRD 工程 review SOP

> 单人项目里，PM 的你写完 PRD，工程的你 review。
> 目的：在动键盘前找出 PRD 里说不清楚 / 跟现状矛盾 / 实现成本被低估的地方。

## 触发

- 用户写完新 PRD 希望 review
- 用户传入外部 PRD 文档
- 用户说"review 这个 PRD" / "分析这个需求"

## 流程

### Step 1：归位

- 新 PRD 存入 `.workflow/prd/PRD_NNN_<短描述>.md`
- 更新 `.workflow/prd/index.md` 加条目 —— 首次本 session 操作 index 前，**先 Read [`../../prd/README.md`](../../prd/README.md) §index.md schema**，按列序 / 列格式写。不要现编。

### Step 2：扫结构性问题

逐章节看，至少检查：

1. **可落地性**：每个字段 / 协议 / 组件，当前技术栈能不能做？
2. **依赖通路**：要的数据 / 外部服务 / 模型 / API，是否就绪？
3. **与现状冲突**：跟项目既有的架构文档（如 `DESIGN.md`）、`CLAUDE.md` 里的铁律、`docs/tech-stack.md`（不引入计划外依赖）有没有矛盾？
4. **维度混淆**：同一份数据是否在不同地方有不同结构、不同生命周期？
5. **自指依赖**：A 依赖 B，B 又依赖 A？
6. **关键约束边界**：新需求是否触碰项目的核心约束（如安全 / 隐私 / 权限默认值）？若与既定铁律冲突，挑出来让 PM 拍板。

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

正文段落：

- **背景**：哪个章节 / 哪段话引起的疑问
- **问题**：具体说不清的是什么
- **选项**：可能的解决方向，每个都列出代价
- **推荐**：我推荐哪一种，为什么
- **决策**（user 填）：最终选择 + 一行理由

### Step 4：拆 TODO

- 没阻塞 → 新建 TODO，frontmatter 标 `prd: "PRD_NNN"`
- 有阻塞 → TODO 标 `todo` + note "等 PRD_NNN_R00M 决策"

### Step 5：更新索引

- `.workflow/prd/index.md` —— 按 [`../../prd/README.md`](../../prd/README.md) §修改规则
- `.workflow/todo/index.md` —— 按 [`../../todo/README.md`](../../todo/README.md) §修改规则
- 给用户简短摘要

## 红线

- **不要默认 PRD 写得对**——你的工作就是找漏洞
- **不要静默重写 PRD**——把问题写进 PRD-R，让 PM 的用户拍板
- **项目核心约束不可妥协**——任何 PRD 暗示要突破项目既定的安全 / 隐私 / 权限铁律，都要在 PRD-R 里挑出来

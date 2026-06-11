---
name: status
description: 看当前项目工作流状态（在做/待办/PRD/EXP 概览）。当用户说"在吗/今天做什么/看看状态/看 TODO 列表"时用。需当前项目已有 .workflow/。
argument-hint: "（无需参数）"
---

# /tf:status — 工作流状态汇报

1. 当前项目**没有 `.workflow/`** → 提示"先 `/tf:init` 初始化"，停。
2. 只读这些的表格（不读详情文件，省 token）：`.workflow/projects.md`（不存在跳过）、`todo/index.md`、`prd/index.md`、`explore/index.md`。
3. 按下面模板输出（≤6 行；数字现场数表格行，不靠 frontmatter）：

```
🟡 在做：#NNN <标题>（其他 in_progress 数量 N）
⚪ 待开始：N 条；下一个建议从 #NNN <标题> 起
🟢 已完成：N 条
📋 PRD：N draft / N ready / N shipped
🌱 EXP：N seed / N exploring
👉 你想推哪个？或者直接派活也行。
```

4. 汇报后停，等用户派活。无 PRD/EXP 域的项目省略对应行。

<!--
  TODO 详情文件模板
  使用方式：复制到 .workflow/todo/TODO_NNN_<短描述>.md，按方括号 / 注释填空。
  SOP 详见同目录 SKILL.md。
-->

---
id: NN
title: "<标题>"
status: todo            # todo | in_progress | on_hold | done | abandoned
added: "YYYY-MM-DD"
completed: null         # done / abandoned 时填日期
prd: "PRD_001"          # 可选，从哪个 PRD 拆来
explore: "EXP_001"      # 可选，从哪个预研转来
epic: "<Epic 名>"       # 可选，属于哪个 Epic（值 = 索引 ### Epic：后的名字）
priority: P0            # 可选：P0 | P1 | P2
note: "一句话当前进展"   # on_hold / abandoned 时 = 原因（搁置含复活条件）
---

# TODO #NN — <标题>

## 背景 / Why

<!-- 一两句话说清楚：为什么有这个 TODO？ -->

## 任务

- [ ] 子任务 1
- [ ] 子任务 2

## 完成定义（DoD）

<!--
  一两句话目标态："完成后世界变成什么样"。
  抽象、隐含可以；但不能"觉得做完了就行"。
-->

## 验收条件（AC）

<!--
  可观测、布尔、独立的检查项；可暂留 TBD。
  但 status: todo → in_progress 之前必须补好（PM 责任）。
  完成时必须全部勾完才能转 done。
-->

- [ ] AC 1
- [ ] AC 2

## 关联

- PRD: 
- 依赖: #NN
- 视觉参考:

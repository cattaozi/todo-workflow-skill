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

<!--
  这是整条 TODO 的总纲。不只写"为什么有这个 TODO"（动机/问题），
  也把驱动实现的**关键约束 / 取舍**写进来（如"必须防枚举""默认 private""不引计划外依赖"）。
  下面的任务为什么这么拆、这么做，读这一节要能懂。
-->

## 关键决策 / 方案

<!--
  可选——只在有"非显然、未来会被人问'为什么这么建'"的决策时写；没有就删掉本节。
  装的是「为什么这么实现」（长存的设计理由），区别于做完即作废的任务清单。
  事前想清的写这里（= 方案）；事中 / 事后冒出来的也补这里（= 关键决策）。
  例：bcrypt 直调不引 passlib（减依赖）；登录失败不区分"用户不存在/密码错"（防枚举）。
-->

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

# Design System of AI Workspace

> **V6 令牌升级（对齐 prd-v6 新设计稿 · 本节为权威，覆盖下文历史描述中与之冲突的值）**
>
> 本轮 UI 改造把设计系统从 V4.5 升级到 V6。**下文正文中的十六进制值、字体、"暖石灰"叙述若与本节冲突，以本节为准**（正文将分阶段逐步重写）。源文件 `src/app/globals.css`、`src/app/layout.tsx`。
>
> **① 字体（Inter → Funnel 超家族）**
> - 正文 = **Funnel Sans**（`--font-funnel-sans`，next/font，300–800），标题 = **Funnel Display**（`--font-funnel-display`），等宽 = JetBrains Mono。
> - CJK 始终回退 PingFang SC；Funnel 只覆盖拉丁字符。`@theme` 暴露 `--font-sans`（=Funnel Sans）/ `--font-display`（=Funnel Display）。
> - 不再是"只有一种 UI 字体"——标题/正文双字体（Display vs Sans）。
>
> **② 灰阶（暖灰 → 纯灰/微冷）** Stone 12 阶改纯灰、菜单微偏蓝绿一点点：
> `--g1 #FCFCFD · --g2 #FAFAFB · --g3 #F1F2F3 · --g4 #ECEDEF · --g5 #E4E5E8 · --g6 #D8D9DD · --g7 #CACBD0 · --g8 #B4B5BB · --g9 #8B8B90 · --g10 #7E7E83 · --g11 #605F66 · --g12 #1F1F23`
>
> **③ 品牌青 --t9（取自 Workspace logo，旧 #0C9488 不准）** `--t9 #0C9488 · --t10 #0A8378`；t1–t8、t11、t12 不变。`--t9` 仍是唯一产品 accent（`--accent` / `--sidebar-primary` / `chart-1` / `.brand-bar`）。
>
> **④ 新增"浮起"阴影体系**（强调真实浮起，非单层加深）：`--sh-card`（白卡浮灰面板）、`--sh-float`、`--sh-pop`、`--sh-panel`（只向下沉的柔影）、`--panel-edge`/`--card-edge`（发丝级暖描边定边界）、`--glow-teal`（青绿活气）、`--ring-accent`（焦点环）。基础 4 档 `--sh-xs/sm/md/lg` 保留不变（仍用 `rgba(33,32,28,≤8%)`）。
>
> **⑤ 字号刻度 token**：`--t-display 34 · --t-h1 21 · --t-h2 17 · --t-lg 15 · --t-body 14 · --t-sm 13 · --t-meta 12`（根字号仍 14px）。**已删 `--t-micro`（原 10）** + `--t-meta` 11.5→12——CJK locale 的 Chrome 强制最小字号 12px（<12 被静默夹到 12，Chromium #36429，CSS 无法覆盖），10px 在中文用户浏览器上实渲就是 12 = 假值。`--t-meta 12` 是真实渲染的最小档，小标签/caption 一律落它。
>
> **⑥ 新增语义别名层 + 品牌色层 + 布局常量**：
> - 语义别名：`--canvas`(=g2 工作画布) `--surface`(白卡) `--surface-agent-binding`(零彩度会话绑定身份条) `--ink/-2/-3/-4` `--line/-soft/-2/-strong` `--desk`(#FBFCFC chrome 底) `--settings-canvas`(#EEF0F4 设置态浅灰)。
> - 品牌色层（换品牌只改这组 + Logo，**仅首页"这扇门"用**，产品 accent 仍走 --t9）：`--brand #1689C4`（偏蓝青）`--brand-strong/-ink/-wash/-soft/-edge/-glow/-glow-soft`。
> - 布局常量：`--nav-h 56 · --gutter 12 · --spine-w 300 · --stage-max 1080 · --stage-narrow 760`；动效 `--ease cubic-bezier(.32,.72,0,1) · --dur .18s · --dur-2 .28s`；半径别名 `--r-sm 6 · --r 8 · --r-lg 12 · --r-xl 16 · --r-pill 999`。
>
> **⑦ 视觉宪法四修正（来源 baseline-spec §7）**：① 边框回归发丝级（灰面板 + 白卡都 1px 暖描边 `--panel-edge` + 柔影）② 三层 canvas（首页品牌画布 / 会话暖灰 / 其余纯白，靠描边+阴影分层）③ 品牌色令牌层 `--brand-*`（首页 hero 走品牌色，可换品牌）④ 输入框规范（无描边、纯白+柔影、focus 极轻青环）。
>
> 后续 P1/P2/P3 会把"信息架构""首页双态""各业务页组件"小节补进本文档。

## 0. Information Architecture（V6 Shell）

> **V7 Shell 落地（2026-06-11 · 本节为权威，下文 V6 描述中与之冲突的值/文件名以本节为准）**
>
> 应用壳已整体迁到 ds 件：`layout/AppShell.tsx` 只做数据接线，chrome 本体 = `ds/patterns/shell/{AppShell,TopNav,Rail,WorkSurface}.tsx` + `ds/primitives/BrandLogo.tsx`；原 `Header/Sidebar/CapabilityTabs/SpaceSwitcher/SpaceAvatar` 已删除，空间/账号下拉 = `layout/{SpaceMenu,UserMenu}.tsx`（ds DropdownMenu，A20/A23）。
>
> - **chrome 底 = `--desk` 暖灰半档（K3）**：`oklch(97.5% .004 80)`，比主舞台低半档、hue 走暖与蓝灰画布（--h-canvas 250）冷暖对置；边界靠 WorkSurface 发丝边 + `--sh-stage` 柔影，不回内凹重质感。
> - **Rail**：同一套 DOM 收/展（图标恒 40 格居中，标签 flex 裁切 + fade）；选中 = 凹槽 well（--surface-well）+ **签名滑动白卡**（与顶栏 Segmented 同语言，--sh-active 浮起、无边框），不 teal 实填。会话列表每条 regular、激活才 medium，行 shrink-0 不被压缩（A17）；每行在 hover、键盘 focus 与粗指针触屏态显示三点菜单，归档不二次确认并做失败回滚。**收起 + 在某对话中 = 两个图标**（①当前对话承选中白卡，nav 三项全不选中 ②DotsThree =「所有对话」浮层：搜索 + 列表 + 当前项指示；两图标对齐 nav 图标列 x=36，带纸张按压反馈，A7）。展开与收起态均另设 Archive「已归档」入口，首次打开才加载，浮层内支持标题搜索、打开只读会话和逐条恢复。左下角「回经营」= ds Button ghost（A24，设置/广场/资产域出现）。
> - **TopNav**：三区栅格；logo 盒对齐 rail 图标列（心 x=36，A21），hover = BrandLogo `luster="soft"` 纯白追光（A22）；能力域切换 = Segmented（本处字号抬到 --t-body），**设置域内保留可见但整组降到 60% 弱化、hover/focus 回满（K5/A25）**，点击 = 先淡出（--dur-1h）再切回对应域首页，不瞬跳；右侧账号触发区无圆角、无底色、无展开态高亮，菜单浮层承担层级焦点，头像保持 `--r-pill` 圆形，键盘 focus 环仅落在头像上。
> - **域导航（K16）**：经营（新对话 /dashboard · 经营主题 /initiatives · 待办 /inbox）· 设置六视图（空间 /space · 成员与角色 /members · 连接 /connector · 世界观 /worldview · 知识 /knowledge · 能力 /skills）· 广场三板块（商店 /agent-plaza · 我的 /agent-plaza/mine · 构建 /agent-plaza/build）· 资产 `/assets` 第三域启用。
> - **主题对象页范式（K14 同形）**：主区 = 左列（对象头 + line Tabs + 内滚内容）+ 右列 ds ChatPanel（embedded + resizable）占满主区整高（顶天立地，不在 Tab 栏下）；线上 `initiatives/[id]` 与 showroom/theme 用同一批件。

V6 把应用壳从「左 Sidebar + 上 Header」重构为「全宽顶栏 + 下方 rail | 主区」三段。源：`src/components/layout/{AppShell,Header,Sidebar,CapabilityTabs,BrandLogo}.tsx`。

- **顶栏 TopNav（`Header.tsx`，对齐 `.nav`）**：全宽、`bg-[var(--desk)]`、`h-14`、三段栅格 `grid-cols-[1fr_auto_1fr]`。
  - 左：品牌字标（`BrandLogo`，内联 SVG，品牌青 currentColor）+ 收起 rail 按钮（`uiStore.toggleSidebar`）+ 空间药丸（`SpaceSwitcher variant="nav"`，复用 popover/switchSpace）。
  - 中：能力域切换 `CapabilityTabs`（`.surf` 分段控件：g3 轨 + 白色激活卡）——**经营 / Agent 广场 / 资产（敬请期待，禁用占位）**；按路由段判定 aria-current，「经营」覆盖除 Agent 广场/资产外的全部业务路由。
  - 右：账号头像（`UserMenu variant="nav"`，`.avatar` 32px 圆形 g12 底白字）。
- **左 rail（`Sidebar.tsx`，对齐 `.rail`）**：`bg-[var(--desk)]`，展开 300px / 收起 64px（`uiStore.sidebarCollapsed`）。
  - 搜索框（P1 静态占位）→ 竖向分段主导航（g3 轨 + 白色激活卡，激活态 `shadow-[var(--sh-xs)]` + `text-teal-11` 图标）：**新对话→/dashboard · 经营主题→/initiatives · 待办→/inbox（amber 计数徽章，数据 `hitlApi.summary`）** → 「对话」分区会话列表（`chatApi.listConversations` → `GET /conversations`，最近活动倒序；`.sess` 行 = 标题 + 状态徽章「在跟」teal /「等你审」amber，点击进 `/chat/[id]`，当前会话高亮）+ 底部统计 `railStats`。
- **主区**：`flex-1 bg-white`，承载各页内容。chrome（nav+rail）用 `--desk`，工作区用白——一眼区分"壳"与"台面"。
- **浮起面板（所有页统一）**：每个页面在主区内套一张浮起卡——外层 `h-full bg-[var(--desk)] pb-3 pr-3`（桌面 + 右/下 12px gutter，顶/左贴边，与 rail 顶部对齐），内层圆角 14 面板。三种皮：**首页/会话 = `gpanel--brand`**（`background.png` 天蓝品牌画布）；**业务页（待办/经营主题/设置等）= `gpanel--plain`**（白底 `border-stone-4` + `shadow-[var(--sh-panel)]`）。面板内常用居中内容栏（待办 780 / 经营主题 1000）。
  - 待办（`HitlInboxPage`，对齐 `pending.html`）：标题+副标题 + KPI 卡 + `.qtabs` 分段（全部/执行澄清/任务审核/执行失败）+ chatnote + 可内联展开 todo 行（kind 徽章 + 来源 chip + 优先级 + 相对时间）。
  - 经营主题（`initiatives/page.tsx`，对齐 `lists.html`）：大气页头（kicker+标题+lede+新建按钮）+ 按状态分组（运行中/筹备中/已归档）的 `.tcard` 2 列网格（渐变首字 mark + 名称 + 承诺 + 策略数）+ `.tadd` 虚线占位卡。

## 0.1 Home / Hero（V6 首页双态）

> **V7 首页升级（2026-06-11 B 线，覆盖下文 background.png 描述）**
> ① 画布 = `--surface-brand` 生成式画布（非图片），**第五轮（2026-06-11 B1）**：基底再沉一档（线性底 L 95.8→93.0 区间）、更灰更深；**hue 行程 蓝→蓝绿**（顶部 --h-canvas 250、向下渐转 --h-canvas-2 205，下半云也分两 hue）；顶部 conic 光束保持。网格 `--canvas-grid` 96px 格距、线 alpha .38，mask 从均匀竖向条带换成**偏心椭圆雾窗**（WorkSurface：网格只在画布腹地隐约成形、四向不等速瓦解，治"方格纸死板"）。
> ② hero logo = ds `BrandLogo height={60} luster="bright"`（B2 三轮）：**磁场悬浮板 + 会员卡扫光带**——指针进磁场（外扩 --s-7）板被牵引侧倾（hero 7°@透视 150 / shell soft 3.5°，rAF 弹簧 14%/帧 = 悬浮惯性）；光 = `--luster-sheen` 115° 斜向纯白扫光带（字形 mask），带心随倾斜矢量滑动、强度∝倾角（不倾不亮）。径向光斑（--luster-spot）退役：owner 实测拍死"很假的一个光点"。reduced-motion 静止低亮光带。
> ③ 提问输入 = ds AskComposer 开 `aura`（B3 二轮）：聚焦时框后浮现不规则双色云光（--aura-cloud，C .038/α .30 灰主青辅），每次进入聚焦云心随机偏移；**composer 焦点全中性化（2026-06-11）**——静息 --sh-card → hover --sh-input-focus → 聚焦 --sh-float 的中性抬起阶梯，描边只走 stone 发丝（聚焦 3→4），无青环无青边，颜色只属于 aura 云（形色分层，治"焦点样式脏"）。
> ④ 模型选择必有默认值，默认展示为“平衡”。showroom/home 同步镜像（K14）。

`/dashboard` 即"新对话"首页。源：`src/components/home/HomeHero.tsx`。

- **home 态布局（严格对齐 `home.html`）**：主区 = 浮在 `--desk` 桌面上的**品牌画布圆角面板**（`.gpanel--brand`：`background.png` cover + 只往下沉的柔影 + 无边框 + radius 14；资源 `src/components/home/background.png`），居中 720 内容栏（顶部 `clamp(88px,18vh,180px)` 留白）。
- 栏内：品牌字标（`BrandLogo` 48px）+ 问候（`home.greeting`，**时段词青色** `text-teal-9`，按 morning/afternoon/evening + `authStore.user.displayName`）+ 摘要句（`home.summaryPending/Clear`，按待办数）+ 提问输入（复用 `ChatBox`，圆角 16 + 柔影）+ 快捷 chips（描边药丸 + 星标，点击填充输入）。
- **active 态 = 跳转式**：提交 → `chatApi.createConversation({scene:'agent_chat'})` → 首条消息存入 `chatStore.pendingPrompt` → `router.push('/chat/[id]')` → `ChatPanel` 水合后经 pendingPrompt 自动发送一次（复用其 `handleSend`，不另写发送逻辑）。
- **下方工作区（`HomeWork` + `TaskRow`，对齐 `.home__work`/`.trow`）**：严格按设计稿的行式任务，**不保留原 dashboard 指标条/简报卡**。继续上次对话（`getLatestConversation`→/chat/[id]，状态"在跟"）/ 今天要你处理的 · N（`dashboardApi.getPendingApprovals`，**按提交时间倒序只展示最近 2 条**，每条→/inbox，状态"等你审" amber）/ 另外 N 件在自己跑（`getRunningTasks`，静默行）。`.trow` 为扁平行（非卡片），hover 仅浅底。复用 dashboard 同款 query key，沿用 `useDashboardStream` 的 SSE 失效。
- 原 `components/dashboard/briefing/*` 的块组件（MetricStrip / PendingApprovals / TaskActivity / RecentResults 等）首页不再引用（`useLocalePath`/`format` 仍复用）。

## 1. Visual Theme & Atmosphere

AI Workspace 是一套**面向企业经营的 AI Agent 控制台**——它要替运营、店长、督导这类"看数+决策"的角色把每天散落在多个后台里的事情拢成一个对话窗口。所以整个视觉系统的骨子里是 **"克制的工作台 + 一抹会动的青绿"**：暖石灰（warm stone）做底，承担 90% 的表面；**Teal Brand `#0C9488`** 只在状态、CTA、侧栏激活、左边那道 3px 品牌竖条上出现——它不是"装饰色"，而是"系统正在替你看着"的信号。

画布从 `#FCFCFD`（最浅暖白 `--g1`）滑到 `#FAFAFB`（侧栏 `--g2`），再到 `#F1F2F3`（assistant 气泡 `--g3`）——比纯白温暖一档，避免长时间盯盘的"医院感"。前景文字用 `#1F1F23`（`--g12`）这种**带一点石灰色的近黑**，而不是 `#000`，配合 14px 的根字号读起来像办公文档而不是 SaaS 营销页。

排版承担大部分品牌声音。**Funnel 超家族**承担英文：标题用 **Funnel Display**、正文用 **Funnel Sans**（300–800 档），CJK 回退 PingFang SC；数字键盘列里启用 `tabular-nums` 让 KPI 不跳动；**JetBrains Mono** 只在代码块出现。两条自定义类是品牌印记：`.pg-title`（20px / 700 / `-0.02em`）落在每个页面的左上角，`.nums-display`（800 / `-0.04em` / tabular）专门给大数字——这是经营产品里"数字是主角"的设计立场。

表面的几何节奏由两个半径主导：**8px (`--radius`)** 是 shadcn 默认（按钮、输入框、tabs），**12px** 是业务卡片（`.card-soft`、Dashboard 的 BlockFrame）。聊天气泡用 **16px 圆角 + 单角削成 4px** 的不对称，让用户气泡（黑色）和 assistant 气泡（muted 灰）一眼能分清"谁在说话"。阴影是 4 档暖灰 (`--sh-xs/sm/md/lg`)——所有 alpha 都低于 8%，从不"砸"出来；卡片悬停时只是边框从 `--g4` 提到 `--g6`、阴影从 xs 提到 sm，是耳语级的反馈。

**关键特征：**
- **Stone × Teal 双 12 阶**色板（`--g1..g12` + `--t1..t12`）+ 4 个语义 3 阶（red/grn/amb/blu × 3/9/11）为色彩底座；V6 在其上新增语义别名层、字号刻度、浮起阴影体系、品牌色层与布局常量（见顶部「V6 令牌升级」节）
- **Teal `#0C9488` 是唯一品牌色**——没有渐变体系、没有第二品牌色，全部克制在状态条/CTA/激活态
- 暖石灰画布（`#FCFCFD` 主页 / `#FAFAFB` 侧栏）替代纯白——长时间盯盘不刺眼
- **根字号 14px**（`html { font-size: 14px }`），所以 `1rem = 14px`、`text-sm = 12.25px`、`text-base = 14px`
- 半径分两层：**8px shadcn 控件** vs **12px 业务卡片**；聊天气泡 **16px + 单角 4px** 的削角是签名手势
- 签名元素：左侧 **3px Teal 品牌条 `.brand-bar`**、Sidebar 激活项的 **3px Teal 圆角条 + Teal-3 底**、Frap 风格的 chat input 固定底部
- 所有阴影都用暖灰 `rgba(33,32,28, ≤8%)`——四档低 alpha 叠层，从不单层重投影
- 暗色模式只翻转 shadcn 语义 token 到 oklch；**Stone/Teal 不变**，保 Teal 在深色面上的高亮地位

**色块页面节奏：** Stone-1 主画布 → Stone-2 侧栏 → 白色卡片浮在 Stone-1 上 → BlockFrame 内部用 `divide-y divide-stone-3` 分行 → assistant 气泡用 Stone-3 muted 底 → user 气泡用近黑微冷 `--primary`（`oklch(20% .006 H)`，非纯黑）——整页是"暖灰底 + 白卡片 + 一处 Teal 重音"的三层结构。

## 2. Color Palette & Roles

**Source files analyzed:** `frontend/src/app/globals.css:96–198`、`src/components/chat/ChatBox.tsx`、`src/components/chat/MessageBubble.tsx`、`src/components/chat/MessageList.tsx`、`src/app/(workspace)/dashboard/page.tsx`、`src/components/dashboard/briefing/BlockFrame.tsx`、`src/components/layout/Sidebar.tsx`、`src/components/layout/Header.tsx`。

> **⚠️ V6.1 OKLCH 生成式迁移（2026-06-05 · 以下覆盖本节旧 HEX 描述）**
> 色彩真源 `globals.css :root` 已从静态 HEX 全量迁到 **OKLCH 生成式**（对齐设计稿 `materials/prd/prd-v6.1/frontend/assets/tokens.css`）。下方各 HEX 表保留作 **≈ 感知近似参照**；**真值以 `globals.css` 的 `oklch()` 为准**。
> - **两个 hue 旋钮**：`--h-accent:186`（主色 Teal · 全系唯一会“响”的色 · 客户部署改这一处全系联动）、`--h-neutral:215`（中性灰 hue）。`--h-brand` 已收敛为 `var(--h-accent)`（跟随主色 · 原 Cloudtree 蓝 245 已弃 · 与设计稿 tokens.css 同口径）。
> - **Stone/Teal/语义 12 阶**全部由 `oklch(L C var(--h-*))` 生成（`--g*`/`--t*`/`--red|grn|amb|blu*`），改一个 hue 全盘连贯，无散落 hex。新增语义描边 `--{red|grn|amb|blu}-line`。
> - **chrome 底 `--desk`（原 #FBFCFC）/ 设置画布 `--settings-canvas`（原 #EEF0F4）/ 主操作 `--primary`（原 #0C0C0C 纯黑→`oklch(20% .006 H)` 近黑微冷）/ 白卡 `--surface`/`--card`** 全部入 OKLCH 体系。
> - **“灯圈” `--glow-teal` / `--ring-accent`** 由散落 `rgba(45,189,168)` 改为锚 `--h-accent` 的 `oklch(...)`（换主色连带变）。
> - **新增 token 族**：宽度 `--w-chat/page/wide`（740/760/920 · 修“每页一套 magic 宽度”真因）、间距 `--s-1..s-9`、高度阶 `--e0..e5`、表面场景 `--surface-nav/chrome/object/settings/chat`、生成式画布 `--surface-brand/--canvas-dots/--mesh-*/--brand-orb`。
> - **Dark Mode 块已删**（`globals.css` light-only · TODO #73）——下方“Dark Mode 策略”一节作废。
> - 仍待清：组件层 684 处裸 Tailwind 调色板色（`bg-violet-500` 等）+ `statusGlow.ts`/`ChartComponent` 硬编码，逐 slice 收口到 token。
>
> **品牌可移植活体演示（`/styleguide` 顶部 · `styleguide-portability-demo`）**：StyleGuide 顶部「可移植 · Brand Hue」面板 + 头部常驻旋钮，运行时改 `--h-accent`（预设 6 hue 青186/蓝250/紫295/品红350/橙70/绿150 + 自由 0–360 滑杆），现场看 accent 12 阶 + `--cat-1..6` 类别环 + 真实 ds 组件全盘重染、中性 stone 不动 —— 「换客户 = 改一行 `--h-accent`」的活证明（实现 `src/app/styleguide/{useBrandHue.ts,HueKnob.tsx,sections/BrandPortabilityDemo.tsx}`）。
> - ⚠️ **运行时换肤的浏览器约束**：`bg-teal-9` 这类「`var()` 撑色」属性若带 `transition`，Blink 在祖先 `--h-accent` 变时**不重解析**（specified value 文本没变），颜色卡旧值。故演示活体区禁用过渡（色阶/类别环本无过渡；真实组件用 `[&_*]:!transition-none` 就地关）。**真实交付客户 = 改 `globals.css` 的 `--h-accent` 后 rebuild**，构建期重算无此约束，整站（含带过渡组件）都正确重染。next-themes 式「换色压制过渡再恢复」对换 class 有效、对换 var 在恢复瞬间会回弹，故不用。

### Stone Scale — 暖灰主轴（12 阶）

承担 90% 表面与文字，比 Tailwind `slate/zinc` 更暖、比 `stone` 更克制。

- **`--g1` `#FCFCFD`** — 最浅暖白；主画布 (`bg-stone-1` / `--background`)
- **`--g2` `#FAFAFB`** — 侧栏底 (`--sidebar`)
- **`--g3` `#F1F2F3`** — assistant 气泡 / muted 表面 / BlockFrame 行分割 (`--muted`, `--secondary`)
- **`--g4` `#ECEDEF`** — 默认描边 (`--border`, `--input`, `--bd-s`)
- **`--g5` `#E6E4E0`** — 次级描边
- **`--g6` `#D8D9DD`** — 卡片 hover 描边 (`--bd`)
- **`--g7` `#CFCCC6`** — disabled
- **`--g8` `#B4B5BB`** — 三级文本 / 占位 (`--fg-d`)
- **`--g9` `#8B8B90`** — 二级文本 / `.pg-sub` (`--fg-s`, `--sidebar-muted`)
- **`--g10` `#82807A`** — 备用次级前景
- **`--g11` `#605F66`** — 强调文字 / 侧栏文字 / muted-foreground (`--fg-m`)
- **`--g12` `#1F1F23`** — 主前景；带石灰感的近黑 (`--foreground`)

### Teal Scale — 品牌青（12 阶，全系唯一品牌色）

- **`--t1` `#FAFEFE`** / **`--t2` `#F1FCFA`** — 极浅 wash（极少用）
- **`--t3` `#E0F8F3`** — Sidebar 激活项底色 (`--sidebar-accent`)
- **`--t4..t6`** `#CCF3EA` / `#B4ECDF` / `#96E2D1` — 中浅 tint
- **`--t7` `#6DD4BD`** — `.num-link` 虚线下划线
- **`--t8` `#2DBDA8`** — 焦点 ring (`--ring`, `--sidebar-ring`)
- **`--t9` `#0C9488`** — **品牌主色 / accent / 激活态品牌条 / chart-1** (`--accent`, `--sidebar-primary`)
- **`--t10` `#0A8378`** — 深品牌
- **`--t11` `#067A6F`** — Sidebar 激活文字 (`--sidebar-accent-foreground`)
- **`--t12` `#10443D`** — 极深（备用）

### Semantic — 红/绿/琥珀/蓝（每色 3 阶：3/9/11）

四组只取三档的语义色，覆盖 alert / badge / chart：

| 角色 | 浅底 (`-3`) | 主色 (`-9`) | 强调 (`-11`) |
|------|-------------|-------------|--------------|
| Red — 错误 / destructive | `#FFEFEF` | `#E5484D` | `#CD2B31` |
| Green — 成功 | `#E9F9EE` | `#30A46C` | `#218358` |
| Amber — 警告 / attention | `#FFF4D5` | `#FFC53D` | `#AD5700` |
| Blue — 信息 | `#EFF6FF` | `#3B82F6` | `#1D4ED8` |

### Surface 与 Action

- **Card surface**: 纯白 `#FFFFFF`（`--card`）——卡片是浮在 Stone-1 画布上的"白纸"
- **Primary action 黑**: `--primary` = `oklch(20% .006 var(--h-neutral))`（近黑微冷，非纯黑 `#000`、非青）——按钮主色不是 Teal 而是近黑；Teal 留给"系统状态/品牌激活"
- **Accent**: Teal `--t9 #0C9488`（`--accent`）——hover、focus ring、激活态、品牌条
- **Accent-ink**: Teal `--t11`（`--accent-ink`，`globals.css`）——青色"可读文字"色；用于青底软胶囊上的文字（`.tbadge--a` / `.io__t` / `.seg` 选中态计数）。对齐设计稿 `tokens.css --accent-ink`
- **Destructive**: Red `--red9 #E5484D`（`--destructive`）

### Sidebar 专属 token

侧栏自成一组以便独立换主题：

- `--sidebar` `#FAFAFB` — 底
- `--sidebar-foreground` `#605F66` — 默认文字
- `--sidebar-muted` `#8B8B90` — 分组小标题（10px 全大写 `tracking-[0.06em]`）
- `--sidebar-accent` `#E0F8F3`（Teal-3）— 激活项底
- `--sidebar-accent-foreground` `#067A6F`（Teal-11）— 激活项文字
- `--sidebar-primary` `#0C9488`（Teal-9）— 激活项左侧 3px 圆角条
- `--sidebar-border` `#ECEDEF` — 右侧分割线

### Chart 调色板

`--chart-1..5` = Teal-9 / Blue-9 / Amber-9 / Green-9 / Red-9——直接复用语义色，保证图表读数和 Alert 颜色含义一致。

### Dark Mode 策略

`.dark` 块（`globals.css:164–198`）**只改 shadcn 语义 token，全部用 `oklch()`**；Stone/Teal/Semantic 12 阶**不动**。这意味着 Teal `#0C9488` 在深色背景上保持完全相同的饱和度——它是"品牌信号"，不是"语义色"。

```css
.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.205 0 0);
  --muted: oklch(0.269 0 0);
  --border: oklch(1 0 0 / 10%);
  --accent: var(--t9);   /* Teal 不变 */
  --sidebar: oklch(0.17 0 0);
  --sidebar-accent-foreground: oklch(0.98 0 0);
}
```

### Gradient 系统

**没有结构性渐变 token。** 唯一一处渐变是 `.alive-surface`：

```css
background: linear-gradient(135deg, rgba(18,165,148,.06) 0%, rgba(253,252,251,.7) 100%);
border: 1px solid rgba(18,165,148,.15);
```

留给"经营简报头部 / 重要通告"等需要"系统在主动告诉你点什么"的场合，密度极低、Teal 含量 6%——是色块系统里的例外，不是规则。

> **光效令牌（2026-06-11 起；上面「没有结构性渐变 token」自此仅余历史陈述）**
> - **`--aura-1` / `--aura-2` / `--aura-cloud`**（二轮收敛）：AskComposer `aura` 的云状光晕——青 C .038/α .30、灰 α .50（灰感>颜色感），三个错位径向渐变叠形。composer 焦点不再叠 `--sh-input-glow` 青环（焦点全中性化，云独自承担焦点的"色"）；`--sh-input-glow` 仅 StrategyCard 起草态继续消费。
> - **`--luster-sheen`**（替役 `--luster-spot`）：115° 斜向纯白扫光带（不带色相），BrandLogo luster 层消费——带做 background、字形 svg 作 mask；带心 `--lx` 由倾斜弹簧逐帧写入（板向哪倾光带滑向哪），径向光斑形态退役。
> - **`--surface-brand`（B1 第五轮）+ `--h-canvas-2: 205`**：基底更深更灰（线性底 L 95.8/93.2/93.0/94.4），hue 行程 蓝(250)→蓝绿(205)；`--canvas-grid` 96px/α.38，mask 换偏心椭圆雾窗（见 WorkSurface）。
> - **`--desk`（K3 调档）**：chrome 底从近白（99.1）调到暖灰半档 `oklch(97.5% .004 80)`，与蓝灰画布冷暖对置。
>
> 双色光效全部锚 `--h-accent` / `--h-neutral` → 换客户品牌色全盘连贯。

## 3. Typography Rules

### Font Family

- **正文 (Body):** `Funnel Sans, -apple-system, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`（`--font-funnel-sans` → `@theme --font-sans`，next/font，权重 300/400/500/600/700/800；CJK 回退 PingFang SC）
- **标题 (Display):** `Funnel Display`（`--font-funnel-display` → `@theme --font-display`，权重 400–800），用于 hero / 大标题
- **Mono:** `JetBrains Mono`（`--font-jetbrains-mono`，400/500）—— 仅代码块、SQL/JSON 预览
- **没有第三方品牌字体；没有 serif；没有 script。** 中文 fallback 链按 Mac/Windows 优雅降级——这是中文 SaaS 必做的小事。
- **地区字形路由（i18n · W1 步2c）：** 正文/标题字族随 `<html lang>` 切——同一套 CJK 码位简/繁/日字形不同（Han 统一），不按 lang 切会拿简体字形渲繁体/日文（=「不像本地」）。`globals.css` 里 `body:lang(zh-Hant)`→PingFang TC/Noto Sans TC、`:lang(ja)`→Hiragino/Noto Sans JP、`:lang(ar)`→Noto Naskh Arabic，**均「系统字优先」、不自托管 CJK 大字库**（沿用上面杜绝-CLS 的取舍，Noto 仅具名兜底）；`zh-CN`（简体）沿用默认 SC 栈。标题（`.font-display` 工具类）因 `@theme inline` 把字族烤成字面量、`--font-display` 非运行时变量，故单列**无层** `:lang() .font-display` 覆盖（无层胜过 `@layer utilities`）。改这些同步本条。验证：styleguide 改 `document.documentElement.lang` → `getComputedStyle(body).fontFamily` 随之切。

### 根字号

`html { font-size: 14px }`（`globals.css:202`），所以 `1rem = 14px`。Tailwind 字号尺寸全部在此基准上重算：

| Tailwind | 实际 px | 用法 |
|----------|---------|------|
| `text-xs` | 10.5px | label、breadcrumb、说明文字 |
| `text-sm` | 12.25px | 默认 body、按钮文字 |
| `text-base` | 14px | 正文段落 |
| `text-[13px]` | 13px | 侧栏导航项（明确写死） |
| `text-[10px]` | 10px | Sidebar 分组小标题（全大写） |
| `text-xl` | 17.5px | MetricCard 数值 |

### Hierarchy

| Role | Class / Style | Size | Weight | Letter / Line | Notes |
|------|---------------|------|--------|---------------|-------|
| Display 数字 | `.nums-display` | 由父级决定 | **800** | `-0.04em` / tabular-nums | KPI 大数字主角 |
| Page Title | `.pg-title` | **20px** | 700 | `-0.02em` / 1.3 | 每页左上角；色 `--g12` |
| Page Sub | `.pg-sub` | 14px | 400 | normal | 副标题；色 `--g9` |
| Card Title | `font-semibold text-sm` | 12.25px | 600 | normal | 卡片头 |
| Section Label | `text-[10px] uppercase tracking-[0.06em]` | 10px | 600 | 0.06em | Sidebar 分组 |
| Body | `text-sm` | 12.25px | 400 | 1.5 | 默认段落 |
| Button | `text-sm font-medium` | 12.25px | 500 | normal | shadcn 默认 |
| KPI 数值 | `text-xl font-semibold tabular-nums` | 17.5px | 600 | tabular | MetricCard |
| Label/Caption | `text-xs text-muted-foreground` | 10.5px | 400 | normal | 字段标签、时间戳 |

### 原则

- **英文走 Funnel 超家族（Display 标题 / Sans 正文）。** 标题与正文区分但同源，保持一致的字形气质；经营场景以可读为先。
- **数字优先用 `tabular-nums`。** MetricCard 的数值、`.nums-display`、表格列都用等宽数字，避免数字滚动 / 切换时跳动。
- **`-0.02em` 到 `-0.04em` 的负字距留给标题与大数字。** 正文 0；按钮 0；只有 `.pg-title` 和 `.nums-display` 用紧排——它们是"主角"。
- **不用纯黑做正文。** `--foreground` = `#1F1F23` 而不是 `#000000`，配合暖石灰画布读起来更柔。
- **中文 fallback 链显式写出**（`PingFang SC` / `Hiragino Sans GB` / `Microsoft YaHei`）——是本地化产品的卫生工作。
- **`--font-jetbrains-mono` 只在 `<code>` 出现**；正文里不要混排等宽英文。

## 4. Component Stylings

### TypeTile · 类型标识（L2 · 全站唯一收口 · 2026-06-11）

凡是表示「这条东西是什么类型 / 哪类来源」的小视觉块 —— 模块图标块、首字块、
原子/专家/技能/Dify 字标、约束/偏好字标 —— 一律用 `ds/components/TypeTile`,
不再在页面里搓 span。设置四页（连接 / 世界观 / 能力 / 知识）与 showroom/styleguide
镜像已全部走它。

**两形态：**

| 形态 | prop | 用在哪 | 尺寸 |
|---|---|---|---|
| tile（方形软底图标 / 首字块） | `icon` 或 `initial` | 行首标识、卡面标识 | `sm`=24px（密集行）· `md`=`--control-h-1`（28，卡面） |
| label（文字类型徽标） | `label` | 行内类型字标（原 .tbadge） | `sm`=`--t-meta`（12，最小档）· `md`=`--t-sm` |

**色律：** 默认 `neutral`（stone-3 底 / stone-11 字）—— 类型是归类，不抢戏。
语义档（`accent/success/warning/info/danger`）全走 soft wash（-3 底 / -11 字），
不占 teal 实填配额；只给设计稿点名的少数类型档，不当装饰分类色。圆角一律
`--r-ctrl`（软方=结构）；禁裸 tailwind 调色板色、禁 10px 字。

**正典 tone 映射（页面层维护，贴业务数据写）：** 行动·原子=neutral / 专家=accent /
技能=warning / Dify=info；准则·约束=neutral / 偏好=accent；模块、来源首字块一律 neutral。
优先级（关键/高/中/低）是状态语义不是类型，继续走 pri 胶囊，不归 TypeTile。

**配套纪律（去后台感）：** 类型/来源的主位给人话名称与说明；编码（`consumer` / `CM` /
`action_code` 这类）一律降为 meta 行的 mono 小字，不进标题位、不进徽标位。

### ChoiceCardGroup · 语义单选卡（L2 · 2026-06-11）

选项需要"把自己说清楚"时（准则类型、调用方式等）用 `ChoiceCardGroup`，不退化成
Segmented（owner：把语义压没"显得非常平庸"）。基于 radix RadioGroup；两密度：
`card`（标题 + 一行说明同时可见）/`chip`（单行刻度）；`tone` 让选中态染语义软底
（danger 红 / warning 琥珀 / muted 灰 / 默认 teal-2），与列表行 pri/tbadge 胶囊同语。
现役：知识页准则表单（类型 card / 优先级 chip 四档带 tone）、构建 Agent 委托书（调用方式）。

### Reveal · 就地展开容器（L2 · 2026-06-11）

「新建准则」类就地展开一律走 `Reveal`（grid-template-rows 0fr↔1fr 过渡，--dur-3 系统缓动）：
有缓动地推下去 / 收回来，不许生硬跳出（owner 2f）。`unmountOnExit` 收完再卸载；
reduced-motion 瞬时。在 space-y 流里用时给 Reveal `-mb-[gap]`、内容内置 `pb-[gap]`
（收起不留双倍空隙，间距随展开长出）。

### 模态与页面进场时长（2026-06-11 · 治「秒出」）

tw-animate-css 的 animate-in 默认 150ms —— 模态档必须显式给时长：Dialog/Sheet 进场
`[animation-duration:var(--dur-4)]` + `--ease-out`（Dialog 另加 slide-in-from-top-2 落定位移），
收场 `--dur-2`（收比进快）。页面切换进场 = WorkSurface 内容 / SettingsView 容器统一
`fade-in + slide-in-from-bottom-1 + --dur-3`（随路由重挂每次导航走一遍）；reduced-motion 全关。

### WorkRail · 会话工作区栏（chat 域 · 2026-06-11）

会话页右缘常驻栏（inflow-build 设计 §2 第一跳）：窄条（--control-h-3，徽标竖排）↔
面板（--w-sheet-sm，白面 + 左发丝边，宽度 --dur-3 过渡推开）。内容组 = 产出物（真接口，
替代原 Sheet 浮层）+ 构建提案（build_proposal 事件接入前只留一行空态说明，零模拟数据）；
工具调用不进右栏（流水留在对话流内 ThoughtChain 折叠行）。`?artifact=` 深链 = 自动展开 + 高亮。


### Buttons（`src/components/ui/button.tsx:7–39`）

shadcn 标准 6 变体 × 5 尺寸。

**1. Default — 主操作**
- 背景: `--primary` `oklch(20% .006 var(--h-neutral))`（近黑微冷，非纯黑、非青；hover `--primary-hover` `oklch(13% .008 H)`），文字 `#FFFFFF`
- Hover: `bg-primary/90` 或 `--primary-hover`
- Radius: `rounded-md` = `--r` (7px)
- 高度: 36px (`h-9`)，padding `px-4`
- 字号: `text-sm font-medium` (12.25px / 500)

**2. Destructive**
- 背景: `--destructive` (`--red9`)，文字白
- 同样 7px / 36px

**3. Outline**
- 背景透明，`border border-input` (`#ECEDEF`)
- Hover: `bg-accent text-accent-foreground` → 切到 Teal `#0C9488` 底
- 用于"次要但不弱"的操作

**4. Secondary**
- 背景: `--secondary` (`#F1F2F3`)，文字 `--foreground`
- 比 Outline 更轻——内嵌在卡片里时用它

**5. Ghost**
- 完全透明，hover 出 `bg-accent`
- Header 里的工具按钮（用户菜单、agent 抽屉触发器）用它

**6. Link**
- 仅文字 + 下划线，文字色 `--primary`

**尺寸：** `xs` 24px / `sm` 32px / `default` 36px / `lg` 40px / `icon-*` 方形等径。**没有 `xl` 尺寸**——经营产品不做营销大按钮。

**没有 `transform: scale(0.95)` 的 active state**——按钮按下只是颜色变化（`/90` 透明度），更克制。

### DS Primitives（`src/components/ds/primitives/` · 从零重建层 · L1-primitives-batch1 + batch2 + batch3 + batch4）

> 这是**设计系统重建层**，与上面的 `ui/`（团队在用的 shadcn 层）并存、不冲突：`ui/` 是现网，`ds/` 是逐块替换它的单一真源。两层都只读 `globals.css` 语义令牌。组件值以源码 + `globals.css` 为准，本文档退为「为什么 + 怎么用」（原则 9）。验收台 = 公开路由 `/styleguide` 的 L1 Primitives 段，渲染真实组件本体全 8 态。

**为什么不直接改 `ui/`**：`ui/button.tsx` 等被全站 `[locale]` 页消费，过夜无人值守改不了团队鉴权页。`ds/` 走 only-add，先建本体 + showcase 像素核，迁移留白天有人时做。

**8 态统一口径**（宪法§6，每个 ds 件都按这套）：`default / hover / focus-visible / active / disabled / loading / selected / error`。其中 hover/focus-visible/active 由真实 CSS 伪类驱动（不写死、不造 prop）；disabled 走 `disabled` 属性；loading/selected/error 走 prop。某态对某组件不适用时（如 input 无 loading）在 showcase 诚实标 N/A，不假装。

#### `Button`（`ds/primitives/Button.tsx`）

CVA 四轴 `variant × tone × size`（+ `iconOnly`），颜色矩阵落 `compoundVariants`，**绝不散落 className 三元**（宪法§3）。

- **`variant`（填充处理）** `solid`(默认) / `outline` / `ghost`。
- **`tone`（颜色角色）** `neutral`(默认) / `accent` / `danger`。`accent` = 品牌青 `--t9`，**稀缺**，只给 hero / 「轮到你动的」（宪法§5）；`neutral` solid = 近黑 `--primary`（主操作不是青）；`danger` = `--red9`。
- **`size`** `sm` 36px(桌面密集态·指针环境，<44 触控门) / `md` ≥44px(默认，满足触控门) / `lg` ≥52px(字号升到 `--t-body`)。`iconOnly` 锁方形等边（36/44/52）。
- **状态**：`disabled` 降到 `--op-disabled`(.40) 且锁交互；`loading` 渲染 Phosphor `CircleNotch` 转圈 + `aria-busy`，**保色只转圈**（与 disabled 的降级区分）；`selected` 走 `aria-pressed`（每组一个按下保持底）；`error` = `tone="danger"`。
- 焦点 = `focus-visible:shadow-[var(--ring-accent)]`（键盘可见环，鼠标不触发）。圆角 `--r`(7)，字号 `--t-sm`(13)。`asChild` → `Slot.Root`（链接戴按钮样式）。图标 Phosphor 钉死 `weight="regular"`（宪法§4）。

#### `Input` / `Textarea`（`ds/primitives/{Input,Textarea}.tsx`）

design.md「表单字段 = 样式库唯一真源」.input/.textarea 的本体。**带标签表单输入**（focus 给 teal 描边 + `--ring-accent` 环），与聊天大输入（`.composer`/`.ask`，无环）是两类，别混。

- 圆角 `--r-lg`(10)，描边 `stone-4`，底 `--surface`，字号 `--t-body`(14)。
- focus：`focus-visible:border-teal-7 + --ring-accent`。
- `invalid` prop → `aria-invalid` → 红描边 `red-9` + 红环（错误样式全走属性选择器，无 className 分支）。⚠️ 红环目前是 `oklch(62.5% .205 25/.30)` 字面量——无 `--ring-danger` 令牌，留作后续补一个 danger 环令牌再收口。
- `disabled` 用 muted 底（`stone-3`）非 opacity（保字可读）；`readOnly` 用 `stone-2`（比 disabled 浅一档，区分「不可编辑的真数据」与「禁用」）。
- `inputSize` `sm`/`md`(≥44，对齐 design.md .input 高 44)/`lg`；Textarea `resize-none` + 按 size 给 `min-h`（64/88/120）。`Input` 支持 `leftIcon`（Phosphor，size=16）。

#### `Field` 组合件（`ds/primitives/Field.tsx`）

纯组合（无 CVA，无变体轴）：`Field`（容器，`--s-2` 竖向节奏）/ `FieldLabel`（`required` → 红星 + `sr-only`「必填」给读屏；`optional` →「选填」灰字）/ `FieldHint`（meta 灰）/ `FieldError`（`role="alert"` 红字）。login / settings / 建表单都用它。

#### 表单控件 batch2（`ds/primitives/{Checkbox,Radio,Switch,Select}.tsx`）

四个都基于 `radix-ui` 统一包（无障碍/键盘原语免费），只贴语义令牌皮肤。共同口径：**选中/激活 = `teal-9`**（design.md §2.2「accent 只在状态/CTA/激活出现」——勾选/单选/开关的「选中/开」就是激活，hover 压暗到 `teal-10`）；未选中性 = `stone`；`focus-visible:shadow-[var(--ring-accent)]` 真伪类环；`disabled` 降到 `--op-disabled`(.40)；`invalid` prop → `aria-invalid` → 红描边 `red-9`。触控：勾选/单选本体 14–18px、开关 22px、Select trigger ≥44px——小控件靠**配对 label 行**构成 ≥44 命中区（源码注释说明，showcase 渲 label 行验证）。

- **`Checkbox`** 方框 `--r-sm`(5)，`size` sm(14)/md(18)。`checked`/`indeterminate`（Radix 三态）都填 `teal-9` + 白勾；勾用 Phosphor `Check`、半选用 `Minus`（钉死 `weight="regular"`）。`loading` N/A（即时本地切换，无异步态）。
- **`Radio`** `RadioGroup`（默认 `grid gap-[var(--s-2)]`）+ `RadioGroupItem`（正圆，sm16/md18）。选中 = `teal-9` 描边 + 居中实心圆点（纯 `<span>` `bg-teal-9`，sm6/md8，**非图标**）。`loading` N/A。
- **`Switch`** 轨 `--r-pill`，md `40×22` / sm `32×18`（design-px）；开 = `teal-9`、关 = `stone-5`(hover `stone-6`)；thumb 白圆 + `--sh-xs`，`transition-transform`。**这是 shadcn `ui/switch.tsx` 裸 emerald/slate + `dark:` 的令牌化最终替代**（only-add，不改 `ui/`，迁移期换 import 指向）。`active/error/loading` N/A（二元即时切换、无校验、无异步）。
- **`Select`** trigger 视觉对齐 `Input`（`--r-lg`(10) + 描边 `stone-4` + focus/open 转 `teal-7` 描边 + `--ring-accent` 环 + `invalid` 红描边）；content = `--popover` 底 + `--sh-pop` + `--r-lg`，item `data-[highlighted]:bg-stone-3`、选中走 `ItemIndicator`（Phosphor `Check`，`teal-11`）。导出全 8 part（Root/Group/Value/Trigger/Content/Item/Label/Separator）。⚠️ `SelectLabel` 必须裹在 `SelectGroup` 内（Radix 约束）。`loading` N/A（同步 portal，异步占位由调用方在 Content 内渲）。

#### `Badge` / `Tag`（`ds/primitives/{Badge,Tag}.tsx`）

纯 CVA（非 Radix），**`tone` 升一等变体**（宪法§3「`<Badge tone="warning">`」）。两者 `tone` 同一套族映射：`neutral→stone / accent→teal / success→grn / warning→amb / info→blu / danger→red`，颜色矩阵落 `compoundVariants`（无散落三元）。

- **`Badge`**（静态状态/计数标签，`--r-sm`(5)，`size` sm/md）`variant` `soft`(默认) / `outline` / `solid`：
  - **`soft`**（推荐/默认）= `bg-{族}-3 + text-{族}-11`——design §2.3 保证 `-11 on -3 ≥4.5:1` AA。
  - **`outline`** = 透明底 + `border-{族}-line` + `text-{族}-11`（neutral 用 `border-stone-5`；**accent 用 `border-teal-7`** —— teal 无 `-line` 令牌，沿用 Button accent-outline 既有档，非杜撰）。
  - **`solid`** = `bg-{族}-9 + 白字`，**两处 a11y 偏离**：`warning` 改 `text-stone-12`（amb-9 太亮，白字不过 AA）；`neutral` 用 `bg-stone-12`（stone-9 太浅，白字不过）。
  - 静态非交互 → hover/focus/active/disabled/selected/loading 多为 N/A（源码注释），8 态在此体现为 variant×tone 视觉覆盖 + `error = tone="danger"`。
- **`Tag`**（可移除归类 chip，`--r`(7)）`variant` `soft`/`outline`（同上色逻辑）；`leadingDot` → 前导 `size-[6px]` `bg-{族}-9` 圆点；`onRemove` → 末尾 Phosphor `X` 按钮（`hover:bg-stone-3`、`focus-visible` 环）。选中/校验语义不放 Tag（归 Checkbox/Radio/表单控件）。

#### Display / Static 件 batch3（`ds/primitives/{Icon,Spinner,Skeleton,Divider,Avatar,Link}.tsx`）

展示 / 反馈 / 占位 / 分隔类。多非交互件 → 8 态多为 N/A（源码 JSDoc 逐条说清由谁承载），不假装。验收台 = `/styleguide` 的 **L1 · Display / Static** 段，渲真实组件本体(像素核 computed styles 全等令牌)。尺寸凡需精确处一律 `[Npx] /* design-px N */`（全站 `html{font-size:14px}` 让 tailwind rem 数字档缩水≠设计 px）。

- **`Icon`**（全站图标唯一收口）钉死 Phosphor `weight="regular"`（§4 禁 faux-bold，本件存在的首要理由）+ 尺寸档 `xs14/sm16/md18(默认)/lg20/xl24`（锚 Button 图标档 14/16/18 向上补，全落 2px 网格，光学贴邻近文字 cap-height）。**不自带 tone**：color 走 `currentColor` 继承父文字色（icon-as-text 现代做法，随父 hover/selected/disabled 自动变色，免复刻 tone 矩阵）。a11y 二态：无 `label`→装饰(`aria-hidden`)、有 `label`→有意义(`role="img"`+`aria-label`)。状态→glyph 语义 registry 留给 L2 Status，本件不碰。
- **`Spinner`**（不定式等待指示器）Phosphor `CircleNotch` + `animate-spin`。`size` `xs14/sm16/md20(默认)/lg24`；默认无 tone = `currentColor` 继承（按钮内白、灰区灰），`tone` `accent(teal-9)`/`neutral(stone-9)` 仅给无父文字色可继承的独立 loading 区。a11y `role="status"` + `sr-only` 文案（`label` 默认「加载中」）。**reduced-motion 保留旋转**（established exception：spinner 是唯一进度信号，冻结即失意义；`animate-spin` 是 tailwind 1s linear 关键帧，不吃 `--dur-*` 令牌）。Button 内已有私有同款,本件供通用场景,不改 Button。
- **`Skeleton`**（内容加载占位）`bg-stone-3` 软底 + `animate-pulse`(透明度脉动)；`variant` `text`(行条 `--r-sm`,`lines`>1 渲多行末行短一截)/`rect`(块)/`circle`(圆,头像占位)，三形贴真实内容几何降 CLS。内容驱动尺寸经 `width`/`height` prop 落 `style`（§8 例外:运行时才知的数据尺寸非设计令牌)。`motion-reduce:animate-none`(静态灰块仍表达占位,冻结安全)。`aria-hidden`(加载语义由父级 `aria-busy` 承载)。8 态全 N/A(占位即 loading 态本身)。
- **`Divider`**（内容分隔）基于 radix `Separator`。`1px stone-3` 发丝线(design-px 防 rem 失真;`stone-3` 比描边档 `stone-5` 更轻——分隔非边框)；`orientation` `horizontal`(默认,`w-full`)/`vertical`(`h-full self-stretch` 取父高)。可选 `children`(仅横向)→「线—`--t-meta`(12) `stone-9` 文字—线」三明治(`role="separator"`)。`decorative`(默认 true,读屏跳过)/false(语义分隔)。
- **`Avatar`** / **`AvatarGroup`**（用户/实体头像）基于 radix `Avatar`(自动编排图片加载/失败兜底)。`size` `xs20/sm24/md32(默认)/lg40/xl48`(2px 网格主流头像梯度,不做 64+ 超大档=page 级)；`shape` `circle`(默认 `--r-pill`)/`square`(`--r`(7),不裸方角)。兜底 = 缩写(**中文取首二字 / 拉丁取首二词首字母**)或 Phosphor `User`(钉死 regular),软底 `bg-stone-3 + text-stone-11`(过 AA)。**`AvatarGroup`** 负叠(随档 6→14px) + 每项 `ring-2 ring-[var(--surface)]` 白边分隔(跟随面色,非裸白) + `isolate` 自成层叠;超 `max` 渲「+N」计数圆(`bg-stone-4` 比兜底 -3 深一档区分「计数非人」)。8 态:`loading`(图加载中)/`error`(图失败)由 radix 自动落 Fallback,其余交互态 N/A(纯展示,可点头像由调用方外层包)。
- **`Link`**（文本/导航链接,区别于 Button 动作触发器）CVA `variant × tone`，色走 `-11/-12` 文字档(过 AA)。`variant` `inline`(嵌正文,**始终带下划线** = 不靠颜色区分,对色盲友好;`underline-offset-3`,hover `decoration-stone-6→current` 加深)/`quiet`(无下划线,卡片/列表可点标题,hover 升一档)/`standalone`(独立链接,`font-medium`,hover 才加线,常配尾箭头)。`tone` `accent`(默认 teal-11——「轮到你动的导航」;accent 稀缺针对实色填充/hero,文本 teal-11 链接常规且克制)/`neutral`(stone-12)/`danger`(red-11)。`external` → `target="_blank"` + `rel="noopener noreferrer"`(切断 opener 反控) + 尾 `ArrowSquareOut` + `sr-only`「在新标签打开」。**`disabled` 走 `aria-disabled`**(`<a>` 无原生 disabled)+ 摘 `href` + `tabindex=-1` + `text-stone-8`(完整不可用语义,光去样式不够)。`asChild` → `Slot.Root`(Next `<Link>` 套样式)。`loading`/`selected`(归 `aria-current`)/`error`/`:visited`(工作台应用对象链接「已访问」无意义,刻意不设)逐条 N/A。

#### Overlay / Floating 件 batch4（`ds/primitives/{Tooltip,Popover,Combobox}.tsx`）

L1 最后一批 = 浮层类(radix Portal + 层级令牌 + 进出动效 + 焦点管理)。验收台 = `/styleguide` 「L1 · Overlay / Floating」段(真实组件本体,悬停/点击/打字走真实交互)。

- **`Tooltip`**（瞬时悬浮说明,不可交互;要交互内容用 Popover）基于 radix `Tooltip`。**反色高对比气泡**(`bg-stone-12` + `text-[var(--surface)]`,现代实践瞬读)+ `--r`(7)小件圆角 + `--t-meta`(12)字 + `--sh-pop` 浮影 + `z-[var(--z-tooltip)]`(700,最高打断档)+ `max-w-[260px]`(防长说明拉成一条)。`showArrow`(默认 true)同底色箭头。进场 `--dur-2` 档(fade+zoom+方向 slide,tw-animate-css)+ `motion-reduce:animate-none`。导出 `TooltipProvider`(默认 `delayDuration=600`/`skipDelayDuration=300`)/`Tooltip`/`TooltipTrigger`/`TooltipContent`。8 态:本体只有 open/closed,hover/focus 属宿主触发器,其余 N/A。
- **`Popover`**（放交互内容的白浮层:小表单/筛选/菜单)基于 radix `Popover`(自带 focus-trap + Esc + outside-click + 焦点归还)。白浮层对齐 `SelectContent`:`bg-[var(--popover)]` + `border-stone-4` + `--r-lg`(10) + `p-[var(--s-4)]` + `--sh-pop` + `z-[var(--z-popover)]`(500),默认 `w-[280px]`(可 className 覆盖)。进场 `--dur-3` 档 + `motion-reduce`。`arrow`(默认 false,opt-in——纯内容面板带箭头反读)。导出 `Popover`/`PopoverTrigger`/`PopoverAnchor`/`PopoverClose`/`PopoverContent`。
- **`Combobox`**（可搜索单选下拉)`cmdk` 未装 → 基于 radix `Popover` + 自建过滤列表 + **手写 WAI-ARIA combobox 模式**(activedescendant:焦点留搜索框,视觉高亮 active 项)。触发器视觉**逐类对齐 `SelectTrigger`**(`--r-lg`/`border-stone-4`/surface 底/`hover:border-stone-5`/`data-[state=open]:border-teal-7`/focus teal 描边+环/disabled `--op-disabled`/min-h 44/CaretDown 收尾)。搜索框内联(`MagnifyingGlass` 左图标,环在外层),listbox `max-h-[240px]` 滚动,选中项 `Check teal-11`、高亮项 `bg-stone-3`。键盘 ↑↓(循环跳 disabled)/Home/End/Enter/Esc/输入过滤;value 受控+非受控。`aria-invalid` 落在 `role=combobox` 的 `<input>`(WAI-ARIA 1.2),触发器用 `data-invalid` 作样式钩。`loading` N/A(同步过滤,异步由调用方备好 options)。导出 `Combobox` + `ComboboxOption`/`ComboboxProps` 类型。

#### ⚠️ 跨件修复:状态色过渡 = 即时切换(不放进 `transition`)

**Blink 实测 bug**:对 `border-color` / `background-color` 做 `transition`,当目标是 `var()`-OKLCH 令牌色(teal-7/teal-9 等)时,颜色**卡在起始值不插值**(open 描边卡 stone-4 不变 teal、动态勾选填充卡白不上 teal),需 reflow 才更新。`--h-accent` 在 styleguide 与生产都是 `:root` 静态 186 → 此为真实渲染缺陷,非换肤态 artifact。**修法**:把 `var()`-OKLCH 状态色移出 `transition` 列表 = 即时切换(对状态信号即时反更利落、跨浏览器稳健),只保留 `box-shadow`(焦点环)等过渡。已落 `Combobox/Select/Input/Textarea/Radio/Button` 删 `border-color`、`Checkbox` 删 `border-color`+`background-color`(填充是其首要选中信号)。computed 像素核全过。**未决**(见 ledger `decisions/transition-var-oklch-color-freeze`):Button 等 hover/active 填充(`background-color`→teal-10)同源,无头预览触发不了 `:hover` 未逐核;备选 `@property{syntax:'<color>'}` 注册令牌色保留插值动画(需改 globals.css,留互动 session)。

### DS L2 Components（`src/components/ds/primitives/` · L2 浮层容器层）

#### Overlay Containers L2（`ds/primitives/{Dialog,Sheet}.tsx`）

L2 第一批 = 浮层**容器**(占据全屏交互焦点的模态/抽屉,区别于 L1 的轻浮层 Tooltip/Popover)。均基于 radix `Dialog`(自带 `role=dialog` + focus-trap + Esc 关 + outside-click 关 + body 滚动锁 + 焦点归还,本层不重做)。验收台 = `/styleguide`「L2 · Overlay Containers」段(真实组件本体,点开真开真关、Tab 走真实 focus-trap、Esc 真关、长内容真内滚)。

- **共用 scrim 权威值**:`bg-[rgb(33_32_28_/_0.32)]` + `backdrop-blur-[2px]`(取 Final 原型 `assets/app.css .scrim`,**不用 shadcn 的 `bg-black/50`**)+ `z-[var(--z-scrim)]`(300) + fade 进出场 + `motion-reduce:animate-none`。content 层 `z-[var(--z-modal)]`(400)。
- **共用 Close**:右上角图标按钮(Phosphor `X` size 18 weight regular),`min-h/w-[44px]`(touch 门)+ `rounded-[var(--r)]`(7) + `hover:bg-stone-3` + `focus-visible:shadow-[var(--ring-accent)]` + `aria-label="关闭"`。hover 色过渡保留(对齐 Button 约定,`transition-[color,background-color] --dur-1`;批4 的即时切换只针对 open/checked **状态**色,不针对 hover)。
- **`Dialog`**(居中模态:聚焦任务/确认/表单)。Content `fixed top/left-1/2 -translate-1/2` 居中 + `w-[92vw]` 视口兜底 + `size`(CVA:sm=`max-w-[400px]`/md=520/lg=720)+ `rounded-[var(--r-xl)]`(12) + `border-stone-4` + `bg-[var(--surface)]` + `shadow-[var(--sh-pop)]`(e5) + `p-[var(--s-6)]`(24) + `max-h-[85vh] overflow-y-auto`(长内容内滚)。进场 `--dur-4`(400,模态档)fade+zoom-95 + `motion-reduce`。`hideClose` 隐藏 X(配 `onEscapeKeyDown`/`onInteractOutside` preventDefault = 强制决策场景)。组合件 `Dialog/DialogTrigger/DialogClose/DialogContent/DialogHeader/DialogTitle/DialogDescription/DialogFooter`(Footer `flex-col-reverse sm:flex-row` 让窄屏主操作落底)。
- **`Sheet`**(边缘锚定浮层)`side` 四向(right 默认/left/top/bottom)。CVA `compoundVariants` 按 side×size 落定位+尺寸+滑入方向:right/left 占满高、`size` 控宽(sm=360/md=460/lg=640,`max-w-[94vw]`)、`rounded-[var(--r-xl)]` 只给朝内一侧、`slide-in-from-{right,left}`;top/bottom 占满宽、`size` 控高(240/360/480,`max-h-[85vh]`)、圆角给朝内边、`slide-in-from-{top,bottom}`。content `shadow-[var(--sh-float)]`(e4 抽屉档)+ `--dur-3`(280)。三段式 `SheetHeader`(`px-[var(--s-5)] py-[var(--s-4)]` + `border-b`)/`SheetBody`(`flex-1 overflow-y-auto p-[var(--s-5)]`)/`SheetFooter`(`border-t` + 右对齐按钮组)。
- **`Drawer` = Sheet `side="right"` 语义预设**(原型 `.drawer` 右侧对象详情停靠面板,width `min(460px,94vw)`=md 档)。**不复制逻辑**:`Drawer/DrawerTrigger/DrawerClose` 直接别名 Sheet 同名件,`DrawerContent` 薄包装只把 `side` 默认钉成 `right`(仍可覆盖)并打 `data-slot="drawer-content"` 便于核。组合内容仍用 `SheetHeader/Body/Footer`。
- **像素核**(`/styleguide`,裸 dev):Dialog overlay `rgba(33,32,28,0.32)`+`blur(2px)` EXACT、z 300/400 EXACT、content white/stone-4 边/r-12/max-w 400(sm)/max-h 85vh、Close 44×44 r-7、`aria-labelledby`+`aria-describedby` 连、focus-trap(焦点入内)+ scroll-lock(`body overflow:hidden`)、Esc 关。Sheet right md:width 460/flush right 0/full-height 100vh/`rounded-l` 12 右侧 0/三段 border 1px/body 内滚。Drawer:`drawer-content` slot + side right 默认 + 460 flush。tsc 0·eslint 0·ds-lint 5/5。
- **a11y 注**:本版 unified `radix-ui` 的 Dialog 未输出 `aria-modal` 属性(role=dialog + focus-trap + scroll-lock 已界定模态边界),与团队既有 shadcn `ui/dialog.tsx` 同基线,非本层引入。

#### V7 ds 打磨与新件（2026-06-11 · wave1-polish / wave2 增量）

- **`Tabs`（line）**：选中记号升级为**测量式滑动指示条**——随选中 label 的 transform/width 滑到位（--dur-3 + --ease 标准缓动），首渲瞬定位不滑入，ResizeObserver 重测，reduced-motion 即时切换（A11）。下划线只压 label 文字宽——count badge 与 attention 点不计入；count badge 与文字 `items-baseline` 基线对齐，间距 --s-1（A12）。
- **`SearchField`**：`field` 变体（白底 + 发丝边 + --field-inset 内凹 + --field-focus 湿青灌槽）恢复为 shell 推荐档（owner 撤回灰底指示，A5）；放大镜走独立 prop `withIcon`（默认 true，与 variant 解耦），左侧 shell 用「白底无图标」；collapsed 恒显居中放大镜；filled 灰底保留可用但不再是 shell 默认。
- **`StatusBadge`**：kind 5→6，新增 `danger`（失败/异常，红族）。**唯一收口映射 `taskStatusToBadge(status)`**（ds barrel 导出）：后端 AgentTaskStatus 14 态 + 旧大写 run 态（toLowerCase 归一）→ kind——running/active=run；pending_review/editing/waiting_signal/waiting_feedback=attn；failed/rejected=danger；completed=done；其余=idle。任务状态配色一律经此映射，**禁止页面自建状态色表**；TaskCard/PendingTaskCard/TaskReviewDialog 已全量迁语义阶（-3 wash / -11 字 / -line 边），hover 守纵深律只换色（hover:shadow 抬影禁绝），待审批草稿卡 = attn 琥珀语义（原 violet 语言废除）。
- **`Segmented`**：图标档修正（A18）——sm/md 档 --icon-sm(16)，lg 档 --icon-md(18)；原 md=--icon-xs(14) 顶栏域切换肉眼偏小。
- **`StrategyCard`**：整卡 hover 缓动统一 --dur-2 + --ease-out（与 InitiativeCard 同口径，A14 残留已修）。
- **`StrategyCanvas` / `StrategyCanvasAdd`（新 L3 pattern，K9）**：经营主题「策略画布」——无边框无底色（画布 = 页面 surface，层次由卡片 --sh-card 承）；CSS multicol 自然高度错落，容器查询自适应列数（`@[700px]:columns-2` / `@[1080px]:columns-3`，保每列 ≥340、卡片 ≥320 体面线）；列/卡间距 --s-5；`relations` prop（{from,to,kind}[]）结构就位本期不画连线。`StrategyCanvasAdd` = 画布内虚线邀请卡（`<button>` 动作语义，区别 AddCard 的 `<a>` 导航；视觉同源：border-dashed stone-6 / hover 转 teal-7 + 抬升 -2px / --dur-2 + --ease-out）。
- **`AskComposer` 新增 `aura` prop（B3）**：聚焦时框后 -z-10 云层浮现（--aura-cloud + blur 24px，--dur-4 + --ease-out），每次从外部进入聚焦云心随机偏移 ±6px，reduced-motion 关移动；forceElevated 期间云保持。
- **dataviz / mask 卫生**：图表取色一律 `--chart-1..5`（SVG fill/stroke 直接消费 CSS 变量），裸 hsl()/hex 数组废除；纯 alpha 蒙版渐变用 CSS 关键字 `black` 不用 `#000`（ds-lint 规则 5 扫 .tsx 裸 hex）。
- **`components/plaza/` 业务域（K7）**：AgentStoreCard（货架卡，密度对齐 AgentRosterCard：p --s-4 + --sh-xs 最浅浮影，货架密铺不上 --sh-card 重影）/ SuggestionCard / BuildDraftCard——业务组合层，内部只 compose ds，文案全走 props（供 showroom 共用）。**「演示态」统一视觉记号 = `Badge tone="warning" variant="soft"`（K13 诚实纪律）**，不可证实内容必带。建议卡范式 = WorkCard + outline「采纳」+ ghost「忽略」双钮（不占 teal 实填配额，teal 留页面唯一主行动）；构建页双栏 = `grid-cols-[minmax(0,1fr)_var(--w-sheet-sm)]` + sticky top --s-4。页头一律 PageHead（--t-h0），「对象页页头单一真源」消费方 +4（商店/我的/构建/资产）。

### Cards & Containers

#### `.card-soft` — 业务卡片基类（`globals.css:235–252`）

```css
.card-soft {
  background: #FFFFFF;
  border: 1px solid var(--g4);   /* #ECEDEF */
  border-radius: 12px;
  box-shadow: var(--sh-xs);       /* 0 1px 2px rgba(33,32,28,.05) */
  transition: all .15s ease;
}
.card-soft:hover {
  border-color: var(--g6);        /* #D8D9DD */
  box-shadow: var(--sh-sm);
}
```

是 Dashboard / BlockFrame / MetricCard 的共同基底——**白纸浮在暖灰画布上**，hover 是耳语级反馈。

#### `Card` (shadcn) — `src/components/ui/card.tsx`

```
<Card>                  flex flex-col gap-6, rounded-xl(12px), border, bg-card, shadow-sm
  <CardHeader>          grid layout, px-6
    <CardTitle>         font-semibold
    <CardDescription>   text-sm text-muted-foreground
    <CardAction>        右上角槽位（按钮/图标）
  <CardContent>         px-6
  <CardFooter>          flex items-center, px-6
```

#### BlockFrame — Dashboard 信息块（`BlockFrame.tsx:50–100`）

经营简报的统一容器，三态（loading / error / empty / normal）共享外壳：

```
<div class="card-soft">
  <div class="flex items-center justify-between px-5 py-4 border-b">
    {icon} {title}                     ← header
    {headerExtra}                       ← 右上角槽
  </div>
  <div class="divide-y divide-stone-3">
    {children}                          ← 行项目
  </div>
</div>
```

支持 `tone="default" | "attention" | "destructive"` 切换 header 颜色到 Amber/Red 语义色。

#### MetricCard — KPI 网格（`MetricCard.tsx:39–79`）

```
<div class="rounded-lg border bg-card p-4 space-y-3">
  <p class="text-sm font-medium">{title}</p>
  <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
    {items.map(...)}
      <p class="text-xs text-muted-foreground">{label}</p>
      <span class="text-xl font-semibold tabular-nums">{value}</span>
      <span class="text-xs text-muted-foreground">{unit}</span>
      {trend ▲ green / ▼ red / · gray}
  </div>
</div>
```

**响应式：** mobile 2 列 → tablet 3 列 → desktop 4 列。趋势箭头复用语义色（Green-9 / Red-9 / Stone-9）。

#### InfoCard — 扁平信息面板

源码：`src/components/ui/info-card.tsx`。项目自定义共享组件。

适用范围：详情页右侧字段表、配置面板、辅助信息卡、监控信号 / 使用的行动 /
约束条件等"不是 Dashboard 信息块、不是 KPI、不是列表项"的信息容器。

结构规则：
- 内部派生自 shadcn `Card` + `CardHeader` + `CardContent`，但**强制扁平**：
  `rounded-[var(--r-lg)] border-stone-4 shadow-none`
- 跟 `ListCard` 同一套视觉语言（圆角令牌 `--r-lg` = 10px / Stone-4 描边 / 无阴影），区别只是
  ListCard 是"列表里一行可点击对象"、InfoCard 是"详情面板容器"
- 标题 `title` 渲染为 `text-sm font-semibold`；可选 `headerExtra` 槽给右上角按钮 / 筛选器
- 内容区 `CardContent` 不限制内部结构，业务自由组合 `dl` / `ul` / 自定义布局

为什么不直接用裸 shadcn `Card`：shadcn 默认 `shadow-sm`（v0/营销页风格），跟项目"克制
工作台 + 暖石灰底"的视觉立场不符。直接用裸 Card 会让信息密集的详情页显得"卡片浮起一
层 v0 风"，跟 ListCard 不一致。InfoCard 把这层定制做成共享件，避免各页自己散落定制。

#### PageHead / PageContainer — 管理页统一页头容器

源码：`src/components/ui/page-head.tsx`。项目自定义共享组件。

适用范围：经营主题列表（`initiatives/page.tsx`，对齐 `lists.html`）、待办（`HitlInboxPage.tsx`，对齐 `pending.html`）、设置子壳五视图（对齐 `settings.html` 的 `.objp--settings`）。把"每页一套 magic 宽度 / 间距"收齐到一个共享件，修用户点名的「首页一套·经营主题一套·待办一套·设置又一套」。

`PageContainer` 视觉规格：
- 居中容器：`mx-auto w-full min-w-0 max-w-[var(--w-wide)] px-[40px] pb-[56px] pt-[34px]`
- `--w-wide` = 920px；padding 用绝对 px（不用 Tailwind rem 档），因为全站 `html{font-size:14px}` 会让 `pt-7` 这类 rem 档算成 24.5px 而非设计稿的 34px。

`PageHead` 视觉规格：
- 标题恒定：`text-[28px] font-bold leading-[1.15] tracking-[-0.022em] text-stone-12`（= 设计稿 `.pane__h1` / `.objp__title`）。
- `kicker`（可选）：标题上方全大写小标签，`text-[10px] font-semibold uppercase tracking-[0.09em] text-stone-8`；存在 kicker 时标题 `mt-[11px]`。
- `subtitle`（可选 slot）：标题下方副标题 / lede，由页面自带样式（终端态 13px vs lede 14px 是设计有意保留的差异）。
- `actions`（可选 slot）：右侧操作区（如"新建"按钮），与标题底对齐。
- `withBorder`（可选 boolean）：页头下分隔线，`border-b border-stone-3 pb-[16px]`（经营主题列表 / 设置用）。

约束：
- 改这些数值 = 同步本节 + `src/components/ui/page-head.tsx` + 设置子壳节奏（`CLAUDE.md §8.2.2`）。
- 三处页面（经营主题 / 待办 / 设置）共用同一节奏；新增管理类页面优先复用，不要散落"再写一套"。
- 设置子壳因 head / content 双带 rhythm 不同，目前仍在 `space/page.tsx` 等处走内联同值（28px / 920），后续可统一收齐到 PageHead 完整接管。

#### List Card Components

列表卡片是列表型业务页面的标准对象呈现组件。源码位于 `src/components/ui/list-card.tsx` 和 `src/components/ui/expandable-list-card.tsx`，它们是项目自定义共享组件，不是 shadcn 生成文件。

**`ListCard` — 普通列表项**

适用范围：对象列表、动态列表、近期结果、关系列表等点击进入详情、弹窗或抽屉的列表项。

结构规则：
- 外壳：`w-full rounded-[var(--r-lg)] border border-stone-4 bg-card px-4 pb-4 pt-3 text-left shadow-none`（圆角令牌 = 10px）。
- 可点击态：`cursor-pointer transition-colors hover:border-stone-6 hover:bg-stone-1`。
- 标题行：`flex min-w-0 items-center justify-between gap-4`，左侧标题和徽标，右侧轻量信息。
- 标题：`h3 truncate text-[15px] font-semibold leading-5 text-foreground`。
- 元数据：`flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-muted-foreground`，项之间统一使用 Stone-7 的 `·`。
- 描述：`text-sm text-muted-foreground`。
- 前置图标：通过 `leading` slot 注入，容器固定为 `h-5 w-4`。

props 规则：
- `title` 表达对象名称，字符串标题自动使用 `ListCard.Title`。
- `titleBadges` 放状态徽标或标题级短标签。
- `titleRight` 放时间、计数等右侧轻量信息，不放主操作按钮。
- `meta` 放来源、时间、类型、系统、模块等辅助信息。
- `description` 放自然语言描述、进度或说明文本。
- `interactiveElement="button"` 用于普通可点击卡片；卡片内部存在交互控件时使用 `interactiveElement="div"`。
- 元数据局部强调使用 `ListCard.MetaHighlight`。

**`ExpandableListCard` — 可展开列表项**

适用范围：知识库规则、世界观动作类型、需要在列表内展开查看字段、配置或说明的对象。

结构规则：
- 折叠态与 `ListCard` 保持相同标题、元数据和描述节奏。
- 外壳：`rounded-[var(--r-lg)] border border-stone-4 bg-card shadow-none transition-colors hover:border-stone-6 hover:bg-stone-1`。
- Header 按钮：`flex w-full cursor-pointer items-stretch gap-3 px-4 pb-4 pt-3 text-left`。
- 展开图标：右侧 `ChevronDown` / `ChevronUp`，`h-5 w-5 text-muted-foreground`。
- 展开内容：`space-y-4 border-t border-stone-3 px-4 pb-4 pt-3`（分隔线走 Stone-3，跟外框 Stone-4 描边同体系但更浅，留出"同一卡内"的暗示）。
- 展开内容只放详情片段、字段组、规则说明或轻量操作，不承载整页级复杂表单。

约束：
- 普通列表使用 `ListCard`，可展开列表使用 `ExpandableListCard`。
- 不在页面里手写同构列表卡片；新增视觉能力时扩展组件 props。
- 编辑、删除、审批等高成本操作进入详情、Dialog 或 Drawer，不铺在列表卡片主视觉层。
- 列表卡片不新增阴影；层级靠 Stone 边框、hover 背景和信息密度表达。

#### AlertCard — 四态通知（`AlertCard.tsx:57–75`）

四态一律走系统语义令牌软底（浅底 `-3` + 描边 `-line` + 可读深字 `-11`），禁止裸 Tailwind 调色板色：

```
info     → bg-blu-3  border-blu-line  text-blu-11
warning  → bg-amb-3  border-amb-line  text-amb-11
error    → bg-red-3  border-red-line  text-red-11
success  → bg-grn-3  border-grn-line  text-grn-11
```

`--{red|grn|amb|blu}-line` 是浅底卡 1px 边（比 wash 深、比主色浅）。light-only，无 dark mode 变体。

#### 操作反馈分级 — Tooltip / Toast / Callout / AlertCard

| 类型 | 业务语义 | 位置与生命周期 |
|---|---|---|
| Tooltip | 解释单个控件或图标；内容不是完成任务的必要前提 | 跟随控件，悬停或键盘聚焦时显示；不放操作或错误 |
| Toast | 保存成功、校验通过等不阻断当前任务的短暂结果 | 全局唯一 Viewport；桌面视口右下，移动端 safe-area 顶部；success/info 默认 2s，warning/danger 默认 6s |
| Callout | 当前字段、操作或内容区强相关的持续说明、可处理警告或校验错误 | 就地靠近对象，直到条件解除；静态默认不是 live region，异步插入由 `live` 显式声明 |
| AlertCard | 高重要度、多行影响说明、需要明确行动的持续状态 | 位于业务内容层级，不自动消失 |

Toast 只能通过 Design System 导出的 `useToast()` 触发：调用方必须显式传入 `tone` 和可见文案，可选传稳定 `id`、操作、持续时间与 warning/danger 的 `live="assertive"`。禁止根据文案关键词、HTTP 文本或具体业务短语推断 tone。同时最多显示 3 条，超出按到达顺序排队；同 id 更新已有项。悬停、焦点位于 Viewport 内或页面不可见时暂停倒计时。

Toast 的进退场只改变 `transform` 与 `opacity`，方向与 Viewport 一致，并通过 `motion-reduce:animate-none` 停用非必要动效。每条均提供有可访问名称的关闭按钮；success/info 使用 polite status，warning/danger 只在需要立即播报时显式选择 assertive alert。视觉、队列与响应式真组件验收入口位于 `/styleguide` 的 **L2 · Operation Feedback**。

#### Settings Sub-shell Components（V6 设置子壳 · 对齐 `settings.html`）

设置域六视图（空间 `/space` · 成员与角色 `/members` · 连接 `/connector` · 世界观 `/worldview` · 知识 `/knowledge` · 能力 `/skills`，K16 2026-06-11；居中容器/页头共享件 = `components/settings/SettingsView.tsx` 的 `SettingsView`/`SettingsViewHead`）共享一套子壳：

- **浮起浅灰画布 `.gpanel--settings`**：`AppShell` 对 `SETTINGS_PREFIXES`（`/space /worldview /knowledge /connector /skills`）路由套 `bg-[var(--desk)] pb-3 pr-3` 外框 + 内层 `rounded-[14px] border-stone-4 bg-[var(--settings-canvas)] shadow-[var(--sh-panel)]`——白卡浮在浅灰画布上。
- **居中容器 `.pin`**：`mx-auto w-full min-w-0 max-w-[820px] px-8 pb-16 pt-7`（表单/列表型视图）；技能为卡片网格故放宽到 `max-w-[920px]`。
- **视图标题 `.vh__t`**：`text-[21px] font-bold tracking-[-0.02em] text-stone-12`（= `--t-h1`）。需要右侧主操作（如"连接系统"）时同排右对齐。
- **分段切换（K4 反转，2026-06-11）**：页内分段一律 ds line Tabs（滑动下划线，知识 文档/业务准则、成员 状态筛选用它）；`Segmented` 留给控件级小切换（世界观 对象/关系/动作）。原 shadcn pill 变体在设置域页内退役。

**行级令牌（核心约定）：** 落地分两种强度：

- **视觉令牌对齐（默认 · 世界观 / 系统对接）：** 真实页比静态稿功能更全（世界观对象/关系卡可展开看 schema、搜索/分页）。按 CLAUDE.md §13，只把设计稿的配色与形态令牌落到既有结构上，**不裁功能、不把可展开卡降级为扁平行**。
- **严格结构对齐（用户明确"严格对齐"时 · 知识）：** 知识视图按设计稿重写为 `.tlist`（白卡 `rounded-[13px] border-[var(--card-edge)] bg-white px-[18px] shadow-[var(--sh-card)]`）+ `.trow`（`flex items-center gap-3 py-3 border-t border-[var(--line-soft)]`）扁平行：**移除统计卡与搜索框**（数量归入 seg 计数）、文档 7 列表格降为单行、准则可展开卡降为单行，编辑/删除收进行尾 `group-hover` 区。tdesc 描述 + 右对齐 `sh` 操作行（上传文档=primary / 创建准则=outline）。

具体映射：

| 设计类 | 真实落点 | 视觉规格 |
|--------|----------|----------|
| `.spcard` 空间身份卡 | `space/page.tsx` | 50px `rounded-[13px]` 渐变青图标（`from-teal-8 to-teal-10` + `font-display`）+ 名称 + `启用中` 圆点徽标（`grn-3/grn-9/grn-11`）+ 元信息 + 描述 |
| `.mchip` 模块胶囊 | `space/page.tsx` | `rounded-full border-stone-4 bg-white px-3.5 py-1.5 text-[13px] shadow-[var(--sh-xs)]`，已启用 `bg-teal-9` 点 / 未启用 `bg-stone-8` 点 |
| `.appcard` + `.appcard__ico` | `space/page.tsx` `ConnectorSection`（`/connector` `/space` `/platform` 共用真组件 · 数据 `getConnectSystems`） | 系统卡 = `overflow-hidden rounded-[var(--r-lg)] border border-[var(--card-edge)] shadow-[var(--sh-card)]`；头 `.appcard__hd` `bg-stone-2 px-4 py-[13px] gap-[11px]`；图标 36px `rounded-[9px]`（内置 `bg-stone-12` · 外部 `bg-stone-8` · 白 glyph/首字母）；`.atype` 徽标 `rounded-[5px] font-mono text-[10px]` 无边框（内置 `bg-teal-3 text-[var(--accent-ink)]` · 外部 `bg-stone-3 text-stone-9`） |
| `.modrow` + `.modrow__ico` | `space/page.tsx` `ConnectorSection` | 模块行 `bg-white px-4 py-3` + `divide-[var(--line-soft)]` 顶边；图标统一 26px `rounded-[7px] bg-stone-11` 中性深块（白 Phosphor glyph / mono 首字母 · 不用彩虹哈希）+ 名称 + `td`(`rounded-[5px] border-stone-4 bg-stone-3 font-mono text-[10px] text-stone-9`) + 对象 chip + 行动/管理键；禁用行 `opacity-50`。添加模块行 `bg-stone-2 hover:bg-stone-3` |
| `.conn` 连接状态 | connector | `inline-flex gap-1.5 text-[12px]` + 7px 圆点：已连接 `grn9/grn11` · 部分就绪 `amb9/amb11` · 未接入 `stone-8/stone-9` |
| `.trow__sq` 对象前置方块 | `worldview/ObjectTypeList` | `h-[9px] w-[9px] rounded-[2px] bg-teal-9` |
| `.tbadge` 类型徽标 | `worldview/ActionTypeList`（原子/专家/技能/Dify）· `knowledge/GuidelineList`（约束/偏好） | `rounded-full px-2 py-[1px] font-mono text-[10px] font-semibold`，软底：n 灰 `g3/ink-3` · a 青 `t3/accent-ink` · c 琥珀 `amb3/amb11` · b 蓝 `blu3/blu11` |
| `.pri` 优先级 | `knowledge/GuidelineList` | 软底胶囊：关键 `red3/red11` · 高 `amb3/amb11` · 中 `g3/ink-2` · 低 `g3/ink-3` |
| `.vstat` 文档状态 | `knowledge/DocumentStatusBadge` | 7px 圆点 + 文字（无底无框）：待处理 `ink-4/ink-3` · 索引中 `amb9/amb11`（`animate-pulse`）· 已就绪 `grn9/grn11` · 待重建 `red9/red11` |
| `.tlist` 列表白卡 | `knowledge/DocumentTable`、`GuidelineList` | `rounded-[13px] border-[var(--card-edge)] bg-white px-[18px] shadow-[var(--sh-card)]`，内含 `.trow` 行；行尾操作按钮 `opacity-0 group-hover:opacity-100` |
| `.trow__ic` 文档图标 | `knowledge/DocumentTable` | 30px `rounded-[8px]` 彩色方块：PDF/默认 蓝 `blu3/blu11` · Markdown 琥珀 `amb3/amb11`；副行 `类型 · 大小`（mono `text-[11px] text-stone-9`）|

**约束：** 设置视图的徽标/状态一律走上表的软底令牌，禁止裸 `bg-green-50`/`text-amber-600` 等 tailwind 调色板色——保证与三层 canvas、暖灰工作台一致。修改任一设置组件视觉时同步本表。

**V7 设置域增量（2026-06-11 K6）：**

- **边聊边建范式（D6）**：连接/世界观页右缘常驻 `components/settings/CoBuildRail.tsx`（compose ds ChatPanel embedded + MessageBubble + ChatBox，收起 = 窄竖条）；用户描述业务 → 建议物化为左侧「待确认」`CoBuildDraftCard`（AI 草稿与已落库值视觉分明）→ 逐条采纳/忽略，**确认才落库，助手永不静默写库**。
- **成员与角色（/members）**：Linear 式成员表 `components/settings/MembersTable.tsx`（头像/姓名/邮箱/角色下拉行内改/状态），line Tabs 状态筛选，`InviteMembersDialog` 多邮箱 + 角色 + 可复制邀请链接；最简 RBAC 三档 owner/admin/member。
- **能力（/skills）去技术化（A27）**：§一 业务动作 = `CapabilityActionList`（可见不可点开 + 适度反馈：点击就地展开一句简介，不暴露实现）；§二 技能包技术字段收进 `SkillPackageCard` 展开后的次级层。
- 各页接口意图与演示态点名见各路由目录 `INTENT.md`（K10/K15）。

### Chat Components

聊天组件是产品级基础组件，源码位于 `src/components/chat/`。所有聊天输入、消息气泡和完整消息流都复用这组组件，业务页面通过 props 和 slot 注入具体行为。

> **K1 收敛（2026-06-11 · 覆盖下文 ChatBox 旧壳值）**：全站输入框体系 = ds `AskComposer` 一套，`ChatBox` / `ChatInput` / 主题页 composer 都是其同语言变体——壳/光晕/工具行 ds 化：联网搜索 = `ChipToggle`（teal 承诺态）、模型选择 = `Select` quiet 紧凑变体（auto width + truncate；**必有默认值：后端模型目录的 enabled 默认项 → 后端 default_model_id → 第一个 enabled 项**）、发送/停止 = 统一 iconOnly Button（停止 = danger Square）。焦点三态对齐 AskComposer（2026-06-11 三轮·全中性化）：静息 `--sh-card` / hover `--sh-input-focus` / focus-within = `--sh-float` + border-stone-4（无青环青边，颜色只属 aura 云）；transition 只列 box-shadow，border 即时切换；模型弹层 open 期间壳保持聚焦档（forceElevated 同治法）。会话页 composer2 壳 = `--w-chat` / `--r` / `--surface` / --s 系（原 14px 圆角退役）。
>
> **聊天正文**：用户气泡与紧凑状态内容使用 `--t-sm`(13px)；assistant Canonical Markdown 的 `answer` Profile 使用 `--t-body`(14px) + `1.65` 行高，优先保证长文、表格和代码的阅读性；`compact` Profile 继续使用 `--lh-body`(1.55)。

> **Canonical Markdown 排版**：标题按 `--t-h1 / --t-h2 / --t-lg / --t-body` 建立层级并启用平衡换行，只使用字阶、字重和留白，不给普通章节增加分割线或卡片；H1 仅在容器首元素时归零，`hr` 自身承担分隔留白，标题不用内距伪造间隔。`answer` Profile 中作者已用 `strong` 标记的内容，仅其中独立的数值片段使用 Teal 品牌文本令牌和 `tabular-nums` 增强扫读，其余文字继续使用现有加粗层级和中性文本色；未加粗数字与 `compact` Profile 保持原样式，禁止根据业务词、单位、正负号或上下文猜测数值重要性。简单表格自适应容器，真正超宽时只在自身容器横向滚动；代码块保留空白、语法高亮、横向滚动、语言标签和复制按钮；图片保持比例、居中且不超过 `80vh`；列表、任务列表与 blockquote 保持原生文档语义。排版 Profile 只由容器选择 `answer / compact`，禁止根据内容长度或 Markdown 结构决定渲染质量。
>
> **conv__head ds 化**：状态徽章 = ds StatusBadge（active→run / wait_user_input→attn）；产出物/归入主题 = ds Button outline accent sm 丸形 + 自绘计数丸（--icon-sm 盒 / --t-meta 字 / bg-teal-9）；头部节奏 pt --s-4 / pb --s-3。
>
> **ds `ChatPanel` 新增 resizable 模式（K8，主题对象页右栏用）**：指针拖左缘改宽，clamp `[340, min(720, 容器宽−380)]`（容器感知上限防窄视口拖穿左邻）；默认 380（design-px，与 --w-sheet-sm=360 是两条线）；默认位 ±24 磁性吸附（仅指针拖拽，键盘步进 16 只 clamp 不吸附）；双击左缘回默认；键盘 ←/→/Home；手柄 = 8px 命中带（role=separator + aria-value*）+ 内侧 --bw-2 指示线（hover teal-7 / 拖中 teal-9 即时显色无过渡）；拖中 body cursor=col-resize + userSelect:none；元素 `pointerup` / `pointercancel` / `lostpointercapture`、窗口 `pointerup` / `pointercancel` / `blur` 和组件卸载都会恢复全局样式；宽度记组件 state（本会话不持久化），走 inline style（运行时用户值豁免）。

#### `ChatBox.tsx` — 统一聊天输入框

适用范围：全局 Agent 对话、策略编辑对话、经营主题详情策略对话、任务审批侧栏对话。

结构规则：
- 外壳：`rounded-lg border border-stone-4 bg-card p-3`，focus 时只把边框提升到 `border-stone-7`。
- 输入区：`Textarea` 使用透明背景、无边框、无 focus ring，`min-h-8 max-h-[160px] px-0 py-1 text-sm leading-6`，输入内容自动增高。
- 底部行：`mt-3 flex items-end justify-between gap-3`，左侧放工具、引用、附件、辅助提示，右侧放提交或停止按钮。
- 提交按钮（默认带标签）：`h-9 px-3 rounded-md text-sm gap-1.5`，主色 `bg-stone-12 text-white`，禁用态 `bg-stone-3 text-stone-8`。
- 停止按钮：`h-9 px-3 rounded-md text-sm`，使用 destructive 语义色。
- **`iconOnlySubmit` 变体（V6，对齐 `home.html` `.ask__send`）**：纯图标小方钮 `h-[34px] w-[34px] rounded-[10px]`，提交色 `bg-primary text-primary-foreground`（默认 ArrowUp 图标），停止色 destructive；label 仅作 `aria-label`。用于首页 hero ask 这类"极简提问"场景。

slot 规则：
- `leadingAction`：左侧主工具入口，例如加号、附件、引用入口。
- `helper`：引用策略 chip、提示文本、文件 chip 等可换行辅助内容。
- `overlay`：用于 @ 提及高亮等视觉覆盖层。
- `submitIcon` / `submitLabel`：允许不同场景使用「发送」「AI 模式」「发起对话」等业务文案，按钮尺寸保持一致。

约束：
- 不在业务页面重新实现 textarea、发送按钮或停止按钮。
- 不使用大号 CTA、胶囊大按钮或营销式按钮。主按钮默认 36px 高；`iconOnlySubmit` 场景为 34px 方钮（二选一，均由 `ChatBox` 提供，不在页面另写）。
- 不在单个页面写一套局部聊天输入样式；需要新增能力时扩展 `ChatBox` props 或 slot。

#### 会话页视觉（V6，对齐 `case.html`）

会话/聊天界面（`ChatPanel`，全屏页与右侧 `AgentSidePanel` 共用）的 V6 视觉：
- **归档只读态**：深链接打开 `status=archived` 会话时，消息、附件和产物仍可查看/下载；标题前显示中性「已归档」StatusBadge，消息流下方以 stone 软底提示替代 composer 与确认面板，并提供「恢复会话」按钮。恢复成功后原地回到 active 并刷新 Rail；归档当前会话成功则返回新对话首页。
- **浮起面板 `.gpanel--brand`**：会话页（`/chat/[conversationId]`）与首页同一套浮起卡——外层 `bg-[var(--desk)] pb-3 pr-3`（桌面 + 右/下 12px gutter，**顶/左贴边 pt-0**，与左 rail 顶部对齐），内层 `rounded-[14px]` + **品牌画布背景 `background.png`（天蓝，cover/top-center）** + 只往下沉的品牌柔影。消息流的白盒（A2UI 卡）、深色用户气泡与 composer 浮在品牌画布上。会话与首页都用 `gpanel--brand`（对齐 `case.html` 标注；此前误用暖灰 g3 已纠正）。`ChatPanel` 根自身透明。所有浮起面板顶部贴边（与 rail 对齐），不留 10px 间隙。
- **头部 `conv__head`**：`flex px-[22px] py-3.5`，状态徽章（active→「在跟」teal / wait_user_input→「等你审」amber）+ 标题 `text-[15px] font-semibold` + 「归入主题」teal 药丸按钮（Case→Theme，视觉就位，流程待后端）。无底分割线。
- **消息列**：`MessageList` 轨道居中，最大宽度为 `calc(var(--w-chat) + var(--s-6) + var(--s-6))`，纵向留白为 `py-5`；`MessageBubble` 自身保留两侧 `--s-6` 安全边距，因此消息卡、用户消息右边界与 composer 的 `--w-chat` 可见边界严格对齐。窄屏时两者同样各保留一层 `--s-6` 页面边距。
- **消息无头像**（对齐 `case.html`）：`MessageBubble` 外层改竖排——用户右对齐、assistant 左对齐，均不显头像圆圈。
- **用户气泡（`m--me`）**：深色 `bg-primary text-primary-foreground`、无边框、`rounded-2xl rounded-br-md`、`max-w-[80%]`、右对齐，无 who 标签。不再用浅青气泡。
- **系统/Assistant（`m--sys`）**：顶一行 `m__who`（18px **近黑实底 `--ink-strong` + 白色 `BrandLogo`** 方块 + 「Workspace」`text-[11.5px] text-stone-9`）+ 下方纯文本 / 白盒工作卡（A2UI `bg-background` 浮在 g3 面板上）。回答内容显式 `select-text`；稳定完成的回答下方放 28px ghost iconOnly 操作组：复制、赞、踩，`gap --s-1`，静息 stone-8、hover stone-11、反馈选中 teal-11。此前的青色渐变 brand-mark 违「品牌色只一处响 + 禁渐变」已纠正。
- **执行过程 `ExecutionProgress`**：时间线默认保留业务计划、协作和核验步骤；配置型子 Agent 的委派会投影为独立的 `subagent` 协作行，用 Agent 名称和当前状态明确展示，并计入步骤总数，不展示角色提示词、版本或内部标识。连续、同标题且不少于 3 条的 `action` 步骤聚合为一条「业务操作 · N 项」。聚合行露出当前或最近一条明细，点击后展开全部动作明细与各自状态/耗时，展开内容不再重复通用动作标题。
- **右侧 Agent 侧边栏已移除**（`AgentDrawer`/`AgentSidePanel` 不再挂载于 `AppShell`）；会话统一走 `/chat/[conversationId]` 主页面。
- **composer（`composer2`）**：会话页专属（非 `ChatBox`，见 CLAUDE.md §8.1 例外）。居中白卡 `mx-auto max-w-[740px] rounded-[14px] border-stone-3 bg-white shadow-[var(--sh-card)]`；普通聊天 textarea 两行起步，紧凑嵌入场景单行起步，均保持自增高（maxh 120）；同一行工具区承载「本会话」teal 范围 chip 与 32px 方形发送/停止钮（`bg-primary`+ArrowUp / `bg-destructive`+Square）。Enter 发送、Shift+Enter 换行。
- 现场内容卡（落位卡 / Case Brief / 证据卡 / 归入主题）依赖后端数据，暂未实现，待后端契约评估。

#### `MessageBubble.tsx` — 统一消息气泡

**用户气泡（右）**
- 容器: `flex-row-reverse`
- 气泡: `border border-teal-4 bg-teal-2 text-stone-12 rounded-2xl rounded-tr-md px-3.5 py-2`
  - 即 16px 主圆角 + 右上角削角，指向头像方向
- 头像: 24×24px，`bg-teal-2 text-teal-10`

**Assistant 气泡（左）**
- 容器: `flex-row`
- 气泡: 通过 `CardRenderer` 渲染 markdown 或结构化卡片；流式占位使用 `bg-stone-2 text-stone-9 rounded-2xl rounded-tl-md px-3.5 py-2`
- 头像: 24×24px，`bg-stone-2 text-stone-9`
- 流式: 三个跳动圆点动画
- 卡片附挂: 气泡下方 `space-y-2`，渲染 MetricCard / AlertCard / TabsCard 等结构化输出
- 回答内容: 显式允许文本选择；流式结束后显示复制、赞、踩三枚 ghost iconOnly 按钮，复制读取实际渲染文本，赞踩保持互斥选中态

**为什么削单角：** 削向头像方向，让气泡视觉上"贴"住说话人——这是替代尾巴尖（tail）的现代方案，更适合多卡片附挂的混合输出。

#### `MessageList.tsx` — 统一消息列表

- 使用 `ScrollArea` 作为滚动容器。
- 使用 `useConditionalAutoScroll` 管理条件自动滚动。
- 新用户消息出现时强制滚到底部；用户向上查看历史时，不用新 token 抢滚动位置。
- 消息项只通过 `MessageBubble` 渲染，页面不直接排列气泡。

样式维护规则：
- 聊天组件修改必须同步检查全局 Agent 对话、策略编辑对话、经营主题详情策略对话、任务审批侧栏对话。
- 颜色只能使用 Stone / Teal / semantic token，不写散落 hex。
- 聊天组件属于产品业务基础组件，不放入 `src/components/ui/`。

### Inputs & Forms

#### Input（`input.tsx`）

- 高度 36px (`h-9`)，padding `px-3`
- 边框 `border-input` (`--g4`)，radius `rounded-md` = `--r` (7px)
- Shadow: 默认 `shadow-xs`，焦点取消阴影
- Focus ring: 3px ring + 50% 透明度 = `--ring` (`#2DBDA8` Teal-8)
- 占位文字: `placeholder:text-muted-foreground`

#### Textarea

- 同 Input 边框/圆角/ring
- `min-h-16` (64px)，`field-sizing-content`（随内容增高）

#### `.clarify-form-host` — LLM 生成表单的字号归一化

```css
.clarify-form-host { font-size: .875rem; line-height: 1.5; }
.clarify-form-host input, textarea, select, button, label {
  font-size: inherit; line-height: inherit;
}
```

防止浏览器默认 16px 把 LLM 动态生成的 `<form>` 撑变形——这是和"AI 生成的 UI 块"共存必须的卫生措施。

### Navigation

> **V7（2026-06-11）：本节 Header / Sidebar / AppShell 描述的组件已删除**。chrome 现由 ds 件承载：`ds/patterns/shell/{AppShell,TopNav,Rail,WorkSurface}` + `layout/AppShell.tsx`（数据接线）+ `layout/{SpaceMenu,UserMenu}`（ds DropdownMenu）。权威描述见 §0 顶部「V7 Shell 落地」；下文保留作历史参照。

#### Header（`Header.tsx:42–116`）

- 高度 `h-14` (56px)，固定 `sticky top-0 z-40`
- 背景: `bg-white/92` + `backdrop-blur-[16px]` + `backdrop-saturate-[1.6]` —— 半透磨砂
- 描边: `border-b border-stone-4`
- 左: 平台标题 `text-sm text-muted-foreground`
- 右: 用户下拉 + 垂直分割线 `Separator h-4` + Agent 抽屉触发按钮

#### Sidebar（`Sidebar.tsx:60–99`）

- 宽度 **220px** 固定（不可折叠）
- 背景 `--sidebar` (`#FAFAFB`)，右描边 `--sidebar-border`
- 分组小标题: `text-[10px] font-semibold uppercase tracking-[0.06em] text-sidebar-muted`
- 导航项: `flex gap-2.5 rounded-md px-3 py-2 text-[13px]`
- **激活态**（签名手势）:
  - 背景 `bg-sidebar-accent` (`#E0F8F3` Teal-3)
  - 文字 `text-sidebar-accent-foreground` (`#067A6F` Teal-11) + 加粗
  - 图标 `text-teal-11`
  - **左侧 3px 宽 Teal-9 竖条 `rounded-r-full`**——是品牌信号在导航上的固化
- Hover（未激活）: `hover:bg-stone-3 hover:text-stone-12`

#### AppShell（`AppShell.tsx:26–59`）

```
<div class="flex h-screen overflow-hidden">
  <Sidebar/>                                    ← 220px
  <div class="flex flex-1 flex-col">
    <Header/>                                   ← 56px
    <div class="flex flex-1">
      <main class="flex-1 overflow-auto bg-stone-1">{children}</main>
      {agentPanelOpen && <AgentSidePanel/>}     ← 右侧抽屉
    </div>
  </div>
  <PlatformDrawer/>
</div>
```

### Chat Composer（页面组合）

- 完整聊天页：`flex h-screen flex-col`，上方使用 `MessageList`，底部输入区使用 `ChatBox`。
- 内嵌业务对话：用页面容器控制位置和宽度，输入能力仍使用 `ChatBox`。
- 消息列表默认以可读宽度呈现，宽屏业务工作台可由页面容器扩展，但消息气泡仍由 `MessageBubble` 负责。

### Image Treatment

经营产品里图片很少。规则简单：
- 头像 8×8px (`size-8`)，圆形或 rounded（看 Avatar 配置），`bg-muted` fallback
- 没有 hero 摄影；没有插画系统
- 图标统一 **Phosphor**（`@phosphor-icons/react`），常见尺寸 16/20/24px；权重统一 Regular（不用 Bold / Duotone，避免 faux-bold）
- 图标颜色跟随父级文字色，不单独着色

### 签名表面类（`globals.css:235–298`）

- **`.card-soft`** — 业务卡片白纸（见上）
- **`.brand-bar`** — 左侧 3px Teal `--t9` 全高竖条，用 `::before` 生成；标记"系统正在主动展示 / 重要"
  ```css
  .brand-bar::before {
    content:''; position:absolute; top:0; left:0;
    width:3px; height:100%; background:var(--t9);
  }
  ```
- **`.alive-surface`** — Teal 6% 到画布 70% 的 135° 渐变 + Teal 15% 描边；唯一渐变面
- **`.num-link`** — Teal-7 虚线下划线 + 加粗近黑文字；可点击数字的轻量交互暗示
- **`.nums-display`** / **`.pg-title`** / **`.pg-sub`** — 排版三件套（见 §3）

## 5. Layout Principles

### Spacing

间距走 `--s-*` 生成式刻度（`globals.css` · base 4px）。**只用这些档，不写散值。** 生成规则：`--s-1=4px` 为 base，小端线性 ×4（4/8/12/16/20/24）、大端跳档（32/48/64）控令牌数；全偶数贴像素格（1.5× DPI 不糊）。

| Token | px | 典型用法 |
|-------|-----|----------|
| `--s-1` | 4px | 极紧内联 |
| `--s-2` | 8px | 按钮内 icon-text |
| `--s-3` | 12px | 字段间 / gutter |
| `--s-4` | 16px | 卡片内默认 |
| `--s-5` | 20px | 块间距 |
| `--s-6` | 24px | 区块间距 |
| `--s-7` | 32px | 容器纵向分区 |
| `--s-8` | 48px | 大留白 |
| `--s-9` | 64px | 页级顶部留白 |

序列 `4/8/12/16/20/24/32/48/64` 严格单调（修了两处真漏点：`--s-5` 22→20 离格半像素糊；删原 `--s-8=72` 手搓逃逸阀致 `--s-8>--s-9` 倒序 bug）。消费面为 styleguide 专属，改值不波及 `[locale]` 团队页。

### Grid & Container

- Dashboard 容器: `mx-auto max-w-[1440px] p-8 space-y-5`
- Dashboard 双列: `grid gap-5 md:grid-cols-2`（768px 以下退回单列）
- MetricCard: `grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4`
- 聊天消息: `max-w-3xl mx-auto`（约 672px）——可读宽度，避免过宽行

### 留白哲学

不用分割线分隔——靠**画布颜色 + 卡片浮起 + 间距**自然分组。BlockFrame 的内部行用 `divide-y divide-stone-3` 是唯一普遍的分隔线，**颜色用 Stone-3 (`#F1F2F3`)** 保证存在感几乎为零。

### Border Radius Scale

> 2026-06-05 收口：单一阶梯 `--r-*`（5/7/10/12，对齐设计真源 `tokens.css §4.1`）。shadcn 圆角链 `--radius-{sm,md,lg,xl,2xl,3xl}` 已统一改引 `--r-*`，**超圆角 `2xl`/`3xl` 封顶 12**——消除原 `--radius`(8px) 第二套系统。
>
> ⏸ **DEFERRED**（不改现值）：foundations-research 建议把 `--r-sm/--r/--r-lg` 收成单旋钮派生 `12/8/6`（5/7 两值一职、更贴格）。本块**不动**，因 `--r-sm/--r/--r-lg` 已被 301+ 团队 `rounded-*` 用法（经 `@theme --radius-*`）+ 多个 `[locale]` 页 `var(--r-*)` 直引消费——收档要跨 301 消费点 codemod，churn 共享层。留迁移期带 codemod 统一对齐，现值保持 5/7/10/12。

| 值 | 令牌 / 类 | 用途 |
|----|------|------|
| 5px | `--r-sm` / `rounded-sm` | chip、badge、tag 等小控件 |
| 7px | `--r` / `rounded-md` | 按钮、输入框、Sidebar 项 |
| 10px | `--r-lg` / `rounded-lg` / `.card-soft` | 卡片与输入框 |
| 12px | `--r-xl` / `rounded-xl`（及 `2xl`/`3xl` 封顶）/ `--r-stage` | 面板 / 浮层 / 气泡 / 主舞台 |
| Full | `--r-pill` / `rounded-full` | 头像、胶囊 |

**铁律：容器一律 12，不再出现 13/14/16；无超圆；无完全方角**（0 半径不存在于品牌词典）。聊天气泡主圆角 12 + 被削单角 `rounded-br`。

### Motion（动效）

时长走 `--dur-*` 生成式刻度（`globals.css` · base 100ms），按"移动距离 / 打断程度"派生（非线性，大动作更慢）。进出不对称（MD3）：入场减速到静止、离场加速消失、原位变化用标准 in-out。

| Token | 值 | 用途 |
|-------|-----|------|
| `--dur-1` | 100ms | 微：hover / focus / 变色 |
| `--dur-2` | 180ms | 默认：下拉 / tooltip / segmented |
| `--dur-3` | 280ms | 中：抽屉 / popover / 手风琴 |
| `--dur-4` | 400ms | 大：modal / 页转场 |
| `--dur` | = `--dur-2` | 旧名别名（back-compat） |
| `--ease` | `cubic-bezier(.32,.72,0,1)` | 标准 in-out（原位变化） |
| `--ease-out` | `cubic-bezier(0,0,0,1)` | 进：减速到静止 |
| `--ease-in` | `cubic-bezier(.3,0,1,1)` | 出：加速离场 |

**`@media (prefers-reduced-motion: reduce)`** 把 `--dur-1..4` + `--dur` 全归零（0.01ms）——尊重系统"减少动态"偏好，位移/缩放停、淡入淡出保留。

### z-index（`--z-*`）

base-100 语义尺，按"打断用户程度"排，步进 100 留插空（防 `z:99999` 军备竞赛）。

| Token | 值 | Token | 值 |
|-------|-----|-------|-----|
| `--z-base` | 0 | `--z-modal` | 400 |
| `--z-sticky` | 100 | `--z-popover` | 500 |
| `--z-dropdown` | 200 | `--z-toast` | 600 |
| `--z-scrim` | 300 | `--z-tooltip` | 700 |

### Breakpoints（`--bp-*`）

桌面工作台功能阈值，按"该宽度布局做什么"命名（rem 随 14px 根缩放）。

| Token | 值 | 等效 px | 含义 |
|-------|-----|---------|------|
| `--bp-collapse` | 61.25rem | 980px | 轨 / 面板收起 |
| `--bp-wide` | 90rem | 1440px | 舒适双栏 |
| `--bp-ultra` | 120rem | 1920px | 三栏 / 封顶居中 |
| `--bp-cinema` | 160rem | 2560px | 居中封顶，别拉长行宽 |

### Border Width（`--bw-*`）

base 1px 语义，按职能取（跳 1.5px 渲染不一致）。

| Token | 值 | 职能 |
|-------|-----|------|
| `--bw-1` | 1px | 结构：分隔 / 输入 / 卡 / 表格 |
| `--bw-2` | 2px | 状态：focus 环 / 选中 |
| `--bw-4` | 4px | 标记：左轨状态条 / 激活 tab |

### Opacity（`--op-*`）

按职能取的不透明度，非线性（对齐 MD3 state-layer：hover ~8% / press ~12%）。

| Token | 值 | 用途 |
|-------|-----|------|
| `--op-disabled` | .40 | 禁用态 |
| `--op-muted` | .62 | 弱化前景 |
| `--op-hover` | .08 | hover 状态层 |
| `--op-press` | .12 | press 状态层 |
| `--op-scrim` | .50 | 遮罩 |

### Category（`--cat-1..6`）

**dataviz 层 ONLY——绝不进 chrome / nav。** 生成式：`--cat-1` 锚 `--h-accent`，其余按 OKLCH **+60° 等距旋转**，固定保守 `--cat-L .65` / `--cat-C .13`（所有 hue 都 in-gamut，避高彩 hue 溢出 sRGB 致 gamut-map 后偏移/发灰）。`@theme` 映射 `--color-cat-1..6`（enable `bg/text/border-cat-N`）。**改 `--h-accent` 一处 → 整环 hue 同步旋转、重新和谐**（正答"客户有自己品牌色怎么办"）。

| Token | hue 偏移 | ≈ 色相 |
|-------|---------|--------|
| `--cat-1` | +0 (锚 `--h-accent`) | ≈186 teal |
| `--cat-2` | +60 | ≈246 蓝 |
| `--cat-3` | +120 | ≈306 品红 |
| `--cat-4` | +180 | ≈6 红 |
| `--cat-5` | +240 | ≈66 琥珀 |
| `--cat-6` | +300 | ≈126 绿 |

封顶 6 类 = 色盲安全的定性编码上限；第 7+ 换形状 / 图案 / 直标，不再加色。

## 6. Depth & Elevation

四档阴影（`globals.css:119–123`），全部用暖灰 `rgba(33, 32, 28, α)`：

| 变量 | 配方 | 用途 |
|------|------|------|
| `--sh-xs` | `0 1px 2px rgba(33,32,28,.05)` | 默认 `.card-soft` / Input |
| `--sh-sm` | `0 1px 3px rgba(33,32,28,.06), 0 1px 2px rgba(33,32,28,.04)` | 卡片 hover / shadcn Card 默认 |
| `--sh-md` | `0 4px 6px -1px rgba(33,32,28,.07), 0 2px 4px -1px rgba(33,32,28,.04)` | Popover / Dropdown |
| `--sh-lg` | `0 10px 15px -3px rgba(33,32,28,.08), 0 4px 6px -2px rgba(33,32,28,.04)` | Dialog / Sheet 抽屉 |

**阴影哲学：** 暖灰双层叠加（≤8% alpha）模拟"室内漫反射 + 微方向光"，从不出现单层重投影。从 xs 到 lg 是**层级序列而非戏剧性差异**——hover 只走一档（xs→sm）。

### 装饰性深度

- **没有渐变体系**（除 `.alive-surface` 一处例外）
- 色块对比承担"深度感"——白卡片浮在 Stone-1 上、Sidebar 比主区暗一档
- 聊天气泡靠**形状**（削角不对称）建立左右关系，不靠阴影

## 7. Do's and Don'ts

### Do
- 用 Stone-1 (`#FCFCFD`) 做主画布、Stone-2 (`#FAFAFB`) 做 Sidebar——比纯白暖一档是签名底色
- Teal `#0C9488` 留给"系统状态信号"：CTA accent、Sidebar 激活条、`.brand-bar`、`.num-link`、focus ring
- 主操作按钮用近黑 (`--primary` `oklch(20% .006 H)`) 而不是 Teal——Teal 是"系统在工作"，黑是"用户在操作"
- 卡片优先用 `.card-soft`（白纸 + Stone-4 描边 + xs 阴影 + hover 升一档）
- KPI 数字用 `.nums-display` (800 / `-0.04em` / tabular-nums) 或 `tabular-nums` 避免数字跳动
- 聊天气泡用 16px 圆角 + 削向头像方向的单角——这是品牌的对话手势
- 聊天输入框统一使用 `ChatBox`，按钮保持 36px 高，不做大号 CTA
- Sidebar 激活态必须三件套同时出现：Teal-3 底 + Teal-11 文字 + 左 3px Teal-9 圆角竖条
- 阴影叠两层，从 xs / sm / md / lg 四档里挑——不要写自定义 box-shadow
- 暗色模式只翻转 shadcn 语义 token；Stone/Teal 不变
- 中文 fallback 链显式写出（`PingFang SC` / `Hiragino Sans GB` / `Microsoft YaHei`）

### Don't
- 不要用纯白 `#FFFFFF` 做画布——只能做卡片；画布必须暖一档
- 不要把 Teal 当通用 accent 撒到所有地方——它是品牌信号不是装饰
- 不要新增第二品牌色或品牌渐变——`.alive-surface` 是唯一的渐变特例
- 不要给按钮加 `transform: scale(0.95)` 之类的弹性反馈——本系统按下只换色（`/90` alpha）
- 不要把数字段落用普通 `font-sans`——会跳；至少加 `tabular-nums`
- 不要用纯黑 `#000` 做正文——`--foreground` 是 `#1F1F23`，配暖画布更柔
- 不要在主聊天流里混 serif / script / emoji 装饰字体——系统只有 Funnel Sans / Funnel Display + JetBrains Mono
- 不要在卡片间加分割线 `<hr>`——靠间距和卡片浮起分组；BlockFrame 内行用 `divide-stone-3` 是唯一例外
- 不要用 `rounded-3xl` 或更大的圆角——12/16px 是上限
- 不要写自定义 box-shadow——用 `--sh-xs/sm/md/lg` 四档
- 不要在 `<form>` 里依赖浏览器默认 16px 字号——给容器加 `.clarify-form-host`

## 8. Responsive Behavior

### Breakpoints

Tailwind 默认四档；本系统主要在 `md` (768px) 和 `lg` (1024px) 切布局：

| 名称 | 宽度 | 关键变化 |
|------|------|----------|
| 默认 (mobile) | < 640px | Sidebar 应隐藏（当前为固定 220px，移动端待优化）；Dashboard 单列；MetricCard 2 列 |
| sm | 640px+ | MetricCard 3 列 |
| md | 768px+ | Dashboard 进入 2 列网格 (`md:grid-cols-2`) |
| lg | 1024px+ | MetricCard 4 列 |
| xl / 2xl | 1280px / 1536px | 不显式切；靠 `max-w-[1440px]` 容器收口 |

### Touch Targets

- 默认按钮 36px (`h-9`) ≥ Material 推荐的最小可点高度，但**低于 WCAG AAA 的 44px**——移动端使用时需要外层 padding 兜底
- `xs` 24px 按钮仅用于密集 toolbar 内嵌，不应作为主操作
- Input / Textarea 36px / 64px 最小高度——满足主流触屏阈值
- Sidebar 项目 `py-2` (~7px) + `text-[13px]` ≈ 33px 高——桌面优先，移动端需要扩高

### Collapsing Strategy

- **Dashboard 网格** `md:grid-cols-2` —— 768px 以下退回单列堆叠
- **MetricCard** `2 → 3 → 4 列` 阶梯
- **Sidebar 当前固定 220px**——移动端策略未来需补（侧滑抽屉 / Sheet）
- **聊天 `max-w-3xl mx-auto`** 居中容器——窄屏自动占满
- **Header 不变高**（始终 56px）——简化心智模型

### Image Behavior

- 头像（用户/Assistant 24×24px）按比例缩放，不裁剪
- 没有 hero 图 / 没有 carousel
- 图标走 Phosphor SVG，尺寸跟随文字大小

## 9. Agent Prompt Guide

### Quick Color Reference

- 主画布: "Stone-1 (`#FCFCFD`)"
- 卡片表面: "White (`#FFFFFF`)"
- Sidebar 底: "Stone-2 (`#FAFAFB`)"
- 主前景文字: "Stone-12 (`#1F1F23`)"
- 二级文字 / 副标题: "Stone-9 (`#8B8B90`)"
- 强调文字 / muted-foreground: "Stone-11 (`#605F66`)"
- 描边: "Stone-4 (`#ECEDEF`)"，hover 升 "Stone-6 (`#D8D9DD`)"
- 主操作按钮: "Primary `oklch(20% .006 H)` 近黑微冷 + 白字（非纯黑、非青）"
- 品牌 accent / 激活态: "Teal-9 (`#0C9488`)"
- Sidebar 激活底 / 激活字 / 激活条: "Teal-3 `#E0F8F3` / Teal-11 `#067A6F` / Teal-9 `#0C9488`"
- Focus ring: "Teal-8 (`#2DBDA8`)，3px 50% 透明度"
- 错误 / destructive: "Red-9 (`#E5484D`)"
- 成功: "Green-9 (`#30A46C`)"
- 警告 / attention: "Amber-9 (`#FFC53D`)"
- 信息: "Blue-9 (`#3B82F6`)"
- assistant 气泡背景: "Stone-3 (`#F1F2F3`) / `--muted`"
- user 气泡背景: "近黑微冷 `oklch(20% .006 H)` / `--primary`"

### Example Component Prompts

1. "做一个 Workspace 主操作按钮 — 近黑微冷 `--primary` (`oklch(20% .006 H)`) 背景、白字、`text-sm font-medium` (12.25px / 500)、Funnel Sans 字体、`rounded-md` = `--r` (7px)、高度 36px、padding `px-4`。Hover 走 `bg-primary/90`。Focus ring 用 Teal-8 `--t8` 3px / 50% alpha。**不要**加 `scale(0.95)` 弹性。"

2. "做一个业务卡片 `.card-soft` — 白底、`1px solid #ECEDEF` (Stone-4) 描边、`border-radius: 12px`、阴影 `0 1px 2px rgba(33,32,28,.05)` (`--sh-xs`)、`transition: all .15s ease`。Hover：描边升到 `#D8D9DD` (Stone-6)、阴影升到 `--sh-sm`。卡片浮在 Stone-1 (`#FCFCFD`) 主画布上。"

3. "做一个 Sidebar 导航激活项 — 父容器宽 220px，背景 `--g2` (Stone-2)；激活项 `bg-teal-3`、文字 `text-teal-11` 加粗、图标 `text-teal-11`、`rounded-md` = `--r` (7px)、padding `px-3 py-2`、字号 13px；**左侧绝对定位 3px 宽 Teal-9 (`#0C9488`) 圆角竖条 `rounded-r-full` 全高**。Hover（未激活）走 `bg-stone-3 #F1F2F3`。"

4. "做一个聊天气泡对 — 使用 `src/components/chat/MessageBubble.tsx`。User 气泡（右）：`border-teal-4 bg-teal-2 text-stone-12`、`rounded-2xl rounded-tr-md`、`px-3.5 py-2`、行高 1.5。Assistant 气泡（左）：markdown 和结构化输出统一走 `CardRenderer`，流式占位用 `bg-stone-2 text-stone-9 rounded-2xl rounded-tl-md`。两侧头像为 24×24px。"

5. "做一个 KPI MetricCard — 白底 (`bg-card`)、`rounded-lg` (8px)、`border` (`#ECEDEF`)、`p-4 space-y-3`。标题 `text-sm font-medium`。下方网格 `grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4`，每项：label `text-xs text-muted-foreground` (`#605F66`)、数值 `text-xl font-semibold tabular-nums` (17.5px / 600 / 等宽)、单位 `text-xs text-muted-foreground`。趋势箭头：上 Green-9 `#30A46C`、下 Red-9 `#E5484D`、平 Stone-9 `#8B8B90`。"

6. "做一个 Dashboard BlockFrame — 用 `.card-soft` 外壳。Header `flex items-center justify-between px-5 py-4 border-b border-stone-4`，左侧 icon (`h-4 w-4`) + 标题 `text-sm font-semibold`，右侧槽位放按钮/筛选器。内容区用 `divide-y divide-stone-3` 分行项目（`#F1F2F3` 极淡分割线）。支持三态外壳：loading（骨架）/ empty（居中提示）/ error（用 `tone='destructive'` 把 header 背景换 Red-3 `#FFEFEF`）。"

7. "做一个 AlertCard 四态 — 一律走系统语义令牌软底（禁裸 Tailwind 调色板色）。info：`bg-blu-3 border-blu-line text-blu-11` + ℹ 图标。warning：`bg-amb-3 border-amb-line text-amb-11` + ⚠。error：`bg-red-3 border-red-line text-red-11` + ⚠。success：`bg-grn-3 border-grn-line text-grn-11` + ✓。圆角 `rounded-lg` = `--r-lg` (10px)、padding `p-4`、左侧 icon 占 `h-5 w-5`。"

8. "做一个 AppShell 框架 — 最外 `flex h-screen overflow-hidden`。左侧 Sidebar 220px 固定 (`#FAFAFB` 底 + `border-r border-#ECEDEF`)。右侧主区垂直栈：Header (`h-14` = 56px、`bg-white/92 backdrop-blur-[16px] backdrop-saturate-[1.6]`、`border-b border-stone-4`、`sticky top-0 z-40`)；下方 main `flex-1 overflow-auto bg-stone-1`，内容容器 `mx-auto max-w-[1440px] p-8 space-y-5`。可选右侧 AgentSidePanel 抽屉。"

9. "做一个 `.brand-bar` 强调卡片 — 任何 `position: relative; overflow: hidden` 的容器，加 `::before { content:''; position:absolute; top:0; left:0; width:3px; height:100%; background:#0C9488; }`——左侧 3px Teal 全高竖条。用于经营简报里的"系统主动告知"块。卡片本身仍用 `.card-soft` 白底 12px 圆角。"

10. "做一个 ChatBox 输入框 — 使用 `src/components/chat/ChatBox.tsx`。外壳 `rounded-lg border border-stone-4 bg-card p-3`，Textarea `min-h-8 max-h-[160px] border-0 bg-transparent px-0 py-1 text-sm leading-6`，底部行 `mt-3 flex items-end justify-between gap-3`。提交按钮 `h-9 px-3 rounded-md text-sm bg-stone-12 text-white`，禁用态 `bg-stone-3 text-stone-8`。业务引用、附件、提示放入 `leadingAction` / `helper` / `overlay`。"

### Iteration Guide

迭代已生成的 Workspace 屏幕时：
1. 先确认色板分工：**黑 = 用户操作；Teal = 系统状态；Stone = 一切表面与文字**——任何 Teal 滥用都是味道
2. 卡片只走 `.card-soft` 或 shadcn `Card`——不要写新阴影
3. 数字必须 `tabular-nums`；大数字用 `.nums-display`
4. 不要引入新字体——只有 Funnel Sans / Funnel Display + JetBrains Mono
5. 不要写自定义 hex——查 `--g*` / `--t*` / 语义 `--red9` 等 12 阶
6. 阴影从 xs/sm/md/lg 四档里挑——不要写新值
7. 圆角只用 `--r-*` 四档 5/7/10/12 (+ `--r-pill`)；超过 12 是错的（容器封顶 12，无超圆）
8. 暗色模式不要改 Stone/Teal——只让 shadcn 语义 token (`--background`, `--card`, `--muted`) 经 oklch 翻转
9. 中文段落必须显式给中文 fallback；不要假设浏览器会"自动选好"
10. AI 生成的动态 `<form>` 一律包 `.clarify-form-host` 防字号穿透
11. 聊天输入、消息气泡和消息列表一律复用 `ChatBox` / `MessageBubble` / `MessageList`

### Known Gaps

- **Sidebar 移动端策略未定**：当前 220px 固定；< 768px 时需要切换为 `Sheet` 抽屉（已具备 shadcn 组件）
- **按钮 36px < WCAG AAA 44px 触屏阈值**：移动端需在容器层补 padding 或临时换大尺寸
- **没有 carousel / hero 图 / 插画系统**：当前产品形态不需要；未来加入"模板市场 / 案例展示"时需补图像规范
- **`.alive-surface` 是孤立的渐变特例**：是该全局收紧"无渐变"原则、还是承认它为正式 token 待决
- **暗色模式下 Teal-3 `#E0F8F3` Sidebar 激活底**没有重写，对比度可能偏低；需评估
- **图表组件**（recharts）的轴/网格颜色未抽象 token——目前直接用 Stone 系列硬编码
- **空态 / 错误态插画**未建立——当前 BlockFrame 只用文字 + 图标，未来需视觉资产规范
- **国际化字体权重**：英文 Funnel Sans 800 在中文 fallback 链下未必有对应字重（PingFang 只到 600），大数字在中文环境会降级

## 10. UX Refactoring Principles

本章节定义 Workspace 页面重构时的判断原则。它用于设计评审、前端实现和后续页面改造，目标是让所有页面共享同一套信息结构、视觉权重和交互语义。

### Information Ownership

每类信息必须有明确归属，避免同一信息在多个区域重复出现。

- **Header**：只表达当前页面上下文，包括页面标题和必要的短副标题。
- **KPI**：只表达系统事实，例如总量、当前系统状态和静态统计结果。
- **Toolbar**：表达当前视图控制，包括搜索、筛选、刷新、新建和视图切换。
- **List**：表达当前命中的数据集合。
- **ListCard**：表达单个对象的标题、元数据、描述和必要状态。
- **Detail / Dialog / Drawer**：承载完整信息、编辑、删除、审批和其他高成本操作。

页面标题、品牌名、日期、状态和说明文案只在最合适的位置出现一次。重复出现通常意味着页面的信息架构需要重排。

### User-facing Copy Rules

界面上的可见文案必须对用户当前任务有直接意义，至少表达以下一类信息：当前对象或任务、已发生的状态、操作的影响与风险、用户需要采取的下一步。

- 禁止把布局变化、实现方式、系统中间过程或开发者视角写成可见说明，例如“在更宽的空间中编辑”、“此处将调用某组件”。
- 禁止用说明文案重复界面已经自解释的内容；标题、字段名和明确的操作按钮足以说明任务时，不再补一句“你可以在这里……”。
- 必须说明时，优先写结果、影响、风险或下一步，不写系统如何实现它。
- 辅助技术所需的标签与说明仍必须具有用户语义；仅当它不应增加视觉密度时使用 `sr-only`。

### KPI Rules

KPI 表达系统事实，不表达当前视图状态。

- KPI 的主数字不能随搜索、筛选、分页、排序等视图控制变化，除非 KPI 本身定义为“当前视图指标”。
- 当前筛选结果、搜索命中数和分页范围属于 Toolbar 或列表区域。
- KPI 文案使用名词或短语，不写完整说明句。
- KPI 不承载操作按钮，不承载筛选状态，不解释筛选条件。
- KPI 数字使用 `.nums-display` 和 `tabular-nums`，字号与 Dashboard KPI 保持一致。

示例：

- 正确：`已加载技能 13`
- 正确：工具区显示 `筛选 7`
- 错误：筛选后把 `已加载技能` 从 `13` 改成 `7`
- 错误：KPI 右侧显示 `已启用 2 个筛选条件`

### Toolbar Rules

Toolbar 是当前列表或视图的控制区，承载用户对当前集合的操作。

- 搜索框常驻在左侧，适用于名称、编码、描述等直接查找路径。
- 复杂筛选收进 Popover，避免多个 Select 横向铺开。
- 筛选按钮可以显示当前命中结果数，用于回应用户“筛选后剩多少”。
- 新建按钮靠近列表工具区，使用降级样式，除非它是页面唯一主任务。
- 刷新按钮默认降级；需要实时性的页面优先自动刷新，不把刷新心智负担转移给用户。
- 视图切换放在它影响的内容上方，不和 KPI 混在一起。

搜索和筛选共同决定列表结果；它们不影响系统事实类 KPI。

### List Card Anatomy

列表卡片采用稳定的三层结构。

1. **Title Row**：对象名称、主要状态、标题级徽标和右侧轻量信息。
2. **Meta Row**：来源、时间、类型、系统、模块等辅助信息。
3. **Description Row**：自然语言描述、当前进度、说明文本。

样式规则：

- 标题使用 `h3`，基础样式为 `text-[15px] font-semibold leading-5 text-foreground`。
- 标题行与下方内容保持固定间距，避免元数据获得与标题相同的视觉权重。
- 元数据区使用 `text-xs text-muted-foreground`，项之间统一使用 `·` 分割。
- 当元数据内部本身存在层级关系时，使用 `/`，避免和元数据分割点冲突。
- 描述区使用 `text-sm text-muted-foreground`。
- 列表卡片默认 `rounded-lg border border-stone-4 bg-card`，hover 升级边框到 `stone-6`，不新增阴影。

### Interaction Rules

交互方式必须在同类页面中保持一致。

- 普通列表项点击进入详情、弹窗或抽屉。
- 编辑、删除、审批等高成本操作进入详情层级，避免列表里铺满按钮。
- 可展开列表使用 `ExpandableListCard`，普通列表使用 `ListCard`。
- 同一页面内如果一个列表采用 hover 或展开操作，其他同类列表应保持一致。
- 按钮只在用户需要立即执行动作时出现；仅用于“导航到详情”的按钮通常可以由整卡点击替代。

### Color Semantics

颜色服务语义，不服务装饰。

- **Teal**：品牌、系统关注、激活态、可用的正向系统信号。
- **Red**：失败、错误、危险、破坏性操作。
- **Amber**：等待、警告、需要注意。
- **Green**：完成、成功、健康。
- **Stone**：默认文本、表面、边框、普通元数据。

同一种颜色不能在同一页面里同时表达无关含义。状态色不能用于装饰性区分，否则会削弱用户对风险、成功和等待的判断。

### Density Rules

信息密度由任务类型决定。

- **扫描型页面**：提升密度，突出列表、状态和数量，例如经营简报、任务动态。
- **阅读型页面**：保留高度和行距，避免长描述压缩，例如技能管理。
- **审批型页面**：突出标题、状态、提交时间和等待时长，审批动作进入详情。
- **配置型页面**：减少装饰，突出字段归属、分组和当前配置状态。

密度不是越高越好。页面应先判断用户任务是“找”“看”“读”“审”还是“配”，再决定卡片高度和信息展开程度。

### Anti-patterns

以下情况应在 UX review 中优先处理：

- 页面内重复标题。
- KPI 随搜索或筛选变化。
- 说明文案解释页面已经自解释的内容。
- 列表项标题、元数据、描述混在同一视觉层级。
- 列表里铺满“查看详情”“编辑”“删除”等按钮。
- 状态被重复表达，例如呼吸点和徽标同时表达同一状态。
- 颜色只用于装饰，或同一颜色表达多种语义。
- Card 阴影、圆角、边框风格在不同页面随机变化。
- 筛选器横向堆叠，挤压搜索和新建。
- 元数据分割符不统一。
- 按钮、图标或日期脱离正文容器对齐。

### UX Review Checklist

评审页面时按以下顺序检查：

1. 页面是否有重复标题或重复品牌信息？
2. KPI 是否只表达系统事实？
3. 搜索、筛选、刷新、新建是否位于 Toolbar？
4. 筛选结果是否作为当前视图状态，而不是 KPI 状态？
5. 列表项是否清楚区分标题、元数据和描述？
6. 元数据是否统一使用分割点？
7. 状态颜色是否具有稳定语义？
8. 卡片圆角、边框、阴影和 hover 是否符合系统规则？
9. 操作按钮是否只在必要层级出现？
10. 页面密度是否符合当前用户任务？
11. 复杂筛选是否收进 Popover？
12. 用户是否能一眼理解当前页面最重要的信息？

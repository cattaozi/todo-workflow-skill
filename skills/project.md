# skills/project —— 我怎么初始化项目域和挂载外部资源

> `projects/` 是 luca 的项目域：放一套账本、项目域总览、长期记忆、用户原始材料、交付产物和项目域脚本。外部项目、源码仓、资料目录通过软链挂到 `projects/links/`。壳仓不收编项目域数据；项目域默认由 `projects/` 自己的本地 git 管理，`projects/links/` 保持可发现，方便 IDE / Git 识别外部仓。

## 什么时候读我

当任务涉及下面情况时读我：

- 第一次把一组外部目录交给 luca 管。
- 需要把多个文件目录地址软链引入。
- 需要把外部资源的启动方式落成项目域启动文件。
- 需要启动、停止、重启或检查项目域记录的本地服务。
- `projects/` 缺失、结构不完整或边界不清。
- `projects/` 已存在但还不是独立 git 仓。
- 需要判断某个文件属于壳仓、项目域，还是外部资源。
- 需要创建、修正、解释项目域结构。

## 我负责什么

- 定义引入项目时生成的最小项目域结构。
- 创建项目域目录和入口文件。
- 初始化 `projects/` 自己的本地 git 仓。
- 将用户提供的外部目录软链到 `projects/links/`。
- 将外部资源移出 luca 的项目域管理。
- 从外部目录的 README、脚本和配置里识别功能、启动方式、停止方式，并写入 `projects/README.md`。
- 维护项目域启动文件 `projects/scripts/dev-services.sh` 的位置、命令形态和日志位置。
- 规划 luca 交付产物的落点 `projects/outbox/`。
- 让 `README.md` 的服务定义和启动文件保持一致。
- 维护三层边界：壳仓、项目域、外部资源。
- 说明各目录职责。

## 我不负责什么

- 不替代 `todo / prd / explore` 的具体推进规则。
- 不定义 `todo / prd / explore` 的账本字段和表结构。
- 不把 `README.md` 扩展成独立工作流。
- 不把 `memory/` 变成项目总览的替代品。
- 不规定外部项目怎么写代码、测试、构建或部署。
- 不规定 `dev-services.sh` 的内部实现模板；脚本内容由我根据当前服务和外部资源实际情况编写。
- 不把 `projects/` 生成物提交进 luca 壳仓。

## 生成结构

```text
projects/
├── .gitignore
├── README.md
├── inbox/
├── outbox/
├── links/
│   ├── app-a -> <外部目录 A>
│   └── app-b -> <外部目录 B>
├── scripts/
│   └── dev-services.sh  # 有本地长期服务时生成
├── todo/
│   ├── index.md
│   └── epic/
│       └── <slug>.md  # 有 Epic 时生成
├── prd/index.md
├── explore/index.md
├── memory/README.md
├── log/
└── room/
    └── dashboard.html  # 按需生成
```

这些文件和目录都在引入外部资源时动态生成，不属于 luca 壳仓资产；壳仓只保留 `projects/.gitkeep` 作为挂载点。项目域默认初始化为独立本地 git 仓，用来查看、提交和回滚账本变化，同时让 `projects/links/` 保持可发现。

职责：

- `links/`：外部资源软链区；用户提供多个目录地址时，统一软链到这里。
- `inbox/`：用户给我的原始材料库，只收用户提供的文件、会议纪要、截图说明、路径说明或其它原件；可以长期保留，入库后不清空。
- `outbox/`：我交付给用户的生成产物库；图片、文档、导出文件和其它可交付成果放这里。
- `README.md`：项目域总览；记录外部资源、人话理解、服务定义、协作约定和待确认事项。
- `scripts/`：项目域脚本区；`dev-services.sh` 是本地长期服务的统一启动文件。
- `todo/`：TODO 总台账、TODO 详情和 Epic 说明文件；具体格式由 `skills/todo.md` 定义。
- `prd/`：需求账本目录；具体格式由 `skills/prd.md` 定义。
- `explore/`：想法和预研账本目录；具体格式由 `skills/explore.md` 定义。
- `memory/`：长期经验与防复发记忆库；组织与召回规则由 `CLAUDE.md` 定义。
- `log/`：我生成的过程草稿和临时沉淀；收尾时要蒸馏或清掉。
- `room/`：给用户看的展示层；`dashboard.html` 从本体、项目域和账本渲染当前状态，我不读回。

## 入口文件内容来源

`project` 只负责编排初始化，不拥有各入口文件的内容格式。生成入口文件前，先读对应真相源：

- `README.md`：本文件定义初始空壳；后续只写项目域总览、服务定义、协作约定和待确认事项。
- `scripts/dev-services.sh`：本文件定义启动文件位置、对外命令形态和日志位置；脚本实现由我按当前服务定义和外部资源实际情况生成。
- `todo/index.md`：读 `skills/todo.md`。
- `todo/epic/<slug>.md`：读 `skills/todo.md`；有 Epic 时再创建。
- `prd/index.md`：读 `skills/prd.md`。
- `explore/index.md`：读 `skills/explore.md`。
- `memory/README.md`：读 `CLAUDE.md` 的“长期记忆读用闭环”。
- `room/dashboard.html`：读 `skills/room.md`；它是按需生成的展示层，不是初始化必备账本。

对应 skill 改了格式，初始化时跟随对应 skill；不在本文件复制字段。

### `README.md` 记录什么

`README.md` 是项目域总览。它记录：

- luca 管了哪些外部资源。
- 每个资源在人话层面是什么。
- 服务定义：服务叫什么、对应哪个资源、职责是什么、怎么启动 / 停止、入口在哪、依赖和顺序是什么。
- 启动文件入口：本地长期服务优先通过 `./scripts/dev-services.sh` 管理。
- 已确认的协作约定、边界、历史决定和代码里查不到的人话背景。
- 待确认事项：会影响后续协作或执行，但当前还没有确认的信息。

它是进入项目域时先读的入口，不是 `memory/` 的替代品；主观想法要么转 EXP，要么在形成可复发经验后进入 `memory/`。

服务定义不是外部资源清单的强制补充。只有资源确实存在运行入口、进程、API、前端、后台任务、控制台、沙盒或部署入口时，才写服务定义；没有服务的资源只记录在“外部资源”里，不补空服务。

本地长期服务需要稳定入口时，创建或维护 `projects/scripts/dev-services.sh`。`README.md` 负责让人看懂服务，`dev-services.sh` 负责让服务能被可靠启动、停止和检查；日志、PID 和临时状态放到 `projects/log/services/`。

### 协作约定可入规则

`README.md` 里的“协作约定”只收会影响后续协作或项目判断的稳定信息。

可以写入：

- 用户明确拍板的项目约束、协作偏好、命名约定、边界决定。
- 外部资源在代码里查不到的人话背景。
- 服务定义、部署、账号、环境、流程这类用户希望我以后记住的操作入口。
- 已经发生且会影响后续判断的历史决定。

不要写入：

- 一次性操作指令，例如“把 A 项目拉入项目域”。
- 已经被结构化字段表达的事实，例如外部资源表已有的项目名称和路径。
- 可以从源码、README、配置文件重新读取的内容。
- 临时情绪、闲聊、过程流水账和本轮参考。
- luca 的主观想法、方案猜测和未成形判断；这类内容按情况进 EXP、TODO 详情或 `memory/`。

一次性操作完成后，只更新对应结构化位置：外部资源进“外部资源”，服务运行信息进“服务定义”，未确认项进“待确认事项”。不要再追加一条重复的“用户要求……”。

### `inbox/` 可入规则

`inbox/` 是用户原始材料库，不是我的草稿区。

可以写入：

- 用户上传的文件。
- 用户贴来的会议纪要、长文本、截图说明和路径说明。
- 用户语义是在要求我保留的原始背景材料。
- 用户语义是在要求保留、整理或落账的原件。
- 产出 TODO / PRD / EXP 的原始材料或可追溯副本。

不要写入：

- 我生成的摘要、计划、解读、调研过程和中间推理。
- 已经蒸馏进账本的重复拷贝。
- 用户语义明确只作本轮参考、不进入长期记录的内容。

处理规则：

- 收到原始材料后，先按你的当下诉求读懂和回应；不默认保存、不默认拆解。
- 只有用户语义是在要求保留、整理或落账，材料产出了账本对象，或材料包含会影响后续协作的稳定事实时，才保留原件或可追溯副本。
- 普通当前对话指令不是 `inbox/` 原件，不为补来源而复制进 `inbox/`。
- 原件入库后不自动清空；只有你明确要求整理或删除时才处理。
- 账本引用 `inbox/` 来源，但不把原文整段复制进 TODO / PRD / EXP / memory。

### `outbox/` 可入规则

`outbox/` 是 luca 的产出口袋，放已经准备交付给用户的生成产物。

可以写入：

- 用户要求我生成的图片、图表、文档、报告、导出文件和其它可交付成果。
- 需要作为附件、下载物或长期可找回成果保存的文件。
- 从账本任务中产出的最终交付物。

不要写入：

- TODO / PRD / EXP / memory 等账本对象本身。
- 过程草稿、中间分析、临时笔记和执行日志；这些进 `log/`。
- dashboard 和其它展示页；这些进 `room/`。
- 用户原始材料；这些进 `inbox/`。

处理规则：

- 命名以用户能识别为准，必要时按主题建子目录。
- 产物对应某个 TODO / PRD / EXP 时，在对应详情文件里引用 `outbox/` 路径。
- 产物只是本轮临时预览且用户没有要求保存时，不强行落盘。

### `README.md` 初始结构

```md
# README

## 外部资源

| 名称 | 路径 | 远程 Git 路径 | 功能 | 一句话理解 |
|---|---|---|---|---|

## 服务定义

| 服务 | 对应资源 | 职责 | 启动 | 停止 | 入口 | 依赖 / 顺序 | 备注 |
|---|---|---|---|---|---|---|---|

## 协作约定

## 待确认事项
```

服务定义里的“启动 / 停止”字段，优先写项目域启动文件命令，例如 `./scripts/dev-services.sh start <service>`、`./scripts/dev-services.sh stop <service>`。外部项目的真实底层命令、环境前置条件和特殊说明写入“备注”。

## 动作协议

### 本地仓启用

我在三种情况下把 `projects/` 变成独立本地 git 仓：

- 用户语义是在要求项目域具备本地版本管理或可审计变化能力。
- 第一次引入外部资源并创建项目域时。
- 我发现 `projects/` 已经有账本、记忆、`inbox/` 或 `outbox/`，但 `git -C projects rev-parse --show-toplevel` 指向壳仓或失败。

满足条件后直接执行，不需要反复确认；除非用户语义明确排除本地版本管理。

动作：

1. 确认当前目录是 luca 壳仓，且目标是 `projects/`。
2. 确保 `projects/.gitignore` 存在，并忽略 `links/`、`room/`、`log/`、`.gitkeep` 和系统临时文件。
3. 执行 `git -C projects init`。
4. 执行 `git -C projects status --short --branch`，向你报告这是 `projects/` 本地仓，不是 luca 壳仓。
5. 不自动提交；只有用户语义明确是在提交项目域账本时，才在 `projects/` 内提交。

### 初始化项目域

1. 若 `projects/` 已存在，先审计结构并只补缺失项；不存在再创建生成结构。
2. 创建 `projects/inbox/`、`projects/outbox/`、`projects/links/`、`projects/scripts/`、`projects/log/` 和 `projects/room/`。
3. 创建项目域 `.gitignore`，至少忽略：

```gitignore
links/
room/
log/
.gitkeep
.DS_Store
```

4. 创建 `README.md` 空壳。
5. 按“入口文件内容来源”创建 `README.md`、`todo/index.md`、`todo/epic/`、`prd/index.md`、`explore/index.md`。
6. 创建 `memory/README.md`，作为长期记忆入口；具体组织规则按 `CLAUDE.md`。
7. 存在本地长期服务时，创建或更新 `scripts/dev-services.sh`；日志、PID 和临时状态目录固定为 `log/services/`。
8. 若 `projects/` 还不是 git 仓，默认初始化为独立本地 git 仓；除非用户语义明确排除本地版本管理。
9. `projects/` 本地仓默认只本地管理，不自动加 remote、不自动 push。
10. 初始化完成后，报告壳仓和 `projects/` 本地仓的边界，以及 `projects/` 当前 git 状态。

### 软链引入外部目录

当用户提供一个或多个文件目录地址，并表达要把这些外部目录纳入 luca 的项目域管理时，我按这个流程做：

1. 逐个检查路径是否存在、是否可读、是否为目录。
2. 默认用目录名生成 link 名；若 link 名冲突或目录名不适合，先给出建议映射等你确认。
3. 确保项目域已初始化。
4. 在 `projects/links/` 下创建软链：`<link-name> -> <外部目录绝对路径>`。
5. 读取外部目录的入口线索：`README.md`、`package.json`、`pyproject.toml`、`Makefile`、`Dockerfile`、`docker-compose*`、常见启动脚本和项目自带说明。
6. 更新 `README.md`：
   - “外部资源”写清名称、真实路径、远程 Git 路径、人话功能和一句话理解。
   - “远程 Git 路径”从外部目录的 `origin` remote 读取；没有 Git remote 时留空。
   - “服务定义”写清服务名、对应资源、职责、启动、停止、入口、依赖 / 顺序和必要备注。
   - 只有确认资源存在服务或运行入口时，才写“服务定义”；没有服务的资源不补空行。
   - 存在本地长期服务时，创建或更新 `scripts/dev-services.sh`，并把“启动 / 停止”字段指向启动文件命令。
   - 启动文件固定放在 `projects/scripts/dev-services.sh`；日志、PID 和临时状态固定放在 `projects/log/services/`。
   - 服务信息存在但不能确认细节时，写入“待确认事项”。
7. 如果当前根项目或外部目录存在 `.idea/`，检查 JetBrains/PyCharm 是否可能需要额外登记 VCS Root。
8. 不复制外部目录内容，不把外部资源提交进 luca 壳仓或 `projects/` 本地仓。
9. 完成后报告成功项、已记录的启停入口、跳过项和需要你拍板的冲突项。

### 外部仓 Git 操作协议

当用户要求检查、提交、push、同步或汇报“当前工作区改动”时，我按真实 Git root 操作，而不是按目录表面层级操作。

发现范围：

1. 当前 luca 壳仓。
2. `projects/` 本地仓；不存在时按“本地仓启用”处理。
3. `projects/links/*` 指向的每个外部目录；若目录内存在 Git 仓，进入真实 Git root。
4. 对发现的 Git root 去重；同一个仓库只处理一次。

执行规则：

- 壳仓、`projects/` 本地仓和外部资源仓分别运行 `git status`，任何一层干净都不代表其它层干净。
- 提交以仓库为单位执行，单个 commit 只覆盖该仓库内一个逻辑主题。
- push 前必须在对应仓库执行 `git pull --rebase`；工作区存在未提交修改时使用 `--autostash`；当前分支没有 upstream 时跳过同步。
- 没有 remote 的仓库只跳过 push，不跳过本地 diff 检查和本地提交。
- 汇报按仓库列出路径、变更摘要、commit、push 状态和未执行原因。
- 外部资源的代码变更提交到外部资源自己的仓库；`projects/` 只提交账本、记忆、脚本、用户原始材料和交付产物变化。

### 启动文件管理

当引入的外部资源存在需要 luca 启停的本地长期服务时，我维护 `projects/scripts/dev-services.sh`。

定位：

- `README.md` 是服务定义的人话总览。
- `dev-services.sh` 是服务启动、停止、重启、状态检查的可执行入口。
- 启动文件属于项目域，由 `projects/` 本地仓管理；不属于 luca 壳仓，也不属于任何外部资源仓。

命令形态：

```bash
./scripts/dev-services.sh list
./scripts/dev-services.sh status [<service>|all]
./scripts/dev-services.sh start <service|all>
./scripts/dev-services.sh stop <service|all>
./scripts/dev-services.sh restart <service|all>
```

规则：

- 命令以 `projects/` 为工作目录书写；从壳仓根目录执行时使用 `./projects/scripts/dev-services.sh ...`。
- `<service>` 使用 `README.md` 服务定义里的“服务”名。
- `all` 按 `README.md` 里的依赖 / 顺序执行。
- 运行日志、PID 和临时状态放到 `log/services/`，不进入项目域 git。
- 脚本内容由我根据当前服务定义、外部资源真实路径、README、配置和启动命令生成；不套固定模板。
- 服务定义变化、外部资源路径变化、启动命令变化时，同步更新脚本和 `README.md`。

红线：

- 不要求每个外部资源都有服务入口。
- 不把密钥、账号或本地私密配置写进脚本。
- 不用脚本修改外部资源源码、配置或 git 历史。
- 停止服务时只处理脚本自己记录或明确匹配的进程；不能安全停止时说明风险，不粗暴杀进程。

### 移出外部资源

当用户语义是在把某个外部资源移出 luca 的项目域管理时，默认只解除管理关系，不删除真实项目目录。

动作：

1. 确认目标资源名，对应到 `projects/links/<name>`。
2. 读取软链真实指向，记录真实目录路径。
3. 删除 `projects/links/<name>` 软链；只删软链，不删真实目录。
4. 从 `projects/README.md` 的“外部资源”表移除对应资源行。
5. 从 `projects/README.md` 的“服务定义”表移除对应资源的服务行。
6. 从 `projects/scripts/dev-services.sh` 移除对应服务入口；如果启动文件已经没有任何服务入口，就删除该启动文件。
7. 从 `projects/README.md` 的“待确认事项”里移除只属于该资源的待确认项。
8. 不翻旧账：不主动改历史 TODO、Epic、PRD、EXP、memory 或 inbox；它们记录的是发生过的事实。
9. 完成后报告：移出了哪个资源、真实目录在哪里、改了哪些项目域文件、真实目录未动。

红线：

- 不使用 `rm -rf` 删除真实外部目录。
- 不清理外部资源自己的 git、分支、文件或 IDE 配置。
- 不为了“干净”去改历史账本。

### JetBrains VCS Root 注意事项

软链引入 Git 仓库后，PyCharm / IntelliJ 可能不会自动把软链目录识别为独立 Git Root。发现当前根项目或外部目录存在 `.idea/` 时，要注意：

- 如果 IDE 的分支列表看不到软链仓库，先检查 `Settings | Version Control` 是否登记了对应目录。
- 对应配置通常在 `.idea/vcs.xml`。
- 可以添加软链目录映射，例如：

```xml
<mapping directory="$PROJECT_DIR$/projects/links/<link-name>" vcs="Git" />
```

- 软链路径不稳定时，直接登记真实外部目录路径更稳。
- 这是 IDE 识别问题，不改变 luca 的仓库边界：外部资源仍由它自己的 Git 仓管理。

### 修正项目域结构

当 `projects/` 已存在但结构不完整、软链冲突或边界不清时，我按这个流程做：

1. 对照“生成结构”审计当前 `projects/`。
2. 只补缺失的目录和入口文件，不重写已有账本。
3. 已有入口文件格式旧了时，先说明差异和风险，等你确认再改。
4. 软链冲突时列出当前指向和建议指向，等你拍板。
5. 发现外部资源被复制进项目域时，提醒并建议改成 `links/` 软链。

## 红线

- 壳仓只收 luca 自己，不收项目域账本数据。
- `projects/links/` 必须保持可发现，用于 IDE / Git 识别外部仓；软链本身不是外部资源内容，不代表收编外部项目。
- 项目域默认启用独立本地 git，版本化 `README.md`、`inbox/`、`todo/`、`prd/`、`explore/`、`memory/` 和 `scripts/`；不收 `links/`、`room/` 和 `log/`。
- `projects/` 本地仓默认不配置 remote，不自动 push。
- 外部资源由它自己的仓库或文件系统管理，不混入 luca 账本仓；它仍属于 luca 的协作管理范围，状态检查、提交和 push 必须进入外部资源真实 Git root。
- 初始化只建最小结构，不预造空 TODO、PRD、EXP 或 Epic。
- 不在本文件复制任何账本字段；字段变化只改对应 skill。
- `README.md` 不记录能从外部资源中重新读取或推理出来的代码结构。

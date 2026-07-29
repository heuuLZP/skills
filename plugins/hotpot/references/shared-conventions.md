# Shared Conventions

> 原子 skill 共享约定：需求隔离、上下文解析、双模式产物、日期和命名。

## 阅读导航

- `Context Resolution`：确定 requirement。
- `Module Resolution`：确定 module scope。
- `Artifact Resolution`：确定模块使用单文件还是业务入口文档包。
- `Business Entry Resolution`：确定当前业务入口及最小读取范围。
- `产物路径`、`读取原则`、`写入原则`：约束各 skill 的输入输出。

## 工作目录：`.hotpot/`

`.hotpot/` 是 hotpot 的固定产物目录。凡是需要被后续 hotpot skill、`/goal` 或人工 review 复用的产物，都写入这里。

```text
.hotpot/
├── .current
├── .branch-map.md
└── user-login-refactor/
    ├── _meta.md
    ├── .last-module
    ├── requirement.md
    ├── pre-analysis.md
    ├── module-split.md
    ├── use-cases.md
    ├── spec.md
    ├── plan.md
    ├── plan-review.md
    ├── check.md
    ├── archive/
    │   └── 2026-06-29-spec.md
    └── modules/
        ├── auth/
        │   ├── README.md
        │   ├── shared-rules.md
        │   ├── entries/
        │   │   ├── 01-login.md
        │   │   └── 02-logout.md
        │   ├── .last-entry
        │   ├── pre-analysis.md
        │   ├── plan.md
        │   ├── plan-review.md
        │   └── check.md
        └── session/
            ├── use-cases.md
            ├── spec.md
            └── ...
```

## 需求隔离

每个需求必须有独立目录：`.hotpot/[requirement]/`。

- `.hotpot/.current` 内容是一行 requirement slug。
- skill 未收到 requirement 参数时，按下方 Context Resolution 执行，不允许静默选择。
- 同一个项目里的多个需求不能混写到同一目录。
- 模块级产物必须放在该需求目录内的 `modules/[module]/`。

## 需求名和模块名

- requirement 使用 kebab-case，如 `user-login-refactor`。
- 模块名使用 kebab-case，如 `auth`、`session-store`。
- 默认不要在 requirement 目录名里加日期，保持路径稳定。
- 如果同名需求已经存在且语义不是同一需求，才追加日期：`user-login-refactor-2026-06-29`。
- `.last-module` 内容是一行模块名，只用于模块选择时标注“上次模块”；不得据此自动选择。

## Branch Binding

实际开发中，一个分支通常对应一个需求。hotpot 可以利用当前 git 分支推断候选 requirement；一旦用户确认分支绑定，后续同一分支不再重复确认，只展示当前上下文。

每个 skill 做 Context Resolution 时，先尝试读取当前分支：

```bash
git branch --show-current
```

如果当前目录不是 git 仓库，跳过分支绑定，只使用 `.hotpot/.current` 和需求目录。

### 分支到需求名

从分支名提取 requirement slug：

| Branch | Requirement candidate |
|---|---|
| `feature/user-login-refactor` | `user-login-refactor` |
| `feat/auth-session` | `auth-session` |
| `bugfix/export-permission` | `export-permission` |
| `abc-123-user-login` | `abc-123-user-login` |

规则：

- 去掉常见前缀：`feature/`、`feat/`、`fix/`、`bugfix/`、`hotfix/`、`chore/`。
- 保留 ticket id 和业务词。
- 转成 kebab-case。
- `main`、`master`、`develop`、`dev`、`release/*` 不自动作为需求候选，只提示当前分支不适合作为需求名。

### 分支映射文件

`.hotpot/.branch-map.md` 记录分支和需求的关系：

```markdown
# Hotpot Branch Map

| Branch | Requirement | Updated |
|---|---|---|
| feature/user-login-refactor | user-login-refactor | 2026-06-29 |
```

`_meta.md` 也记录分支：

```markdown
# Requirement: user-login-refactor

- Created: 2026-06-29
- Updated: 2026-06-29
- Status: active
- Branch: feature/user-login-refactor
- Current module: auth
- Summary: 用户登录改造
```

### 已确认绑定

Context Resolution 时按优先级收集候选：

1. 用户显式指定的 requirement。
2. 当前 git 分支在 `.branch-map.md` 中已绑定的 requirement。
3. 当前 git 分支推导出的 requirement candidate。
4. `.hotpot/.current`。
5. 已有需求目录列表。

如果当前有效分支已经在 `.hotpot/.branch-map.md` 中绑定 requirement，且该 requirement 目录存在，则直接使用该 requirement，不再等待确认。

开始工作前输出 context banner，让用户能看出当前使用的是哪个需求：

```text
Hotpot context
- branch: feature/user-login-refactor
- requirement: user-login-refactor
- path: .hotpot/user-login-refactor/
- source: .hotpot/.branch-map.md
```

若 `.hotpot/.current` 不同，但 branch-map 绑定的 requirement 目录存在，自动把 `.current` 同步为 branch-map 的 requirement，并在 context banner 中提示：

```text
Hotpot context
- branch: feature/user-login-refactor
- requirement: user-login-refactor
- path: .hotpot/user-login-refactor/
- source: .hotpot/.branch-map.md
- note: 已将 .hotpot/.current 从 data-export 同步为 user-login-refactor
```

### 需要确认的情况

以下情况必须列出候选并让用户确认：

- 当前分支没有 branch-map 绑定，只能推导出 requirement candidate。
- 用户显式指定的 requirement 与 branch-map 绑定不同。
- branch-map 指向的 requirement 目录不存在。
- 当前分支是 `main`、`master`、`develop`、`dev` 或 `release/*`，不能作为需求候选。
- 没有有效分支，且 `.current` / 需求目录不足以唯一确定上下文。

候选不一致时的确认示例：

```text
检测到多个 hotpot 上下文信号：

| 来源 | Requirement |
|---|---|
| 当前分支 feature/user-login-refactor | user-login-refactor |
| .hotpot/.current | data-export |

我建议使用分支对应的 user-login-refactor。
请选择要使用的需求，或输入 new 创建新需求。
```

用户确认后：

- 更新 `.hotpot/.current`。
- 更新 `.hotpot/.branch-map.md`。
- 更新 `.hotpot/[req]/_meta.md` 的 `Branch` 和 `Updated`。

## Context Resolution

每个 hotpot skill 在做阶段工作前，必须先解析上下文并输出 context banner。不要静默使用第一个需求、当前需求或上次模块；但已确认的分支绑定可直接复用，不需要每次重复确认。

### Requirement Startup

当没有明确 requirement 时：

1. 读取当前 git 分支、`.hotpot/.branch-map.md`、`.hotpot/.current` 和 `.hotpot/` 下已有需求目录。
2. 若当前分支已有有效 branch-map 绑定且目录存在，输出 context banner 后继续。
3. 其他状态输出一条明确的确认信息，然后 STOP 等用户确认。

场景 A：没有 `.hotpot/.current`，也没有任何需求目录。

```text
未检测到 hotpot 需求。

我打算创建新需求：
- requirement: user-login-refactor
- branch: feature/user-login-refactor
- path: .hotpot/user-login-refactor/

确认创建吗？也可以给一个不同的需求名。
```

用户确认后才创建：

```text
.hotpot/
├── .current                    # user-login-refactor
├── .branch-map.md               # 若当前是有效 git 分支
└── user-login-refactor/
    └── _meta.md
```

场景 B：没有 `.current`，但已有需求目录。

```text
检测到已有 hotpot 需求：

| # | Requirement | Updated | Status |
|---|---|---|---|
| 1 | user-login-refactor | 2026-06-29 | active |
| 2 | data-export | 2026-06-28 | active |

请选择要使用的需求，或输入 new 创建新需求。
```

场景 C：当前分支已有 branch-map 绑定，且目录存在。

```text
Hotpot context
- branch: feature/user-login-refactor
- requirement: user-login-refactor
- path: .hotpot/user-login-refactor/
- source: .hotpot/.branch-map.md
```

场景 D：`.current` 存在，但没有有效分支绑定，且用户没有显式指定别的需求。

```text
当前 hotpot 需求是 user-login-refactor。

我将使用：
- requirement: user-login-refactor
- path: .hotpot/user-login-refactor/
- source: .hotpot/.current

确认继续吗？也可以选择其他需求或输入 new 创建新需求。
```

场景 E：用户显式指定了需求名。

- 若目录存在：说明将切换/使用该需求，更新 `.current` 后继续。
- 若目录不存在：说明将创建该需求目录，等用户确认后创建。

### Requirement Creation

创建需求时必须写：

```text
.hotpot/.current
.hotpot/.branch-map.md（如果当前是有效 git 分支）
.hotpot/[req]/_meta.md
```

`_meta.md` 初始内容：

```markdown
# Requirement: user-login-refactor

- Created: 2026-06-29
- Updated: 2026-06-29
- Status: active
- Branch: feature/user-login-refactor
- Current module: -
- Summary: 用户登录改造
```

创建后输出：

```text
✅ hotpot 需求已创建

当前需求：user-login-refactor
产物目录：.hotpot/user-login-refactor/
```

### Requirement Selection

选择已有需求时必须：

- 将 `.hotpot/.current` 写为所选 requirement。
- 若当前是有效 git 分支，将分支映射写入 `.hotpot/.branch-map.md`。
- 输出所选 requirement 和路径。
- 不修改其他需求目录。

## Module Resolution

只有当用户要求模块级产物，或当前 skill 明确需要模块 scope 时，才解析模块。需求可以没有模块；没有模块时使用 requirement scope。

模块解析规则：

1. 用户显式给模块名：说明将使用该模块；若目录不存在，说明将创建 `.hotpot/[req]/modules/[mod]/` 并等确认。
2. 用户没有给模块名：读取 `.hotpot/[req]/.last-module` 和 `module-split.md` 中的模块列表。
3. 若没有模块列表，也没有 `.last-module`：说明“当前需求没有模块”，询问是否按 requirement scope 继续，或先运行 `hot-module-split`。
4. 若只有一个候选模块：说明将使用该模块并等待确认。
5. 若有多个候选模块：列出模块，标注 `.last-module`，让用户选择。

多模块选择示例：

```text
当前需求：user-login-refactor

检测到模块：

| # | Module | Artifact mode | 业务产物 | plan | check |
|---|---|---|---|---|---|
| 1 | auth | entry-bundle | README + 2 entries | ⬜ | ⬜ |
| 2 | session | single-file | use-cases | ⬜ | ⬜ |
| 3 | ui | 未选择 | ⬜ | ⬜ | ⬜ |

上次模块：auth

请选择模块，或输入 all 使用需求级 scope。
```

无模块示例：

```text
当前需求 user-login-refactor 没有模块列表。

我可以：
1. 按需求级 scope 写入 .hotpot/user-login-refactor/spec.md
2. 先运行 hot-module-split 拆模块

请选择。
```

模块选择后必须：

- 模块级产物写入 `.hotpot/[req]/modules/[mod]/...`。
- 更新 `.hotpot/[req]/.last-module`。
- 更新 `_meta.md` 的 `Current module` 和 `Updated`。

## Artifact Resolution

业务入口只用于 module scope。Requirement scope 始终使用现有单文件产物。

模块业务产物支持两种模式：

| Artifact mode | 判定 | 业务产物 |
|---|---|---|
| `single-file` | 不存在业务入口文档包结构 | `use-cases.md`、`spec.md` |
| `entry-bundle` | 同时存在 `README.md`、`shared-rules.md` 和至少一个 `entries/*.md` | `README.md`、`shared-rules.md`、`entries/*.md` |

所有模块级 skill 在读取业务产物前必须：

1. 先完成 Module Resolution。
2. 检查模块目录中的两种 artifact mode。
3. 若 `entry-bundle` 结构完整，读取 `README.md` 的业务入口索引并进入 Business Entry Resolution。
4. 若不存在 bundle 结构，按 `single-file` 回退到固定文件名。
5. 若 bundle 结构不完整，停止写入并报告缺少的文件或 entry。
6. 若 bundle 与 `use-cases.md` 或 `spec.md` 同时存在，停止并要求用户选择 canonical 模式或完成迁移；不得静默任选一套。
7. 不创建只有链接或导航作用的兼容 `use-cases.md`、`spec.md`。

`README.md` Metadata 中的 `Artifact mode: entry-bundle` 用于一致性校验，但不能代替目录结构判定。

### 模式选择与切换

- 已有模块不自动迁移。
- 用户明确要求“按业务入口拆分”或“每次只处理一个入口”时，直接采用 `entry-bundle`。
- 未明确指定时，若出现任一强信号，先建议 `entry-bundle` 并等待确认：
  - 三个及以上可独立进入的业务入口。
  - 两个及以上可独立验收的主流程，且角色、页面或提交链路不同。
  - 多个待确认项、权限、失败方式或接口链路只影响特定入口。
  - 不同参与者可以分别确认一部分，而不需要理解整个模块。
- 单一入口的状态分支、纯实现文件差异、不可独立验收的步骤继续使用 `single-file`。
- `hot-module-split` 只记录模式建议；首个写业务产物的 `hot-use-cases` 或 `hot-spec` 在用户确认后创建 bundle。
- 从 single-file 切换时移动内容，不复制内容。删除旧文件前先搜索 `.hotpot/` 内引用。

## Business Entry Resolution

业务入口是模块内可独立理解、讨论和验收的业务入口或主流程。它可以是页面入口、操作流程、系统触发流程或数据处理流程，不要求一定对应页面。

进入 `entry-bundle` 后按以下规则解析：

1. 用户显式指定业务入口时，只选择该 entry。
2. 用户未指定，但请求可由 `README.md` 索引唯一定位时，说明定位结果后继续。
3. 不能唯一定位时，列出业务入口并等待选择。
4. 用户要求整个模块时读取全部 entries，但输出仍按业务入口组织，不重新压平成一张总表。
5. 单入口任务只读取 `README.md`、`shared-rules.md`、目标 entry 和必要的 `pre-analysis.md` / `plan.md` 内容。
6. 模块目录中的 `.last-entry` 只用于标注上次入口，不得据此静默选择。
7. 选择业务入口后更新 `.last-entry`；读取整个模块时不更新。

Context banner 示例：

```text
Hotpot context
- requirement: user-login-refactor
- module: auth
- artifact mode: entry-bundle
- business entry: 02-admin-login
- sources: README.md, shared-rules.md, entries/02-admin-login.md
```

### 信息归属

| 信息类型 | 权威位置 |
|---|---|
| 两个及以上入口共用的规则或问题 | `shared-rules.md` |
| 单一入口的流程、局部规则、接口依赖和验收 | 对应 `entries/*.md` |
| 入口索引、模块全景、问题摘要、跨 Case 边界 | `README.md` |
| 当前代码、协议和技术风险事实 | `pre-analysis.md` |

- 共享规则只详细写一次；entry 只引用规则 ID 或简短说明。
- 接口依赖默认回到受影响 entry，不建立脱离入口的模块级总表。
- 其他 Case 的内容只能作为边界或参考，不得自动关闭当前 Case 的问题。
- `hot-use-cases` 维护 entry 的入口目标、主流程、分支、失败竞态、非目标和验收场景。
- `hot-spec` 维护 entry 的页面/行为、局部规则、问题、接口依赖、验证和业务边界，并维护 `shared-rules.md`。
- `本入口相关问题` 仅在存在入口局部问题时创建；没有该章节表示当前未记录入口局部问题，已有章节和已解决记录不得自动删除。
- 两个 skill 必须先读完整现有文件，只修改自己负责的章节；发现冲突时报告，不静默覆盖。

## 日期规则

日期要明确，但不进入默认文件名。

- `_meta.md` 必须记录需求 `Created` / `Updated`。
- 每个产物的 `Metadata` 节必须记录 `Created` / `Updated` / `Skill` 或 `Skills` / `Scope`。
- 日期格式固定为 `YYYY-MM-DD`，使用当前本地日期。
- single-file 的 canonical 文件名保持稳定；entry-bundle 使用 `README.md`、`shared-rules.md` 和 `entries/*.md`。
- 若需要保留历史版本，复制到 `archive/YYYY-MM-DD-[artifact].md`，不要替代 canonical 文件。

`_meta.md` 推荐格式：

```markdown
# Requirement: user-login-refactor

- Created: 2026-06-29
- Updated: 2026-06-29
- Status: active
- Branch: feature/user-login-refactor
- Current module: auth
- Summary: 用户登录改造
```

## 产物路径

| Scope | Skill | Path |
|---|---|---|
| requirement | `hot-requirement-analysis` | `.hotpot/[req]/requirement.md` |
| requirement | `hot-pre-analysis` | `.hotpot/[req]/pre-analysis.md` |
| requirement | `hot-module-split` | `.hotpot/[req]/module-split.md` |
| requirement | `hot-use-cases` | `.hotpot/[req]/use-cases.md` |
| requirement | `hot-spec` | `.hotpot/[req]/spec.md` |
| requirement | `hot-plan` | `.hotpot/[req]/plan.md` |
| requirement | `hot-plan-review` | `.hotpot/[req]/plan-review.md` |
| requirement | `hot-check` | `.hotpot/[req]/check.md` |
| module | `hot-pre-analysis` | `.hotpot/[req]/modules/[mod]/pre-analysis.md` |
| module, single-file | `hot-use-cases` | `.hotpot/[req]/modules/[mod]/use-cases.md` |
| module, single-file | `hot-spec` | `.hotpot/[req]/modules/[mod]/spec.md` |
| module, entry-bundle | `hot-use-cases` / `hot-spec` | `.hotpot/[req]/modules/[mod]/README.md`、`shared-rules.md`、`entries/*.md` |
| module | `hot-plan` | `.hotpot/[req]/modules/[mod]/plan.md` |
| module | `hot-plan-review` | `.hotpot/[req]/modules/[mod]/plan-review.md` |
| module | `hot-check` | `.hotpot/[req]/modules/[mod]/check.md` |

`hot-requirement-analysis` 只产出需求级文档，因为它定义需求理解与路由。
`hot-module-split` 只产出需求级文档，因为它定义模块边界。

## 读取原则

原子 skill 不要求固定前置链路，但应复用当前需求目录里的已有产物：

| 当前 skill | 优先读取 |
|---|---|
| `hot-requirement-analysis` | 原始需求来源（PRD / ticket / 对话 / bug report）；更新时可读取 `[req]/requirement.md` |
| `hot-pre-analysis` | `[req]/requirement.md`、需求描述、相关代码、现有 docs |
| `hot-module-split` | `[req]/requirement.md`、`[req]/pre-analysis.md`、需求描述 |
| `hot-use-cases` | `[req]/requirement.md`、`[req]/module-split.md`、同 scope 的 `pre-analysis.md`；模块级先做 Artifact / Business Entry Resolution |
| `hot-spec` | `[req]/requirement.md`、`module-split.md`、`pre-analysis.md`；single-file 读取 `use-cases.md`，entry-bundle 读取索引、共享规则和相关 entries |
| `hot-plan` | `pre-analysis.md`、相关代码；single-file 读取 `spec.md`，entry-bundle 读取索引、共享规则和相关 entries |
| `hot-plan-review` | `[req]/requirement.md`、`plan.md`；按 artifact mode 读取 `spec.md` 或业务入口文档包 |
| `hot-check` | `[req]/requirement.md`、`plan.md`、实际改动；按 artifact mode 读取单文件或业务入口文档包 |

缺少上游产物时，不要自动补跑其他 skill。说明缺口，能继续就继续；不能继续才 STOP。
若 `hot-plan` 发现 `requirement.md` 与 canonical 业务产物冲突，先修订业务产物，不绕过已确认规则做技术决策。

## 写入原则

- 如果用户只是问一个轻量判断，可以只在对话中回答。
- 如果输出会作为后续依据，必须写入上表路径。
- 写模块级产物时，先确保 `.hotpot/[req]/modules/[mod]/` 存在。
- 写 entry-bundle 时维护 `README.md` 索引与 entry 文件的一致性，不生成兼容单文件。
- 写任意产物后更新 `_meta.md` 的 `Updated`。
- 写模块级产物后更新 `.last-module`。

## 不自动链式触发

每个 skill 结束时只能给“建议下一步”，不能自动触发其他 skill，也不能模拟其他 skill 的完整产物。

## P19：单测默认关闭

默认不新建单测文件。验证优先使用：

- 跑应用或关键命令。
- 走查 `hot-use-cases` / `hot-spec` 中枚举的场景。
- 运行已有测试。

只有 `hot-spec` 的 `Verification` 明确写“需单测”时，`hot-plan` 才要求新增单测。

## P20：Codex review 不起子代理

Codex 中 review 默认就地完成：

- `hot-plan-review` 由当前 agent 对照 spec/plan 审查。
- `hot-check` 由当前 agent 对照产物与实际改动检查。
- 不自动派发 review 子代理。

## 结束输出

每个 skill 完成后输出：

```text
✅ [产物名] 已完成

产物路径：[固定 .hotpot 路径，或说明“仅对话输出，未落盘”]
建议下一步：[一个或多个可选动作，不自动执行]
```

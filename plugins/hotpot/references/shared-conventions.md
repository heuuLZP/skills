# Shared Conventions

Hotpot skills 共享需求隔离、上下文解析、产物模式和写入约定。只在需要对应能力时读取相关章节。

## 固定目录与命名

可复用产物统一写入 `.hotpot/[requirement]/`；requirement 和 module 均使用 kebab-case。需求级和模块级路径如下：

| Skill | Requirement scope | Module scope |
|---|---|---|
| `hot-requirement-analysis` | `requirement.md` | - |
| `hot-pre-analysis` | `pre-analysis.md` | `modules/[mod]/pre-analysis.md` |
| `hot-module-split` | `module-split.md` | - |
| `hot-use-cases` | `use-cases.md` | `modules/[mod]/use-cases.md` 或 entry-bundle |
| `hot-spec` | `spec.md` | `modules/[mod]/spec.md` 或 entry-bundle |
| `hot-plan` | `plan.md` | `modules/[mod]/plan.md` |
| `hot-plan-review` | `plan-review.md` | `modules/[mod]/plan-review.md` |
| `hot-check` | `check.md` | `modules/[mod]/check.md` |

辅助文件：

- `.hotpot/.current`：当前 requirement。
- `.hotpot/.branch-map.md`：已确认的 Git branch → requirement 绑定。
- `[req]/_meta.md`：需求元数据。
- `[req]/.last-module`、`modules/[mod]/.last-entry`：只用于提示上次选择，绝不自动选择。
- 历史版本放 `archive/YYYY-MM-DD-[artifact].md`，canonical 文件名保持稳定。

## Context Resolution

每个 skill 开始前解析 requirement 并显示 requirement、路径、来源；有分支时也显示 branch。不得根据 slug 猜需求内容。

按优先级收集候选：

1. 用户显式指定的 requirement。
2. 当前分支在 `.branch-map.md` 中的有效绑定。
3. 当前分支去掉 `feature/`、`feat/`、`fix/`、`bugfix/`、`hotfix/`、`chore/` 后得到的候选。
4. `.hotpot/.current`。
5. 已有需求目录。

`main`、`master`、`develop`、`dev`、`release/*` 不生成分支候选。非 Git 仓库跳过分支逻辑。

只有“分支已有绑定且目录存在”可直接复用，并同步不一致的 `.current`。以下情况必须展示候选后停止等待确认：

- 只能从未绑定分支推导候选。
- 显式 requirement 与分支绑定冲突。
- 绑定目录不存在。
- 主干/release 分支无法生成候选。
- 没有足够信息唯一确定上下文。

用户确认创建或切换后才写 `.current`；有效分支同时更新 `.branch-map.md`。创建需求时写：

```markdown
# Requirement: [requirement]

- Created: YYYY-MM-DD
- Updated: YYYY-MM-DD
- Status: active
- Branch: [branch 或 -]
- Current module: -
- Summary: [一句话]
```

不要静默创建、选择或混写需求目录。

## Module Resolution

只在用户要求模块 scope，或当前任务必须落到模块时解析：

1. 用户显式指定 module：说明目标；目录不存在时等待创建确认。
2. 未指定：读取 `module-split.md` 的模块和 `.last-module`。
3. 无候选：让用户选择 requirement scope 或先执行 `hot-module-split`。
4. 一个候选：说明候选并等待确认；多个候选：列出并让用户选择。

确认模块后，模块产物写入 `modules/[mod]/`，更新 `.last-module` 及 `_meta.md` 的 `Current module`、`Updated`。

## Artifact Resolution

Requirement scope 始终使用单文件。Module scope 在读取业务产物前识别：

| Mode | 判定 | Canonical artifacts |
|---|---|---|
| `single-file` | 不存在完整 bundle | `use-cases.md`、`spec.md` |
| `entry-bundle` | 同时存在 `README.md`、`shared-rules.md`、至少一个 `entries/*.md` | 这三类文件 |

处理规则：

1. 先完成 Module Resolution，再检查目录结构。
2. 完整 bundle 进入 Business Entry Resolution；无 bundle 使用 single-file。
3. bundle 不完整时停止并列出缺失项。
4. bundle 与 `use-cases.md` / `spec.md` 并存时停止，让用户选择 canonical 模式或迁移。
5. 不创建只做导航的兼容 `use-cases.md` 或 `spec.md`。

已有模块不自动迁移。用户明确要求按入口组织时采用 `entry-bundle`；否则出现任一强信号时先建议并等待确认：

- 至少 3 个可独立进入的业务入口。
- 至少 2 个角色、页面或提交链路不同且可独立验收的主流程。
- 多个问题、权限、失败方式或接口链路只影响特定入口。
- 不同参与者能分别确认部分内容。

单一入口的状态分支、实现文件差异或不可独立验收的步骤使用 `single-file`。从 single-file 迁移时移动内容、不复制；删除旧文件前搜索 `.hotpot/` 内引用。

## Business Entry Resolution

业务入口是可独立理解、讨论和验收的页面入口、操作流程、系统触发流程或数据处理流程。

- 显式指定 entry 时只选它；请求能由 README 索引唯一定位时说明后继续；否则列出候选并等待选择。
- 整模块任务读取全部 entries，但仍按 entry 输出；单入口只读取 README、shared rules、目标 entry 和必要的分析/计划片段。
- `.last-entry` 只作提示；确认单入口后更新，整模块读取时不更新。

信息归属：

| 信息 | 权威位置 |
|---|---|
| 两个以上入口共用的规则或问题 | `shared-rules.md` |
| 单入口流程、局部规则、接口依赖、验收 | 对应 `entries/*.md` |
| 入口索引、模块全景、问题摘要、跨 Case 边界 | `README.md` |
| 当前代码、协议和技术风险事实 | `pre-analysis.md` |

`hot-use-cases` 维护入口目标、流程、分支、失败/竞态、非目标和验收场景；`hot-spec` 维护行为、规则、问题、接口、验证和边界。两者修改前读取完整文件，不覆盖对方章节。

single-file 的 `待澄清问题` 和 entry 的 `本入口相关问题` 是临时工作区：仍有未确认项时保留完整区域；全部确认后，先把每项结论及来源 Case 写入正式契约章节，再统一删除整个问题区。删除 entry 问题区时同步 README 摘要与阻断数。`共享待确认项` 不采用删除式生命周期，确认后保留原记录和状态。

其他 Case 只能作为边界或参考，不能自动确认当前 Case。共享规则只详细写一次；entry 引用规则 ID 或简述。

## 读写规则

- 原子 skill 不要求固定前置链路。读取当前 scope 已有的相关产物；缺少上游时能安全继续就继续，否则说明缺口并停止，不自动补跑 skill。
- 轻量判断可只在对话回答；会被后续 skill、`/goal` 或人工复用的结果必须落盘。
- 写前读取完整目标文件；冲突时报告，不静默覆盖。
- 每个产物包含 `Metadata`：Requirement、Scope、Module、Branch、Skill(s)、Created、Updated；日期为本地 `YYYY-MM-DD`。
- 写产物后更新 `_meta.md` 的 `Updated`；模块级再更新 `.last-module`，选定 entry 时更新 `.last-entry`。
- entry-bundle 写入后运行 `<plugin-root>/scripts/validate_artifacts.py <module-dir>`，保持 README 索引和 entries 一致。
- 每个 skill 只建议下一步，不自动触发其他 skill。

## 验证与审查

默认验证为运行应用或关键命令、走查场景、运行已有测试。只有 `hot-spec` 明确写 `需单测：是` 时，`hot-plan` 才要求新增单测。

`hot-plan-review` 与 `hot-check` 在 Codex 中由当前 agent 就地完成，不自动启动 review 子代理。

## 完成输出

```text
✅ [产物名] 已完成
产物路径：[固定路径，或“仅对话输出，未落盘”]
建议下一步：[可选动作，不自动执行]
```

---
name: hot-spec
description: Use when a requirement or module needs a business specification or behavior contract before technical planning, including shared and entry-local rules, boundaries, states, interface dependencies, acceptance criteria, and verification; supports both single-file artifacts and business-entry bundles.
---

# Hotpot Spec

定义必须成立的行为契约、规则、状态、边界、接口依赖和验证期望。不设计目录/组件，不写代码，不默认要求新单测。

开始前按需读取 `../../references/shared-conventions.md` 中的 Context、Module、Artifact Resolution、Business Entry Resolution 和问题生命周期。写入时再读取 `../../references/output-style-guide.md`，以及 `../../references/artifact-templates.md` 的“规格”或业务入口 README/Shared Rules/Entry 模板。

## Workflow

1. 解析 requirement 与 scope；模块 scope 先做 Artifact Resolution 和 Business Entry Resolution。无业务产物时沿用 `hot-use-cases` 的模式选择规则。
2. 读取 `requirement.md` 与 canonical scenarios。没有用例时只补足写契约所需的最小场景，不冒充完整 use-case 分析。
3. single-file：仅有开放问题时创建 `待澄清问题`。任一问题未确认时保留整个区；全部确认后，先把每项结论及来源 Case 写入规则、接口、代码外工作项或其他正式章节，再统一删除整个问题区。
4. entry-bundle：
   - 两个以上 entry 共用的规则或问题放 `shared-rules.md`，局部内容留在目标 entry。
   - 仅有局部开放问题时创建 `本入口相关问题`；沿用同样的完整保留与统一删除生命周期。
   - 删除 entry 问题区时同步 README 问题摘要和阻断数；`共享待确认项` 的已确认记录保留。
   - 保留 `hot-use-cases` 负责的目标、流程、分支、失败、竞态、非目标和验收场景。
5. 每个问题记录类型、来源 Case、影响 entries、当前口径、阻断状态和确认状态；推断不得标为 PRD 已确认，跨 Case 信息不得确认当前 Case。
6. 查找重复共享规则、失去 entry 语境的接口问题，以及按规则类型平铺导致的入口上下文丢失。
7. 填写 Verification：默认跑应用、走查场景、运行已有测试；仅纯逻辑、复杂状态机、回归敏感规则或明确要求时写 `需单测：是` 并说明理由。
8. 修改前读完整文件；冲突时停止。写 Metadata、更新指针，并对 entry-bundle 运行 validator。

## Quality Bar

产物必须让 `hot-plan` 无需重新决定业务行为即可回答：实现什么、不能违反什么、哪些状态/边界重要、如何验证。出现文件路径、import、实现偏好、无理由单测或重复局部规则时应修正。

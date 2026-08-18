---
name: hot-use-cases
description: Use when a requirement or module needs scenario enumeration before spec or implementation, including main flows, branches, failures, races, non-goals, and acceptance scenarios; supports both single-file artifacts and selecting or updating one or more business entries in an entry-bundle.
---

# Hotpot Use Cases

枚举可观察场景，不定义业务契约、实现文件或测试方案，也不默认新增单测。

开始前按需读取 `../../references/shared-conventions.md` 中的 Context、Module、Artifact Resolution、Business Entry Resolution 和章节所有权。写入时再读取 `../../references/output-style-guide.md`，以及 `../../references/artifact-templates.md` 的“用例”或业务入口 README/Entry 部分。

## Workflow

1. 解析 requirement 与 scope；模块 scope 必须先做 Artifact Resolution 和 Business Entry Resolution。
2. 模块尚无业务产物时按模式信号选择：简单模块用 single-file；强复杂度信号先建议 entry-bundle 并等待确认，除非用户已明确要求。
3. 读取已有 `requirement.md`、`module-split.md` 和相关 `pre-analysis.md`。
4. 从主流程开始，补充分支、边界、失败、竞态、非目标和可检查的验收场景。
5. single-file 使用“用例”模板。
6. entry-bundle 只读取 README、shared rules 和选中 entries（整模块请求除外）；只维护 Entry 从“入口与目标”到“验收场景”的章节，同时更新 README 索引和摘要。保留 `hot-spec` 所有章节。
7. 修改前读完整文件；冲突时停止报告，不覆盖其他 skill 内容。
8. 写 Metadata、更新 module/entry 指针，并运行 artifact validator。

## Quality Bar

- 不只列 happy path；必须考虑相关失败和竞态。
- 场景停在行为层，不夹带库、文件或组件决定。
- 每个验收场景以后能被 `hot-check` 明确判定。
- 单入口请求不读取或重写无关 entries；entry-bundle 不创建导航型 `use-cases.md`。

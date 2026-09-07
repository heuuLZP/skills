---
name: hot-pre-analysis
description: Use when a requirement or module needs codebase reconnaissance before use cases, specs, or planning, especially when implementation, data flow, dependencies, reuse points, risks, or code-path coverage across business entries are unclear.
---

# Hotpot Pre Analysis

回答“现状是什么、在哪里、如何运作、可复用什么、有哪些风险”。只记录代码与协议事实，不定义产品规则或技术方案，不开始实现。

开始前按需读取 `../../references/shared-conventions.md` 的 Context、Module、Artifact Resolution 与 Business Entry Resolution。写入时再读取 `../../references/output-style-guide.md` 和 `../../references/artifact-templates.md` 的“前置分析”模板。

## Workflow

1. 解析 requirement 和可选 module；已有 `requirement.md` 只用于聚焦搜索。
2. 模块 scope 先做 Artifact Resolution；entry-bundle 先读 README 索引，仅在请求指向某入口时解析该 entry。
3. 用快速文件/文本搜索定位入口，再读取能证明当前行为的最小文件集合，包括必要的路由、API、模型、测试、配置和文档。
4. 将事实、假设、风险分开；每个事实引用文件、文档或命令。标注代码路径、接口和风险覆盖哪些 entry，以及是共享还是局部。
5. 默认写一个 module-level `pre-analysis.md`；独立路径可用 entry 小节，不机械拆文件。
6. 按模板记录现状、结构、数据流/依赖、复用点、风险和影响后续决策的未知项，包含 Metadata。

## 架构事实分类

在“当前状态”和“数据流 / 依赖”中额外记录以下事实；只描述证据，不给方案：

- 系统边界：前端、BFF、后端和第三方分别负责什么；
- 跨项目或跨模块依赖：调用、共享包、共享配置和发布耦合；
- 共享能力候选：哪些能力被多个入口或项目使用；
- 数据或状态所有权：谁产生、保存、修改和消费；
- 构建、部署、运行拓扑：本次需求是否触及交付链路；
- 性能、可用性、安全和兼容性等非功能约束。

若这些事实显示可能触及系统级边界，在产物中标记为待 `hot-module-split` 或 `hot-plan` 判断的信号；不得在本阶段设计方案或自动调用 `$arch-coach`。

## Quality Bar

- 摘要先行；流程、结构、依赖或数据流使用 Mermaid。
- 读者无需重复搜索即可找到相关代码并理解现有行为。
- 不把代码现状当作已确认业务规则，不枚举完整用例、拆模块或提出实现方案。

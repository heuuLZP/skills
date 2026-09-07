# heuuLZP Skills

个人维护的 Claude Code、Codex 与 ZCode skills/plugin 集合。独立能力以 skill 提供，需要共享上下文的完整工作流以 plugin 提供。

## 独立 Skills

| Skill | 何时使用 | 主要结果 | 示例 |
|---|---|---|---|
| `ai-reflect` | 回顾近期 AI 使用习惯、协作质量或依赖程度 | 基于 Claude Code 与 Codex 会话生成四维协作复盘报告 | “分析我最近一周使用 AI 的情况” |
| `arch-coach` | 显式调用后，按阶段练习架构理解、诊断、决策或复盘 | 基于真实证据完成一次架构训练；review 同时支持改动复盘和架构盲点训练 | `$arch-coach diagnose 诊断这个项目的权限架构问题` |
| `commit` | 需要分析 Git 改动、生成提交信息或拆分提交 | 合理暂存并创建一个或多个 Git commit | “提交当前改动” |
| `human-review` | 显式选择该 skill，逐批理解、修复和批准待提交改动 | AI 先建立改动地图并评估工程质量，获授权后修复问题并逐批提交 | `/human-review` |

`arch-coach` 和 `human-review` 仅在用户通过技能选择器或显式写出 skill 名称时启用。`arch-coach` 使用 `understand → diagnose → decide → review` 四个独立阶段，阶段之间不会自动串联；其中 `review` 已包含原 `arch-review` 的 Git diff 扫描、三层盲点对比、思考题和可选记录能力，原 `$arch-review` 入口不再提供。普通架构问题不加载该训练流程。其余独立 skill 可以直接描述任务，也可以在提示词中明确指定名称，客户端会根据 description 判断是否加载完整工作流。

`arch-coach` 默认先在对话中预览，不会自动创建文档。用户明确要求归档后，按内容所有权选择唯一权威位置：跨项目全景和跨系统决策保存到用户确认的独立架构文档仓库；单项目、模块、组件或需求相关内容保存到该项目仓库的 `docs/architecture/`（已有项目约定优先）；个人训练复盘保存到 `~/.agents/data/arch-coach/`。项目架构事实不会写入个人全局目录，不同位置之间只保留链接或摘要，避免形成多份相互冲突的文档。

## Hotpot Plugin

Hotpot 是一组用于需求协作的原子 skill。它不强制执行固定流水线，而是让人根据需求复杂度组合需要的分析步骤；代码实现交给正常的编码流程，Hotpot 负责把需求从模糊输入推进到可执行、可检查的状态。

Hotpot 以整包 plugin 发布，因为 8 个 skill 共享上下文解析规则、产物模板和评审规范，不能只复制其中一个 skill 使用。

### Skill 使用表

| Skill | 何时使用 | 主要产物 | 不负责 |
|---|---|---|---|
| `hot-requirement-analysis` | 收到原始需求、工单、PRD 或讨论记录时 | `requirement.md`：目标、范围、约束、澄清点和下一步建议 | 不看代码、不写规格、不拆模块 |
| `hot-pre-analysis` | 对现有实现、数据流或复用点不熟悉时 | `pre-analysis.md`：现状、代码结构、依赖、架构事实、风险和未知项 | 不定义业务规则或技术方案 |
| `hot-module-split` | 需求包含多个职责，或模块内可能还有多个独立业务入口时 | `module-split.md`：模块、边界、依赖、业务入口索引、artifact mode 和架构决策信号 | 不展开入口内部规则或做架构取舍 |
| `hot-use-cases` | 主流程、异常、边界、竞态或验收口径复杂时 | 简单模块写 `use-cases.md`；复杂模块按 `entries/*.md` 写场景 | 不做技术设计 |
| `hot-spec` | 需要锁定业务规则和行为契约时 | 简单模块写 `spec.md`；复杂模块维护共享规则和入口局部规则 | 不决定目录、组件或文件职责 |
| `hot-plan` | 规格明确，需要技术落地方案时 | `plan.md`：目录、组件、状态、数据流、文件职责、架构决策依据和验证点 | 高影响架构变更无确认摘要时停止；不写代码 |
| `hot-plan-review` | 执行前需要检查 spec/plan 是否遗漏或冲突时 | `plan-review.md`：按严重度排列的问题、架构决策检查、建议与结论 | 不修改代码、不代替实现或架构取舍 |
| `hot-check` | 实现完成后，需要对照前序产物检查闭环时 | `check.md`：通过结论、场景闭环、架构决策偏离、验证证据和改动摘要 | 不做泛化代码审查或深度排错 |

### 推荐组合

所有需求默认先理解需求：

```text
hot-requirement-analysis
```

小而清晰的需求：

```text
hot-requirement-analysis
→ hot-pre-analysis       （不熟代码时）
→ hot-use-cases          （边界复杂时）
→ hot-spec
→ hot-plan               （技术落地复杂时）
→ hot-plan-review        （风险较高时）
→ 实现
→ hot-check
```

中大型需求：

```text
hot-requirement-analysis
→ hot-module-split
→ 按模块执行 hot-pre-analysis / hot-use-cases / hot-spec / hot-plan
→ hot-plan-review
→ 实现
→ hot-check
```

模块业务产物支持两种模式：

- `single-file`：职责单一，继续使用 `use-cases.md` 和 `spec.md`。
- `entry-bundle`：包含多个可独立理解和验收的业务入口，使用 `README.md`、`shared-rules.md` 和 `entries/*.md`。

业务入口可以是页面入口、操作流程、系统触发流程或数据处理流程。共享规则只写一次，入口局部问题留在对应 entry；下游 skill 会先解析 artifact mode，不依赖固定文件名猜测业务上下文。

这些步骤由人选择，不会由某个 skill 自动触发下一个 skill。Hotpot 产物统一保存到当前项目的 `.hotpot/<requirement>/`。当需求涉及系统边界、跨项目依赖、共享能力、数据所有权、运行拓扑或重大非功能约束时，`hot-plan` 要求用户先显式运行 `$arch-coach decide`，带回已确认的架构决策摘要；这是人工交接，不是 skill 依赖或自动调用。

## 从 GitHub 安装

安装 Hotpot plugin：

```bash
codex plugin marketplace add heuuLZP/skills
codex plugin add hotpot@heuulzp-skills

claude plugin marketplace add heuuLZP/skills
claude plugin install hotpot@heuulzp-skills --scope user
```

如果需要四个独立 skill，克隆仓库后运行安装脚本：

```bash
git clone https://github.com/heuuLZP/skills.git
cd skills
./scripts/install.sh
```

## 本地安装

安装四个独立 skill：

```bash
./scripts/install.sh
```

本地安装脚本为 Claude Code、Codex 与 ZCode 桌面客户端准备共享技能目录。仓库是唯一源码，`~/.agents/skills` 作为三端共享入口；Codex 与 Claude Code 桌面客户端额外使用兼容软链接，ZCode 桌面客户端直接发现共享入口。脚本不升级或配置 CLI，技能加载和 smoke check 仅以三款桌面客户端的新会话为验收对象；遇到已有真实目录时，会先备份再建立软链接。

本地安装 Hotpot plugin：

```bash
codex plugin marketplace add "$(pwd)"
codex plugin add hotpot@heuulzp-skills

claude plugin marketplace add "$(pwd)"
claude plugin install hotpot@heuulzp-skills --scope user
```

安装或新增 skill 后请新开会话，让客户端重新加载清单。

## 数据位置

- `ai-reflect` 报告：`~/.agents/data/ai-reflect/reports/`
- `arch-coach` 跨项目架构：用户指定并确认的独立架构文档仓库
- `arch-coach` 项目内架构：`<project>/docs/architecture/`，已有项目约定优先
- `arch-coach` 可选配置：`~/.agents/data/arch-coach/config.json`
- `arch-coach` 个人训练记录：`~/.agents/data/arch-coach/retrospectives.md`
- 旧 `arch-review` 数据：保留在 `~/.agents/data/arch-review/`，不自动迁移或删除
- Hotpot 项目产物：`<project>/.hotpot/`

## 验证

```bash
./scripts/validate.sh
```

## 卸载独立 Skills

```bash
./scripts/uninstall.sh
```

卸载脚本只删除仍然指向本仓库的软链接，不删除用户数据或备份。

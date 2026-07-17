# Review Checklist

> 用于 `hot-plan-review` 和 `hot-check` 的就地审查清单。

## Plan Review 维度

| 维度 | 检查问题 |
|---|---|
| Requirement 覆盖 | plan/spec 是否偏离 `requirement.md` 的目标、范围、约束和阻断澄清点 |
| Spec 覆盖 | plan 是否覆盖 spec 的全部行为、规则、边界和验收场景 |
| 可落地性 | 文件职责、数据流、状态流转是否足够明确 |
| 依赖方向 | 是否存在循环依赖、层级倒置、跨边界调用 |
| 交互基础设施 | 拖拽、滚动、请求、缓存、竞态是否使用成熟方案或已有模式 |
| 验证点 | 每个关键场景是否有验证方式 |
| P19 | 是否默认新建了不必要的单测 |
| 注释/JSDoc | 复杂导出函数、非显然状态机、竞态处理是否要求注释 |

## Completion Check 维度

| 维度 | 检查问题 |
|---|---|
| 需求范围 | 实际改动是否仍符合 `requirement.md` 的目标、范围和约束 |
| 用例闭环 | primary flow、edge case、failure case 是否都有结果 |
| Spec 合规 | 行为契约、业务规则、边界是否被满足 |
| Plan 对照 | 文件职责、状态、数据流是否按 plan 落地 |
| 验证证据 | 命令输出、应用走查、已有测试是否支撑结论 |
| 偏离记录 | 与 spec/plan 的偏离是否说明原因和影响 |

## 不检查

- 不做泛泛代码质量 review。
- 不排查新 bug；发现 bug 线索时建议使用 `superpowers:systematic-debugging`。
- Codex 中不自动起 review 子代理。

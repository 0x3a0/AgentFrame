# Aier - 开箱即用的 Agent Framework

## 待办事项

- [x] 修改tool加载方式 - 手动传入更准确的 tool schema
- [x] 将 llm client 从 model 中分离
- [x] API响应默认流式处理
- [x] ReActAgent - 实现 ReAct 架构的 agent 模块
- [ ] PlanAndSolveAgent - 实现 PlanAndSolve 架构的 agent 模块 将任务拆解为多个子任务按步骤执行，给模型一个显示、稳定、可反复更新的计划状态
- [ ] Memory System
    - [ ] Short Term Memory - 将短期记忆拆分成一个单独的模块，按需加载
    - [ ] Long Term Memory - 将长期记忆拆分成一个单独的模块，按需加载
- [ ] Skill System
- [ ] Context Engineering
    - [ ] 上下文压缩
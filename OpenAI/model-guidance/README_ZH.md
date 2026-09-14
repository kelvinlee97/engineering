# OpenAI 最新模型指南

[English](README.md) · 简体中文

## 来源

- 官方指南：[Model guidance](https://developers.openai.com/api/docs/guides/latest-model)
- 发布方：OpenAI
- 查阅日期：2026-09-14
- 查阅时对应模型：`gpt-6-astra`

原页面是持续更新的指南，默认模型可能变化。在做生产环境的模型或 API 决策前，应重新查看官方页面。

## 一句话总结

OpenAI 推荐 GPT-6 Astra 处理高难度、端到端的 API 工作，包括推理、编程、浏览器操作、computer use、
科研和专业工作流。使用时应通过 Responses API 指定 `model: "gpt-6-astra"`。

迁移不只是替换模型名称。应用还需要检查 reasoning effort、工具调用、不再支持的采样参数、prompt cache，
以及控制自治程度、写作风格、任务委派和验证方式的 prompt。

## GPT-6 Astra 的新增能力

- **异步工具调用：** 为 function 或 custom tool 设置 `async: true`。应用执行工具期间，模型可以继续处理
  其他工作，之后再通过原始 `call_id` 接收结果。
- **中途调整指令：** 使用 WebSocket 连接 Responses API 时，可以在 response 进行中加入新的用户指令，
  同时保留已经完成的工作。
- **对话中调整推理强度：** 使用 `configuration_update` input item 改变 reasoning effort，并保留稳定的
  prompt 前缀以继续利用 cache。
- **已有 agent 能力：** computer use、Structured Outputs、streaming、programmatic tool calling、
  multi-agent orchestration、prompt caching、persisted reasoning、compaction 和 pro mode。
- **失准监控：** OpenAI 表示其异步安全机制会监控潜在 misalignment，并在需要时触发告警。

应用仍然负责真正执行工具和管理 pending calls；异步工具调用没有把这项责任交给模型。

## 需要适配的 Prompt 行为

### 主动性与持续执行

当答案可能改变结果时，GPT-6 Astra 比早期模型更倾向于先澄清。如果应用期望它自主完成任务，应明确要求
模型推断常规细节、在已授权范围内行动、持续执行到完成，并且只在决策会实质影响结果时提问。

### 指令遵循

模型更能遵循长指令，同时也更容易受到 skills、`AGENTS.md` 和其他上下文文件的影响。应检查这些文件中
是否存在过期、隐藏或冲突的规则，并明确不同指令来源的优先级。

### 写作风格

默认回答可能较详细，并大量使用格式化结构。应明确指定篇幅、结构、用词和受众，不要期待模型在没有指令时
自动保持应用所需的固定风格。

### 任务委派

如果工作流适合使用多个 agent 并行处理，应说明何时需要委派、委派多少工作，不要假设模型会自行选择预期的
并行程度。

### 测试

模型可能对很小的代码改动也执行较广泛的验证。应定义与风险相称的检查，并明确何时必要测试已经足够；只有
发生失败、新改动或仍有未解决风险时才扩大验证范围。

## 迁移检查清单

1. 把模型改为 `gpt-6-astra`。
2. 工具调用使用 Responses API。GPT-6 Astra 支持 Chat Completions，但其工具调用必须使用 Responses。
3. 如果旧配置的 reasoning effort 是 `none` 或 `minimal`，先改成 `low`；否则保留原本的有效设置，并用
   eval 比较质量、延迟和成本。
4. 删除不支持的参数：`temperature`、`top_p` 和 `top_logprobs`。使用 Chat Completions 时还要删除
   `logprobs`；使用 Responses 时，从 `include` 中删除 `message.output_text.logprobs`。
5. 如需在多次 response 之间调整 reasoning effort，在兼容的标准单 agent 请求中优先使用
   `configuration_update`，以保持 prompt cache 前缀稳定。
6. 从 GPT-5.5 或更早版本迁移时，把 `prompt_cache_retention` 替换成
   `prompt_cache_options.ttl: "30m"`，并检查新的 cache 边界和写入计费规则。
7. 重新运行应用 eval，并根据结果调整主动性、指令优先级、写作风格、任务委派和验证相关 prompt。

## 重要限制

- GPT-6 Astra 不支持 `none` reasoning effort。
- 工具调用必须使用 Responses API。
- 使用 EU data residency 时应选择 Standard processing；GPT-6 Astra 在该场景不支持 `fast` 或
  `priority` service tier。
- Fast mode 没有延迟 SLA。
- 可用性、限制、价格和功能支持可能变化，正式上线前应查看最新官方文档。

## 实践建议

把迁移当成一次需要 eval 的配置变更：

1. 从生产工作中选择一组有代表性的任务。
2. 修改模型和必要的 API 参数。
3. 先保留原 prompt，再根据观察到的问题定点调整，不要一开始全部重写。
4. 比较任务成功率、工具调用正确率、延迟、输出 token 和每个已完成任务的总成本。
5. 逐步放量，在新配置得到验证前保留一个固定版本的回退模型。

## 核心结论

GPT-6 Astra 面向复杂 agent 工作，但可靠落地取决于它周围的系统。使用 Responses、只保留受支持的参数、
明确规定模型的工作行为，并用真实任务验证完整工作流。

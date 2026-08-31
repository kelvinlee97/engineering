# 每家公司都应该拥有一个“大脑”

[English](summary.md) | 简体中文

## 来源

- 视频：[Every company should have a Brain — Garry Tan, Y Combinator](https://www.youtube.com/watch?v=eBUyTS7SzV4)
- 发布者：AI Engineer
- 时长：21:08
- 来源覆盖：已完整读取 YouTube 自动生成的英文 Transcript，00:01–20:48

本文只整理 Garry Tan 在视频中提出的主张与案例，不独立验证其中的效率或营收数字。自动生成字幕可能存在识别错误。

## 核心论点

Tan 认为，普通与极高 AI 杠杆之间的差异不在模型本身：人们可能使用相同的模型权重、context window 和 API，却得到截然不同的结果。真正的杠杆来自如何组织工作。他观察到的高增长创始人把 AI 当成 workforce，而不只是 autocomplete；不过，他也明确表示无法证明 AI 生成代码导致了这些增长。

他提出的 AI 原生公司，是一个精简的人类团队：把重复工作编码为 agent 可读的 skills、路由规则、测试和经过治理的组织记忆。在这个模型里，使用 agent 不只是写软件，而是在招聘、训练和管理一支部分由 Markdown 与代码表达的 workforce。

视频依据：[03:00](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=180s)、[03:22](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=202s)、[05:52](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=352s)

## 把 skills 变成组织的运行方式

Tan 把 agent 基础设施映射成一家公司：

- Skill file 是拥有单一、明确能力的员工；
- Resolver table 是负责分派任务的组织图；
- Filing rules 是内部流程；
- Trigger evaluations 是检查正确指令是否被加载的绩效评估。

他说，一些 YC 的 AI 原生公司把销售、客服、运营和财务工作编码为可复用 skills，再聘请工程师维护这些 skills，并处理尚未覆盖的任务。这并不限于程序员：他还描述了 YC 的媒体、活动和财务人员自行构建 skills、cron jobs 与内部应用。

视频依据：[04:31](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=271s)、[06:45](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=405s)、[07:43](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=463s)

## 把计算放到正确的位置

视频区分两类计算：

1. **Latent space：** 让模型处理品味、判断、理解模糊的人类意图，以及其他非确定性选择；
2. **Deterministic space：** 让普通代码和数据结构负责精确存储、约束与可重复计算。

Startup School 的座位安排案例需要两者结合：LLM 可以判断哪些参与者适合认识，但 800 个座位的精确排列应放在确定性结构里，而不是 context window。Tan 认为，许多 AI 工程问题都源于把工作放在这条边界的错误一侧。

视频依据：[08:36](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=516s)、[09:04](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=544s)、[09:37](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=577s)

## 公司大脑：图书馆加图书管理员

Agent 的工作记忆可以远超个人，但一家公司拥有的信息仍远大于任何单次 context window。Tan 把 company brain 定义为两部分：图书馆包含邮件、会议、决策、客户对话和复盘；图书管理员则为当前任务挑选最相关的一小部分。Retrieval 只是底层能力，真正困难的产品问题是：什么值得记录、知识如何连接、哪些内容进入 hot memory，以及事实冲突时由谁裁决。

他称自己的系统约有 22 万页，来源包括邮件、会议、20 年笔记和 agent 生成的材料。在回复创始人的危机邮件前，系统可以调出过往对话、经历过类似问题的 portfolio companies，以及当时有效的处理方法。他用这一点区分 assistant 与 colleague：后者会带着相关组织记忆行动。

视频依据：[10:53](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=653s)、[12:23](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=743s)、[12:53](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=773s)、[13:28](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=808s)

## 记忆必须具备生产级治理

视频承认，没人维护的 company brain 会变成“搜索能力很强的垃圾场”：系统可能极有信心地返回过时事实，错误的 skill 也可能永久固化错误流程。因此，真正需要的是“记忆加卫生”：为事实保留 provenance，在新旧信息冲突时进行检查，并由人和 agent 共同负责清理过时材料。Tan 建议把 company brain 当成生产基础设施，而不是无差别存储空间。

视频依据：[14:24](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=864s)、[14:46](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=886s)

## 不要做一次性工作

Tan 的实践规则是：把已经成功完成、未来还会重复的任务转成可复用 skill。如果 agent 的第一次输出不好，就纠正它；结果满意以后，应保存整个流程，而不是下次再次提出相同要求。能记录这些经验的组织会持续复利，不能记录的组织每天都会失忆。他的概括是：模型质量是租来的，积累下来的组织大脑才属于公司。

视频依据：[15:27](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=927s)、[16:24](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=984s)

## 他建议现在构建什么

视频最后建议从第一天就构建 AI 原生公司：保持小团队，把工作沉淀成可复用 skills，让技术型创始人继续贴近实现，并从第一周开始积累 company brain。Tan 也把记忆与 librarian 这一层视为尚未被占据的创业机会。他强调，概念比他偏好的具体工具重要，而且可以迁移到不同技术栈。

视频依据：[16:41](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=1001s)、[17:15](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=1035s)、[17:52](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=1072s)、[18:24](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=1104s)、[20:21](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=1221s)

## 内容边界

这是一场倡议性质的演讲，不是受控研究或实施规范。视频没有为 400× 效率主张提供独立证据，没有证明 AI 生成代码与公司增长之间的因果关系，也没有详细讨论隐私、安全、访问控制、评估质量、运行成本或劳动影响。结尾的医疗案例属于激励性叙述，而不是医疗建议。

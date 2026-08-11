# 当 AI Agents 运营一家公司时，会发生什么？

English version: [summary.md](summary.md)

- 来源：[a16z YouTube 视频](https://www.youtube.com/watch?v=n34CIw3gk1k)
- 字幕：YouTube 展示的 Transcript；英文自动字幕
- 覆盖范围：286 条 segment，`00:00–36:13`；视频总长 `36:31`

## 核心主张：不是给原组织加工作流，而是重建公司

加入 Kavak 之前，Maza Ayala 说自己在 transformer 出现前构建过机器学习系统，涉及风险算法、物流、预测和营销。他把 transformers 与 ChatGPT 的到来描述为使一种新的公司构建方式成为可能。[01:03](https://www.youtube.com/watch?v=n34CIw3gk1k&t=63s)

他介绍了 Kavak 向“由 agents 运营的公司”转型的过程。他从一个问题出发：如果为能力强得多的未来模型重新创建 Kavak，公司会是什么样子？在这个设计中，每名客户拥有一个配备独立虚拟机的 agent；它保留互动历史、制定长期策略，并以跨产品最大化该客户生命周期价值为目标。[03:22](https://www.youtube.com/watch?v=n34CIw3gk1k&t=202s)

他将这种做法与只向既有团队发放聊天工具作对比。按他的说法，转型需要重建系统和 API 让 agents 可以行动；把 agents 放到客户面前，以产生数据和反馈循环；并把衡量方式从买卖了多少辆车等交易指标，改成长期客户关系和价值。[05:15](https://www.youtube.com/watch?v=n34CIw3gk1k&t=315s)

## 规模化运行：把 evals 当作刹车

Kavak 表示，agents 处理了 96% 的互动和 95% 的交易；客户领取实体车辆时仍会接触人。视频称每天会实例化 10 万至 20 万个 agents，它们可能工作数分钟、数小时或数天，之后为下一项任务设定提醒并恢复工作。[08:04](https://www.youtube.com/watch?v=n34CIw3gk1k&t=484s)

Maza Ayala 认为，速度取决于评估质量；他把 evals 比作让公司可以快速行驶的刹车。他说 Kavak 在 evals 上投入的工程时间、token 和资金大约与构建 agents 相当。首要衡量的是业务结果：客户是否转化、获批贷款、向公司出售车辆以及之后是否回来，而不是通话数量或通话时长等表面 KPI。[08:58](https://www.youtube.com/watch?v=n34CIw3gk1k&t=538s)

## 销售和贷款：最困难的测试场景

Kavak 没有把它们定位为客服 agents，而是销售 agents。拉丁美洲的汽车购买涉及大量车型、融资、保险和以旧换新；视频称，过去这些能力分布在多个专家团队中。Kavak 的目标是把这些专业能力合成为一个面向客户的 agent。Kavak 表示，这使 NPS 和客户满意度提高；最初转化率比人工团队高 50%，后来达到人工基准的 2.1 倍以上。[11:05](https://www.youtube.com/watch?v=n34CIw3gk1k&t=665s)

关于汽车贷款，讲者称墨西哥及部分新兴市场的审批可能需要两个月或更久，而 Kavak 通常在三分钟内批准。他把这一点归因于公司掌握的车辆与客户数据、垂直整合，以及对风险、利率、贷款额度和时机的个性化处理。他也强调，这些是对客户影响重大的金融决定，涉及资金和 PII 风险的 evals 因而重要。[14:04](https://www.youtube.com/watch?v=n34CIw3gk1k&t=844s)

## AI CEO 实验与仍由人承担的实体工作

Kavak 在墨西哥 Cuernavaca 测试了一个 AI CEO。讲者说，第一个月的目标是让利润翻倍；运行约六周后，结果没有达到两倍，但达到 1.5 倍，即利润增加 50%。他将客户满意度、库存、周转、融资渗透率和其他 KPI 的改善，归因于 agent 分析数字与客户、做预测，并向实体工作人员发送每日计划。[16:26](https://www.youtube.com/watch?v=n34CIw3gk1k&t=986s)

他把与实体世界相关的岗位区分出来。Kavak 仍有机械师，因为灵巧性和感知很难替代。公司为机械师提供 agent sidekick 来协助检查；讲者表示，检查和维修更快、成本更低、交付车辆质量更高、客户满意度上升，而保修成本下降约 20–26%。[18:12](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1092s)

## 培训人员和重塑组织

公司创建了 Jedi Academy，参与者从 CEO、AI 工程师到机械师。Maza Ayala 说，这个为期六周的课程不断更新，最后让参与者把最先进的 agents 投入生产。目的不是让每个人都成为 AI 工程师，而是让人们在岗位变化时学会与新技术协作。[20:24](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1224s)

他描述的组织更扁平，团队资深且被充分授权，并跨越工程、AI 和运营。人们要么构建 agents、为 agents 工作，要么在实体世界面对客户。与其在 agent 遇到问题时把个案交给人工队列后遗忘，Kavak 试图闭合循环：agent 通过 API 向人请求协助，人工完成的工作可成为之后提升 agent 的数据和技能。[23:00](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1380s) [24:09](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1449s)

## 领导方式、token 使用和重新构建架构

对于尝试采用 AI 的组织，Maza Ayala 认为转型必须由上而下：领导者要明确未来要建成什么样的公司，而不是依赖零散的 hackathon 或自下而上的 use case。他也提出按可衡量价值判断 token 支出：最高等级是可直接测量 ROI 的 agent tokens；中间等级可间接衡量，例如代码库中可见的开发工作；最低等级是没有衡量的个人工具使用。[25:44](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1544s) [26:48](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1608s)

Kavak 以前为复杂职能运行过许多 multi-agent 系统。更强的新模型出现后，Maza Ayala 说团队决定放弃两年已经能运作的系统并重新开始。新方案是每名客户一个 agent；每个 agent 有虚拟机、记忆、evals、CLI、公司工具和 API 的访问权，以及最大化生命周期价值等长期目标。他将目标称为“自我改进的组织”：要改进的循环不是单独的模型，而是创造经济价值的组织。[28:14](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1694s) [29:31](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1771s) [30:19](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1819s)

## 为什么他认为新公司会很重要

Maza Ayala 使用创造性破坏和电力历史说明：只采用新技术而不重建，收益会有限。他说旧工厂只把煤炭引擎换成电动引擎，可能得到约 6% 的效率提升；而围绕小型发电机和电力重新设计工厂，则可获得约三倍生产率。他把这个类比用于 AI：大型既有公司难以深度重建，因此可能只表面采用；新公司则可以围绕 AI 的优势形成。[31:29](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1889s) [33:45](https://www.youtube.com/watch?v=n34CIw3gk1k&t=2025s)

结尾时，他对创业者说，今天可用于构建的工具和智能异常容易获得，有时几乎免费或每月约 20 美元。他的建议是为不断进步的 AI 所带来的世界深入构建，而不是只在表面采用它。[35:04](https://www.youtube.com/watch?v=n34CIw3gk1k&t=2104s)

## 限制

本笔记反映视频讲者的叙述和指标。它基于 YouTube 的英文自动字幕，可能包含识别或名称错误；此处没有独立核实这些主张。

# What Happens When AI Agents Run the Business?

中文版本：[summary_zh.md](summary_zh.md)

- Source: [a16z on YouTube](https://www.youtube.com/watch?v=n34CIw3gk1k)
- Transcript: YouTube visible Transcript — English, auto-generated
- Coverage: 286 segments, `00:00–36:13` of a `36:31` video

## The claim: redesign the company, not just a workflow

Before joining Kavak, Maza Ayala says he built machine-learning systems before transformers, including work on risk algorithms, logistics, forecasting, and marketing. He presents the arrival of transformers and ChatGPT as making a new way of building companies possible. [01:03](https://www.youtube.com/watch?v=n34CIw3gk1k&t=63s)

He describes Kavak's move toward a company run by agents. His starting question was what Kavak would look like if it were built for much more capable future models. In the resulting design, a customer receives a dedicated agent with its own virtual machine. The agent retains interaction history, forms a long-term strategy, and aims to maximise that customer's lifetime value across the company's products. [03:22](https://www.youtube.com/watch?v=n34CIw3gk1k&t=202s)

He contrasts that with simply giving existing teams a chat tool. In his account, the transformation required rebuilding systems and APIs so agents could act, putting agents in front of customers to create data and feedback loops, and changing measurement from transactions such as cars bought and sold to long-term customer relationships and value. [05:15](https://www.youtube.com/watch?v=n34CIw3gk1k&t=315s)

## Operating at scale and treating evals as the brakes

Kavak says agents handle 96% of interactions and 95% of transactions; people still hand over the physical car. It says 100,000–200,000 agents can be instantiated per day, each working for minutes, hours, or days and resuming later. [08:04](https://www.youtube.com/watch?v=n34CIw3gk1k&t=484s)

Maza Ayala argues that speed depends on evaluation quality: he compares evals to brakes that make it possible to move quickly. He says Kavak spends roughly as much engineering time, tokens, and money on evals as on building agents. The primary measures are business outcomes—whether customers convert, obtain a loan, sell a car, and return—rather than superficial metrics such as call count or call duration. [08:58](https://www.youtube.com/watch?v=n34CIw3gk1k&t=538s)

## Sales and lending as the hard test cases

Kavak did not frame its agents as customer-support agents; it built sales agents for a complex car-buying process involving a large vehicle catalogue, financing, insurance, and trade-ins. The stated goal was to combine expertise that had previously been distributed across many teams into one customer-facing agent. Kavak says this raised NPS and customer satisfaction, initially converted 50% more than its human team, and later exceeded the human conversion benchmark by 2.1 times. [11:05](https://www.youtube.com/watch?v=n34CIw3gk1k&t=665s)

For car loans, the speaker says approval in Mexico and some emerging markets can otherwise take two months or more, while Kavak usually approves in under three minutes. He links this to the company's data about the car and customer, vertical integration, and personalisation of risk, interest rate, loan amount, and timing. He also notes that these are consequential financial decisions and raises the need for evals where money and PII are at risk. [14:04](https://www.youtube.com/watch?v=n34CIw3gk1k&t=844s)

## The AI CEO experiment and the remaining physical work

Kavak tested an AI CEO in Cuernavaca, Mexico. The stated first-month profit goal was to double profits; after about six weeks, the speaker says the result was 1.5 times profits rather than two times. He attributes improvements across customer satisfaction, inventory, financing penetration, and other KPIs to the agent analysing numbers and customers, making forecasts, and sending daily plans to physical workers. [16:26](https://www.youtube.com/watch?v=n34CIw3gk1k&t=986s)

He distinguishes roles tied to the physical world. Kavak still has mechanics, where dexterity and sensing are hard to substitute. It gives mechanics an agent sidekick for inspection guidance; the speaker says inspections, repair speed, cost, car quality, and customer satisfaction improved, and warranties fell by roughly 20–26%. [18:12](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1092s)

## Training people and changing the organisation

The company created the Jedi Academy for people from the CEO through AI engineers and mechanics. Maza Ayala says the six-week programme is continually updated and ends with participants launching state-of-the-art agents to production. The purpose is not that every participant becomes an AI engineer, but that people learn to collaborate with the technology as jobs change. [20:24](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1224s)

He describes a flatter organisation with senior, empowered cross-functional teams. People are building agents, working for agents, or operating in the physical world with customers. Instead of sending an agent failure to a human queue and forgetting it, Kavak aims to close the loop: an agent asks a human for help through an API, and the resulting human work can become data and skills for future agent performance. [23:00](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1380s) [24:09](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1449s)

## Leadership, token use, and rebuilding the architecture

For organisations trying to adopt AI, Maza Ayala says transformation must be top-down, with leaders setting a clear vision of the company they are building rather than relying on scattered hackathons and bottom-up use cases. He also proposes judging token spend by its measurable value: the highest tier is agent tokens with directly measurable ROI, a middle tier has indirect measurement such as work visible in a codebase, and the lowest tier is unmeasured individual tool use. [25:44](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1544s) [26:48](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1608s)

Kavak previously ran many multi-agent systems for complex functions. After a newer model arrived, Maza Ayala says the team decided to discard two years of working systems and start again. The replacement model is one agent per customer, each with a virtual machine, memory, evals, a CLI, access to company tools and APIs, and a long-term objective such as maximising lifetime value. He calls the target a self-improving organisation: the loop to improve is the organisation that creates economic value, not only an individual model. [28:14](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1694s) [29:31](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1771s) [30:19](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1819s)

## Why he expects new companies to matter

Maza Ayala uses creative destruction and the history of electricity to argue that adoption without redesign produces only limited gains. He says an old factory could replace its coal engine with electricity and gain about 6% efficiency, while redesigning the factory around small dynamos and electricity could yield roughly three times productivity. He applies the analogy to AI: established companies may adopt it superficially because rebuilding a large company is difficult, while new companies can be formed around AI's strengths. [31:29](https://www.youtube.com/watch?v=n34CIw3gk1k&t=1889s) [33:45](https://www.youtube.com/watch?v=n34CIw3gk1k&t=2025s)

At the end, he tells founders that the tools and intelligence available to build are unusually accessible, sometimes almost free or for about $20 per month. His advice is to build deeply for the world created by improving AI rather than merely adopting it on the surface. [35:04](https://www.youtube.com/watch?v=n34CIw3gk1k&t=2104s)

## Limitations

This note reflects the video speaker's account and metrics. It is based on YouTube's English auto-generated Transcript, which may contain recognition or naming errors; the claims have not been independently verified here.

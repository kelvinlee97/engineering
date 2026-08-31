# Every Company Should Have a Brain

[简体中文](summary_zh.md)

## Source

- Video: [Every company should have a Brain — Garry Tan, Y Combinator](https://www.youtube.com/watch?v=eBUyTS7SzV4)
- Publisher: AI Engineer
- Duration: 21:08
- Source coverage: Complete auto-generated English YouTube Transcript, 00:01–20:48

This summary reports Garry Tan's claims and examples as presented. It does not independently verify the performance or revenue figures, and auto-generated captions may contain recognition errors.

## The main argument

Tan argues that the difference between modest and extreme AI leverage is not the model: people can use the same weights, context window, and API yet obtain very different results. The leverage comes from how work is structured. The fastest-growing founders he observes treat AI as a workforce rather than autocomplete, although he explicitly says he cannot prove that AI-generated code caused their growth.

His proposed AI-native company is a thin human team whose recurring work is encoded into agent-readable skills, routing rules, tests, and a curated organizational memory. In this model, using an agent means hiring, training, and managing a workforce expressed partly through Markdown and code.

Video references: [03:00](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=180s), [03:22](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=202s), [05:52](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=352s)

## Skills as the operating organization

Tan maps agent infrastructure to a company:

- A skill file is an employee with one clearly described capability.
- A resolver table is an org chart that routes incoming work.
- Filing rules are internal operating procedures.
- Trigger evaluations are performance reviews that test whether the right instructions were loaded.

He says AI-native YC companies encode work in sales, support, operations, and finance as reusable skills, then employ engineers to maintain those skills and handle tasks not yet covered. He also stresses that this is not limited to programmers: he describes YC media, events, and finance staff building skills, cron jobs, and internal applications.

Video references: [04:31](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=271s), [06:45](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=405s), [07:43](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=463s)

## Put computation in the right place

The talk separates two kinds of computation:

1. **Latent space:** use the model for taste, judgment, interpreting vague human intent, and other nondeterministic choices.
2. **Deterministic space:** use ordinary code and data structures for exact storage, constraints, and repeatable computation.

The Startup School seating example combines both: an LLM can judge which attendees should meet, but the exact arrangement of 800 seats should live in deterministic structures rather than the context window. Tan says many AI engineering problems come from putting work on the wrong side of this boundary.

Video references: [08:36](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=516s), [09:04](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=544s), [09:37](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=577s)

## The company brain: library plus librarian

An agent may hold far more working context than a person, but a company contains much more than any single context window. Tan defines a company brain as both the library—emails, meetings, decisions, customer conversations, and postmortems—and the librarian that selects the small subset relevant to the current task. Retrieval is only the primitive; the harder product questions are what gets recorded, how knowledge is linked, what stays hot, and how contradictions are resolved.

He describes his personal system as roughly 220,000 pages derived from email, meetings, two decades of notes, and agent-generated material. Before responding to a founder crisis, it can retrieve prior conversations, comparable portfolio-company situations, and earlier remedies. His distinction is that an assistant answers a request, while a colleague acts with relevant organizational memory.

Video references: [10:53](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=653s), [12:23](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=743s), [12:53](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=773s), [13:28](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=808s)

## Memory needs production hygiene

The talk acknowledges that an uncurated brain becomes a searchable garbage dump: stale facts may be returned confidently, and a bad skill can preserve a bad process. The required primitive is therefore memory plus hygiene—provenance for facts, contradiction checks, and human-plus-agent curation that prunes obsolete material. Tan recommends treating the brain as production infrastructure rather than indiscriminate storage.

Video references: [14:24](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=864s), [14:46](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=886s)

## Never do one-off work

Tan's practical rule is to turn a successfully completed recurring task into a reusable skill. If an agent's first output is weak, correct it; once the result is satisfactory, preserve the process instead of asking for the same work again. An organization that captures these lessons compounds, while one that does not starts each day with amnesia. His formulation is that model quality is rented, but the accumulated organizational brain is owned.

Video references: [15:27](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=927s), [16:24](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=984s)

## What he recommends building

The closing recommendation is to build an AI-native company from day one: a small team, reusable skills, a technical founder who remains close to implementation, and a company brain that compounds from the first week. Tan also sees the memory and librarian layer itself as an open startup opportunity. He says the concepts matter more than his preferred tools and can travel across stacks.

Video references: [16:41](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=1001s), [17:15](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=1035s), [17:52](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=1072s), [18:24](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=1104s), [20:21](https://www.youtube.com/watch?v=eBUyTS7SzV4&t=1221s)

## Content boundaries

This is an advocacy talk, not a controlled study or implementation specification. It does not supply independent evidence for the 400× productivity claim, establish causation between AI-generated code and company growth, or detail privacy, security, access control, evaluation quality, operating cost, or labor consequences. Its medical anecdote is motivational rather than medical guidance.

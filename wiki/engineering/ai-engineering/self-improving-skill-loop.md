---
type: Pattern
title: Self-improving skill loop
description: A scheduled agent reads human feedback on another agent's output and opens a pull request that edits that agent's skill file.
tags: [agents, skills, feedback-loops]
sources:
  - id: warp-self-improving-agents
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/self-improving-agents/README.md
    title: How Warp Builds Self-Improving Agents on Claude
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: ai-native-company-structure-video
    resource: https://github.com/kelvinlee97/engineering/blob/main/YouTube/startup/building-and-structuring-an-ai-native-company--Z3JyAqh4ixg/summary.md
    title: Building and Structuring an AI-Native Company (video summary)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: kavak-agents-video
    resource: https://github.com/kelvinlee97/engineering/blob/main/YouTube/claude/what-happens-when-ai-agents-run-the-business--n34CIw3gk1k/summary.md
    title: What Happens When AI Agents Run the Business? (video summary)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:45:00Z }
status: draft
---

In this pattern an agent's behaviour improves by editing a text file, not the model. A second, scheduled agent reads human feedback on the first agent's work and opens a pull request that changes the [skill](../claude-code/agent-skill.md) file the first agent reads. There is no fine-tuning, embeddings store, or memory service.[^warp-self-improving-agents]

## The problem it solves

Warp's code review agent, used across roughly 800,000 monthly developers, kept making suggestions engineers had already rejected: the reviewer's explanation lived in one session's context and was discarded, so the next run read the same instructions.[^warp-self-improving-agents]

## Two loops

| | Inner loop | Outer loop |
| --- | --- | --- |
| Runs | Per task (every PR) | On a schedule, over many past runs |
| Reads | The skill file, the diff, repository context | Accumulated feedback and the skill file |
| Produces | The code review | A small, focused edit to the skill file |
| Applied by | Immediately, in the session | A pull request a person merges |

As described in the source.[^warp-self-improving-agents] The outer skill never does the task; it compares what the agent suggested with how people responded and proposes an edit.[^warp-self-improving-agents]

## Feedback quality over volume

A thumbs-down says the output was wrong but not why. A comment such as "our convention is that this kind of global variable uses this naming pattern" states a rule the improver can write into the skill. A small amount of detailed feedback from a senior engineer is worth more than a large volume of cursory ratings.[^warp-self-improving-agents]

## Adopting it

1. Keep the agent's instructions in a file in the repository.
2. Capture feedback as text, attached to the run it answers.
3. Write the improver as its own skill: read feedback since the last run, compare with the skill file, propose one small edit, open a PR.
4. Schedule it; per-task improvement has too little evidence and churns.
5. Review the PRs, rejecting one reviewer's preference presented as team convention.

[^warp-self-improving-agents]

## The same loop elsewhere

- YC's English-to-SQL data agent gained a second, overnight agent that reviews the day's failed queries and opens pull requests for them, so a query that failed one day may work the next.[^ai-native-company-structure-video]
- Kavak routes an agent's failure to a person through an API instead of a forgotten queue, and aims to turn the human work into data and skills for future agents.[^kavak-agents-video]

In all three, the improvement is proposed from observed failures and applied through a reviewable change.

## Where it breaks down (analysis from the source)

The note's author lists: skill files that grow into long, partly contradictory lists without periodic pruning; overfitting to the people who write the most feedback; product complaints turned into skill rules; and no measurement after merge, so a bad change shows up only slowly in later feedback.[^warp-self-improving-agents]

## Related

- Source: [What happens when AI agents run the business](../../sources/kavak-agents-video.md)
- Source: [Building and structuring an AI-native company](../../sources/ai-native-company-structure-video.md)
- [Agents propose, people and policy accept](propose-accept-boundary.md): why the improvement is a PR.
- Source: [How Warp Builds Self-Improving Agents on Claude](../../sources/warp-self-improving-agents.md)

[^warp-self-improving-agents]: How Warp Builds Self-Improving Agents on Claude
[^ai-native-company-structure-video]: Building and Structuring an AI-Native Company (video summary)
[^kavak-agents-video]: What Happens When AI Agents Run the Business? (video summary)

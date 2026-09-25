---
type: Pattern
title: Deterministic checks and model judgment
description: Put enforcement, exact data, and repeatable computation in deterministic code, and use a model only where judgment or interpretation is needed.
tags: [agents, architecture, governance]
sources:
  - id: company-brain-video
    resource: https://github.com/kelvinlee97/engineering/blob/main/YouTube/startup/every-company-should-have-a-brain--eBUyTS7SzV4/summary.md
    title: Every Company Should Have a Brain (video summary)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: ai-native-sdlc-playbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/ai-native-sdlc-playbook/README.md
    title: The AI-Native SDLC Playbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: claude-auto-mode
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/auto-mode/README.md
    title: How Claude Code Auto Mode Works
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:45:00Z }
status: draft
---
Several sources draw the same line: deterministic code for things that must be exact or enforced, the model for things that need judgment. Many AI engineering problems, one talk argues, come from putting work on the wrong side of this line.[^company-brain-video]

| Source | Deterministic side | Model side |
| --- | --- | --- |
| Company brain talk | Exact storage, constraints, repeatable computation, such as the arrangement of 800 seats | Taste, judgment, interpreting vague intent, such as who should meet |
| AI-native SDLC playbook | Enforcement, and monitoring that detects a breached control band | Judgment and diagnosis |
| Claude Code Auto Mode | Permission rules (`deny`, `ask`, `allow`) as hard enforcement | The classifier's guidance, which is not deterministic |

As stated in each source.[^company-brain-video][^ai-native-sdlc-playbook][^claude-auto-mode]

The practical rule that follows: never rely on a model to enforce a boundary that deterministic code can enforce. (Analysis: this wiki itself applies it, with `wiki_check.py` enforcing the format and the LLM writing the content.)

## Related

- [Least-privilege tool access](../claude-code/least-privilege-tool-access.md)
- [Company brain](company-brain.md)
- Source: [Every company should have a brain](../../sources/company-brain-video.md)
- Source: [The AI-Native SDLC Playbook](../../sources/ai-native-sdlc-playbook.md)
- Source: [How Claude Code Auto Mode Works](../../sources/claude-auto-mode.md)

[^company-brain-video]: Every Company Should Have a Brain (video summary)
[^ai-native-sdlc-playbook]: The AI-Native SDLC Playbook
[^claude-auto-mode]: How Claude Code Auto Mode Works

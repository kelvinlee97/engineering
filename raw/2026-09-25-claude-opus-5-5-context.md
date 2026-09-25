---
url: https://claude.com/blog/claude-opus-5-5-built-for-coding-sessions-that-use-more-context
fetched: 2026-09-25T00:00:00Z
title: Coding sessions are longer and use more context. Claude Opus 5.5 is built with that in mind.
---
# Coding sessions are longer and use more context. Claude Opus 5.5 is built with that in mind.

**Date:** September 24, 2026

**Reading time:** 5 min

**Author:** Michael Segner

---

## Key Points

Claude Opus 5.5 costs approximately 40% less to operate than Opus 5 for typical workloads billed by token, with the greatest savings for longer-running, higher-context sessions typical of Claude Code work.

## Claude Code Usage Trends (March-September 2026)

Recent data reveals significant shifts in how developers use Claude Code:

- Claude now works "3.3x longer on each prompt with more than 40% more model calls per prompt" and experiences "68% fewer interruptions"
- Context per request has grown 2.6x
- The input-to-output token ratio changed from 189:1 to 324:1
- Developers are twice as likely to use connected tool servers or skills
- Cached token reads now comprise the majority of agentic work costs

## Cost Efficiency Factors

Three primary changes drive Opus 5.5's cost-effectiveness:

**1. Reduced Pricing**
Input and output tokens cost 20% less, while cached token reads dropped 60% in price. A cached token on Opus 5.5 costs "a fifth of what it does compared to competing models."

**2. Improved Cache Management**
"Input that misses the cache decreased by more than 50%." Features like preventing accidental login resets and enabling effort-level changes without cache resets improve cache reliability. Subagents now start from parent cache rather than repaying for identical context.

**3. Fewer Task Turns**
Opus 5.5 can complete tasks in fewer turns than previous models, particularly on open-ended work. The model generates output over 30% faster than Opus 5.

---

**Key Recommendations:**
- Run `/usage` in Claude Code to monitor cached reads
- Choose your model at session start
- Set one-hour cache lifetime for long sessions on API keys or cloud providers

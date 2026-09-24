# Kelvin’s Engineering Notes

Practical notes on troubleshooting systems, working with AI coding tools, and making everyday engineering tasks easier.

I collect explanations, commands, and references worth revisiting, from SRE runbooks to developer tooling. Articles are available in English and Chinese.

## Start with a real problem

- **[Git branches have diverged. What next?](Git/README.md)** Inspect the state, choose a sync strategy, and recover safely.
- **[How should I publish changes to GitHub?](Git/publish-to-github/README.md)** Follow a beginner-safe branch, commit, push, pull request, and squash-merge workflow.
- **[A Pod is stuck Pending. Could it be IP capacity?](Kubernetes/runbooks/insufficient-ip-or-eni/README.md)** Distinguish subnet capacity, node limits, and other causes.

## Explore by what you want to do

### Troubleshoot and operate systems

- [Git](Git/README.md): Synchronisation, release tracking, rollback, and recovery; start with the [beginner publishing workflow](Git/publish-to-github/README.md).
- [Kubernetes](Kubernetes/README.md): Operations and incident runbooks.
- [AWS](AWS/README.md): Cloud references and runbooks grounded in official documentation.
- [Nginx & OpenResty](Nginx/README.md): Deployment and operations for beginners.
- [Node.js & Express](Nodejs/README.md): BFF deployment and incident response.
- [ZooKeeper](ZooKeeper/README.md): Operations and incident handling.

### Work with AI coding tools

- [Claude subagents](Claude/subagents/README.md): Study guide for Anthropic Academy’s introductory course.
- [Claude Code GitHub Actions](Claude/github-actions/README.md): Run interactive and automated Claude workflows with explicit permissions and security boundaries.
- [Claude Managed Agents](Claude/managed-agents/README.md): Hosted agent harness for long-running, asynchronous tasks, as an alternative to the Messages API.
- [AI-native SDLC playbook](Claude/ai-native-sdlc-playbook/README.md): Redesign delivery around versioned artifacts, feedback loops, and explicit governance gates.
- [Warp’s self-improving agents](Claude/self-improving-agents/README.md): Turn human feedback on agent output into reviewed pull requests against the agent’s own skill file.
- [GitHub Certified: Agentic AI Developer](Claude/github-agentic-ai-developer/README.md): Exam domains, course structure, and an in-depth look at agent architecture and SDLC integration.
- [Claude Code cloud sessions](Claude/cloud-sessions/README.md): Run sessions in an Anthropic-managed VM, hand work between terminal and cloud, and auto-fix pull requests.
- [Building an AI-native revenue organization](Claude/ai-native-revenue-org/README.md): Roll Claude out across a sales org, covering the maturity ladder, three-phase plan, ROI measurement, and common pitfalls.
- [Claude Projects, redesigned](Claude/projects/README.md): One conversation coordinates parallel cloud-session threads over shared memory and a shared library.

### Prepare for SRE interviews

- [Python exercises](Python/README.md): Log processing and algorithms.
- [Bash exercises](Bash/README.md): Log analysis and process inspection.

### Set up your development environment

- [Ghostty & terminal tools](Ghostty/README.md): Platform-specific setup and a reusable [Ghostty configuration](Ghostty/config.ghostty).
- [Ubuntu APT](Ubuntu/apt/README.md): Package installation, upgrades, inspection, and troubleshooting.
- [Apple Container](apple/container/README.md): Architecture, usage, and limitations.

### Explore ideas from videos

- [YouTube learning notes](YouTube/README.md): Video summaries organised by topic, including startups and AI agents.

## About these notes

These notes reflect personal study and experience; they are not official product documentation. I prioritise primary sources and distinguish personal interpretation from documented behaviour. The collection evolves as I study new topics and revisit existing notes.

Paired English and Chinese articles keep matching structure, links, and factual scope. Use the language link at the top of an article to switch.

## For contributors and maintainers

Keep contributions focused, reusable, and suitable for a public repository. Do not include credentials, employer or client code, confidential data, conversation history, caches, or machine-specific information.

- [Visual-first notes workflow](.agents/skills/visual-first-notes/SKILL.md): Turn source material into a plain-language framing, appropriate diagrams, and concise supporting text.
- [YouTube transcript workflow](.agents/skills/youtube-transcript/SKILL.md): How video summaries are prepared and checked.
- [Transcript tool module](youtube-transcript/): Supporting tooling.

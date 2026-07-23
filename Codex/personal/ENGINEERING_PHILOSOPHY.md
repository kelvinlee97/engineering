# Personal Engineering Philosophy

These principles apply across projects. Project-level `AGENTS.md` files should contain only project-specific additions or overrides.

## Close the Loop

Completion means the requested outcome is demonstrably deliverable, not merely that code was changed.

Work through the full loop whenever the environment and authorization allow:

1. Understand the intended user outcome.
2. Inspect the current implementation and runtime state.
3. Implement the smallest sufficient change.
4. Build and run the result.
5. Exercise the real user flow and relevant edge cases.
6. Fix defects found during verification.
7. Run focused regression checks.
8. Deliver only when the outcome is ready to use.

Do not leave verification to the user when it can be completed independently.

## Evidence Before Claims

Never use “should work” or “theoretically fixed” as a substitute for evidence.

Every completion claim should identify what was actually verified, such as:

- the build succeeded;
- the application launched;
- the affected workflow was exercised;
- the defect was reproduced and its regression check passed;
- the final artifact was inspected at its canonical location.

Clearly separate verified facts, static inference, unverified behavior, environmental limits, and remaining risk. Never claim an action or check that was not performed.

## Product-Level Quality

Technical correctness is an intermediate state. A change is deliverable only when the intended user can understand and use it successfully.

Consider whether:

- the workflow is direct and convenient;
- behavior matches platform conventions;
- entry points and outcomes are obvious;
- errors and boundary states are understandable;
- the change creates unnecessary choices, friction, or confusion.

Apply professional judgment rather than mechanically reproducing the request.

## Stable Delivery

Each project should have one canonical, predictable delivery location.

- Trace the complete artifact lifecycle—source, generation, distribution, installation, and launch—before judging whether delivery logic is correct.
- Distinguish a locally generated artifact from a public distribution artifact; an ignored build output may still be the correct local launch target.
- Update the existing delivery artifact instead of creating a new path each time.
- Keep internal checks and temporary artifacts out of the delivery location.
- State the single delivery location clearly.
- Do not present incomplete work as finished.

## Autonomy, Risk, and Authorization

Proceed independently on ordinary implementation details within the authorized scope.

Before merging, publishing, overwriting, migrating, or performing another high-impact action:

1. Inspect the current state.
2. Identify the affected targets and risks.
3. Continue only when the action is within scope and the risk is acceptable.
4. Ask when a material ambiguity, irreversible consequence, or new authority is involved.

Approval of a modification does not automatically authorize committing, pushing, publishing, or deleting unrelated material. Treat each authorization according to its explicit wording.

## Repository Hygiene

A public repository is part of the product. Commit only material with clear, durable value.

- Do not commit temporary checks, logs, screenshots, caches, generated artifacts, or internal agent notes.
- Keep stable regression tests only when they are repeatable, protect important behavior, and justify ongoing maintenance.
- Report one-off verification results, wait for confirmation, then remove temporary verification files before publishing.
- Keep documentation current, non-duplicative, and consistent with actual behavior.
- Report stale content outside the requested scope; do not remove it without authorization.

## Communication

Report outcomes and evidence rather than tool-call narration. Make the current state explicit:

- completed;
- in progress;
- verified;
- unverified or blocked;
- remaining risk;
- next action requiring authorization.

When corrected, extract the reusable engineering principle and avoid repeating the same class of mistake.

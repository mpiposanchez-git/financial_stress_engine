You are the coding agent for the repository "financial_stress_engine".

Your mission is to implement the entire backlog in:
- docs/implementation/backlog_master.md
AND to respect feature tiering and guardrails described in:
- docs/methodology/methodology_textbook.md
- docs/methodology/poc_flyer.md
- docs/methodology/brd_implementation_plan.md
- docs/implementation/backlog_summary

CRITICAL OPERATING RULES (must follow exactly):
1) Work in PR-sized tasks ONLY.
   - Implement exactly ONE task block at a time (e.g., WS1-01, then stop).
   - Do NOT start the next task until I explicitly reply "Proceed".
2) After finishing each PR-sized task, you must output:
   A) A concise summary of what changed (files created/modified, key logic).
   B) A checklist of commands I must run (backend tests + lint + frontend tests + typecheck).
   C) Any docs that must be updated due to the changes (and what you changed in them).
   D) The exact git commands I should run to commit and push the branch (branch name suggestion + commit message).
   E) Ask: "Proceed to next task?"
3) Testing discipline:
   - For every task, ensure relevant unit tests are added/updated.
   - Ensure existing tests remain passing.
   - Never change behaviour without adding or updating tests.
4) Documentation discipline:
   - If a task affects user-visible behaviour, API contracts, methodology, data sources, privacy, or tiering:
     - update the corresponding doc sections in docs/methodology_textbook.md and/or docs/brd_backlog.md and/or docs/poc_flyer.md.
   - Keep documents consistent with code. No contradictions.
5) Guardrails (non-negotiable):
   - Clerk authentication stays ALWAYS ON; remove/avoid any bypass flags.
   - Premium features MUST be enforced server-side (entitlement checks), not only UI.
   - Do not store user scenario inputs/outputs server-side.
   - Do not log request bodies or auth tokens.
   - Money uses integer pence; rates/shocks use integer basis points; explicit rounding (round-half-up).
   - UK benchmark ranking uses BHC (Before Housing Costs) by default.
6) Scope discipline:
   - Do not refactor unrelated code.
   - Keep each task small, reviewable, and auditable.
   - If you detect missing/ambiguous requirements, propose the smallest safe assumption and document it in the task summary (do not ask new questions unless absolutely necessary).

EXECUTION ORDER:
Follow the order of tasks in docs/poc_backlog_master.md:
- Start from WS1-01 and proceed sequentially through WS9.
- Do not skip tasks unless they are already implemented; if already implemented, summarize evidence (files/tests) and mark as done.

NOW START:
Implement the first PR-sized task in the backlog: WS1-01 — Mortgage module extraction.

When you finish WS1-01, stop and provide the required summary + checklist + docs updates + git commands, then ask me to proceed.
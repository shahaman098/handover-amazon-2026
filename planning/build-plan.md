# Build plan: mut-r1-07-evidence-handoff-ledger

Build Handover as a tightly bounded Alexa+ conversational simulation for an applicant and community adviser reconciling fictional documents. Preserve the existing medium delivery risk and dependencies: transactional persistence, an inspectable dependency graph, and an executable confirmation workflow. The demonstrable result is a durable, attributed supersession transaction, precise assessment updates, and an exported handoff receipt. Allocate the supplied ten focused hours in dependency order, reserving recording and submission time; these slots are planning limits, not a delivery guarantee.

Scheduling: **scheduled**
Build window: Planning budget: ten focused development hours on Friday 23 October 2026, solo from scratch. Submission deadline 20:00 Europe/London; aim to submit by 18:00. At review time approximately fifteen elapsed hours remained. Reserve time for recording and submission; stop optional features before the deadline.

## Existing feasibility (reused, not reassessed)
- Delivery risk: medium
- Non-fakeable core: Applicant confirmation must cause an actual durable, attributed supersession transaction that preserves history, updates precisely the affected assessments and rejects stale writes without partial mutation.
- Minimum loop: Load conflicting fictional assertions. Have the helper propose a correction, retrieve its source and require applicant confirmation. Commit the replacement, display the affected dependency closure and export a receipt retaining unresolved conflicts. Reload to prove persistence, reject a stale correction and check cycle rejection. Deliver runnable licensed source, English documentation and feedback, public demonstration video and completed Devpost entry.
- Critical dependencies: A transactional persistent ledger enforcing version checks, append-only history and atomic correction acceptance., A complete small dependency graph with independently checked invalidation and recomputation, including unaffected nodes., An executable conversational confirmation workflow plus repository, public video, feedback and submission artifacts within the available time.
- Permitted mocks: Fictional documents, pre-extracted assertions and explicitly fictional benefits rules., Two clearly labeled simulated roles instead of production authentication., A fixed small dependency graph and local receipt export.
- Notes: Feasible only as a tightly bounded local simulation with prepared assertions; OCR, real benefits rules, real identity and distributed collaboration would threaten the ten-hour budget. The transactional graph semantics create more failure cases than the polished demo suggests. Simulated role selection proves workflow attribution, not authenticated identity. No real applicant data or benefits expertise is needed for the explicitly fictional scope. Existing gate passes provide no implementation evidence.

## Architecture
- A local web conversational client supports source inspection, correction proposals, clarification, applicant confirmation, and receipt export. Label the experience as an entrant-built Alexa+ simulation and both roles as simulated.
- Bundle one fictional case with three original documents, prepared assertions, two dependent draft answers, unrelated ID evidence, a preparation checklist, and explicitly fictional program rules.
- A server owns the persistent append-only ledger and all mutation guards. Confirmation binds the proposal contents, replacement assertion, source version, simulated actor session, and expected case revision.
- One atomic transaction records confirmation, replacement, attribution, supersession, affected assessment IDs, and the new case revision. Preserve original assertions and reject stale, changed, cyclic, or unauthorized-by-workflow proposals without partial mutation.
- An inspectable authored acyclic graph drives dependent-closure invalidation and topological recomputation. Preserve unresolved conflicts; unknown dependency coverage marks relevant answers unresolved and blocks ready-to-export status. A diagnostic handoff receipt remains exportable.
- Use bounded typed conversation as the declared runtime fallback without requiring a model, API key, speech recognition, hardware, or AWS. Attempt MCP only within the first-hour gate; retain it only if specification 2025-11-25 or later over Streamable HTTP is actually demonstrated.

## Tasks
### T1: Prove the conversational runtime and durable mutation path
- Owner role: Solo developer — runtime integration
- Depends on: none
- Slot: Focused hour 0–1
- Deliverable: A runnable local conversational simulation with one proposal, explicit confirmation, server-side revision check, durable append, and reload; a recorded runtime-route decision.
- Acceptance test: Within the first-hour gate, type a correction, inspect the proposed replacement, confirm it, and reload to recover the appended event. Before confirmation, persistence remains unchanged. If Codex CLI application integration is tested but fails or has unsuitable latency, repeat using declared bounded typed conversation. Retain MCP only after an actual compliant Streamable HTTP exchange; otherwise use the simulation route. If no complete runtime-to-transaction path works, record the failed gate rather than claiming the selected core is demonstrated.

### T2: Author the fictional case and independent expected outcomes
- Owner role: Solo developer — fixture and verification design
- Depends on: T1
- Slot: Focused hour 1–2
- Deliverable: Three original fictional documents, prepared conflicting assertions, a branching dependency manifest, two draft answers, unrelated ID evidence, checklist state, and separately authored expected affected/unaffected sets.
- Acceptance test: Every assessment exposes its supporting assertion and source-version IDs. A manual source-to-answer table agrees with the graph. Include an unresolved conflict and an unknown-coverage case whose answer cannot become complete. Explain the applicant/helper handoff problem using the fixture without claiming validated demand or dependency completeness for unfamiliar documents.

### T3: Implement the complete provenance transaction
- Owner role: Solo developer — ledger and graph implementation
- Depends on: T2
- Slot: Focused hours 2–4
- Deliverable: Server-enforced atomic correction acceptance, append-only history, supersession edges, revision checks, dependent-closure invalidation, topological recomputation, and cycle rejection.
- Acceptance test: A confirmed correction preserves the original assertion and appends exactly one attributed replacement transaction. Its affected IDs match the independent expected set; unrelated ID evidence remains unchanged. Changed proposals require renewed confirmation. Duplicate confirmation, stale revision, wrong simulated actor session, cycle creation, and an interrupted failed commit produce no partial mutation. Reload preserves the committed state.

### T4: Complete the applicant/helper reconciliation and receipt loop
- Owner role: Solo developer — conversational interface
- Depends on: T3
- Slot: Focused hours 4–6
- Deliverable: A source-inspection conversation, ambiguous-reference clarification, exact-proposal confirmation screen, visible assessment transitions, preparation checklist, and downloadable handoff receipt.
- Acceptance test: Typing 'That is my old payslip. Use the September document instead' prompts clarification when multiple sources match. The selected source, old and proposed assertions, affected answers, actor session, and revision appear before confirmation. Cancellation makes no change. After confirmation, display withdrawn old conclusions and recomputed or unresolved answers. The receipt includes supersession history, source versions, confirmation, affected IDs, and remaining conflicts; unknown coverage blocks ready-to-export status while allowing a clearly marked unresolved handoff receipt.

### T5: Verify unseen corrections and failure behavior
- Owner role: Solo developer — verification
- Depends on: T4
- Slot: Focused hours 6–7.5
- Deliverable: A reproducible reset-and-check procedure, an independent state checker, and saved proof for the complete loop and rejected mutations.
- Acceptance test: Enter a previously unused correction value within the declared case schema and compare actual affected and unaffected outputs with the separately maintained dependency expectations. Check append-only history, exact closure, recomputation order, unresolved conflicts, unknown-coverage blocking, persistence after server restart, stale helper proposal rejection, and cycle rejection. Rejected requests leave ledger contents and revision unchanged. Exercise the bounded runtime fallback and label unsupported utterances rather than inferring a mutation.

### T6: Package reproducible source and submission materials
- Owner role: Solo developer — documentation and release
- Depends on: T5
- Slot: Focused hours 7.5–8.5
- Deliverable: Complete GitHub source and assets, setup/reset/run/check instructions, license or authorized private access, English project description, tool-by-tool feedback, and an evidence-backed limitations statement.
- Acceptance test: Follow the documented setup from a clean local state and reproduce the correction, receipt, restart, and stale-write rejection without assumed credentials. Documentation identifies the selected Alexa+ simulation route, bounded conversation behavior, fictional data, authored dependencies, simulated attribution, and qualifying development work. Every used tool, API, and SDK has purpose, strengths, shortcomings, onboarding experience, and reuse rationale.

### T7: Record the functioning demo and complete the entry
- Owner role: Solo developer — demonstration and submission
- Depends on: T6
- Slot: Focused hours 8.5–10, reserved for recording and submission
- Deliverable: A public YouTube or Vimeo video targeted below three minutes and a completed Devpost submission with verified repository and video access.
- Acceptance test: The English video shows actual input, clarification, exact confirmation, persisted supersession, affected and unaffected answers, unresolved receipt, reload, and stale-write rejection. Verify public playback and repository access. Complete required fields and confirm submission status, aiming for 18:00 Europe/London and respecting the 20:00 deadline. Stop optional features before consuming this reserved slot.

## Demo script
1. Reset to the bundled fictional case. Identify the applicant and adviser as simulated roles and the runtime as an entrant-built Alexa+ simulation. Show three documents, conflicting assertions, two draft answers, unrelated ID evidence, and the initial case revision.
2. As the adviser, inspect an answer's source, then type 'That is my old payslip. Use the September document instead.' Resolve the deliberately ambiguous reference by selecting its exact document version.
3. Enter a correction value not hardcoded into the demonstration, within the declared schema. Show the exact replacement, source version, affected answer IDs, actor session, and expected revision. Show that proposing it has not changed the ledger.
4. Switch to the simulated applicant and explicitly confirm the displayed proposal. Show one appended transaction, the retained original assertion, supersession edge, new revision, withdrawn old conclusions, and recomputed or unresolved dependent answers. Show unrelated ID evidence unchanged.
5. Run the independent checker and display its expected-versus-actual affected/unaffected IDs. Explain that this checks the authored graph, while unknown coverage remains unresolved and blocks completion.
6. Export and open the handoff receipt containing confirmation, provenance, affected IDs, and unresolved conflicts. Restart the local server and reload to show the same committed history and state.
7. Attempt the adviser proposal prepared against the old revision and show rejection with no ledger change. Show cycle rejection and, if the primary conversational runtime is unavailable, the rehearsed bounded typed fallback with the same mutation guards.

## Cut scope
- Keep one synthetic case, three documents, prepared facts, two dependent answers, and an inspectable authored graph. Exclude OCR, arbitrary dependency discovery, unfamiliar-document correctness claims, and real applicant records.
- Exclude real benefits eligibility, policy accuracy, causal inference, counterfactual optimization, validated demand, and validated impact claims. Position the build as a provenance transaction prototype.
- Use two explicitly simulated roles. Attribution records workflow actions and does not establish authenticated identity or independently verified consent.
- Never cut exact-proposal and revision-bound confirmation, server-side atomicity, append-only persistence, precise invalidation, stale-write rejection, cycle rejection, or unknown-coverage completion blocking.
- Cut live-model integration and MCP if they do not pass the first-hour gate; retain a functioning bounded typed conversational simulation and disclose its limits.
- Exclude multi-tenant login, distributed collaboration, external application actions, speech recognition, real Alexa+ deployment, gated tooling, and hardware integrations.
- Exclude Fire TV, Bee, Ring, AWS Builder, and Open Source mini-challenge work from this entry. Optional friction logs and feature requests use only already captured evidence after the main demonstration and mandatory artifacts are complete.
- If the first-hour complete runtime/transaction proof fails, record the supplied Departure Interlock fallback trigger explicitly; do not silently switch concepts or substitute an animation for this plan's core.

## Submission checklist
- Verify entrant eligibility, residence, conflicts, ownership, applicable support restrictions, and live Devpost registration; confirm final submission status before 20:00 Europe/London on 23 October 2026, aiming for 18:00.
- Select Alexa+ as the primary track using the functioning entrant-built simulation route. No mandatory framework, SDK, or MCP interface applies to that route. If MCP is retained and claimed, supply actual specification 2025-11-25-or-later Streamable HTTP runtime evidence.
- Provide a working application created during the qualifying period, or explain and demonstrate significant qualifying changes if any pre-existing project is used.
- Submit an English description covering the applicant/adviser workflow, operation, durable state change, fictional inputs, dependency limits, simulated roles, and bounded conversational behavior.
- Provide a GitHub repository containing all necessary source, original fixture assets, setup/run/reset instructions, verification procedure, and receipt export. Use a public repository with a detectable open-source license or private access for all specified reviewers; resolve the redacted Devpost reviewer details if using private access.
- Publish the functioning demonstration publicly on YouTube or Vimeo, target less than three minutes, and include its URL in Devpost. Show the accepted simulation actually operating with real local persistence and visible failure handling.
- Provide product feedback for every tool, API, and SDK used, including development assistance: purpose, strengths, shortcomings, onboarding, and whether and why it would be used again.
- Keep the project available free of charge and without testing restrictions through November 20, 2026 at 12:00 Pacific Time. A locally runnable repository and video satisfy the supplied Alexa+ access route; supply credentials if any private website is used.
- Provide English materials or translations, verify rights to code, data, media, and trademarks, and document dependency licenses. Use original fictional documents and avoid real applicant information.
- Leave optional mini challenges unselected for this scoped entry. Include friction logs or prioritized feature requests only if already captured without displacing required artifacts; ensure multiple submissions, if any, are substantially different.
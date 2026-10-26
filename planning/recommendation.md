# Recommendation: Handover

**Decision:** enter the Alexa+ track with a tightly scoped version of the engine's Evidence Handoff Ledger. Working product name: **Handover**.

**Pitch:** A voice-assisted application workspace that shows where each draft answer came from—and flags every affected answer when its supporting evidence changes.

## The customer and the problem

An applicant and a community adviser prepare an application for support. They exchange revised documents and corrections over several conversations. A new document can make several draft answers outdated, while other information remains current. A change message alone does not establish which answers were reviewed or which version the next adviser should trust.

Handover lets the applicant inspect a source, clarify a correction, approve the exact replacement, and hand over a packet with a persistent revision receipt. Its value proposition is keeping preparation work consistent during corrections and handoffs. Customer demand and effectiveness still need validation.

## The demo to build

Use one original synthetic case, three documents, two dependent draft answers and a small preparation checklist.

1. Show a draft answer linked to an August payslip, plus unrelated identity evidence.
2. The applicant says or types: “That is my old payslip. Use September instead.” If the reference is ambiguous, ask which document.
3. Show the proposed replacement, affected answers and exact case revision. Ask for confirmation.
4. Commit the change once. Mark dependent answers stale and preserve unrelated evidence. Show a short explanation of each affected answer.
5. Review the corrected answers and export a handoff packet with current source references, unresolved items and a revision receipt.
6. Reload to show persistence. Attempt an adviser edit prepared against the old revision; reject it without overwriting the accepted correction.

The decisive proof is a server-enforced state change. A judge should be able to introduce another correction within the declared case schema and obtain the correct affected/unaffected result.

## The actual technical contribution

Maintain an explicit graph from versioned documents to prepared facts, draft answers and checklist items. A confirmed source change invalidates its dependent closure. Database transactions and revision checks prevent partial or stale writes. Confirmation is bound to the exact proposed change; modifying a proposal requires fresh confirmation.

Keep the dependency graph authored and inspectable. Unknown dependency coverage leaves outputs unresolved and prevents a “ready” status. This prototype does not establish authoritative eligibility decisions, automatic understanding of arbitrary documents, authenticated identity, causal inference, or real-world savings.

Aim to expose source inspection, proposal, confirmation and export as genuine MCP tools through Streamable HTTP, with a custom Alexa+-style web client. The first-hour spike must prove the transport and one complete persisted mutation. A working, accurately labelled conversational simulation is also an accepted event route. Do not imply a connection to a real Alexa+ device or the unavailable partner console.

## Why this is my choice

The live HackForge run generated 48 candidate variants, collision-audited 12, reviewed 11 for feasibility, and blind-judged six finalists. Five of six judge roles preferred Evidence Handoff Ledger; it won all five of its pairwise comparisons. The demo-risk role preferred the simpler Departure Interlock.

The automatic final report promoted Rep Trace after red-team review. That promotion explicitly depended on first proving a Fire TV runtime and remote navigation. The local machine has a configured phone emulator but no TV profile, and the feasibility review rated Rep Trace high risk. I do not treat that conditional promotion as a demonstrated reason to change tracks.

This is therefore a **human recommendation after reviewing the engine**, rather than its automatic final primary. The original report is preserved unchanged. The red team's criticism still matters: a ledger is a familiar mechanism, demand is unvalidated, a hand-authored graph can omit dependencies, and a conversational interface must earn its place. The narrow scope and adversarial demo above address delivery and proof; they do not erase those uncertainties.

| Official criterion | What the entry should demonstrate |
|---|---|
| Tech Implementation | Real tool calls, atomic corrections, selective invalidation, persistence and stale-write rejection |
| Design | One clear conversation with visible sources, clarification and an understandable confirmation card |
| Potential Impact | A specific applicant/adviser handoff problem; treat the benefit as a hypothesis until tested |
| Quality of the Idea | Correction-aware, evidence-linked conversational work with a coherent end-to-end result |

The four criteria are equally weighted. Friction logs can receive a discretionary bonus of up to 10%; record only actual observed tool friction and useful reproduction details.

## Delivery boundary

Budget approximately ten focused development hours, including verification and packaging. Use the accompanying [build plan](build-plan.md). Prove the persisted correction loop first, then build the smallest interface that exposes it clearly. Freeze features before recording. Aim to submit by **18:00 UK time**, leaving two hours before the official deadline.

Exclude OCR, live benefits rules, real applicant data, multi-tenant authentication, external account actions, real Alexa+ deployment, and extra prize work until the main demo is complete. No AWS runtime access, active local model service, speech recognition or special hardware has been confirmed. The engine's Codex CLI authentication worked; application-runtime integration and latency still require a spike.

**Fallback:** Departure Interlock, the demo-risk judge's preference, if the first-hour Handover transaction/runtime proof fails. It has a smaller implementation surface but a weaker originality and impact case. Rep Trace is conditional on a separately proven TV runtime.

## Event and submission facts

- Event: [Build, Ship, Shape: Amazon Developer Hackathon](https://amazonappdev2026.devpost.com/).
- Deadline: **Friday 23 October 2026, 20:00 Europe/London** (19:00 UTC / 12:00 PDT). Rechecked against the [official updates](https://amazonappdev2026.devpost.com/updates) on 23 October.
- The local tracker records registration, citing the 30 September confirmation. Live submission/account status remains unverified because the Devpost connector needs reauthentication.
- Submit the project explanation, runnable GitHub source with appropriate licence/access, a public functioning-demo video under three minutes, track selections, and specific tool-by-tool product feedback. See the [formal rules](https://amazonappdev2026.devpost.com/rules).
- Amazon explicitly permits an entrant-built Alexa+ simulation or a real MCP client/server demo without physical hardware or gated partner tools. A locally runnable repository and video can suffice without permanent hosting. See the [FAQ](https://amazonappdev2026.devpost.com/details/faqs).

The plan is a competitive hypothesis, not a prediction or guarantee of a prize.

## Supporting artifacts

- [Original completed engine recommendation](engine-runs/corrected/2026-10-22-competition-brief-input-2/final-recommendation.md)
- [Blind judging and pairwise comparisons](engine-runs/corrected/2026-10-22-competition-brief-input-2/blind-judge-results.json)
- [Human selection and scope conditions](research/selection-review.json)
- [Execution notes, rule correction and limitations](research/engine-run-notes.md)
- [Public analogues supplied to collision review](research/manual-analogues.json)

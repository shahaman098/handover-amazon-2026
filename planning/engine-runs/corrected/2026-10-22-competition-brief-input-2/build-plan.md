# Build plan: concept-026

Build Rep Trace for older adults following one previously selected home routine: real Fire TV remote confirmations and monotonic timer events drive progression, three-valued temporal verdicts, and reproducible subset-minimal explanations. Retain the existing high delivery risk and immediate platform smoke-test gate. The relative slots allocate the supplied approximately 10 focused build hours; recording and submission require an additional reserve and completion is not guaranteed.

Scheduling: **scheduled**
Build window: Participant execution planning assumption: approximately 10 focused build hours remaining, one developer starting from scratch, before 2026-10-23 20:00 Europe/London. Reserve additional time for recording and submission. Official qualifying dates remain in facts.

## Existing feasibility (reused, not reassessed)
- Delivery risk: high
- Non-fakeable core: Real remote and timer events must feed the evaluator that controls progression, producing satisfied, violated, or indeterminate results and an executable subset-minimal explanation for the same identified violation.
- Minimum loop: Deploy to an accepted Fire TV runtime and complete one short routine using remote input. Request the next set early to trigger a live block and computed counterexample; remove each necessary event and rerun to verify that specific violation disappears. Demonstrate a missing-confirmation indeterminate result and a corrective action. Publish runnable licensed source, English instructions and tool feedback, a short public platform-demo video, and the completed submission.
- Critical dependencies: A proven Fire OS or Vega OS deployment and remote-control route on an actual device or accepted emulator, currently unconfirmed., Consistent three-valued temporal evaluation and trace minimization that preserves the same violation without corrupting session context., Delivery of the TV interface, live event capture, corrective interaction, reproducible repository, and required submission artifacts within the solo time budget.
- Permitted mocks: One original minimal instructional routine., Clearly labeled synthetic regression traces., Remote-reported repetitions and preparation instead of sensed movement.
- Notes: Retain only with an immediate platform smoke-test gate; abandon if deployment consumes the implementation budget. This has fewer lifecycle obligations than Ready-Window but still combines unfamiliar platform work with nontrivial evaluator semantics. Event removal can turn a violation into missing context, so minimality must be defined against a fixed rule and session horizon. Keep the claim limited to reported sequence events; physical safety and exercise effectiveness are unproven. Copied conditional technology roles and deterministic gate passes are not compliance evidence.

## Architecture
- One local application running on Fire OS or Vega OS through a proven accepted device or emulator, with readable TV instructions, remote focus navigation, instruction replay, and corrective actions.
- One original authored routine and explicit temporal rules. Record preparation acknowledgements, reported repetitions, rest starts/completions, next-set requests, and stop requests with monotonic timestamps and session identifiers.
- A deterministic finite-state evaluator consumes the actual event log and controls progression. Report satisfied, violated, or indeterminate over an explicit session horizon; missing confirmations never establish incorrect movement.
- A trace reducer reruns the same evaluator against a fixed rule, violation identity, routine configuration, and session horizon. Preserve event order and original timestamps; return a subset-minimal trace, without claiming a globally shortest explanation.
- A local replay view exposes inputs, verdicts, responsible events, and removal checks. Keep generated regression traces visibly separate from sessions captured through actual remote use.

## Tasks
### T1: Prove the accepted Fire TV runtime and remote route
- Owner role: Solo developer — platform
- Depends on: none
- Slot: Focused build hours 0–1; immediate go/no-go gate
- Deliverable: A minimal application installed on Fire OS or Vega OS with a documented launch route, focusable controls, and recorded remote input.
- Acceptance test: Launch on the actual device or accepted emulator and use directional navigation plus Select to change visible application state. Record runtime identity and reproduction commands. If this route fails within its allocated slot, invoke the existing abandonment condition rather than substitute a desktop mock.

### T2: Implement the routine model and three-valued evaluator
- Owner role: Solo developer — verification
- Depends on: T1
- Slot: Focused build hours 1–3
- Deliverable: One authored routine, event schema, monotonic clock abstraction, finite-state evaluator, and labeled regression inputs.
- Acceptance test: For a demonstration rest rule of 10 seconds, a next-set request at rest-start plus 3 seconds is violated; a request after recorded rest completion is satisfied; absent preparation acknowledgement is indeterminate. Show the fixed session horizon and rule identifier. Reordering relevant events or changing rest duration changes the appropriate verdict. Unknown prerequisite context cannot silently pass.

### T3: Connect real remote events to controlled progression
- Owner role: Solo developer — application
- Depends on: T2
- Slot: Focused build hours 3–6
- Deliverable: A complete TV loop covering preparation, reported repetitions, timed rest, next-set requests, correction, instruction replay, and session termination.
- Acceptance test: Complete one routine using the remote. An early next-set request is logged but leaves progression blocked. Missing preparation produces an indeterminate explanation and blocks progression until an explicit acknowledgement or session end. A later acknowledgement is timestamped as a new report and does not rewrite earlier events. Stop ends the session and prevents pending timers from advancing it. Screens distinguish reported events from observed physical performance.

### T4: Compute and replay subset-minimal explanations
- Owner role: Solo developer — verification
- Depends on: T3
- Slot: Focused build hours 6–8
- Deliverable: A reducer and TV explanation view generated from the same captured event log used for progression.
- Acceptance test: Capture an early-next-set violation with irrelevant events present. Reduction retains the rest-start and early request while removing irrelevant events. Under the unchanged rule, configuration, timestamps, and horizon, the reduced trace preserves that specific violation; removing either retained event eliminates that violation, potentially yielding indeterminate. Replay the captured log to reproduce its verdict. Display the subset-minimal qualification and missing-context limits.

### T5: Verify the demonstrable loop and package reproducible source
- Owner role: Solo developer — release and QA
- Depends on: T4
- Slot: Focused build hours 8–10
- Deliverable: Runnable licensed repository, English setup and testing instructions, repeatable demo inputs, tool feedback, and a recording-ready application.
- Acceptance test: Follow documented setup from a clean checkout on the proven runtime. Reproduce complete, early-request, and missing-confirmation cases through live remote use and labeled replay. Introduce an unrecorded-in-the-script rest-duration change and verify that the evaluator and explanation respond consistently. Confirm focus visibility, readable explanations, replay, correction, and stop. Document every used tool/API/SDK and all remaining limitations.

### T6: Record the platform proof and complete the submission
- Owner role: Solo entrant — submission
- Depends on: T5
- Slot: Additional recording and submission reserve specified by the build window; after T5 and before 2026-10-23 20:00 Europe/London, with no invented duration
- Deliverable: Public YouTube or Vimeo video under three minutes, complete Devpost entry, accessible repository, project description, and product feedback.
- Acceptance test: Check the public video and repository links without entrant authentication. Video shows the accepted Fire TV runtime, real remote input, timer-driven blocking, computed trace removal checks, indeterminate handling, and correction. Confirm all required Devpost fields and Fire TV selection before the supplied deadline. If build work consumes the additional reserve, report the incomplete artifacts rather than claiming submission readiness.

## Demo script
1. Show the accepted Fire TV device or emulator, runtime identity, remote navigation, and one original routine. State that Rep Trace tracks reported sequence events, not body position, exercise suitability, or physical safety.
2. Start a real session, acknowledge preparation, report repetitions, and start the visible 10-second demonstration rest. Request the next set after approximately 3 seconds. Show actual recorded timestamps, a violated verdict, blocked progression, and the incomplete-rest explanation.
3. Open the computed explanation. Show irrelevant events removed and the retained rest-start/early-request pair. Rerun after removing each retained event separately: the same violation disappears. Keep rule, session horizon, and routine configuration visible and unchanged.
4. Restore the captured log and reproduce its verdict. Change the rest duration to 2 seconds in a clearly labeled replay configuration; the original early-rest violation disappears. Restore the original configuration.
5. Start a new live session and request progression without preparation acknowledgement. Show indeterminate, the missing confirmation, and blocked progression. Replay instructions, then explicitly acknowledge preparation; show the new timestamped event and reevaluation without rewriting history.
6. Complete a correctly ordered session, waiting for recorded rest completion before requesting the next set. Show satisfied for the modeled rules and horizon. Demonstrate End Session preventing further timer-driven progression.
7. Point to repository setup instructions and separately labeled regression traces so judges can reproduce the same cases and introduce their own event or rule changes.

## Cut scope
- Keep one authored routine and local sessions. Cut routine libraries, accounts, cloud services, cross-device features, and optional mini challenges.
- Do not replace the accepted Fire TV runtime, real remote capture, monotonic timers, evaluator-controlled progression, or executable trace reduction with scripted screens.
- Permit only the existing feasibility allowances: original minimal instructional content, clearly labeled generated regression traces, and remote-reported preparation/repetitions instead of sensed movement.
- Exclude camera analysis, automatic movement judgments, fall-prevention claims, exercise-effectiveness claims, and validated-demand claims. Confirmation records a user's report, not independently observed performance.
- Describe deterministic temporal provenance and subset-minimal explanations without causal-inference, counterfactual-optimization, or globally-shortest-trace claims.
- Exclude Alexa+, Bee, Ring, and AWS qualification assertions copied into candidate metadata; the selected implementation and evidence concern Fire TV only.
- Treat the supplied applicant/helper ledger conditions as belonging to another concept. Apply their relevant evidence limits here through explicit authored-rule boundaries, missing-context handling, reproducible changed-input tests, and demonstrated platform use.
- If platform deployment exhausts its gate allocation, follow the existing abandonment condition. Cut optional polish before core proof or required submission artifacts.

## Submission checklist
- Verify live Devpost registration, participant eligibility, exclusions, ownership, and required fields; complete submission before October 23, 2026 at 20:00 Europe/London.
- Select Fire TV as the primary track. Demonstrate functioning Fire OS or Vega OS software on actual hardware or an accepted emulator; do not claim qualification from a desktop interface.
- Provide a working application created or significantly updated during the qualifying period. If pre-existing code is used, explain and demonstrate the significant qualifying changes.
- Submit an English description covering the older-adult workflow, reported-event limits, authored temporal rules, three-valued verdicts, progression controls, and subset-minimal explanation method.
- Provide all source, assets, setup/run instructions, runtime requirements, and reproducible tests in GitHub. Prefer a public repository with a detectable open-source license. If private, resolve the official Devpost reviewer address and ensure accepted reviewer access for knmeiss, giolaq, anishamalde, mosesroth, emersonsklar, and the specified Devpost reviewer before the deadline.
- Publish a public YouTube or Vimeo video targeted below three minutes with English narration or translation. Show live platform operation, actual inputs, state changes, trace-removal proof, and failure handling; include its URL in Devpost.
- Supply product feedback for every used tool, API, and SDK: purpose, strengths, shortcomings, onboarding, and whether and why it would be used again.
- Keep the project free and available without testing restrictions through November 20, 2026 at 12:00 Pacific Time. Provide local judging instructions and any necessary credentials; continuous hosting is unnecessary for this local application.
- Use original or authorized instructional content, consented session traces, appropriately licensed dependencies, and authorized media. Keep generated regression inputs distinct from live-session evidence.
- Leave optional mini challenges unselected unless their additional qualifying work and documentation actually exist. A public primary-project repository alone does not establish the separate Open Source contribution requirement.
- Include optional friction logs or feature requests only from actual development observations and only after required artifacts are complete.

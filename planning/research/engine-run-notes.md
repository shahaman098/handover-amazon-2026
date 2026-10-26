# Engine execution and corrections

This analysis uses the real local HackForge 0.5.0 pipeline with the authenticated live Codex backend. No dry-run fixture provider supplies recommendations, collision results, feasibility reports, judge votes, or the build plan.

## Preserved live generation
The initial balanced run generated 24 opportunity cards, 24 mechanism cards, 32 initial concepts and 16 mutations. Its original artifacts remain in `engine-runs/2026-10-22-competition-brief-input/`. These are 48 candidate variants across a limited set of problem families, not evidence of 48 independently novel markets.

## Event-specific rule correction
The original mandatory-technology gate combined conditional requirements for all four primary tracks and the AWS mini-challenge into a universal list. It rejected all 48 candidates; 45 shared the same rejection concerning a copied Ring role containing the word “optional”. This contradicted the event's primary-track selection rule.
The affected process was stopped, preserving its outputs. `research/resume_engine.py` applies an isolated event adapter before the existing gates: retain unconditional requirements, apply only the selected primary track's technology and platform conditions, and preserve all applicable artifact/data/delivery/demo gates. Unknown track declarations fail closed. Behavioral checks retain failures for absent technology roles and missing submission plans; results are in `rule-scope-checks.json`. The corrected gate accepted 47 candidates and rejected one.

The scored criterion list was also restricted to the four equally weighted Stage Two criteria. Stage One qualification and the discretionary friction-log bonus remain in the evidence but are not treated as additional equally weighted criteria.

## Bounded evaluation
The first corrected attempt exceeded the collision auditor's 120,000-character input limit: 160,316 characters. The resumed adapter retains all twelve shortlisted candidates and audits them in batches of three; feasibility reviews use batches of four. No JSON is truncated and no candidate is omitted to evade the limit. The adapter records completed batches as checkpoints.
Cached research, patterns, opportunities, mechanisms and concepts come from the original live run. Collision, feasibility, blind judging, red-team review and build planning use fresh live model calls. The engine checkout's source files were not edited.

## Evidence and limits
Additional primary/public analogues are recorded in `manual-analogues.json`: a September 2026 constrained-optimisation audio-description paper, W3C extended audio description, Dwell, BOLT and Amazon's board-game companion-skill guide. The collision review rejected the main dialogue-scheduling proposal following the close prior art.
The local MiniLM transformer was available and used for semantic candidate diversity. A populated FAISS public-project index was unavailable; the collision review is not a comprehensive semantic census of all products or competition entries.
Customer demand and real-world effectiveness are not validated by generated concepts, fictional datasets, finite regression suites, internal scores or model judge preferences. These outputs help choose what to build; they do not establish a probability of winning.

## Participant assumptions
The user confirmed solo, starting from scratch. Ten focused build hours is a planning assumption, with time reserved for sleep, testing, recording and submission; it is not the official hackathon duration. The local Android SDK has a Pixel phone emulator profile, with no TV profile configured. No physical Amazon device, real Bee data or AWS runtime access was confirmed.

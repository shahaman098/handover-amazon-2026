# Verified event findings — 22 October 2026

Event: [Build, Ship, Shape: Amazon Developer Hackathon](https://amazonappdev2026.devpost.com/).
Deadline: Friday 23 October 2026, 20:00 Europe/London (19:00 UTC; 12:00 PDT). Official updates confirm the date.
Registration: local tracker records registered, citing the 30 September confirmation. Current submission/account state not verified because the Devpost connector needs reauthentication.

## Selection constraints
- Approximately 23 hours elapsed time remained at analysis start. Assumed delivery budget: one developer, 10 focused build hours, then testing, recording and submission. This is an operating assumption, not an event rule.
- Actual hardware, live Bee data, AWS runtime credentials and gated partner tooling are not confirmed available.
- Alexa+ accepts a custom simulated experience. A real Streamable HTTP MCP implementation and custom client provide stronger protocol proof without partner access.
- Fire TV requires proof on a supported device/emulator. Ring requires a real SDK/API/simulator path. Bee requires actual wearable data; fixture-only Bee is insufficient.

## Judging
The four formal criteria are equally weighted: Tech Implementation; Design; Potential Impact; Quality of the Idea. See [formal rules](https://amazonappdev2026.devpost.com/rules).
The event can award up to a 10% friction-log bonus. Log only observed problems, exact reproduction steps, workarounds and useful product feedback. Bonus is discretionary.

## Delivery requirements
GitHub source with complete setup/run instructions and appropriate access/license; public English demo video under three minutes on YouTube/Vimeo; written project explanation; product feedback for every tool/API/SDK; selected track and mini-challenge fields. Existing work must distinguish changes made during the event.
Alexa+ FAQ permits locally runnable code and demo video without permanent hosting. See [FAQ](https://amazonappdev2026.devpost.com/details/faqs).

## Competitive observations (limited public search)
- [Dwell](https://devpost.com/software/dwell-build-ship-shape) already targets stateful domestic task scheduling, including wait/drying time. Do not claim generic household scheduling is novel.
- [BOLT for Alexa+](https://devpost.com/software/bolt-for-alexa) already presents simulated workflow/audit UX. A stronger entry needs working computation and persisted state, not only interface animation.
- [Amazon's existing Alexa+ capabilities](https://www.aboutamazon.com/news/devices/new-alexa-plus-amazon-devices) include family calendars, personalised reminders, shopping and recipe digitisation. These features alone are a weak differentiation story.
Public search is incomplete and cannot establish how many actual entries exist, relative track crowding, absolute originality, or likelihood of winning.

## Engine
HackForge 0.5.0; live Codex backend passed its doctor completion check. Balanced profile requests 32 initial concepts plus 16 mutations, 12 collision audits and up to 6 blind-judged finalists, returning 1 recommendation and 2 distinct backups. No dry-run fixture provider is used.
The MiniLM transformer is available for semantic candidate diversity. A populated FAISS public-project index is absent; no claim of a comprehensive semantic collision corpus audit is warranted. See engine-run-notes.md for the rule-scope correction and bounded evaluation.

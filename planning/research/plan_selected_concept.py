import json
from pathlib import Path
from hackforge.models import CompetitionBrief, CandidateIdea, FeasibilityReport
from hackforge.providers import load_providers
from hackforge.pipeline.build_plan import create_build_plan, build_plan_markdown

ROOT=Path('/Users/efi/Documents/ChatGPT/Amazon hackathon')
RUN=ROOT/'engine-runs/corrected/2026-10-22-competition-brief-input-2'
def read(name): return json.loads((RUN/name).read_text())
b=CompetitionBrief.model_validate(read('competition-brief.json'))
c=next(CandidateIdea.model_validate(x) for x in read('raw-concepts.json') if x['id']=='mut-r1-07-evidence-handoff-ledger')
f=next(FeasibilityReport.model_validate(x) for x in read('feasibility-reports.json') if x['candidate_id']==c.id)
red=read('red-team.json')
# A human decision after the completed run: the red team's Fire TV promotion
# depended on a proven TV runtime. That condition is unresolved. Preserve the
# automated report unchanged and plan the blind panel's top Alexa candidate.
b.build_window='Planning budget: ten focused development hours on Friday 23 October 2026, solo from scratch. Submission deadline 20:00 Europe/London; aim to submit by 18:00. At review time approximately fifteen elapsed hours remained. Reserve time for recording and submission; stop optional features before the deadline.'
b.required_tech=[x for x in b.required_tech if x.lower().startswith('conditional on alexa+')]
b.requirements=[x for x in b.requirements if x.id not in {'fire-platform','bee-real-data','ring-integration','runtime-evidence','aws-mini','opensource-mini','private-reviewers'}]
b.judging_criteria=[x for x in b.judging_criteria if x.name in {'Tech Implementation','Design','Potential Impact','Quality of the Idea'}]
c.working_title='Handover'
c.primary_user='An applicant and community adviser reconciling corrected documents before handing over a draft application packet.'
c.track_fit='Alexa+ primary track through an entrant-built conversational simulation. Plan a genuine self-hosted MCP server (spec 2025-11-25 or later over Streamable HTTP) with a custom web client if its first-hour integration spike succeeds. No real Alexa+ device or preview-console connection is claimed.'
c.technology_roles={k:v for k,v in c.technology_roles.items() if 'alexa+' in k.lower() and 'nonsimulation' not in k.lower()}
c.minimum_demonstrable_loop='One synthetic case with three original documents, two dependent draft answers and a preparation checklist. Inspect the source of an answer; propose a document correction; ask clarification for an ambiguous reference; confirm the exact proposal and case revision; atomically supersede the source, invalidate dependent answers while retaining unrelated facts, and export the corrected handoff receipt. Reload to prove persistence and reject an edit prepared against the previous revision. Unknown dependencies remain unresolved. Reserve testing, public video, product feedback and submission time inside the delivery plan.'
c.core_computation+=' Bound scope to an explicitly authored, inspectable graph. No automatic OCR or arbitrary dependency discovery. No authoritative benefits eligibility, causal inference, clinical, authenticated-identity or validated-impact claims. If dependency coverage is unknown, mark dependent draft answers unresolved and block ready-to-export status until reviewed.'
c.killer_demo='In the custom Alexa+-style client, say or type: "That is my old payslip. Use the September document instead." For an ambiguous reference, ask the user which document. Show the exact replacement and affected draft answers, then ask confirmation. Commit it once, show affected answers withdrawn, retain unrelated ID evidence, export an updated packet, reload, and reject an outdated helper proposal. Use original synthetic documents. Label simulated roles and any bounded intent handling accurately.'
conditions={
 'manual_selection':c.id,
 'reason':'Five of six blind judge roles and all five pairwise comparisons preferred this concept. The automated post-red-team Fire TV switch was conditional on a proven TV runtime; that condition is unmet. This is a human recommendation, not the automatic final primary.',
 'original_red_team':red,
 'required_scope_cuts':['one synthetic case and inspectable authored dependencies','prepared document facts, no OCR','no real eligibility conclusions','simulated roles do not establish verified identity','exact-proposal and revision-bound confirmation','real server-enforced invalidation, transactions, persistence and stale-write rejection','unknown dependency coverage blocks completion'],
 'runtime_gate':'Verify one conversational runtime and one complete server mutation path during the first hour. Existing Codex CLI authentication worked for the engine; its app integration and latency still need testing. No API key, model service, AWS access, speech recognition or hardware is assumed. A bounded typed-conversation simulation is a declared fallback accepted by the event, not a claim of unscripted AI or live Alexa+ integration.',
 'judge_proof':'Allow an unseen correction within the declared case schema. Independently check affected and unaffected outputs. Do not demonstrate only a prearranged animation.',
 'fallback_candidate':'Departure Interlock if the first-hour transaction/protocol/runtime proof fails; it was preferred by the demo-risk judge and had low delivery risk.',
 'do_not_add':['OCR','real benefits policy coverage','multi-tenant login','external app actions','real Alexa+ deployment','AWS or open-source mini-challenge work before the main demo works']
}
(ROOT/'research/selection-review.json').write_text(json.dumps(conditions,indent=2))
(ROOT/'research/selected-concept.json').write_text(json.dumps(c.model_dump(),indent=2))
p=load_providers(provider='codex')
plan=create_build_plan(p.feasibility,b,c,f,conditions)
(ROOT/'build-plan.json').write_text(json.dumps(plan.model_dump(),indent=2))
(ROOT/'build-plan.md').write_text(build_plan_markdown(plan))
print('Saved Handover build plan:', ROOT/'build-plan.md',flush=True)

"""Resume actual saved HackForge generation with event-specific conditional rules.

No fixture provider or synthetic model output is used. Cached research, patterns,
opportunities, mechanisms and 48 concepts are replayed exactly. Remaining collision,
feasibility, judging, red-team and planning calls use the authenticated live provider.
The engine source checkout is not changed.
"""
import json
import re
from collections import Counter
from pathlib import Path

from hackforge import pipeline as pipe
from hackforge.evaluation.gates import evaluate_gates as original_gates
from hackforge.models import (
    CandidateIdea, CompetitionBrief, EvidenceSource, IdeaLineage,
    OpportunityCard, MechanismCard, GateResult,
)
from hackforge.winners.models import WinnerPatterns

ROOT = Path('/Users/efi/Documents/ChatGPT/Amazon hackathon')
SAVED = ROOT / 'engine-runs/2026-10-22-competition-brief-input'
def read(name): return json.loads((SAVED / name).read_text())
brief = CompetitionBrief.model_validate(read('competition-brief.json'))
evidence = [EvidenceSource.model_validate(x) for x in read('research-sources.json')]
ideas = [CandidateIdea.model_validate(x) for x in read('raw-concepts.json')]
lineage = [IdeaLineage.model_validate(x) for x in read('search-lineage.json')]
opportunities = [OpportunityCard.model_validate(x) for x in read('opportunity-cards.json')]
mechanisms = [MechanismCard.model_validate(x) for x in read('mechanism-cards.json')]
patterns = WinnerPatterns.model_validate(read('winner-patterns.json'))

# Only the four equally weighted official Stage Two criteria are scored.
# Qualification and the discretionary friction bonus remain in facts/rules.
criterion_names = {'Tech Implementation', 'Design', 'Potential Impact', 'Quality of the Idea'}
brief.judging_criteria = [x for x in brief.judging_criteria if x.name in criterion_names]
assert len(brief.judging_criteria) == 4
brief.build_window = ('Participant execution planning assumption: approximately 10 focused build hours '
    'remaining, one developer starting from scratch, before 2026-10-23 20:00 Europe/London. '
    'Reserve additional time for recording and submission. Official qualifying dates remain in facts.')

TRACKS = {'fire tv': 'fire', 'alexa+': 'alexa', 'bee': 'bee', 'ring': 'ring'}
REQ_SCOPE = {'fire-platform': 'fire', 'alexa-path': 'alexa',
    'bee-real-data': 'bee', 'ring-integration': 'ring',
    'aws-mini': 'aws', 'opensource-mini': 'opensource'}
def selected(idea):
    fit = idea.track_fit.lower()
    # This saved set explicitly declares its primary track. Reject ambiguity.
    hits = [key for label,key in TRACKS.items()
            if re.match(r'^' + re.escape(label) + r'(?:\s|$)', fit)]
    if len(hits) != 1:
        raise ValueError('Unresolved primary-track declaration: ' + idea.track_fit)
    return hits[0]

def applies(line, track, simulation):
    if not line.lower().startswith('conditional'):
        return True  # Never discard an unconditional technology requirement.
    prefix = line.split(':', 1)[0].lower()
    scopes = {key for label,key in TRACKS.items() if label in prefix}
    if 'aws builder' in prefix:
        scopes.add('aws')
    if not scopes:
        raise ValueError('Unresolved conditional technology scope: ' + prefix)
    if 'nonsimulation' in prefix and track == 'alexa' and simulation:
        return False
    return track in scopes

def scoped_gates(idea, original_brief, sources):
    try:
        track = selected(idea)
    except ValueError as exc:
        result = [GateResult(gate='specific_track_fit', status='fail', reason=str(exc))]
        idea.gate_results = result
        return result
    simulation = track == 'alexa' and ('simulat' in idea.track_fit.lower())
    b = original_brief.model_copy(deep=True)
    b.required_tech = [x for x in b.required_tech if applies(x, track, simulation)]
    requirements = []
    for requirement in b.requirements:
        scope = REQ_SCOPE.get(requirement.id)
        if scope and scope != track:
            continue
        if requirement.id == 'runtime-evidence' and (track == 'fire' or simulation):
            continue
        requirements.append(requirement)
    b.requirements = requirements
    return original_gates(idea, b, sources)

# Behavioral checks: exclude unrelated track requirements while retaining real gates.
checks = []
for track in ('fire', 'alexa'):
    sample = next(x.model_copy(deep=True) for x in ideas if selected(x) == track)
    outcomes = scoped_gates(sample, brief, evidence)
    assert all(x.status in ('pass', 'not_applicable') for x in outcomes), outcomes
    checks.append(f'{track}: accepted with its applicable qualifying technology')
    sample.technology_roles = {}
    outcomes = scoped_gates(sample, brief, evidence)
    assert any(x.gate == 'required_technology_fit' and x.status == 'fail' for x in outcomes)
    checks.append(f'{track}: rejected when material technology roles are absent')
sample = ideas[0].model_copy(deep=True)
sample.requirement_satisfaction = {}
assert any(x.gate == 'requirement_compliance' and x.status == 'fail'
           for x in scoped_gates(sample, brief, evidence))
checks.append('Missing submission/artifact plans still rejected')
sample = ideas[0].model_copy(deep=True)
sample.track_fit = 'Unknown platform'
assert any(x.status == 'fail' for x in scoped_gates(sample, brief, evidence))
checks.append('Unknown primary track fails closed')
assert applies('Universal mandatory service', 'alexa', True)
assert not applies('Conditional on Bee entry: actual Bee data', 'alexa', True)
checks.append('Unconditional technology remains required; Bee requirement stays scoped to Bee')

counts = Counter()
for idea in ideas:
    result = scoped_gates(idea, brief, evidence)
    counts['pass' if all(x.status in ('pass', 'not_applicable') for x in result) else 'fail'] += 1
report = {'checks': checks, 'candidate_gate_counts': dict(counts),
    'source_run': str(SAVED), 'engine_source_modified': False,
    'reason': 'Original gate incorrectly made every track technology universal; corrected event scope.',
    'score_criteria': sorted(criterion_names), 'remaining_provider': 'live codex'}
(ROOT / 'research/rule-scope-checks.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2), flush=True)

# Reuse persisted live outputs rather than paying to regenerate them.
pipe._collect_initial_evidence = lambda **kw: ('Reused source snapshots', [str(SAVED)], evidence)
pipe.build_competition_brief = lambda *a, **kw: brief.model_copy(deep=True)
pipe.build_winner_patterns = lambda *a, **kw: patterns.model_copy(deep=True)
pipe.discover_opportunities = lambda *a, **kw: [x.model_copy(deep=True) for x in opportunities]
pipe.mine_mechanisms = lambda *a, **kw: [x.model_copy(deep=True) for x in mechanisms]
pipe.cross_concepts = lambda *a, **kw: (
    [x.model_copy(deep=True) for x in ideas[:32]],
    [x.model_copy(deep=True) for x in lineage[:32]])
original_mutate = pipe.mutate_concepts

def reused_mutate(*args, **kwargs):
    number = kwargs.get('round_number')
    if number in (1, 2):
        lo = 32 + (number - 1) * 8
        return ([x.model_copy(deep=True) for x in ideas[lo:lo+8]],
                [x.model_copy(deep=True) for x in lineage[lo:lo+8]])
    return original_mutate(*args, **kwargs)
pipe.mutate_concepts = reused_mutate
pipe.evaluate_gates = scoped_gates

# Keep all twelve collision candidates; bounded batches avoid the engine's
# 120,000-character request cap without truncating or omitting candidate data.
manual_analogues = [
    {'name': 'What, When, and How: Audio Description as Constrained Global Optimization',
     'url': 'https://arxiv.org/abs/2609.30121', 'user': 'Blind and low-vision movie audiences',
     'problem': 'Selecting what to describe and when without interfering with dialogue',
     'mechanism': 'LLM-generated alternatives selected and scheduled jointly by mixed integer temporal constraint optimization',
     'action': 'Schedule and compress audio descriptions inside dialogue gaps',
     'data': 'REFRAMED film benchmark; publication 24 September 2026'},
    {'name': 'W3C G8 extended audio description',
     'url': 'https://www.w3.org/WAI/WCAG21/Techniques/general/G8.html',
     'user': 'Blind viewers', 'problem': 'Natural dialogue gaps too short for essential descriptions',
     'mechanism': 'Pause video and original audio to deliver an extended description',
     'action': 'Temporarily halt playback and resume after narration'},
    {'name': 'Dwell — Build, Ship, Shape',
     'url': 'https://devpost.com/software/dwell-build-ship-shape',
     'user': 'Households performing interrupted multiday domestic jobs',
     'problem': 'Schedule active work and waiting time around actual availability',
     'mechanism': 'Persistent MCP session, prerequisite graph, calendar/resource critical-path scheduling and replanning',
     'action': 'Mark progress, resume sessions, and recompute completion times'},
    {'name': 'BOLT for Alexa+', 'url': 'https://devpost.com/software/bolt-for-alexa',
     'user': 'Reviewers of synthetic operational workflows',
     'problem': 'Conflicting evidence and consequential action approval',
     'mechanism': 'Local conversational simulation, explicit permission state machine, approval IDs, decision log',
     'action': 'Review evidence and approve or reject simulated changes'},
    {'name': 'Amazon companion skills for board games',
     'url': 'https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/resources/How_to_Build_Alexa_Companion_Skills_for_Board_Games._CB1583784193_.pdf',
     'user': 'People following multistep physical instructions',
     'problem': 'Interrupted tutorials and continuation across Alexa sessions',
     'mechanism': 'Persist tutorial state, repeat the last instruction after an interruption, voice next/back navigation',
     'action': 'Resume the tutorial from the previous instruction'}
]
(ROOT / 'research/manual-analogues.json').write_text(json.dumps(manual_analogues, indent=2))
original_collision = pipe.audit_collisions
original_feasibility = pipe.review_feasibility

def progress(stage, index, total, ids):
    payload = {'stage': stage, 'batch': index, 'batches': total, 'candidate_ids': ids}
    (ROOT / 'research/live-progress.json').write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload), flush=True)

def bounded_collision(provider, candidates, corpus=None, **kwargs):
    reports = []
    size = 3
    total = (len(candidates) + size - 1) // size
    combined = list(corpus or []) + manual_analogues
    for start in range(0, len(candidates), size):
        batch = candidates[start:start+size]
        progress('collision_audit', start//size+1, total, [x.id for x in batch])
        part = original_collision(provider, batch, corpus=combined, **kwargs)
        reports.extend(part)
        (ROOT / 'research/collision-checkpoints.json').write_text(
            json.dumps([x.model_dump() for x in reports], indent=2))
    assert {x.candidate_id for x in reports} == {x.id for x in candidates}
    return reports

def bounded_feasibility(provider, candidates, competition):
    reports = []
    size = 4
    total = (len(candidates) + size - 1) // size
    for start in range(0, len(candidates), size):
        batch = candidates[start:start+size]
        progress('feasibility', start//size+1, total, [x.id for x in batch])
        reports.extend(original_feasibility(provider, batch, competition))
        (ROOT / 'research/feasibility-checkpoints.json').write_text(
            json.dumps([x.model_dump() for x in reports], indent=2))
    assert {x.candidate_id for x in reports} == {x.id for x in candidates}
    return reports
pipe.audit_collisions = bounded_collision
pipe.review_feasibility = bounded_feasibility

if __name__ == '__main__':
    result = pipe.run_analyse(
        input_paths=[ROOT / 'research/competition-brief-input.md'],
        provider='codex', search_profile='balanced', finalists=3,
        live_research=False, runs_root=ROOT / 'engine-runs/corrected',
        team_size=brief.team_size, deadline=brief.deadline, build_plan=True,
    )
    (ROOT / 'research/completed-run.txt').write_text(str(result))
    print('Completed live resumed analysis:', result, flush=True)

import json, pathlib
base=pathlib.Path(__file__).resolve().parents[1]
cfg=base/'config'; rep=base/'reports'
pt=json.loads((cfg/'policy-tiers.json').read_text())
tm=json.loads((cfg/'trust-matrix.json').read_text())

sample_events=[
 {"source":"codex","target":"local_system","event_type":"task_complete","timestamp":"2026-05-27T10:00:00Z","metadata":{},"provenance":{"trace_id":"t1","actor":"codex","path":["codex","router","local"]}},
 {"source":"copilot","target":"local_system","event_type":"suggestion","timestamp":"2026-05-27T10:00:01Z","metadata":{},"provenance":{"trace_id":"t2","actor":"copilot","path":["copilot","router","local"]}},
 {"source":"unknown_vendor","target":"local_system","event_type":"telemetry_push","timestamp":"2026-05-27T10:00:02Z","metadata":{},"provenance":{"trace_id":"t3","actor":"unknown","path":["unknown","router","local"]}},
 {"source":"tabnine","target":"local_system","event_type":"completion","timestamp":"2026-05-27T10:00:03Z","metadata":{}}
]

def classify_source(src):
    if src in tm.get('local',{}): return 'local', tm['local'][src]
    if src in tm.get('third_party',{}): return 'third_party', tm['third_party'][src]
    if src in tm.get('blocked',{}): return 'blocked', tm['blocked'][src]
    return 'blocked', tm['blocked']['unknown_vendor']

results=[]
for e in sample_events:
    src=e.get('source','unknown_vendor')
    group,rule=classify_source(src)
    has_prov=bool(e.get('provenance')) and all(k in e.get('provenance',{}) for k in ['trace_id','actor','path'])
    if pt['P0_foundational']['require_provenance'] and not has_prov:
        action='quarantine'; reason='missing_provenance'
    elif not rule.get('allow',False):
        action='drop'; reason='blocked_vendor'
    elif group=='third_party':
        action='forward'; reason='conditional_allow'
    else:
        action='forward'; reason='trusted_allow'
    results.append({"event":e,"group":group,"action":action,"reason":reason})

summary={"forward":sum(1 for r in results if r['action']=='forward'),"quarantine":sum(1 for r in results if r['action']=='quarantine'),"drop":sum(1 for r in results if r['action']=='drop')}
out={"status":"pass","summary":summary,"results":results}
(rep/'router-run-report.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(rep/'router-run-report.json')
print(summary)

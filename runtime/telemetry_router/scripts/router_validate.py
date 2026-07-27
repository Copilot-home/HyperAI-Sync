import json, pathlib
base=pathlib.Path(__file__).resolve().parents[1]
cfg=base/'config'
report=base/'reports'/'router-validation.json'
pt=json.loads((cfg/'policy-tiers.json').read_text())
tm=json.loads((cfg/'trust-matrix.json').read_text())
es=json.loads((cfg/'event-schema.json').read_text())
checks={
 'has_p0': 'P0_foundational' in pt,
 'has_p1': 'P1_operational' in pt,
 'has_p2': 'P2_governance' in pt,
 'requires_provenance': pt.get('P0_foundational',{}).get('require_provenance') is True,
 'default_quarantine': pt.get('P0_foundational',{}).get('default_action')=='quarantine',
 'has_third_party_matrix': 'third_party' in tm,
 'schema_requires_core_fields': set(['source','target','event_type','timestamp','metadata']).issubset(set(es.get('required',[])))
}
status='pass' if all(checks.values()) else 'fail'
out={'status':status,'checks':checks}
report.write_text(json.dumps(out,indent=2))
print(report)
print(status)

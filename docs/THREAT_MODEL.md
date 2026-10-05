# Threat model

| Threat | Control |
|---|---|
| Principal impersonates delegate | sender-bound acceptance and plan |
| Delegate accepts different mandate | exact stored digest comparison |
| Plan survives changed mandate | revision atomically marks old handoff `STALE` |
| One party floods objections | role-specific slots plus two one-per-wallet auditor slots |
| LLM follows untrusted text | explicit data boundary, structured schema, deterministic gate |
| Unknown becomes positive | any consequential unknown routes to `UNRESOLVED` |
| Caller self-selects verdict | assessment accepts no verdict input; validator consensus controls every semantic field |
| Completion claim presented as proof | state/reason and docs explicitly identify it as delegate-authored claim |
| Deployer controls lifecycle | no deployer address or admin method stored |
| Rejected call mutates state | regression tests compare authoritative pre/post state |

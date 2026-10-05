# Test matrix

| Invariant / path | Expected result |
|---|---|
| Exact delegate accepts exact digest | `ACCEPTED` |
| Wrong delegate or digest | revert; full state unchanged |
| Plan before acceptance / principal submits plan | revert |
| Aligned plan | `ALIGNED` |
| Extra authority or violated constraint | `OUT_OF_SCOPE` |
| Mandatory unknown | `UNRESOLVED` |
| Ambiguous verdict | `REVIEW_REQUIRED` |
| Material objection | cannot become `ALIGNED` |
| Principal, delegate or unrelated wallet triggers assessment | accepted; consensus alone controls verdict |
| One principal + one delegate + two auditor slots | accepted deterministically |
| Same auditor twice / third auditor | revert; state unchanged |
| Revision | prior becomes `STALE`; new digest and acceptance required |
| Assess stale revision | revert |
| Prompt injection | treated as data |
| Consensus failure / malformed schema | `UNRESOLVED` |
| Completion before alignment / wrong actor | revert |
| Completion after alignment by delegate | `COMPLETION_RECORDED` claim only |
| Invalid or zero delegate address | revert before storage |
| Arbitrary wallet creates mandate | succeeds; deployer privilege absent |

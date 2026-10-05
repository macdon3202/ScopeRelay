# ScopeRelay

ScopeRelay is a contract-only GenLayer application for verifying whether a
delegate's sealed execution plan remains within an accepted natural-language
mandate. It uses a multi-party rendezvous, fixed objection slots and revision
invalidation rather than a creator/reviewer certificate flow.

## Why GenLayer

Determining whether differently worded actions preserve every mandate
constraint, request extra authority or respond to a material objection is a
bounded semantic judgment. Validators establish those facts; deterministic
contract code controls actors, phases, digests, revisions and terminal states.

## Lifecycle

```text
principal creates mandate
→ exact delegate accepts exact mandate digest
→ delegate locks execution plan
→ principal/delegate/auditors may fill bounded objection slots
→ either participant or any wallet triggers validator consensus
→ ALIGNED | OUT_OF_SCOPE | REVIEW_REQUIRED | UNRESOLVED
→ delegate may record a completion claim only after ALIGNED
```

The completion record is explicitly a delegate-authored claim. ScopeRelay does
not prove external execution, ownership, legal authority or economic outcome.

## Permission model

- Deployer has no stored role or runtime authority.
- Any wallet may create its own mandate.
- Only the exact delegate can accept, submit the plan and record completion.
- Any wallet may trigger adjudication, including either participant, but the
  caller cannot supply or select the verdict; validator consensus controls it.
- Two unrelated auditor slots, one principal slot and one delegate slot prevent
  submission-order flooding across parties.
- A revision atomically marks the prior handoff `STALE` and requires fresh
  delegate acceptance and adjudication.

## Verification

```bash
python -m pytest -q
python -X utf8 -m genvm_linter.cli check contracts/scope_relay.py
```

Current result: **25 tests passing**, lint and validation passing.

Deployed on StudioNet at
[`0x5Edc6C71F4820A471F18581e0E2013e8D03D632E`](https://explorer-studio.genlayer.com/address/0x5Edc6C71F4820A471F18581e0E2013e8D03D632E).
The finalized five-transaction happy path and exact post-write readbacks are in
[`docs/STUDIONET_E2E.md`](docs/STUDIONET_E2E.md) and
[`docs/studionet-e2e.json`](docs/studionet-e2e.json). Local fixtures remain
clearly separated from network evidence.

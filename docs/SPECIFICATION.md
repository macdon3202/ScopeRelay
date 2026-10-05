# ScopeRelay proof specification

## Claim

The exact delegate plan serves the sealed objective, preserves every sealed
constraint, requests no additional authority and is not defeated by a material
objection in the bounded evidence set.

## Evidence and authority

The contract does not claim objective truth about external work. It authenticates
who authored each on-chain statement through `message.sender`: principal for
mandate/revision, delegate for acceptance/plan/completion, and each objection
author for its fixed slot. Exact bytes, actors and revision are contract state.

## Consequential consensus fields

- mandate understood
- plan understood
- objective alignment
- constraint preserved
- extra authority requested
- objection material
- verdict

`ALIGNED` requires all mandatory positive predicates, no extra authority, no
material objection and verdict `ALIGNED`. Any unknown is `UNRESOLVED`. A known
violation is `OUT_OF_SCOPE`. An otherwise unresolved semantic verdict is
`REVIEW_REQUIRED`.

## Deterministic enforcement

AI cannot select actors, accept a digest, submit/revise plans, allocate evidence
slots or record completion. Any wallet may trigger assessment, but the caller
provides no verdict parameter and has no verdict authority. The contract
enforces all roles, exact phase, revision staleness, fixed slot limits and
terminality; independent validators establish every consequential semantic
field.

# StudioNet E2E evidence

Status: **PASS — live StudioNet evidence recorded 2026-10-05**.

Contract: [`0x5Edc6C71F4820A471F18581e0E2013e8D03D632E`](https://explorer-studio.genlayer.com/address/0x5Edc6C71F4820A471F18581e0E2013e8D03D632E)

The deployment wallet did not act as principal or delegate. The principal was
`0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43`; the delegate was
`0xc67532aeF9D2879cBA9375a02E6217A3524657B8`. The principal triggered
assessment but supplied no verdict; independent validator consensus produced
the consequential semantic fields.

| Step | Transaction | Final result | Readback state |
|---|---|---|---|
| Create mandate | [`0x46d847...d7e21`](https://explorer-studio.genlayer.com/tx/0x46d8474edf6721502355b80b17afb79851fafdf5b2b36eae3d6910c4200d7e21) | `FINALIZED / MAJORITY_AGREE / SUCCESS` | `OPEN` |
| Exact delegate accepts exact digest | [`0x808b9c...15a00`](https://explorer-studio.genlayer.com/tx/0x808b9ce77e6dfa53ab20f7bbeddb78bc43807a807c0b4f53ee216812a9415a00) | `FINALIZED / MAJORITY_AGREE / SUCCESS` | `ACCEPTED` |
| Delegate locks plan | [`0x90742e...a6ed4`](https://explorer-studio.genlayer.com/tx/0x90742e2d131fccb95f28e2bcf8d7ce7b29e269abd790733f0214d76cdfca6ed4) | `FINALIZED / MAJORITY_AGREE / SUCCESS` | `PLAN_LOCKED` |
| Consensus assessment | [`0xfc7e84...39d8e`](https://explorer-studio.genlayer.com/tx/0xfc7e8465ec0b386d551eedede599421482e5582492875279da538666f3a39d8e) | `FINALIZED / MAJORITY_AGREE / SUCCESS` | `ALIGNED` |
| Delegate records scoped completion claim | [`0xe924a7...27948`](https://explorer-studio.genlayer.com/tx/0xe924a76d723662e83317c28785ae47cd2aa114262dbca800613efd4f4d327948) | `FINALIZED / MAJORITY_AGREE / SUCCESS` | `COMPLETION_RECORDED` |

The assessment readback was `objective_alignment=YES`,
`constraint_preserved=YES`, `extra_authority_requested=NO`,
`objection_material=NO`, `verdict=ALIGNED`. The final record labels the last
statement `DELEGATE_COMPLETION_CLAIM_RECORDED`; it does not claim external
execution was independently proven.

The complete machine-readable transaction results and post-write snapshots are
stored in [`studionet-e2e.json`](studionet-e2e.json).

## Live failure and rollback path

Handoff `2` deliberately submitted a plan that transfers registrar ownership
and changes billing, contradicting the sealed constraints. Consensus returned
`OUT_OF_SCOPE`, with `objective_alignment=NO`, `constraint_preserved=NO` and
`extra_authority_requested=YES`.

| Adversarial action | Transaction | Expected error | Snapshot rollback |
|---|---|---|---|
| Principal attempts delegate acceptance | [`0xaac282...f6387`](https://explorer-studio.genlayer.com/tx/0xaac2823191b080362ad2ce8b320a6cd3dde087bfb26cd4565db28fb0778f6387) | `DELEGATE_REQUIRED` | verified identical |
| Delegate accepts wrong digest | [`0xbf4082...f262e`](https://explorer-studio.genlayer.com/tx/0xbf4082ae268653ed07331b8b89013eb2baabf39f1015ed388425be88738f262e) | `MANDATE_DIGEST_MISMATCH` | verified identical |
| Principal attempts delegate plan submission | [`0x9c95cf...71236`](https://explorer-studio.genlayer.com/tx/0x9c95cf3379b2f7f549fbfd9bef0ca8b300aebdc7f2d95b2fb8ed9028d1171236) | `DELEGATE_REQUIRED` | verified identical |
| Delegate claims completion before assessment | [`0xb933d6...050bb`](https://explorer-studio.genlayer.com/tx/0xb933d661d22b67f0a1a62714163392f2e73883ca9cedb234426ff6d0457050bb) | `HANDOFF_NOT_ALIGNED` | verified identical |
| Delegate claims completion after rejection | [`0x245c0b...b1e53`](https://explorer-studio.genlayer.com/tx/0x245c0b946f2417a8d0b6dad4e51d374c7fd650073e3a4a5958e6c392e05b1e53) | `HANDOFF_NOT_ALIGNED` | verified identical |

All rejected calls were `FINALIZED / MAJORITY_AGREE / ERROR`. The adversarial
assessment transaction [`0x1518d7...46737`](https://explorer-studio.genlayer.com/tx/0x1518d786726248fdce6bf7e7f2572400ab65318edb292b765a4ff47e86c46737)
was `FINALIZED / MAJORITY_AGREE / SUCCESS` and persisted the terminal
`OUT_OF_SCOPE` state. Full inputs, outputs and snapshots are stored in
[`studionet-negative-e2e.json`](studionet-negative-e2e.json).

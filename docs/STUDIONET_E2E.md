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

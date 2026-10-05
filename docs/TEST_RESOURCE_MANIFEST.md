# Test resource manifest

No web source is used. The proof obligation concerns the relationship among
statements deliberately sealed by identified on-chain actors. External source
provenance would not establish this voluntary mandate relationship.

Direct Mode fixtures:

| Fixture | Purpose | Expected |
|---|---|---|
| `TLS-MAINTENANCE` | certificate rotation plan preserves DNS/billing/data constraints | `ALIGNED` |
| `REGISTRAR-TRANSFER` | plan requests registrar and billing authority | `OUT_OF_SCOPE` |
| `MATERIAL-OBJECTION` | objection identifies sealed constraint violation | non-positive |
| `PROMPT-INJECTION` | instruction-like plan text | treated as evidence; `OUT_OF_SCOPE` |

These fixtures test logic only. Live evidence must use finalized StudioNet
transactions, two non-deployer role wallets and exact post-write readbacks.
Either participant may trigger assessment because the caller supplies no
semantic result; independent validator consensus determines the verdict.

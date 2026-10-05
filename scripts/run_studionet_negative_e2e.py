"""Record live failure, rollback and out-of-scope evidence for ScopeRelay."""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

RPC = "https://studio.genlayer.com/api"
EX = "https://explorer-studio.genlayer.com"
ROOT = Path(__file__).resolve().parents[1]


def load() -> None:
    for raw in (ROOT.parent / "secrets" / "genlayer-test-wallets.env").read_text(encoding="utf-8").splitlines():
        if "=" in raw and not raw.lstrip().startswith("#"):
            key, value = raw.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\"").strip("<>"))


def plain(value):
    if isinstance(value, dict):
        return {str(key): plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(item) for item in value]
    return value if isinstance(value, (str, int, float, bool)) or value is None else str(value)


def signals(tx):
    status = str(tx.get("status_name") or tx.get("status") or "UNKNOWN").upper()
    consensus = str(tx.get("result_name") or tx.get("consensus_result") or "UNKNOWN").upper()
    data = tx.get("consensus_data") if isinstance(tx.get("consensus_data"), dict) else {}
    rows = data.get("leader_receipt") or data.get("validators") or []
    rows = [rows] if isinstance(rows, dict) else rows
    leader = next((row for row in rows if isinstance(row, dict) and str(row.get("mode", "")).lower() == "leader"), rows[0] if rows else {})
    execution = str(leader.get("execution_result") or "UNKNOWN").upper()
    result = leader.get("result") if isinstance(leader.get("result"), dict) else {}
    payload = result.get("payload")
    returned = payload.get("readable") if isinstance(payload, dict) else payload
    return status, consensus, execution, returned


def wait(client, tx_hash, expect_success):
    for _ in range(200):
        status, consensus, execution, returned = signals(plain(client.get_transaction(tx_hash)))
        if status == "FINALIZED":
            agreed = consensus in {"MAJORITY_AGREE", "AGREE", "ACCEPTED"}
            succeeded = execution == "SUCCESS"
            if not agreed or succeeded != expect_success:
                raise AssertionError((tx_hash, status, consensus, execution, returned, expect_success))
            return {"hash": tx_hash, "url": f"{EX}/tx/{tx_hash}", "status": status, "consensus": consensus, "execution": execution, "returned": returned}
        time.sleep(3)
    raise TimeoutError(tx_hash)


def send(client, address, account, method, args, expect_success=True):
    tx_hash = str(client.write_contract(address=address, function_name=method, account=account, args=args, value=0))
    print(json.dumps({"submitted": tx_hash, "method": method, "expect_success": expect_success}), flush=True)
    return wait(client, tx_hash, expect_success)


def read(client, address, account, method, args):
    return plain(client.read_contract(address=address, function_name=method, args=args, account=account))


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: run_studionet_negative_e2e.py CONTRACT_ADDRESS")
    address = sys.argv[1]
    load()
    principal = create_account(os.environ["SERVICE_LEDGER_KEY_A"])
    delegate = create_account(os.environ["SERVICE_LEDGER_KEY_B"])
    client = create_client(chain=studionet, account=principal, endpoint=RPC)

    create = send(client, address, principal, "create_mandate", ["DNS_BOUNDARY", "Rotate the public API TLS certificate.", "Do not change DNS, registrar ownership, billing, or production data.", str(delegate.address)])
    handoff_id = int(str(create["returned"]).strip('"'))
    opened = read(client, address, principal, "get_handoff", [handoff_id])

    wrong_actor = send(client, address, principal, "accept_mandate", [handoff_id, opened["mandate_digest"]], False)
    after_wrong_actor = read(client, address, principal, "get_handoff", [handoff_id])
    assert after_wrong_actor == opened

    wrong_digest = send(client, address, delegate, "accept_mandate", [handoff_id, "0" * 64], False)
    after_wrong_digest = read(client, address, delegate, "get_handoff", [handoff_id])
    assert after_wrong_digest == opened

    accept = send(client, address, delegate, "accept_mandate", [handoff_id, opened["mandate_digest"]])
    accepted = read(client, address, delegate, "get_handoff", [handoff_id])
    wrong_plan_actor = send(client, address, principal, "submit_plan", [handoff_id, "Transfer registrar ownership."], False)
    after_wrong_plan_actor = read(client, address, principal, "get_handoff", [handoff_id])
    assert after_wrong_plan_actor == accepted

    submit = send(client, address, delegate, "submit_plan", [handoff_id, "Transfer the domain to another registrar and replace billing details."])
    locked = read(client, address, delegate, "get_handoff", [handoff_id])
    premature_completion = send(client, address, delegate, "record_completion", [handoff_id, "Claimed complete before assessment."], False)
    after_premature_completion = read(client, address, delegate, "get_handoff", [handoff_id])
    assert after_premature_completion == locked

    assess = send(client, address, principal, "assess_handoff", [handoff_id])
    rejected = read(client, address, principal, "get_handoff", [handoff_id])
    assert rejected["state"] == "OUT_OF_SCOPE"
    completion_after_rejection = send(client, address, delegate, "record_completion", [handoff_id, "Attempt after rejection."], False)
    final = read(client, address, delegate, "get_handoff", [handoff_id])
    assert final == rejected

    evidence = {
        "network": "studionet",
        "contract": address,
        "handoff_id": handoff_id,
        "principal": str(principal.address),
        "delegate": str(delegate.address),
        "create": create,
        "wrong_actor_accept": wrong_actor,
        "wrong_actor_rollback": after_wrong_actor == opened,
        "wrong_digest_accept": wrong_digest,
        "wrong_digest_rollback": after_wrong_digest == opened,
        "accept": accept,
        "wrong_plan_actor": wrong_plan_actor,
        "wrong_plan_actor_rollback": after_wrong_plan_actor == accepted,
        "submit_out_of_scope_plan": submit,
        "premature_completion": premature_completion,
        "premature_completion_rollback": after_premature_completion == locked,
        "assess": assess,
        "rejected": rejected,
        "completion_after_rejection": completion_after_rejection,
        "terminal_rollback": final == rejected,
        "opened": opened,
        "accepted": accepted,
        "locked": locked,
        "final": final,
    }
    output = ROOT / "docs" / "studionet-negative-e2e.json"
    output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()

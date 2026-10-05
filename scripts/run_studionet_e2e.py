"""Run ScopeRelay end to end with exactly two non-deployer role wallets."""
from __future__ import annotations
import json,os,sys,time
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
RPC="https://studio.genlayer.com/api";EX="https://explorer-studio.genlayer.com";ROOT=Path(__file__).resolve().parents[1]
def load():
    for raw in (ROOT.parent/"secrets"/"genlayer-test-wallets.env").read_text(encoding="utf-8").splitlines():
        if "=" in raw and not raw.lstrip().startswith("#"):
            k,v=raw.split("=",1);os.environ.setdefault(k.strip(),v.strip().strip("'\"").strip("<>"))
def plain(v):
    if isinstance(v,dict):return {str(k):plain(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [plain(x) for x in v]
    return v if isinstance(v,(str,int,float,bool)) or v is None else str(v)
def signals(x):
    status=str(x.get("status_name") or x.get("status") or "UNKNOWN").upper();consensus=str(x.get("result_name") or x.get("consensus_result") or "UNKNOWN").upper();d=x.get("consensus_data") if isinstance(x.get("consensus_data"),dict) else {};rows=d.get("leader_receipt") or d.get("validators") or [];rows=[rows] if isinstance(rows,dict) else rows;leader=next((r for r in rows if isinstance(r,dict) and str(r.get("mode","")).lower()=="leader"),rows[0] if rows else {});execution=str(leader.get("execution_result") or "UNKNOWN").upper();result=leader.get("result") if isinstance(leader.get("result"),dict) else {};payload=result.get("payload");returned=payload.get("readable") if isinstance(payload,dict) else payload;return status,consensus,execution,returned
def wait(c,tx):
    for _ in range(200):
        s,k,e,r=signals(plain(c.get_transaction(tx)))
        if s=="FINALIZED":
            if k not in {"MAJORITY_AGREE","AGREE","ACCEPTED"} or e!="SUCCESS":raise AssertionError((tx,s,k,e,r))
            return {"hash":tx,"url":f"{EX}/tx/{tx}","status":s,"consensus":k,"execution":e,"returned":r}
        time.sleep(3)
    raise TimeoutError(tx)
def send(c,address,account,method,args):
    tx=str(c.write_contract(address=address,function_name=method,account=account,args=args,value=0));print(json.dumps({"submitted":tx,"method":method}),flush=True);return wait(c,tx)
def read(c,address,account,method,args):return plain(c.read_contract(address=address,function_name=method,args=args,account=account))
def main():
    if len(sys.argv)!=2:raise SystemExit("usage: run_studionet_e2e.py CONTRACT_ADDRESS")
    address=sys.argv[1];load();principal=create_account(os.environ["SERVICE_LEDGER_KEY_A"]);delegate=create_account(os.environ["SERVICE_LEDGER_KEY_B"]);c=create_client(chain=studionet,account=principal,endpoint=RPC)
    cfg=read(c,address,principal,"get_config",[])
    if cfg.get("version")!="SCOPE_RELAY_V1" or cfg.get("deployer_authority")!="NONE":raise AssertionError(cfg)
    create=send(c,address,principal,"create_mandate",["PROD_MAINTENANCE","Maintain the production API and rotate expiring TLS certificates.","Do not change DNS ownership, registrar control, payment accounts, or production data.",str(delegate.address)]);hid=int(str(create["returned"]).strip('"'));opened=read(c,address,principal,"get_handoff",[hid]);accept=send(c,address,delegate,"accept_mandate",[hid,opened["mandate_digest"]]);accepted=read(c,address,delegate,"get_handoff",[hid]);submit=send(c,address,delegate,"submit_plan",[hid,"Renew the TLS certificate, update the load balancer certificate reference, and restart the API gateway."]);locked=read(c,address,delegate,"get_handoff",[hid]);assess=send(c,address,principal,"assess_handoff",[hid]);aligned=read(c,address,principal,"get_handoff",[hid]);
    if aligned["state"]!="ALIGNED":raise AssertionError(aligned)
    completion=send(c,address,delegate,"record_completion",[hid,"Certificate reference updated; gateway restart recorded by delegate."]);final=read(c,address,delegate,"get_handoff",[hid]);e={"network":"studionet","contract":address,"contract_url":f"{EX}/address/{address}","principal":str(principal.address),"delegate":str(delegate.address),"assessment_trigger":"principal; verdict controlled by independent validator consensus","config":cfg,"create":create,"accept":accept,"submit_plan":submit,"assess":assess,"completion":completion,"opened":opened,"accepted":accepted,"locked":locked,"aligned":aligned,"final":final};(ROOT/"docs"/"studionet-e2e.json").write_text(json.dumps(e,indent=2)+"\n",encoding="utf-8");print(json.dumps(e,indent=2))
if __name__=="__main__":main()

import hashlib,json
from pathlib import Path
import pytest
from run_retail import checked_contracts,main

def test_contract_changes_rejected(tmp_path):
 (tmp_path/'reports/execution').mkdir(parents=True);(tmp_path/'reports/diagnosis').mkdir(parents=True)
 (tmp_path/'framing').mkdir();path=tmp_path/'framing/retail_contract.yaml';path.write_text('fixed')
 h=hashlib.sha256(path.read_bytes()).hexdigest()
 (tmp_path/'reports/diagnosis/human-approval.json').write_text(json.dumps({'decision':'PASS','contracts':{'framing/retail_contract.yaml':h}}))
 (tmp_path/'reports/execution/approved-contracts.json').write_text(json.dumps({'approved_sha256':{'framing/retail_contract.yaml':h}}))
 ap=tmp_path/'reports/diagnosis/human-approval.json';a=json.loads(ap.read_text());a['compiled_contract_sha256']=hashlib.sha256((tmp_path/'reports/execution/approved-contracts.json').read_bytes()).hexdigest();ap.write_text(json.dumps(a))
 assert checked_contracts(tmp_path)['approved_sha256']['framing/retail_contract.yaml']==h
 path.write_text('changed')
 with pytest.raises(ValueError,match='hash'):checked_contracts(tmp_path)

def test_holdout_command_reserved_before_validation(tmp_path):
 with pytest.raises(ValueError,match='reservado'):main(['holdout','--root',str(tmp_path)])

def test_path_escape_in_manifest_rejected(tmp_path):
 (tmp_path/'reports/execution').mkdir(parents=True);(tmp_path/'reports/diagnosis').mkdir(parents=True)
 (tmp_path/'reports/diagnosis/human-approval.json').write_text(json.dumps({'decision':'PASS','contracts':{'../secret':'x'}}))
 (tmp_path/'reports/execution/approved-contracts.json').write_text(json.dumps({'approved_sha256':{'../secret':'x'}}))
 ap=tmp_path/'reports/diagnosis/human-approval.json';a=json.loads(ap.read_text());a['compiled_contract_sha256']=hashlib.sha256((tmp_path/'reports/execution/approved-contracts.json').read_bytes()).hexdigest();ap.write_text(json.dumps(a))
 with pytest.raises(ValueError,match='path'):checked_contracts(tmp_path)

def test_compiled_contract_representation_tampering_rejected(tmp_path):
 (tmp_path/'reports/execution').mkdir(parents=True);(tmp_path/'reports/diagnosis').mkdir(parents=True)
 path=tmp_path/'reports/execution/approved-contracts.json';path.write_text(json.dumps({'approved_sha256':{},'retail':{'capacity':100}}))
 approved=hashlib.sha256(path.read_bytes()).hexdigest()
 (tmp_path/'reports/diagnosis/human-approval.json').write_text(json.dumps({'decision':'PASS','contracts':{},'compiled_contract_sha256':approved}))
 assert checked_contracts(tmp_path)['retail']['capacity']==100
 path.write_text(json.dumps({'approved_sha256':{},'retail':{'capacity':999}}))
 with pytest.raises(ValueError,match='representación'):checked_contracts(tmp_path)

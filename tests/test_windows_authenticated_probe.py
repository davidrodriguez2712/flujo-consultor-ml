"""Checks de las trazas del probe, sin turns de modelo."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'scripts/ci'))
spec = importlib.util.spec_from_file_location('windows_authenticated_probe', ROOT / 'scripts/ci/windows_authenticated_probe.py')
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def test_skill_claim_is_not_trace():
    events = [{'type':'item.completed', 'item':{'type':'agent_message',
               'text':'MARK validation BLOCKED: falta fecha de disponibilidad de labels. Usé design-validation: split temporal.'}}]
    result = probe.evidence('codex', '\n'.join(map(json.dumps,events)), 'MARK', True)
    assert not result['passed']


def test_codex_read_and_state_are_verified():
    events = [{'type':'item.completed', 'item':{'type':'command_execution',
               'command':'Get-Content .agents/skills/design-validation/SKILL.md', 'exit_code':0}},
              {'type':'item.completed', 'item':{'type':'agent_message',
               'text':'MARK validation BLOCKED: falta fecha de disponibilidad de labels; split temporal.'}}]
    assert probe.evidence('codex', '\n'.join(map(json.dumps, events)), 'MARK', True)['passed']


def test_claude_requires_native_skill_tool():
    event = {'type':'assistant', 'message':{'content':[
        {'type':'tool_use', 'id':'skill-1', 'name':'Skill', 'input':{'skill':'design-validation'}},
        {'type':'text','text':'MARK validation BLOCKED: falta fecha de disponibilidad de labels; split temporal.'}]}}
    result = {'type':'user', 'message':{'content':[{'type':'tool_result',
              'tool_use_id':'skill-1','content':'Launching skill: design-validation','is_error':False}]}}
    assert probe.evidence('claude', json.dumps(event)+'\n'+json.dumps(result), 'MARK', True)['passed']


def test_claude_skill_error_is_not_a_successful_invocation():
    event = {'type':'assistant', 'message':{'content':[
        {'type':'tool_use','id':'skill-1','name':'Skill','input':{'skill':'design-validation'}},
        {'type':'text','text':'MARK validation BLOCKED: falta fecha de disponibilidad de labels; split temporal.'}]}}
    result = {'type':'user', 'message':{'content':[{'type':'tool_result',
              'tool_use_id':'skill-1','content':'Skill unavailable','is_error':True}]}}
    assert not probe.evidence('claude',json.dumps(event)+'\n'+json.dumps(result),'MARK',True)['passed']


def test_fixture_is_generated_with_stale_views_and_no_gate_approvals(tmp_path):
    skill = ROOT / 'tests/fixtures/windows-runtime/design-validation/SKILL.md'
    project, marker = probe.fixture(tmp_path, skill)
    assert marker in (project / '.acos/state.yaml').read_text()
    assert marker not in (project / 'STATE.md').read_text()
    assert 'gate_reviews: {}' in (project / '.acos/state.yaml').read_text()
    assert probe.hashes(project)


def test_console_decoding_preserves_ascii_marker_with_oem_bytes():
    raw = b'CHURN-WIN-MARK: retenci\xa2n'
    assert 'CHURN-WIN-MARK' in probe.decode_console(raw)

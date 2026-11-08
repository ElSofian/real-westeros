"""Real private assembly with synthetic native inputs, not a CK3 simulation."""
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from tools import prepare_final_campaign as pack
from test_g1_native_choice import FIXTURE as WAR
from test_native_house_confiscation import FIXTURE as REVOKE
from test_native_restitution import FIXTURE as GRANT
from test_g1_royal_response import contract_errors as royal_errors
from test_declaration_law_context import contract_errors as law_errors
from test_native_war_intervention import errors as intervention_errors
from test_war_receipt_lifecycle import errors as lifecycle_errors
from test_external_war_responses import FILES as EXTERNAL_FILES, routing_errors
from test_external_native_intervention import FILES as EXTERNAL_NATIVE_FILES, intervention_errors as external_native_errors
from test_external_mediation import FILES as MEDIATION_FILES, mediation_errors
from test_external_war_ai import VALUES as WAR_AI_VALUES, ACTION_DIGESTS as WAR_AI_EVENTS, policy_errors as war_ai_errors
from test_peer_war_ai import VALUES as PEER_AI_VALUES, SHARED as PEER_AI_SHARED, EVENT as PEER_AI_EVENT, peer_policy_errors
from test_external_title_stakes import CONTEXT as EXTERNAL_TITLE_STAKES_CONTEXT, stakes_errors as external_title_stakes_errors
from test_peer_title_stakes import CONTEXT as PEER_TITLE_STAKES_CONTEXT, stakes_errors as peer_title_stakes_errors
from test_protected_title_stakes import CONTEXT as TITLE_STAKES_CONTEXT, stakes_errors
from test_external_beneficiary import CONTEXT as EXTERNAL_BENEFICIARY_CONTEXT, beneficiary_errors as external_beneficiary_errors
from test_peer_beneficiary import CONTEXT as BENEFICIARY_CONTEXT, beneficiary_errors
from test_committed_war_support import support_errors
from test_declaration_military_risk import military_errors
from test_declaration_ai import VALUES as DECLARATION_AI_VALUES, CONTEXT as DECLARATION_AI_CONTEXT, declaration_policy_errors


WAR_FILES = {
    'triggers': 'common/scripted_triggers/rw_unlawful_war_choice_triggers.txt',
    'response': 'common/scripted_effects/rw_unlawful_war_response_effects.txt',
    'story': 'common/story_cycles/rw_unlawful_war_responses.txt',
    'law_triggers': 'common/scripted_triggers/rw_declaration_law_triggers.txt',
    'law_effects': 'common/scripted_effects/rw_declaration_law_effects.txt',
    'law_story': 'common/story_cycles/rw_declaration_law.txt',
    'intervention': 'common/scripted_effects/rw_unlawful_war_intervention_effects.txt',
    'lifecycle': 'common/scripted_effects/rw_war_lifecycle_effects.txt',
}


def war_guard_errors(sources):
    """Reuse source checks on delivered bytes; this does not execute game logic."""
    return {
        'royal': royal_errors(sources['triggers'], sources['response'], sources['story']),
        'law': law_errors(sources['law_triggers'], sources['law_effects'], sources['law_story']),
        'intervention': intervention_errors(sources['triggers'], sources['intervention']),
        'lifecycle': lifecycle_errors(sources['triggers'], sources['lifecycle'], sources['story']),
    }


class CampaignPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.TemporaryDirectory(prefix='rw-pack-fixture-')
        cls.fixture = Path(cls.shared.name)
        repo = cls.fixture/'repo'
        shutil.copytree(pack.REPO/'mod', repo/'mod')
        for name in (*pack.distribution.DOCS, *pack.distribution.G3_FILES):
            target=repo/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(pack.REPO/name,target)
        def git(*args):
            return subprocess.check_output(['git','-C',str(repo),*args],stderr=subprocess.PIPE)
        git('init','-q');git('config','core.autocrlf','false');git('add','.')
        git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid',
            '-c','core.hooksPath=/dev/null','commit','-qm','Fixture')
        cls.commit=git('rev-parse','HEAD').decode().strip()
        cls.archive=cls.fixture/'release.zip'
        pack.distribution.build(repo,cls.archive)

    @classmethod
    def tearDownClass(cls):cls.shared.cleanup()

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='rw-pack-test-');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.agot=self.root/'AGOT';self.agot.mkdir();self.out=self.root/'private'
        self.archive=self.root/'release.zip'
        shutil.copyfile(self.__class__.archive,self.archive)
        shutil.copyfile(self.__class__.archive.with_suffix('.zip.sha256'),self.archive.with_suffix('.zip.sha256'))
        (self.agot/'descriptor.mod').write_text('version="0.5.2.1"\nsupported_version="1.19.0.6"\n')
        self.inputs={pack.war.INTERACTION:WAR.encode(),
            pack.war.HELPER:b'war_declarer_needs_hook_on_liege = { scope:actor = { synthetic_peer = scope:recipient } }',
            pack.war.CLAIM:b'claim_cb = { on_declaration = { original = yes } on_victory = {} on_defeat = {} on_white_peace = {} on_invalidated = {} }',
            pack.war.VASSAL:b'stop_attacker_vassal_war_interaction = { on_accept = { synthetic_negotiation = yes } }',pack.revoke.INPUT:REVOKE.encode(),pack.grant.INPUT:GRANT}
        for name,data in self.inputs.items():
            dest=self.agot/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        self.pins={n:hashlib.sha256(b).hexdigest() for n,b in self.inputs.items()}
        for module,name,value in ((pack.war,'pinned_sources',{n:self.pins[n] for n in (pack.war.INTERACTION,pack.war.HELPER,pack.war.CLAIM,pack.war.VASSAL)}),
                                  (pack.revoke,'pin',self.pins[pack.revoke.INPUT]),(pack.grant,'pin',self.pins[pack.grant.INPUT])):
            p=patch.object(module,name,return_value=value);p.start();self.addCleanup(p.stop)

    def prepare(self):return pack.prepare(self.archive,self.agot,self.out)

    def rewrite(self,change):
        with zipfile.ZipFile(self.archive) as z:entries=[(i,z.read(i)) for i in z.infolist()]
        entries=change(entries)
        with zipfile.ZipFile(self.archive,'w') as z:
            for info,data in entries:z.writestr(info,data)
        self.archive.with_suffix('.zip.sha256').write_text(hashlib.sha256(self.archive.read_bytes()).hexdigest()+'  release.zip\n')

    def rejected(self):
        with self.assertRaises((ValueError,KeyError,OSError,zipfile.BadZipFile)):self.prepare()
        self.assertFalse(self.out.exists())
        self.assertFalse(list(self.root.glob('rw-private-campaign-*')))

    def test_assembles_exact_base_and_three_real_builders(self):
        before={n:(self.agot/n).read_bytes() for n in self.inputs}
        result=self.prepare()
        self.assertEqual(self.commit,result['distribution_commit'])
        self.assertEqual(0,result['engine_cases_executed'])
        self.assertEqual(5,len(result['load_order']))
        with zipfile.ZipFile(self.archive) as z:
            for name in z.namelist():
                if not name.endswith('/'):self.assertEqual(z.read(name),(self.out/name).read_bytes())
        for adapter in result['adapters']:
            r=json.loads((self.out/adapter['receipt']).read_text())
            for row in r['runtime_sources']:
                self.assertEqual(row['sha256'],hashlib.sha256((self.out/'mod/real_westeros'/row['path']).read_bytes()).hexdigest())
            for row in r['outputs']:
                self.assertEqual(row['sha256'],hashlib.sha256((self.out/'mod'/adapter['id']/row['path']).read_bytes()).hexdigest())
            self.assertIn('path="mod/'+adapter['id']+'"',(self.out/'mod'/(adapter['id']+'.mod')).read_text())
        self.assertEqual(before,{n:(self.agot/n).read_bytes() for n in self.inputs})
        serialized=json.dumps(result)+''.join((self.out/a['receipt']).read_text() for a in result['adapters'])
        self.assertNotIn(str(self.agot),serialized)
        self.assertEqual(result,json.loads((self.out/pack.READY).read_text()))
        self.assertIn('ne jamais publier',(self.out/'PRIVATE_README.txt').read_text())
        sources = {key: (self.out/'mod/real_westeros'/name).read_text(encoding='utf-8-sig')
                   for key, name in WAR_FILES.items()}
        self.assertEqual({name: [] for name in ('royal', 'law', 'intervention', 'lifecycle')},
                         war_guard_errors(sources))

        # Inspect the delivered adapter, including the genuine CB identifier.
        adapter = self.out/'mod'/pack.war.MOD_ID
        declaration = (adapter/'common/character_interactions/zz_rw_native_war_choice.txt').read_bytes().decode('utf-8-sig')
        for addition in (pack.war.GUARD, pack.war.OPTION, pack.war.ACCEPT):
            self.assertEqual(1, declaration.count(addition))
            declaration = declaration.replace(addition, '', 1)
        self.assertEqual(pack.war.top_definition(self.inputs[pack.war.INTERACTION], 'declare_war_interaction'),
                         declaration.removesuffix('\n'))
        claim = (adapter/'common/casus_belli_types/zz_rw_native_claim_law.txt').read_bytes().decode('utf-8-sig')
        for addition in (pack.war.LAW_PREFIX, *pack.war.TERMINAL_PREFIXES.values()):
            self.assertEqual(1, claim.count(addition))
            claim = claim.replace(addition, '', 1)
        self.assertEqual(pack.war.top_definition(self.inputs[pack.war.CLAIM], 'claim_cb'), claim.removesuffix('\n'))

    def test_assembled_war_guards_detect_foreign_stale_bypassed_and_replayed_paths(self):
        self.prepare()
        sources = {key: (self.out/'mod/real_westeros'/name).read_text(encoding='utf-8-sig')
                   for key, name in WAR_FILES.items()}
        mutations = (
            ('response', 'rw_uw_selected_defiance_trigger = yes', 'always = yes', 'royal'),
            ('triggers', 'var:rw_uw_serial = scope:rw_uw_serial', 'has_variable = rw_uw_serial', 'royal'),
            ('triggers', 'var:rw_uw_war = scope:rw_uw_war', 'var:rw_uw_war = scope:rw_uw_authority', 'royal'),
            ('triggers', 'holder = scope:rw_uw_issuer', 'always = yes', 'royal'),
            ('triggers', 'is_character_interaction_valid = {', 'always = {', 'intervention'),
            ('law_effects', 'rw_dl_link_response_effect = {',
             'rw_dl_link_response_effect = { rw_dl_capture_effect = yes', 'law'),
            ('lifecycle', 'every_war_participant = {', 'every_war_attacker = {', 'lifecycle'),
            ('lifecycle', 'remove_variable = rw_uw_live', '', 'lifecycle'),
            ('lifecycle', 'NOT = { has_variable = rw_uw_terminal_seen }', 'always = yes', 'lifecycle'),
        )
        for file, before, after, family in mutations:
            with self.subTest(file=file, guard=before):
                self.assertIn(before, sources[file])
                changed = dict(sources)
                changed[file] = changed[file].replace(before, after)
                self.assertTrue(war_guard_errors(changed)[family])

    def test_completion_receipt_covers_every_other_file(self):
        r=self.prepare();names={x['path'] for x in r['files']}
        self.assertEqual(names|{pack.READY},{p.relative_to(self.out).as_posix() for p in self.out.rglob('*') if p.is_file()})
        for x in r['files']:
            raw=(self.out/x['path']).read_bytes();self.assertEqual(len(raw),x['size']);self.assertEqual(hashlib.sha256(raw).hexdigest(),x['sha256'])

    def test_external_authority_guards_in_delivered_files(self):
        self.prepare()
        sources = {key: (self.out/'mod/real_westeros'/name).read_text(encoding='utf-8-sig')
                   for key, name in EXTERNAL_FILES.items()}
        self.assertEqual([], routing_errors(sources))
        for file, token in (
            ('triggers', 'var:rw_dl_accepted_choice = flag:defy_selected'),
            ('triggers', 'var:rw_dt_parent_serial = scope:rw_xw_source.var:rw_dl_serial'),
            ('effects', 'remove_variable = rw_xw_route_ready'),
            ('triggers', 'var:rw_xw_serial = scope:rw_xw_serial'),
            ('triggers', 'has_variable = rw_xw_demanded_on'),
            ('effects', 'modifier = rw_uw_refused_stop_opinion'),
        ):
            with self.subTest(file=file, guard=token):
                changed = dict(sources)
                changed[file] = changed[file].replace(token, 'always = yes')
                self.assertTrue(routing_errors(changed))

    def test_external_native_intervention_in_delivered_files(self):
        self.prepare()
        sources = {key: (self.out/'mod/real_westeros'/name).read_text(encoding='utf-8-sig')
                   for key, name in EXTERNAL_NATIVE_FILES.items()}
        self.assertEqual([], external_native_errors(sources))
        for file, token in (
            ('triggers', 'var:rw_xw_role = flag:declaring_liege'),
            ('triggers', 'is_character_interaction_valid = {'),
            ('triggers', 'NOT = { has_variable = rw_xw_native_bound_on }'),
            ('effects', 'var:rw_xw_native_send_record.var:rw_xw_war = { save_scope_as = target }'),
        ):
            with self.subTest(file=file, guard=token):
                changed = dict(sources)
                changed[file] = changed[file].replace(token, 'always = yes')
                self.assertTrue(external_native_errors(changed))

    def test_external_mediation_in_delivered_files(self):
        self.prepare()
        sources = {key: (self.out/'mod/real_westeros'/name).read_text(encoding='utf-8-sig')
                   for key, name in MEDIATION_FILES.items()}
        self.assertEqual([], mediation_errors(sources))
        for file, token in (
            ('triggers', 'var:rw_xm_native_ticket = scope:rw_xm_job'),
            ('effects', 'NOT = { has_variable = rw_xm_handoff_started }'),
            ('native', 'NOT = { this = scope:rw_xw_busy_check }'),
        ):
            with self.subTest(file=file, guard=token):
                changed = dict(sources)
                changed[file] = changed[file].replace(token, 'always = yes')
                self.assertTrue(mediation_errors(changed))

    def test_external_war_ai_in_delivered_files(self):
        self.prepare()
        base = self.out/'mod/real_westeros'
        values = (base/WAR_AI_VALUES).read_text(encoding='utf-8-sig')
        events = {file: (base/file).read_text(encoding='utf-8-sig') for file in WAR_AI_EVENTS}
        self.assertEqual([], war_ai_errors(values, events))
        for token in ('rw_xw_can_queue_native_trigger = yes',
                      'target = scope:rw_xw_record.var:rw_xw_target.var:rw_dt_holder',
                      'rw_xw_other_native_attempt_trigger = yes'):
            with self.subTest(guard=token):
                self.assertTrue(war_ai_errors(values.replace(token, 'always = yes'), events))

    def test_peer_war_ai_in_delivered_files(self):
        self.prepare()
        base = self.out/'mod/real_westeros'
        values = (base/PEER_AI_VALUES).read_text(encoding='utf-8-sig')
        shared = (base/PEER_AI_SHARED).read_text(encoding='utf-8-sig')
        event = (base/PEER_AI_EVENT).read_text(encoding='utf-8-sig')
        self.assertEqual([], peer_policy_errors(values, shared, event))
        for token in ('rw_uw_can_queue_native_trigger = yes', 'scope:rw_uw_defender', 'scope:rw_uw_war'):
            with self.subTest(guard=token):
                self.assertTrue(peer_policy_errors(values.replace(token, 'always = yes'), shared, event))

    def test_external_title_stakes_in_delivered_files(self):
        self.prepare()
        base = self.out/'mod/real_westeros'
        values = (base/WAR_AI_VALUES).read_text(encoding='utf-8-sig')
        context = (base/EXTERNAL_TITLE_STAKES_CONTEXT).read_text(encoding='utf-8-sig')
        self.assertEqual([], external_title_stakes_errors(values, context))
        for token in ('rw_xm_turn_trigger = yes',
                      'var:rw_dt_holder = scope:rw_xw_defender',
                      'var:rw_dt_parent_serial = scope:rw_xw_record.var:rw_xw_source_serial'):
            with self.subTest(guard=token):
                self.assertTrue(external_title_stakes_errors(values, context.replace(token, 'always = yes')))

    def test_peer_title_stakes_in_delivered_files(self):
        self.prepare()
        base = self.out/'mod/real_westeros'
        values = (base/PEER_AI_VALUES).read_text(encoding='utf-8-sig')
        context = (base/PEER_TITLE_STAKES_CONTEXT).read_text(encoding='utf-8-sig')
        self.assertEqual([], peer_title_stakes_errors(values, context))
        for token in ('var:rw_dl_targets_state = flag:all_titles_recorded',
                      'var:rw_dt_parent_serial = scope:rw_uw_record.var:rw_dl_link_serial',
                      'is_vassal_or_below_of = scope:rw_uw_defender'):
            with self.subTest(guard=token):
                self.assertTrue(peer_title_stakes_errors(values, context.replace(token, 'always = yes')))

    def test_protected_title_stakes_in_delivered_files(self):
        self.prepare()
        base = self.out/'mod/real_westeros'
        values = (base/WAR_AI_VALUES).read_text(encoding='utf-8-sig')
        context = (base/TITLE_STAKES_CONTEXT).read_text(encoding='utf-8-sig')
        self.assertEqual([], stakes_errors(values, context))
        for token in ('var:rw_dl_targets_state = flag:all_titles_recorded',
                      'var:rw_dt_parent_serial = scope:rw_xw_record.var:rw_xw_source_serial',
                      'var:rw_dt_title = { holder = prev.var:rw_dt_holder }'):
            with self.subTest(guard=token):
                self.assertTrue(stakes_errors(values, context.replace(token, 'always = yes')))

    def test_external_beneficiary_in_delivered_files(self):
        self.prepare()
        base = self.out/'mod/real_westeros'
        values = (base/WAR_AI_VALUES).read_text(encoding='utf-8-sig')
        context = (base/EXTERNAL_BENEFICIARY_CONTEXT).read_text(encoding='utf-8-sig')
        self.assertEqual([], external_beneficiary_errors(values, context))
        for token in ('rw_xm_turn_trigger = yes',
                      'var:rw_dl_serial = prev.var:rw_xw_source_serial',
                      'var:rw_dl_claimant_state = flag:known'):
            with self.subTest(guard=token):
                self.assertTrue(external_beneficiary_errors(values, context.replace(token, 'always = yes')))

    def test_peer_beneficiary_in_delivered_files(self):
        self.prepare()
        base = self.out/'mod/real_westeros'
        values = (base/PEER_AI_VALUES).read_text(encoding='utf-8-sig')
        context = (base/BENEFICIARY_CONTEXT).read_text(encoding='utf-8-sig')
        self.assertEqual([], beneficiary_errors(values, context))
        for token in ('rw_dl_match_response_trigger = yes',
                      'var:rw_dl_serial = prev.var:rw_dl_link_serial',
                      'var:rw_dl_claimant_state = flag:known'):
            with self.subTest(guard=token):
                self.assertTrue(beneficiary_errors(values, context.replace(token, 'always = yes')))

    def test_committed_war_support_in_delivered_files(self):
        self.prepare()
        base = self.out/'mod/real_westeros'
        sources = {name: (base/name).read_text(encoding='utf-8-sig')
                   for name in (PEER_AI_VALUES, WAR_AI_VALUES)}
        self.assertEqual([], support_errors(sources))
        for name in sources:
            with self.subTest(profile=name):
                changed = dict(sources)
                changed[name] = changed[name].replace('current_military_strength > 0', 'always = yes', 1)
                self.assertTrue(support_errors(changed))

    def test_declaration_military_risk_in_delivered_files(self):
        self.prepare()
        values = (self.out/'mod/real_westeros'/DECLARATION_AI_VALUES).read_text(encoding='utf-8-sig')
        self.assertEqual([], military_errors(values))
        for token in ('scope:recipient = { current_military_strength > 0 }',
                      'scope:actor.liege = { current_military_strength > 0 }',
                      'max_military_strength > 0'):
            with self.subTest(denominator=token):
                self.assertTrue(military_errors(values.replace(token, 'always = yes')))

    def test_declaration_ai_in_delivered_files(self):
        self.prepare()
        base = self.out/'mod/real_westeros'
        values = (base/DECLARATION_AI_VALUES).read_text(encoding='utf-8-sig')
        context = (base/DECLARATION_AI_CONTEXT).read_text(encoding='utf-8-sig')
        choices = (base/WAR_FILES['triggers']).read_text(encoding='utf-8-sig')
        shared = (base/PEER_AI_SHARED).read_text(encoding='utf-8-sig')
        self.assertEqual([], declaration_policy_errors(values, context, choices, shared))
        for token in ('subtract = rw_ai_wd_honor_value', 'has_usable_hook = scope:actor.liege',
                      'has_dread_level_towards = { target = scope:actor.liege level = 2 }'):
            with self.subTest(input=token):
                self.assertTrue(declaration_policy_errors(values.replace(token, 'always = yes'), context, choices, shared))

    def test_bad_or_missing_checksum_rejected(self):
        self.archive.with_suffix('.zip.sha256').write_text('0'*64+'  release.zip\n');self.rejected()
        self.archive.with_suffix('.zip.sha256').unlink();self.rejected()

    def test_changed_payload_even_with_updated_zip_checksum_rejected(self):
        self.rewrite(lambda entries:[(i,b'changed' if i.filename=='README.md' else data) for i,data in entries]);self.rejected()

    def test_unmanifested_payload_rejected(self):
        self.rewrite(lambda e:e+[(zipfile.ZipInfo('private.txt'),b'not public')]);self.rejected()

    def test_old_running_tools_cannot_mix_with_new_zip(self):
        def changed(entries):
            changed=[];digest=None;size=None
            for info,data in entries:
                if info.filename=='tools/validate_mod.py':
                    data+=b'\n# another release\n';digest=hashlib.sha256(data).hexdigest();size=len(data)
                changed.append((info,data))
            result=[]
            for info,data in changed:
                if info.filename=='MANIFEST.json':
                    m=json.loads(data)
                    row=next(x for x in m['files'] if x['path']=='tools/validate_mod.py')
                    row.update(size=size,sha256=digest);data=json.dumps(m).encode()
                result.append((info,data))
            return result
        self.rewrite(changed)
        with self.assertRaisesRegex(ValueError,'exact distribution'):self.prepare()
        self.assertFalse(self.out.exists())

    def test_shipped_entrypoint_runs_without_git_or_repository_cwd(self):
        extracted=self.root/'extracted'
        with zipfile.ZipFile(self.archive) as z:z.extractall(extracted)
        import sys
        result=subprocess.run([sys.executable,str(extracted/'tools/prepare_final_campaign.py'),'--help'],
            cwd=self.root,capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stderr)
        self.assertIn('--distribution',result.stdout)

    def test_traversal_absolute_windows_and_case_collision_rejected(self):
        original=self.archive.read_bytes();original_sum=self.archive.with_suffix('.zip.sha256').read_bytes()
        for name in ('../escape','/absolute','C:/escape','tools\\escape','readme.md'):
            with self.subTest(name=name):
                self.archive.write_bytes(original);self.archive.with_suffix('.zip.sha256').write_bytes(original_sum)
                self.rewrite(lambda e:e+[(zipfile.ZipInfo(name),b'escape')]);self.rejected()
        self.assertFalse((self.root/'escape').exists())

    def test_symlink_archive_entry_rejected(self):
        info=zipfile.ZipInfo('link');info.create_system=3;info.external_attr=(stat.S_IFLNK|0o777)<<16
        self.rewrite(lambda e:e+[(info,b'README.md')]);self.rejected()

    def test_wrong_native_bytes_abort_before_ready_output(self):
        for name,data in self.inputs.items():
            with self.subTest(name=name):
                (self.agot/name).write_bytes(data+b'changed');self.rejected();(self.agot/name).write_bytes(data)

    def test_wrong_version_or_missing_source_rejected(self):
        (self.agot/'descriptor.mod').write_text('version="0.5.2.2"\nsupported_version="1.19.0.6"');self.rejected()
        (self.agot/'descriptor.mod').write_text('version="0.5.2.1"\nsupported_version="1.19.0.6"')
        (self.agot/pack.grant.INPUT).unlink();self.rejected()

    def test_existing_destination_is_untouched(self):
        self.out.mkdir();(self.out/'KEEP').write_text('original')
        with self.assertRaises(ValueError):self.prepare()
        self.assertEqual(['KEEP'],[p.name for p in self.out.iterdir()])
        self.assertEqual('original',(self.out/'KEEP').read_text())

    def test_no_output_in_installation_or_checkout_or_their_parent(self):
        for out in (self.agot/'new',self.agot,self.root,pack.REPO/'new'):
            with self.subTest(out=out),self.assertRaises(ValueError):pack.prepare(self.archive,self.agot,out)

    def test_symlink_source_directory_or_output_parent_rejected(self):
        link=self.root/'linked'
        try:link.symlink_to(self.agot,target_is_directory=True)
        except OSError as exc:
            if getattr(exc,'winerror',None)==1314:self.skipTest('Windows symlink privilege unavailable')
            raise
        with self.assertRaises(ValueError):pack.prepare(self.archive,link,self.out)
        with self.assertRaises(ValueError):pack.prepare(self.archive,self.agot,link/'new')

    def test_adapter_runtime_mismatch_rejected_and_globals_restored(self):
        previous=(pack.war.REPO,pack.war.TEMPLATES)
        with patch.object(pack.war,'build',return_value={'runtime_sources':[{'path':'descriptor.mod','sha256':'0'*64}]}):self.rejected()
        self.assertEqual(previous,(pack.war.REPO,pack.war.TEMPLATES))

    def test_final_copy_failure_leaves_no_ready_or_partial_destination(self):
        # Windows can expand 8.3 temp paths during resolve(). Exercise an alias
        # on every platform so the injected I/O failure still reaches final copy.
        (self.root/'nested').mkdir()
        self.out=self.root/'nested'/'..'/'private'
        original=shutil.copytree
        def fail(src,dst,*args,**kwargs):
            if Path(dst).resolve()==self.out.resolve():
                (self.out/'partial').write_text('partial');raise OSError('synthetic disk error')
            return original(src,dst,*args,**kwargs)
        with patch.object(pack.shutil,'copytree',side_effect=fail):self.rejected()

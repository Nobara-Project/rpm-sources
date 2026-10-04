#!/usr/bin/python3
"""Run the rebuild helper against temporary boot trees and a recording dracut."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SOURCE = Path(__file__).with_name('drm-awaiter-initramfs').read_text()


class InitramfsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.boot = self.root / 'boot'
        self.modules = self.root / 'modules'
        self.runtime = self.root / 'run'
        self.boot.mkdir()
        self.modules.mkdir()
        self.calls = self.root / 'calls.jsonl'
        dracut = self.root / 'dracut'
        dracut.write_text('''#!/usr/bin/python3
import json, os, sys
with open(os.environ['TEST_CALLS'], 'a') as stream:
    stream.write(json.dumps(sys.argv[1:]) + '\\n')
if '--regenerate-all' in sys.argv or os.environ.get('TEST_FAIL_KERNEL') in sys.argv:
    print("dracut[F]: Cannot write to an absent EFI kernel directory", file=sys.stderr)
    sys.exit(1)
''')
        dracut.chmod(0o755)
        # No test-only path or command overrides are exposed in production.
        script = SOURCE.replace('/run/drm-awaiter', str(self.runtime))
        script = script.replace('/lib/modules', str(self.modules)).replace('/boot', str(self.boot))
        script = script.replace('/usr/bin/dracut', str(dracut))
        self.helper = self.root / 'helper'
        self.helper.write_text(script)
        self.env = dict(os.environ, TEST_CALLS=str(self.calls))
        self.pending = self.runtime / 'initramfs-pending'

    def kernel(self, version, *, layout='split', image='vmlinuz'):
        modules = self.modules / version
        modules.mkdir()
        (modules / 'modules.dep').touch()
        if layout == 'split':
            (self.boot / (image + '-' + version)).write_text('kernel')
        elif layout == 'module':
            (modules / 'vmlinuz').write_text('kernel')
        return modules

    def run_helper(self, action, *, success=True):
        result = subprocess.run(['bash', str(self.helper), action], env=self.env,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout + result.stderr)
        return result

    def recorded(self):
        return [json.loads(line) for line in self.calls.read_text().splitlines()] if self.calls.exists() else []

    def test_orphan_modules_do_not_abort_installed_kernel_rebuild(self):
        self.kernel('7.1.8-old', layout='orphan')
        self.kernel('7.2.8-current')
        (self.boot / 'efi/loader/entries').mkdir(parents=True)
        self.run_helper('request')
        result = self.run_helper('flush')
        self.assertIn('Skipping module tree without an installed kernel image: 7.1.8-old', result.stdout)
        self.assertEqual(self.recorded(), [['--force', '--kver', '7.2.8-current', '--no-uefi',
                                           str(self.boot / 'initramfs-7.2.8-current.img')]])
        self.assertTrue((self.modules / '7.1.8-old/modules.dep').exists())
        self.assertFalse(self.pending.exists())

    def test_all_retained_kernels_are_rebuilt_once_per_queued_transaction(self):
        for version in ('6.18-lts', '7.2-mainline', '7.3-custom'):
            self.kernel(version)
        self.run_helper('request')
        self.run_helper('request')
        self.run_helper('flush')
        self.run_helper('flush')
        self.assertEqual([args[2] for args in self.recorded()], ['6.18-lts', '7.2-mainline', '7.3-custom'])

    def test_real_failure_retains_request_and_still_checks_other_kernels(self):
        self.kernel('6.18-lts')
        self.kernel('7.2-mainline')
        self.env['TEST_FAIL_KERNEL'] = '6.18-lts'
        self.run_helper('request')
        result = self.run_helper('flush', success=False)
        self.assertIn('GPU initramfs rebuild failed', result.stderr)
        self.assertTrue(self.pending.exists())
        self.assertEqual(len(self.recorded()), 2)
        self.env.pop('TEST_FAIL_KERNEL')
        self.run_helper('flush')
        self.assertFalse(self.pending.exists())
        self.assertEqual(len(self.recorded()), 4)

    def test_module_image_layout_keeps_native_dracut_destination_policy(self):
        self.kernel('7.2-uki', layout='module')
        self.run_helper('request')
        self.run_helper('flush')
        self.assertEqual(self.recorded(), [['--force', '--kver', '7.2-uki']])

    def test_boot_image_layout_wins_even_when_module_image_also_exists(self):
        modules = self.kernel('7.2-split')
        (modules / 'vmlinuz').touch()
        self.run_helper('request')
        self.run_helper('flush')
        self.assertEqual(self.recorded()[0][-1], str(self.boot / 'initramfs-7.2-split.img'))

    def test_alternative_split_kernel_names_have_explicit_destinations(self):
        self.kernel('7.2-debug', image='vmlinux')
        self.kernel('7.2-custom', image='kernel')
        self.run_helper('request')
        self.run_helper('flush')
        self.assertEqual(len(self.recorded()), 2)
        for args in self.recorded():
            self.assertEqual(args[-1], str(self.boot / ('initramfs-' + args[2] + '.img')))

    def test_missing_kernel_images_cannot_claim_rebuild_success(self):
        for orphan in (False, True):
            with self.subTest(orphan=orphan):
                if orphan:
                    self.kernel('removed-kernel', layout='orphan')
                self.run_helper('request')
                result = self.run_helper('flush', success=False)
                self.assertIn('No installed kernel images found', result.stderr)
                self.assertTrue(self.pending.exists())
                self.assertFalse(self.recorded())

    def test_no_pending_request_does_no_work(self):
        self.kernel('7.2-current')
        self.run_helper('flush')
        self.assertFalse(self.recorded())


if __name__ == '__main__':
    unittest.main()

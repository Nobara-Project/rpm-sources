#!/usr/bin/python3
"""Exercise boot topology decisions without loading modules or writing to /run."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).with_name('drm-module-awaiter-generator').read_text()


class GeneratorTests(unittest.TestCase):
    def run_fixture(self, devices=(), config='', cmdline='', initrd=False, missing=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pci = root / 'pci'
            pci.mkdir()
            aliases = root / 'aliases'
            aliases.mkdir()
            for index, device in enumerate(devices):
                path = pci / str(index)
                path.mkdir()
                (path / 'class').write_text(device.get('class', '0x030000'))
                alias = device.get('alias', f'pci:fixture-{index}')
                (path / 'modalias').write_text(alias)
                (aliases / alias).write_text(''.join(m + '\n' for m in device.get('modules', [])))
                (path / 'driver_override').write_text(device.get('override', '(null)'))
                if 'bound' in device:
                    (path / 'driver').symlink_to('/drivers/' + device['bound'])
            (root / 'cmdline').write_text(cmdline)
            if initrd:
                (root / 'initrd-release').touch()
            script = SOURCE.replace('/sys/bus/pci/devices', str(pci))
            script = script.replace('/proc/cmdline', str(root / 'cmdline'))
            script = script.replace('/etc/initrd-release', str(root / 'initrd-release'))
            (root / 'generator').write_text(script)
            # Bash functions mock kmod only. The production script has no test
            # environment overrides for sysfs or command execution.
            harness = '''
modprobe() {
    case "$1" in
        -c) printf '%s\\n' "$CONFIG" ;;
        -b) [[ $2 == -R ]] || return 1
            cat "$ALIASES_DIR/$3" ;;
        *) return 1 ;;
    esac
}
modinfo() { [[ $MISSING != 1 ]]; }
source "$1"
generate "$2"
'''
            env = dict(os.environ, CONFIG=config,
                       ALIASES_DIR=str(aliases),
                       MISSING=str(int(missing)))
            result = subprocess.run(['bash', '-c', harness, 'fixture', str(root / 'generator'), str(root / 'out')],
                                    env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.stderr = result.stderr
            return {str(p.relative_to(root / 'out')): p.read_text()
                    for p in (root / 'out').rglob('*') if p.is_file()}

    def test_nvidia_only_actively_loads_drm(self):
        files = self.run_fixture([{'modules': ['nvidia', 'nouveau']}], 'blacklist nouveau')
        service = files['drm-module-load.service']
        self.assertIn('ExecStart=-/usr/sbin/modprobe -b nvidia_drm', service)
        self.assertNotIn('modprobe -b nouveau', service)
        self.assertIn('TimeoutStartSec=30s', service)
        self.assertIn('After=drm-module-load.service', files['drm-module-load.target'])
        for unit in ['display-manager.service', 'getty@tty1.service']:
            self.assertIn('After=drm-module-load.target', files[unit + '.d/50-drm-awaiter.conf'])

    def test_hybrid_deduplicated_and_nvidia_last(self):
        files = self.run_fixture([{'modules': ['nvidia']}, {'modules': ['amdgpu']}, {'modules': ['amdgpu']}])
        service = files['drm-module-load.service']
        self.assertEqual(service.count('modprobe -b amdgpu'), 1)
        self.assertLess(service.index('modprobe -b amdgpu'), service.index('modprobe -b nvidia_drm'))

    def test_nouveau_wildcard_resolution(self):
        files = self.run_fixture([{'alias': 'pci:full-wildcard-alias', 'modules': ['nouveau']}])
        self.assertIn('modprobe -b nouveau', files['drm-module-load.service'])

    def test_intel_probe_policy_left_to_kernel(self):
        files = self.run_fixture([{'modules': ['i915', 'xe']}], 'options xe force_probe=1234')
        self.assertIn('modprobe -b i915', files['drm-module-load.service'])
        self.assertIn('modprobe -b xe', files['drm-module-load.service'])

    def test_blacklists_and_normalized_names(self):
        for config, cmdline in [('blacklist nvidia-drm', ''), ('blacklist nvidia', ''),
                                ('blacklist nvidia_modeset', ''), ('', 'module_blacklist=nvidia-drm')]:
            with self.subTest(config=config, cmdline=cmdline):
                self.assertEqual(self.run_fixture([{'modules': ['nvidia']}], config, cmdline), {})

    def test_missing_dkms_module(self):
        self.assertEqual(self.run_fixture([{'modules': ['nvidia']}], missing=True), {})

    def test_nvidia_preferred_over_competing_drivers(self):
        for modules in [['nouveau', 'nvidia'], ['nvidia', 'nouveau'],
                        ['nova-core', 'nova-drm', 'nouveau', 'nvidia']]:
            with self.subTest(modules=modules):
                files = self.run_fixture([{'modules': modules}])
                commands = [line for line in files['drm-module-load.service'].splitlines()
                            if line.startswith('ExecStart=')]
                self.assertEqual(commands, ['ExecStart=-/usr/sbin/modprobe -b nvidia_drm'])
                self.assertIn('competing drivers', self.stderr)

    def test_nvidia_preference_respects_blacklists(self):
        for config, cmdline in [('blacklist nvidia', ''), ('blacklist nvidia-drm', ''),
                                ('blacklist nvidia_modeset', ''),
                                ('', 'module_blacklist=nvidia'),
                                ('', 'module_blacklist=nvidia-drm')]:
            with self.subTest(config=config, cmdline=cmdline):
                files = self.run_fixture([{'modules': ['nvidia', 'nouveau']}], config, cmdline)
                service = files['drm-module-load.service']
                self.assertIn('modprobe -b nouveau', service)
                self.assertNotIn('modprobe -b nvidia_drm', service)

    def test_nouveau_fallback_when_nvidia_drm_is_missing(self):
        files = self.run_fixture([{'modules': ['nvidia', 'nouveau']}], missing=True)
        service = files['drm-module-load.service']
        self.assertIn('modprobe -b nouveau', service)
        self.assertNotIn('modprobe -b nvidia_drm', service)

    def test_driver_selection_is_per_device(self):
        files = self.run_fixture([{'modules': ['nvidia', 'nouveau']},
                                  {'modules': ['nouveau']}, {'modules': ['amdgpu']}])
        service = files['drm-module-load.service']
        for module in ['nouveau', 'amdgpu', 'nvidia_drm']:
            self.assertEqual(service.count('modprobe -b ' + module), 1)

    def test_existing_nouveau_binding_is_not_replaced(self):
        device = {'bound': 'nouveau', 'modules': ['nvidia', 'nouveau']}
        files = self.run_fixture([device])
        service = files['drm-module-load.service']
        self.assertIn('modprobe -b nouveau', service)
        self.assertNotIn('modprobe -b nvidia_drm', service)
        self.assertEqual(self.run_fixture([device], 'blacklist nouveau'), {})
        self.assertIn('already bound to blacklisted driver nouveau', self.stderr)

    def test_headless_unknown_and_non_display(self):
        for devices in [[], [{'modules': ['snd_hda_intel']}], [{'class': '0x020000', 'modules': ['amdgpu']}]]:
            self.assertEqual(self.run_fixture(devices), {})

    def test_initrd_and_recovery_opt_out(self):
        self.assertEqual(self.run_fixture([{'modules': ['amdgpu']}], initrd=True), {})
        for cmdline in ['quiet nomodeset', 'drm_awaiter=0']:
            self.assertEqual(self.run_fixture([{'modules': ['amdgpu']}], cmdline=cmdline), {})

    def test_passthrough_and_bound_driver(self):
        for device in [{'override': 'vfio-pci', 'modules': ['amdgpu']},
                       {'bound': 'vfio-pci', 'modules': ['amdgpu']}]:
            self.assertEqual(self.run_fixture([device]), {})
        files = self.run_fixture([{'bound': 'xe', 'modules': ['i915', 'xe']}])
        self.assertIn('modprobe -b xe', files['drm-module-load.service'])
        self.assertNotIn('modprobe -b i915', files['drm-module-load.service'])


if __name__ == '__main__':
    unittest.main()

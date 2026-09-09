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
            for index, device in enumerate(devices):
                path = pci / str(index)
                path.mkdir()
                (path / 'class').write_text(device.get('class', '0x030000'))
                (path / 'modalias').write_text(device.get('alias', 'pci:full-wildcard-alias'))
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
        -b) [[ $2 == -R && $3 == pci:full-wildcard-alias ]] || return 1
            printf '%s\\n' "$ALIASES" ;;
        *) return 1 ;;
    esac
}
modinfo() { [[ $MISSING != 1 ]]; }
source "$1"
generate "$2"
'''
            env = dict(os.environ, CONFIG=config,
                       ALIASES='\n'.join(dict.fromkeys(m for d in devices for m in d.get('modules', []))),
                       MISSING=str(int(missing)))
            result = subprocess.run(['bash', '-c', harness, 'fixture', str(root / 'generator'), str(root / 'out')],
                                    env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
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
        files = self.run_fixture([{'modules': ['nvidia', 'amdgpu']}, {'modules': ['amdgpu']}])
        service = files['drm-module-load.service']
        self.assertEqual(service.count('modprobe -b amdgpu'), 1)
        self.assertLess(service.index('modprobe -b amdgpu'), service.index('modprobe -b nvidia_drm'))

    def test_nouveau_wildcard_resolution(self):
        files = self.run_fixture([{'modules': ['nouveau']}])
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

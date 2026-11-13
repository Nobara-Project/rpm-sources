#!/usr/bin/python3
"""Source the dracut configuration as dracut does."""
from pathlib import Path
import subprocess
import unittest


CONF = Path(__file__).with_name('90-drm-awaiter.conf')
NVIDIA = {'nouveau', 'nova_core', 'nova_drm', 'nvidia', 'nvidia_modeset', 'nvidia_drm', 'nvidia_uvm'}


class DracutConfTests(unittest.TestCase):
    def omitted(self):
        result = subprocess.run(['bash', '-c', f'set -u; omit_drivers=" ide-cd "; . {CONF}; printf "%s" "$omit_drivers"'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        # dracut warns when an appended value lacks surrounding spaces.
        self.assertTrue(result.stdout.startswith(' ') and result.stdout.endswith(' '), repr(result.stdout))
        return set(result.stdout.split())

    def test_only_nvidia_nouveau_and_nova_are_omitted(self):
        self.assertEqual(self.omitted(), NVIDIA | {'ide-cd'})


if __name__ == '__main__':
    unittest.main()

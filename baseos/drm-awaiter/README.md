# drm-awaiter

This is a Nobara/dracut adaptation of [CachyOS PR 1695](https://github.com/CachyOS/CachyOS-PKGBUILDS/pull/1695),
commit `e2d9934981ff9d01285ee311e86e8596d764e210` (merged September 7, 2026).
The upstream generator is copyright 2026 Vasiliy Stelmachenok and permits
GPL-2.0-or-later; this adaptation is distributed under GPL-3.0-or-later,
with the license in COPYING.

The firmware framebuffer and built-in SimpleDRM provide the early console.
Dracut excludes AMD, Intel and NVIDIA GPU modules (including Nouveau) and
their otherwise-unneeded firmware. After mounting the real root, the
generator detects PCI display devices and orders the display manager and
tty1 login after a bounded module-loading service. NVIDIA packages retain
their Nouveau/Nova blacklists to select the installed NVIDIA driver. There
is no longer a NVIDIA-package-specific tradeoff between Nouveau and NVIDIA
in initramfs: both are loaded from the root filesystem.

## Differences from CachyOS

* Resolve complete PCI modaliases with kmod, including wildcard matches.
* Handle NVIDIA-only machines and explicitly insert `nvidia_drm`.
* Wait for synchronous module insertion to finish, rather than module-device
  uevents, which can arrive before driver initialization finishes. No extra
  udev rule is needed and already-loaded drivers work without another event.
* Use a 30-second service start timeout and Wants dependencies so driver
  failures do not permanently block login. Failures remain in the journal.
* Honor blacklists, existing driver bindings, driver overrides and nomodeset.
  Intel force_probe and AMD si_support/cik_support remain kernel probe policy.
* Request non-NVIDIA modules first, without upstream's global softdeps or
  dependency on plymouth-quit (which can conflict with display-manager ordering).
  Normal udev probing can still occur concurrently.
* Use dracut configuration and RPM dependencies instead of mkinitcpio/chwd.

## Packaging and rollout

Build this noarch package first and publish it with the updated kernel-core
and nvidia-kmod-common packages. Integration currently targets LTS 6.18,
mainline 7.2, production 595.99.02 and beta 595.45.04; historical source
directories and the separate new-feature driver channel are unchanged.
The kernel dependency covers machines without NVIDIA. Either NVIDIA flavor
also pulls the package in for machines still running an older kernel package.
Both selected kernel configs explicitly retain SimpleDRM and framebuffer console.

Build locally (use an absolute directory for `SOURCE_DIR`):

```sh
SOURCE_DIR="$PWD"
rpmbuild -ba --define "_sourcedir $SOURCE_DIR" drm-awaiter.spec
```

The package queues an initramfs rebuild during installation. Shared RPM
transaction file triggers consume that request once after package scriptlets
complete; subsequent kernel-install builds inherit the same policy. An upgrade removes
the old packaged `/usr/lib/dracut/dracut.conf.d/99-nouveau.conf` automatically.
Locally created `/etc/dracut.conf.d` configuration is not deleted or rewritten.
Check such overrides and any external updater scripts that explicitly force
GPU drivers into an image. A rebuild failure is reported and must be corrected
before relying on the migration. No reboot is performed by the RPM.

The production/beta `nvidia-boot-update` helper remains installed and is still
called by the package hooks and NVIDIA HTPC installer. Both `post` and `preun`
now only remove the previously managed boot arguments; neither adds anything.
This includes Nouveau/Nova blacklist entries, the old modesetting/framebuffer
arguments set to 1, and the historical nomodeset/SimpleDRM-disabling workarounds.
Unrelated module names in comma-separated blacklists and unrelated user options
(including explicit NVIDIA modesetting overrides set to 0) are preserved.
Cleanup covers GRUB defaults, kernel cmdline files, both BLS locations, and
GRUB's saved kernelopts. GRUB is regenerated only when cleanup requires it,
using `/boot/grub2/grub.cfg` for both BIOS and UEFI. No EFI forwarding stub is
overwritten. The helper requires Python 3 and skips OSTree installations.
Run `python3 nvidia/tests/test_boot_update.py` from the repository root for the
isolated cleanup regression suite; it never edits the host's boot files.

## Batched NVIDIA initramfs updates

Starting with drm-awaiter 1-2 and the updated production/beta DKMS RPMs,
NVIDIA build/install/remove scriptlets use DKMS 3.4.3's per-command
`--directive post_transaction=` override. This leaves `/etc/dkms/framework.conf`
and other DKMS modules unchanged. NVIDIA builds print the target kernel and
report failures, continuing with other installed kernels. Reinstalling an
already-registered module version is supported.

The scriptlets call `/usr/libexec/drm-awaiter-initramfs request` before changing
modules. The drm-awaiter package does the same when its policy is installed or
updated. A locked pending marker under `/run/drm-awaiter` combines these requests.
Transaction file triggers on the NVIDIA source paths and the dracut policy run
`flush` after normal package scriptlets. Install and erase triggers can both
fire during an upgrade, but only the first successful flush rebuilds images.
A failed rebuild retains the request and reports the manual retry command:

```sh
sudo /usr/libexec/drm-awaiter-initramfs flush
```

The marker is runtime state, so after rebooting following a failed transaction,
use `sudo dracut --regenerate-all --force` directly. Rebuilds remain necessary
for migration and machines with a local early-KMS override; this change does
not yet eliminate rebuilding on subsequent NVIDIA updates. Kernel-install and
unrelated packages can still request their own rebuilds.

Updated DKMS RPMs provide `nvidia-dkms-batched-initramfs = 1`. CFHDB's production
profile uses this capability to skip its extra rebuild and only retry pending
work. Older packages retain the legacy dracut fallback. The profile also writes
its modesetting configuration before DNF, so the RPM's final rebuild sees it.
The corresponding upstream profile patch and rollout instructions are in
`baseos/cfhdb/nvidia-batched-initramfs-profiles.patch` and
`baseos/cfhdb/README-dkms-batching.md` in the RPM sources repository.

Publish drm-awaiter 1-2 together with the updated DKMS RPMs, then publish the
CFHDB profile change. Old installed NVIDIA packages retain their original
uninstall scriptlets: the first upgrade from those versions may still invoke
an additional DKMS rebuild. CFHDB's separate removal transactions also retain
their existing cleanup. No change to the global DKMS hook is required.

## Validation before release

`python3 test-generator.py` runs isolated topology/blacklist/recovery fixtures;
it does not load host modules. RPM `%check` runs this suite and bash syntax
validation. These checks do not replace a boot test.

Test both kernels with each NVIDIA channel, plus AMD, Intel, Nouveau,
hybrid graphics, a VM and a machine without a GPU. For each relevant machine:

1. Test an upgrade with existing initramfs images and a fresh kernel install.
   Use `lsinitrd /boot/initramfs-<kernel-version>.img` to confirm vendor GPU
   modules and their GPU-only firmware are absent, while storage, keyboard
   and encryption support remain present. Compare image sizes before/after.
2. Boot with LUKS and verify the password prompt, keyboard, display handoff,
   SDDM/GDM and tty1 autologin/gamescope. Test BIOS/UEFI paths in use by Nobara.
3. Check `journalctl -b -u drm-module-load.service`,
   `systemctl cat drm-module-load.target display-manager.service`, and
   `systemd-analyze critical-chain display-manager.service` for completion
   before graphical login; verify the expected driver with `lspci -k`.
4. Check a failed/missing NVIDIA DKMS build and blacklisted GPU: no indefinite
   login wait. Verify switching NVIDIA flavors and uninstalling NVIDIA restores
   Nouveau selection after reboot. Verify resume and external displays.

Early GPU-accelerated Plymouth is intentionally lost. Firmware with no usable
framebuffer can require early KMS for a visible encrypted-root prompt; verify
this on hardware before publishing broadly. Non-PCI GPUs and late hotplug
remain handled by normal udev and are not synchronized by this generator.

## Recovery / early-KMS override

To restore early GPU loading on a machine, mask the vendor dracut policy and
rebuild its images:

```sh
sudo ln -s /dev/null /etc/dracut.conf.d/90-drm-awaiter.conf
sudo dracut --regenerate-all --force
```

If that filename already exists, review it rather than replacing it blindly.
With NVIDIA installed, Nouveau remains blacklisted; NVIDIA can be included
again by ordinary dracut detection or a local `add_drivers` setting. The
awaiter is harmless with early-loaded modules. `drm_awaiter=0` on the
kernel command line disables its boot ordering, but does not restore modules
to an already-generated initramfs. Keep a known-working boot image when
testing. To re-enable the smaller-image policy, remove only the local mask
created above and regenerate the images again.

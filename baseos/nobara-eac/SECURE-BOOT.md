# Secure Boot and Easy Anti-Cheat on Nobara

Nobara's kernels and GRUB are signed with Nobara's Secure Boot keys, so Nobara
can boot with Secure Boot enabled. For games that use Easy Anti-Cheat (EAC)
Linux v2, Nobara has a second kernel, **kernel-eac**, which boots the way EAC
requires.

Nobara signs with two separate keys, each with its own certificate authority
(CA), and you enroll both:

| CA | Signs |
|---|---|
| Nobara EAC CA | GRUB, the EAC kernel and its signed drivers |
| Nobara Secure Boot CA | The normal kernel |

When the computer starts, the firmware records which CA verified GRUB and the
kernel. That's how EAC knows you started the EAC kernel and not the normal
one.

| Kernel | Package | What it's for |
|---|---|---|
| Normal kernel | `kernel` | Everyday use. Loads every driver, including ones DKMS or akmods build on your computer. Works with Secure Boot on or off. |
| EAC kernel | `kernel-eac` | EAC games. Needs Secure Boot. Only loads drivers signed by Nobara. |

Both are installed side by side, and you choose between them in the GRUB boot
menu. The EAC kernel's entries start with `[EAC]`. The EAC kernel comes with
the normal kernel's updates: you don't need to install it yourself, and you
can remove it (see [Configuration](#configuration)).

> **Already set up Secure Boot with nobara-eac 1.0 or 1.1?** You need to enroll
> one more key. See [Upgrading from the earlier setup](#upgrading-from-the-earlier-setup).

This guide takes about 15 minutes and needs two restarts that you start. The
updater and MokManager add automatic restarts in between. You will:

1. Check that the EAC kernel is installed, enroll the keys and prepare the
   update. No restart yet.
2. Restart once: confirm the keys in MokManager, and the update installs.
3. Restart into your firmware (BIOS/UEFI setup) and turn on Secure Boot and
   the TPM.
4. Check that everything works.

Nothing here is required. If you don't play EAC games, you can skip this
guide: without Secure Boot the normal kernel stays the default, and Nobara
keeps working the way it always has. You can also remove the EAC kernel.

> **Required packages.** Secure Boot and EAC need at least these versions:
>
> | Package | Minimum version |
> |---|---|
> | `kernel-core` | `7.3.1-202.nobara` (mainline) or `6.18.60-200.lts.nobara` (LTS) |
> | `kernel-eac-core` | `7.3.1-202.eac.nobara` (mainline) or `6.18.60-200.lts.eac.nobara` (LTS) |
> | `grub2-efi-x64` | `2.12-65` |
> | `nobara-eac` | `1.2-1` |
> | `nobara-updater` | `2.0.1-92` |
> | `nobara-kernel-manager` | `0.1.6`, to switch between Mainline and LTS |
> | `shim-x64` | any (Fedora's signed shim, installed by default) |
>
> Kernels before `7.3.0-203.nobara` / `6.18.55-200.lts.nobara` aren't signed
> and won't boot with Secure Boot on. EAC kernels before `7.3.1-202` /
> `6.18.60-200` are signed with the Nobara Secure Boot CA, so EAC doesn't
> accept them.

> **Windows dual boot with BitLocker:** changing Secure Boot settings can make
> Windows ask for your BitLocker recovery key on its next boot. Get the key
> first from <https://aka.ms/myrecoverykey>.

## The EAC kernel

The EAC kernel boots with these kernel options: `lockdown=integrity`,
`module.sig_enforce=1`, `sysctl.kernel.kexec_load_disabled=1`,
`iommu.passthrough=0`, `intel_iommu=on`, and an `lsm=` list that includes
`bpf`. It also enforces module signatures and lockdown itself. Two things
matter for daily use:

- **It only loads kernel drivers signed by Nobara.** That's the drivers that
  come with the kernel, and Nobara's signed builds of the drivers listed in
  [Kernel modules](#kernel-modules) (NVIDIA, Xbox controllers, Razer, racing
  wheels, DisplayLink, r8125, nct6687d, and ZFS on the LTS kernel).
  Drivers that DKMS or akmods build on your computer don't load in it, even
  if their key is enrolled.
- **Some tools don't work in it**, because they need to change the running
  kernel: hibernation, kexec, `/dev/mem` tools, and other drivers. Use the
  normal kernel when you need them.

The EAC kernel becomes the default boot entry once it can work:

- Secure Boot is on.
- The Nobara EAC CA is enrolled.
- For every driver in [the signed list](#nobara-signed-drivers-for-the-eac-kernel)
  that you use with the normal kernel, the Nobara-signed build is installed
  for the EAC kernel, and no other unsigned driver is installed for it.

Until then, the normal kernel stays the default. After a system update, the
computer first starts the updated normal kernel once; the EAC kernel is the
default again from the next restart on.

## Requirements

- A UEFI computer. Legacy BIOS/CSM boot can't use Secure Boot.
- TPM 2.0. On Intel it's called PTT, on AMD fTPM, or it's a discrete TPM chip.
- Firmware that trusts the Microsoft 3rd Party UEFI CA. Almost every PC
  does, but some Lenovo laptops and Microsoft Surface devices turn it off by
  default.

## 1. Prepare (no restart yet)

Do all of this in one session, in this order. The restart in step 2 then
confirms the keys and installs the update in one go.

### Check that the EAC kernel is installed

```
rpm -q kernel-eac
```

It comes with the normal kernel, from kernel `7.3.1-201` / `6.18.55-202` on.
If it says `not installed` (you removed it, or your kernel is older), install
it:

```
sudo dnf install kernel-eac
```

It brings nobara-eac, which sets up the `[EAC]` boot entries, and the
Nobara-signed builds of the drivers you have installed (see
[Kernel modules](#kernel-modules)).

Installing packages with `dnf` is fine. Don't update the system with
`dnf update`; use the Nobara updater, as below.

### Enroll the keys

```
sudo nobara-eac-enroll
```

You can also do this without a terminal. With Secure Boot on and the EAC
kernel installed, Nobara shows a notification after you log in, "The Easy
Anti-Cheat kernel needs a Secure Boot key", until the Nobara EAC CA is
enrolled. Choose **Set up**, choose a one-time password, and enter your own
password when asked. It enrolls the same keys as the command. **Don't ask
again** stops the notification; to get it back, delete
`~/.local/state/nobara-updater/eac-enroll-declined`.

The command enrolls up to four keys in one step:

- **The Nobara EAC CA.** This lets shim trust Nobara's GRUB and the EAC
  kernel.
- **The Nobara Secure Boot CA.** This lets shim trust the normal kernel.
- **Your DKMS key** (`/var/lib/dkms/mok.pub`), if you use DKMS, for example
  `dkms-nvidia` or `xone`.
- **Your akmods key** (`/etc/pki/akmods/certs/public_key.der`), if you use
  akmods, for example `akmod-nvidia`.

The DKMS and akmods keys are for the **normal kernel**: with them enrolled,
the drivers DKMS and akmods build keep loading in it with Secure Boot on. The
EAC kernel ignores them. The keys are created on your computer; their private
halves never leave it.

The command asks you to choose a one-time password. Pick something short,
because you will type it once more in MokManager. MokManager may use a US
keyboard layout.

Don't restart yet. The keys are confirmed on your next restart, which should
be the one that installs the update (step 2).

The SHA-256 fingerprints of the Nobara CAs are:

```
Nobara EAC CA          97:D9:BA:02:B5:50:05:36:05:8E:C8:F3:4D:4B:60:7C:AB:AF:81:FD:5D:8F:21:32:7E:35:E2:9D:15:86:3B:C2
Nobara Secure Boot CA  A3:6D:9C:67:6F:ED:15:D6:45:A3:D2:84:5F:CE:8B:73:AB:54:CC:2B:DF:33:BD:A4:37:05:F7:40:68:41:6A:2E
```

You can compare them with your copies:

```
openssl x509 -inform der -in /usr/share/nobara/eac/nobara-eac-ca.der -noout -fingerprint -sha256
openssl x509 -inform der -in /usr/share/nobara/eac/nobara-sb-ca.der -noout -fingerprint -sha256
```

### Prepare the update

Open **DNF App Center**, go to **Updates** and choose **Update System**. From
a terminal you can run `sudo nobara-sync cli` instead.

Wait until the updater says "System update will install on the next
restart". Kernel and bootloader updates install offline, during the restart,
so they never change the running system.

If the updater finds nothing to update, that's fine. Check the versions in
step 2 after the restart.

## 2. Restart: confirm the keys and install the update

Save your work and restart. Then:

1. **MokManager.** Right after the firmware logo, a blue MokManager screen
   appears ("Perform MOK management"). It waits only about 10 seconds, so be
   ready and press any key.
   1. Choose **Enroll MOK**.
   2. Optional: choose **View key 0/1/2/3** to check the keys. The Nobara ones
      are "Nobara EAC CA" and "Nobara Secure Boot CA".
   3. Choose **Continue**, then **Yes**.
   4. Type the one-time password you chose.
   5. Choose **Reboot**.

   If you miss the screen, see [Troubleshooting](#troubleshooting).
2. **The update installs** before the desktop starts. Then the computer
   restarts by itself, into the normal kernel. Keep it powered on until the
   desktop is back.

Now check the versions and the keys:

```
rpm -q kernel-core kernel-eac-core grub2-efi-x64 shim-x64 nobara-eac nobara-updater
nobara-eac-enroll --list
```

The versions must be at least the ones in the table at the top, and both
Nobara CAs must be `enrolled`. If the kernel or GRUB is older, your mirror
may not have the new packages yet. Run the updater again later; that update
needs one more restart. Don't turn on Secure Boot until all of them are at
least these versions.

Finally, check that the firmware starts Nobara through shim, not straight
through GRUB:

```
efibootmgr
```

The `BootCurrent` entry, usually labelled `Fedora` or `Nobara`, must end in
`\EFI\fedora\shimx64.efi`. If it ends in `grubx64.efi` instead, see
[Troubleshooting](#troubleshooting).

## 3. Restart into the firmware: turn on Secure Boot and the TPM

Restart straight into your firmware setup:

```
systemctl reboot --firmware-setup
```

If that doesn't work, restart and press <kbd>Del</kbd>, <kbd>F2</kbd>,
<kbd>F10</kbd> or <kbd>F12</kbd> at the logo.

The menu names differ between vendors. Look for these settings:

- **TPM**: enable TPM 2.0, Intel PTT or AMD fTPM. Many computers have it on
  already.
- **Boot mode**: UEFI only. Disable CSM / Legacy boot.
- **OS Type** (only if your firmware has this dropdown): set it to
  **Windows UEFI Mode**. See [the OS Type dropdown](#the-os-type-dropdown)
  below.
- **Secure Boot**: set it to **Enabled**.
  - If the firmware says it is in **Setup Mode**, or there are no keys, choose
    **Restore factory keys**, **Install default keys** or **Standard mode**.
  - If there is an option for the **Microsoft 3rd Party UEFI CA** or "Allow
    3rd party CA", enable it.

Save and exit. Nobara starts.

On this first boot with Secure Boot on, the GRUB menu still defaults to the
normal kernel. To use EAC right away, choose the `[EAC]` entry in the GRUB
menu. If the menu is hidden, hold <kbd>Shift</kbd> or press <kbd>Esc</kbd>
while booting to show it. From the next boot on, the EAC kernel is the
default, as long as it can work (see [The EAC kernel](#the-eac-kernel)).

### The OS Type dropdown

Many ASUS boards, and some other vendors' boards, have an **OS Type**
dropdown, usually under **Boot → Secure Boot**. Its options are:

| Option | What it does |
|---|---|
| Other OS | Secure Boot stays off, even if it says Enabled elsewhere. Often the default. |
| Windows UEFI Mode | Secure Boot is on, using the standard Microsoft keys. |

Choose **Windows UEFI Mode**, even though you're running Nobara. The name is
misleading: it doesn't make the computer Windows-only. It just turns on Secure
Boot with the Microsoft keys, and Nobara's shim is signed by Microsoft.

If your firmware has no OS Type dropdown, skip this; setting Secure Boot to
Enabled is enough.

To check it worked, run this after Nobara starts:

```
mokutil --sb-state    # SecureBoot enabled
```

## 4. Check that everything works

Make sure you booted the EAC kernel (`uname -r` contains `.eac.`). Then run:

```
uname -r                                            # ...eac.nobara...
mokutil --sb-state                                  # SecureBoot enabled
cat /sys/kernel/security/lockdown                   # none [integrity] confidentiality
cat /sys/module/module/parameters/sig_enforce       # Y
cat /proc/sys/kernel/kexec_load_disabled            # 1
cat /sys/kernel/security/lsm; echo                  # ...,bpf,...
cat /sys/kernel/iommu_groups/0/type                 # DMA or DMA-FQ (not identity)
ls /dev/tpmrm0                                      # /dev/tpmrm0
```

If you use NVIDIA, check that the Nobara-signed driver is loaded:

```
nvidia-smi
modinfo -n nvidia    # .../updates/nobara/nvidia-prod/nvidia.ko (or nvidia-nf)
```

## Kernel modules

| Drivers | Normal kernel | EAC kernel |
|---|---|---|
| Drivers that come with the kernel (including v4l2loopback, xpad and xpadneo) | Load | Load |
| The drivers in the table below (NVIDIA, xone, OpenRazer, racing wheels, DisplayLink, r8125, ...) | Load (DKMS/akmods build) | Load (Nobara-signed build) |
| Other DKMS or akmods drivers | Load. With Secure Boot on, once the DKMS/akmods key is enrolled | Don't load |
| Drivers you built by hand | Load with Secure Boot off, or signed with an enrolled key | Don't load |

### Nobara-signed drivers for the EAC kernel

For every EAC kernel there are signed packages of these drivers:

| Package | For |
|---|---|
| `kmod-nvidia-prod-signed-<kernel>` | NVIDIA production branch driver |
| `kmod-nvidia-nf-signed-<kernel>` | NVIDIA new feature branch driver |
| `kmod-xone-signed-<kernel>` | `xone` (Xbox wireless dongle and controllers) |
| `kmod-xpad-noone-signed-<kernel>` | `xpad-noone` |
| `kmod-openrazer-signed-<kernel>` | `openrazer-kernel-modules-dkms` (OpenRazer) |
| `kmod-hid-tmff2-signed-<kernel>` | `hid-tmff2` (Thrustmaster wheels), including `hid-tminit` |
| `kmod-hid-fanatecff-signed-<kernel>` | `hid-fanatecff` (Fanatec wheels and pedals) |
| `kmod-new-lg4ff-signed-<kernel>` | `new-lg4ff` (Logitech wheels force feedback) |
| `kmod-evdi-signed-<kernel>` | `displaylink` (DisplayLink docks and USB displays) |
| `kmod-r8125-signed-<kernel>` | `dkms-r8125` (Realtek RTL8125 2.5GbE) |
| `kmod-nct6687d-signed-<kernel>` | `nct6687d` (Nuvoton NCT6687-R sensors, MSI boards) |
| `kmod-zfs-signed-<kernel>` | `zfs-dkms` (OpenZFS, from the OpenZFS repository). **LTS EAC kernel only** |

**ZFS needs the LTS kernel.** OpenZFS releases support new mainline kernels
late, so Nobara signs ZFS for the LTS EAC kernel only. If you use ZFS, switch to
LTS in **Nobara Kernel Manager**. On the mainline kernel, the EAC kernel doesn't
become the default while `zfs-dkms` is installed.

**You normally don't install them yourself.** Each new EAC kernel brings the
packages for the drivers you have installed, and the NVIDIA one matches your
driver branch. Check which ones you have:

```
rpm -qa 'kmod-*-signed-*'
```

If you install one of these drivers later, add its signed build for the EAC
kernels you have (Nobara Driver Manager does this for NVIDIA by itself):

```
sudo nobara-eac-kmods
```

`nobara-eac-kmods --list` shows what is missing without installing it.

Keep the DKMS and akmods packages (`dkms-nvidia`, `akmod-nvidia`, `xone`, ...):
the normal kernel still uses them.

NVIDIA beta drivers have no signed builds. With a beta driver, the EAC kernel
doesn't become the default and has no NVIDIA driver.

### Drivers Nobara doesn't sign

Some DKMS and akmods drivers have no Nobara-signed build, so they don't load
in the EAC kernel. They keep working in the normal kernel: start it from the
GRUB menu when you need them.

| Driver | Why there's no signed build |
|---|---|
| ZFS (`zfs-dkms`) on the **mainline** kernel | ZFS needed manual fixes to build on kernel 7.3, and that would happen again with each new mainline kernel. It is signed for the LTS kernel, see above. |
| VirtualBox (`akmod-VirtualBox`) | A third-party driver that Nobara doesn't provide. There are alternatives that need no extra kernel module, such as virt-manager with QEMU/KVM, or GNOME Boxes. KVM comes with the kernel and works in the EAC kernel. |
| Broadcom Wi-Fi (`broadcom-wl`, `akmod-wl`) | It contains a precompiled binary from Broadcom. Nobara has no access to its source code, so it can't review it or vouch for what it does, and Epic wouldn't accept it as a signed module. |

Normally DKMS and akmods don't build these for the EAC kernel at all, so they
are just missing there. If one is built for it anyway (with `kernel-eac-devel`
installed), the EAC kernel doesn't become the default; see "The EAC kernel
isn't the default" in [Troubleshooting](#troubleshooting).

### Switching drivers or kernels

- **NVIDIA branch** (Production or New Feature) in **Nobara Driver Manager**:
  it installs the matching signed build for your EAC kernels by itself.
  Restart afterwards, as the Driver Manager asks.
- **Mainline or LTS** in **Nobara Kernel Manager**: if the EAC kernel is
  installed, the switch replaces it with the EAC kernel of the family you
  chose, together with its signed drivers. If you removed it, the switch
  doesn't bring it back. Nothing else to do; restart afterwards.
- **Other drivers from the list**, installed with `dnf`: run
  `sudo nobara-eac-kmods` afterwards, as above.

If a signed build isn't available yet, for example right after a new NVIDIA
driver is released, the EAC kernel doesn't become the default until it is, and
the normal kernel keeps working. Run `sudo nobara-eac-kmods` again later, or
just update the system: the next EAC kernel brings it.

## Upgrading from the earlier setup

### From nobara-eac 1.1 (one Nobara CA)

Until nobara-eac 1.2, GRUB and both kernels were signed with the Nobara Secure
Boot CA. Since then, GRUB and the EAC kernel use the Nobara EAC CA, and you
need to enroll it too:

1. Get the new key, then enroll it. nobara-eac 1.1 doesn't have it yet:
   ```
   sudo dnf upgrade --refresh nobara-eac
   sudo nobara-eac-enroll
   ```
   It enrolls only the Nobara EAC CA; your other keys are already enrolled.
2. Prepare the update, as in [Prepare the update](#prepare-the-update).
3. Restart, and confirm the key in MokManager as in [step 2](#2-restart-confirm-the-keys-and-install-the-update).
   Then the update installs, including the new GRUB.

Secure Boot can stay on. Until the Nobara EAC CA is enrolled, the update keeps
your current GRUB on the EFI partition, so the computer keeps booting; the new
GRUB is installed on the first restart after the enrollment. The EAC kernel
only becomes the default once the Nobara EAC CA is enrolled.

If you just update instead, the notification from
[Enroll the keys](#enroll-the-keys) appears after the update's restart, once
you log in. Choose **Set up** and confirm the key in MokManager on the next
restart. This takes one more restart than the steps above.

### From nobara-eac 1.0 (one kernel with two entries)

nobara-eac 1.0 used a single signed kernel with two boot entries (with and
without `[EAC]`) and the DKMS and akmods keys enrolled. Epic doesn't accept
that: the EAC boot must not load drivers signed with keys you enrolled. If you
set that up:

1. **Update the system** with the Nobara updater, as in
   [Prepare the update](#prepare-the-update), and restart. nobara-eac 1.1
   removes the old duplicate entries and the `[EAC]` marks from the normal
   kernel. The normal kernel keeps working with Secure Boot on, with your
   DKMS and akmods drivers, because your keys stay enrolled. Nothing else
   changes until the EAC kernel is installed.
2. **Check the EAC kernel**: `rpm -q kernel-eac`. The update brings it with
   kernel `7.3.1-201` / `6.18.55-202`. If it's missing, install it with
   `sudo dnf install kernel-eac`. It brings the Nobara-signed builds of the
   drivers you have installed.
3. **Restart.** Your keys are already enrolled and Secure Boot is already on,
   so there's no MokManager or firmware step. The `[EAC]` entry is the EAC
   kernel now, and it becomes the default from the restart after the first
   one. Check it as in [step 4](#4-check-that-everything-works).

If you set `EAC_ENTRIES=no` in `/etc/sysconfig/nobara-eac`, it has no effect
any more: without kernel-eac there are no EAC entries.

## Configuration

`/etc/sysconfig/nobara-eac` chooses the default kernel:

```
EAC_DEFAULT=auto   # the EAC kernel once it can work, else the normal kernel (default)
EAC_DEFAULT=yes    # always the EAC kernel
EAC_DEFAULT=no     # never the EAC kernel; it stays in the menu
```

The change applies on the next boot. To apply it right away, run:

```
sudo /usr/lib/kernel/install.d/95-nobara-eac.install apply-all
```

Your own kernel options, for example set with `grubby` or in
`/etc/default/grub`, apply to both kernels. In the EAC kernel's entries,
options that conflict with EAC are left out, for example `iommu=pt`,
`amd_iommu=off` or another `lockdown=`.

To stop using the EAC kernel, remove it:

```
sudo dnf remove 'kernel-eac*'
```

It stays removed: kernel updates and switching between Mainline and LTS in
Nobara Kernel Manager don't bring it back. To get it back later, run
`sudo dnf install kernel-eac`.

## Troubleshooting

**`bad shim signature` / `Verification failed: (0x1A) Security Violation`**

The kernel or GRUB you chose isn't signed by Nobara, or its CA isn't enrolled:
the EAC kernel needs the Nobara EAC CA, the normal kernel the Nobara Secure
Boot CA. Check with `nobara-eac-enroll --list`, and choose a newer kernel. If no
entry boots, turn Secure Boot off, update with the Nobara updater, run
`sudo nobara-eac-enroll`, and check the versions in step 2.

**The updater says it kept the current GRUB**

`grub2-esp-update` keeps the GRUB already on the EFI partition while Secure
Boot is on and the Nobara EAC CA isn't enrolled, because the new GRUB wouldn't
boot. Run `sudo nobara-eac-enroll` and restart: the new GRUB is installed on
the first boot after the enrollment. Check with
`journalctl -b -u grub2-esp-update`.

**`mokutil --sb-state` says SecureBoot disabled, although the firmware says Enabled**

Your firmware probably has an OS Type dropdown still set to Other OS. Set it
to Windows UEFI Mode; see [the OS Type dropdown](#the-os-type-dropdown). If
the firmware says it is in Setup Mode, restore its factory (default) keys.

**The boot entry ends in `grubx64.efi` instead of `shimx64.efi`**

Check that shim is on the EFI partition:

```
sudo ls /boot/efi/EFI/fedora/shimx64.efi
```

If the file is missing, reinstall the package with
`sudo dnf reinstall shim-x64`.

Then create a firmware boot entry that points at shim. First find the disk
and partition of `/boot/efi`:

```
findmnt /boot/efi
```

For example, `/dev/nvme0n1p1` is disk `/dev/nvme0n1`, partition `1`. Then:

```
sudo efibootmgr --create --disk /dev/nvme0n1 --part 1 --label Nobara --loader '\EFI\fedora\shimx64.efi'
```

**I missed the MokManager screen**

The update still installs normally; only the keys aren't enrolled yet. Don't
turn on Secure Boot yet. Run `sudo nobara-eac-enroll` again. If it says the
keys are "waiting for confirmation", just reboot and watch for the blue
screen. If the screen never appears, cancel the request and start over:

```
sudo mokutil --revoke-import
sudo nobara-eac-enroll
```

**A DKMS or akmods driver doesn't load in the normal kernel with Secure Boot on**

Its key isn't enrolled, or the driver was built before the key existed. Check
with `nobara-eac-enroll --list`, and `modinfo -F signer <driver>`. Enroll the
keys with `sudo nobara-eac-enroll` (and confirm them in MokManager on the next
restart), then rebuild the drivers:

```
sudo bash -c 'dkms status | while IFS=", :" read -r mod kver arch state; do
    case "$state" in installed*)
        dkms build --force "$mod" -k "$kver" && dkms install --force "$mod" -k "$kver" ;;
    esac
done'
sudo akmods --force --rebuild
```

**NVIDIA (or another driver) doesn't load in the EAC kernel**

Check that the signed package for the running EAC kernel is installed:

```
rpm -qa 'kmod-*-signed-*' | grep "$(uname -r)"
modinfo -n nvidia    # must be in .../updates/nobara/...
```

If it's missing, install it:

```
sudo nobara-eac-kmods
```

If it says no signed build is available yet, for example right after an NVIDIA
update, use the normal kernel until it is. Drivers that aren't in
[the signed list](#nobara-signed-drivers-for-the-eac-kernel) only load in the
normal kernel.

**The EAC kernel isn't the default**

Check the conditions from [The EAC kernel](#the-eac-kernel):

```
mokutil --sb-state                                  # SecureBoot enabled
nobara-eac-enroll --check && echo enrolled          # enrolled (the Nobara EAC CA)
nobara-eac-kmods --list                             # nothing
ls /lib/modules/*eac*/extra 2>/dev/null
```

The EAC kernel needs the signed build of each driver from
[the signed list](#nobara-signed-drivers-for-the-eac-kernel) you have
installed: `nobara-eac-kmods --list` shows the missing ones, and
`sudo nobara-eac-kmods` installs them. Any other driver in its `extra/`
directory, which DKMS only adds if you installed `kernel-eac-devel`, also
keeps it from being the default. Fix that, or choose the `[EAC]` entry yourself
in the GRUB menu, or set `EAC_DEFAULT=yes`. Then reboot once.

Right after a system update the normal kernel starts once, to confirm the
update; the EAC kernel is the default again from the next restart.

**Turning Secure Boot off again**

Turn it off in the firmware. With `EAC_DEFAULT=auto`, the normal kernel becomes
the default again on the next boot. The EAC kernel still starts without Secure
Boot, but EAC games won't accept it. The enrolled keys can stay.

**Uninstalling**

Remove the EAC kernel and nobara-eac:

```
sudo dnf remove 'kernel-eac*' nobara-eac
```

If you also want to remove the enrolled keys, turn Secure Boot off first, and
keep it off: Nobara's GRUB doesn't boot with Secure Boot on without the Nobara
EAC CA, nor the normal kernel without the Nobara Secure Boot CA. Then:

```
sudo mokutil --delete /usr/share/nobara/eac/nobara-eac-ca.der /usr/share/nobara/eac/nobara-sb-ca.der /var/lib/dkms/mok.pub
```

Add `/etc/pki/akmods/certs/public_key.der` to that command if you enrolled it.
You'll confirm the deletion in MokManager on the next reboot.

# Framework Laptop 13 Pro / Panther Lake on Nobara LTS

Audited 2026-09-18 against CachyOS `cachyos-6.18.52-1`, commit
`f6a87c3e8826aade3f62f15e968f9d6b99475909`, with Nobara's existing patches.
Package: `6.18.52-201.lts.nobara`.

## Scope and vendor requirements

[Framework's current Laptop 13 Pro Linux page](https://frame.work/laptop13pro?tab=linux)
lists kernel **6.19 minimum, 7.0+ recommended**, and the latest kernel for the
best experience. The explicit 7.1 requirement appears in the
[Laptop 12 Core Series 3 announcement](https://community.frame.work/t/framework-laptop-12-now-with-core-series-3/84179).
These are different platforms. There is no published exhaustive patch list
that turns a 6.18 kernel into a Framework-certified 7.1 equivalent.

This series backports identified missing audio, power-management and display
changes from upstream 6.19 through 7.1. Some are functional fixes; others are
power-management improvements or diagnostic support, not prerequisites for
booting. It does not replace all of DRM, the wireless stack or x86 entry code.
Hardware validation on the actual laptop is still required.

The [Framework Sakura hardware description](https://doc.coreboot.org/mainboard/framework/sakura.html)
identifies BE211 Wi-Fi, Realtek ALC285 HDA audio, I2C HID touch devices,
USB camera/fingerprint, and S0ix suspend. That description is used here only
as a hardware reference. This series requires no BIOS replacement.

## Added upstream commits

Patch numbers match `kernel.spec`. Original authorship and upstream commit
messages are preserved in each patch.

| Patch | Upstream change | Reason |
| --- | --- | --- |
| 30 | [67c738152207](https://github.com/torvalds/linux/commit/67c73815220784074ff13ec07df955911caf1b73) — Framework PTL microphone gain | Prevents internal-microphone clipping above 50% input volume; keeps the jack fix chained. Matches Pro `f111:000f` and classic chassis `f111:010f`. |
| 31 | [d51de21b4c3a](https://github.com/torvalds/linux/commit/d51de21b4c3a34a2cc592319df63864e14b18b29) — Panther Lake idle table | Supplies Intel's C1/C1E/C6S/C10 latency and residency values instead of depending on firmware tables. |
| 32 | [34976eaf5f83](https://github.com/torvalds/linux/commit/34976eaf5f83d2bda76eeb54c5bbcafe87245e82) — C-state performance counters | Enables Panther Lake residency counters for power diagnostics. |
| 33 | [169934ba2b73](https://github.com/torvalds/linux/commit/169934ba2b73f07df59c3371acdc26f45eb99c5e) — TCC cooling CPU IDs | Enables the existing thermal cooling driver on Panther Lake. The upstream Wildcat/Nova Lake IDs are retained; their definitions already exist in this LTS tree. |
| 34 | [c17add734982](https://github.com/torvalds/linux/commit/c17add73498245bd94cb8a05345c73366606e671) — L3-cache helper | Prerequisite for the following energy-model change. |
| 35 | [d852b6f67b71](https://github.com/torvalds/linux/commit/d852b6f67b71dd22cd2af8ee29306eccbd6c06bf) — hybrid energy-model rules | Distinguishes LP-E, E and P cores using CPU type and L3 availability instead of fragile frequency-scaling ratios. Applies to supported Intel hybrid CPUs generally, not just Framework. |
| 36 | [ace7dcc81813](https://github.com/torvalds/linux/commit/ace7dcc8181373a0338efa1686c5e36eb121dff2) — Panel Replay constant | Defines the `0xffff` full-line X-granularity sentinel. |
| 37 | [a99cac460dde](https://github.com/torvalds/linux/commit/a99cac460ddeb3705cb54a8421339f351586b25d) — Panel Replay granularity handling | Avoids rejecting selective updates when a panel reports full-line granularity. Relevant upstream report: [drm/xe issue 7284](https://gitlab.freedesktop.org/drm/xe/kernel/-/issues/7284). Applicability to a particular Framework panel is conditional on its DPCD capabilities. |
| 38 | [0f8d0d764cc93](https://github.com/torvalds/linux/commit/0f8d0d764cc936cb834f39f0279c7776e0c1209d) — Xe3 display clock programming | Stops programming the removed CD2X pipe-select field and checks the required default divider. |

Patch 37 is adapted to 6.18's existing `intel_dp->psr` capability storage,
avoiding an unrelated connector refactor. It substitutes the mode width for
`0xffff` only when Panel Replay is selected. Ordinary granularity values,
PSR2 behavior and vertical-granularity checks remain intact. Both i915 and
Xe compile this shared display source. The other eight patches retain their
upstream code unchanged and apply without fuzz.

The CPU-type helper preceding patches 34/35 is already present in this
CachyOS source, including its newer `hwp_get_cpu_scaling()` behavior. Do not
reapply the older helper-introduction patch over it.

## Already present or not applicable

The baseline already enables Panther Lake's Xe driver without force-probe,
IWLMLD/BE211 support, PCIe Intel Bluetooth, Intel pinctrl, HDA Realtek audio,
I2C HID/multitouch, Chrome EC support and the USB camera driver. No additional
kernel config changes were necessary.

These later fixes are already present in 6.18.52 (sometimes with stable
adaptations), so they are not duplicated:

- [801a6e61f5fb](https://github.com/torvalds/linux/commit/801a6e61f5fbab2c0dd76c8360f45b625b49e410): disable GuC DCC on Panther Lake.
- [547456038177](https://github.com/torvalds/linux/commit/5474560381775bc70cc90ed2acefad48ffd6ee07): restrict Panther Lake C10 PHY handling to PHY A.
- [3549a9649dc7](https://github.com/torvalds/linux/commit/3549a9649dc7c5fc586ab12f675279283cdcb2a7): hold a DC-off reference while Panel Replay vblank interrupts are enabled.
- [314f6179e370](https://github.com/torvalds/linux/commit/314f6179e370988ac00dadf373a4f6166eb3db15): initialize the selective-update cursor state.
- [75519f5df2a9](https://github.com/torvalds/linux/commit/75519f5df2a9b23f7bf305e12dc9a6e3e65c24b7): use adjusted display mode boundaries for selective update.
- [92cee08dc4f0](https://github.com/torvalds/linux/commit/92cee08dc4f00e77fd1317e4343c5d458b0abab7): prevent runaway Wi-Fi MLD TSO processing with zero AMSDU subframes.
- [a229809c1892](https://github.com/torvalds/linux/commit/a229809c18926e79aeca232d5b502157beb0dec3): Panther Lake uncore frequency support.
- Framework's original PTL microphone-jack quirk and the signed firmware-version arithmetic fix in iwlwifi are also present.

The later AUX-interrupt timeout fix does not apply: this LTS driver already
polls for AUX completion and has not acquired the intervening interrupt-only
regression. Intel THC quickspi/quicki2c sleep fixes are not selected for the
documented I2C HID devices. SoundWire codec changes for other Panther Lake
laptops do not match Framework's HDA codec. FRED remains at the existing LTS
default; enabling it globally is not required for this laptop. Newer protected
content/PXP features and optional PMU/EDAC additions are outside this series.

The existing two local `btintel_pcie` suspend patches are preserved. They
remain downstream candidates requiring suspend/resume testing; the new
idle-state patch is not evidence that the Bluetooth wake issue is resolved.

## Firmware and userspace

Keep compatible Intel wireless and graphics firmware installed, along with
Panther Lake-capable Mesa and the userspace support for the fingerprint
reader. Kernel backports alone cannot provide those components.

[Intel lists BE211 support from 6.18](https://www.intel.com/content/www/us/en/support/articles/000005511/wireless.html),
whereas BE213 is listed from 7.1. The existing LTS driver accepts firmware
cores 97–99 for SC devices, including the old API-numbered
`iwlwifi-sc-a0-wh-b0-101.ucode` (API 101 means core 98). That file is present
in this system's firmware package; its header and TLVs were checked. The
newer `...-c101.ucode` is a different firmware core and is not accepted by
this LTS driver. Do not remove the compatible old API-101 file or simply
raise the driver's maximum version to force newer firmware to load.

[Intel's Core98 release notes](https://downloadmirror.intel.com/870814/ReleaseNotes_WiFi_LinuxCore98.pdf)
also identify 6.18 and BE211 as supported. No Wi-Fi firmware-limit change is
included. The firmware present on this desktop is evidence of package
availability, not a runtime test of the laptop's BE211.

## Validation and remaining hardware checks

- All 28 patches, including the four ARM64 patches, apply in spec order to
  fresh source files with `--fuzz=0`; no rejected hunks.
- Full x86_64 RPM `%prep` and `olddefconfig` pass.
- Nine affected x86_64 objects compile: Intel idle, C-state perf counters,
  TCC cooling, Intel P-state, Realtek alc269, and PSR/CDCLK under both i915
  and Xe. This checks the older display API adaptation in both consumers.
- No complete binary kernel build, boot test or Framework hardware test has
  been performed. ARM64 patch application is checked, not cross compilation.

Before treating this build as supported on the laptop, test cold boot and
graphics acceleration, all display ports and refresh rates, internal and
headset microphones, touchpad/touchscreen, Wi-Fi throughput/reconnection,
Bluetooth, and repeated lid/power-button S0ix resume on AC and battery.
Compare idle package residency and battery drain with a current mainline
kernel using the same BIOS, firmware and userspace. Check both hybrid CPU
performance and power consumption because the energy-model change affects
other Intel hybrid systems as well. Record any firmware-load failures,
GPU resets, PSR warnings or Bluetooth timeouts from the kernel journal.

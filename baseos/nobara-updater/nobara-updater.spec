Name:          nobara-updater
Version:       2.0.2
Release:       3%{?dist}
License:       GPL-3.0-or-later
Summary:       Nobara System Updater

URL:            https://github.com/nobara-project/nobara-core-packages
Source0:        %{URL}/releases/download/1.0/nobara-updater.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  make
BuildRequires:  systemd-rpm-macros

Provides:   nobara-updater

# App Deps
Requires: python
Requires: python3
Requires: python3-gobject
Requires: python3-psutil
Requires: python3-requests
Requires: python3-dnf
Requires: python3-libdnf5 >= 5.4.3
Requires: libdnf5-plugin-actions >= 5.4.3
Requires: python3-packaging
Requires: python3-tkinter
Requires: python3-dasbus
Requires: python3-cairo
Requires: python3-pillow
Requires: python3-pillow-tk
Requires: python3-evdev
Requires: python3-vdf

Requires: akmods
Requires: dracut
Requires: lvm2
Requires: grub2-tools
Requires: btrfs-progs
Requires: dnf5 >= 5.4.3
Requires: flatpak
Requires: glib2
Requires: gtk3
Requires: gtk4
Requires: libadwaita
Requires: adw-gtk3-theme
Requires: rpm
Requires: python3-rpm
Requires: systemd
Requires: util-linux
Requires: vte291
Requires: xdg-utils
Requires: xprop
Requires: libnotify
Requires: pbcli
# pkexec, for the Secure Boot key setup dialog
Requires: polkit
# nobara-eac-enroll --password-stdin and the Nobara EAC CA
Requires: (nobara-eac >= 1.2 if nobara-eac)

Provides: nobara-sync
Obsoletes: nobara-sync

%description
Nobara System Updater.

%prep
%autosetup -p1 -n nobara-updater

%install
make all DESTDIR=%{buildroot} PYTHON=%{python3} PYTHON_SITE_PACKAGES=%{python3_sitelib}

%posttrans
# Earlier workers used umask 077 for DNF, making its public state unreadable.
for nobara_state_name in packages nevras groups environments modules system; do
    nobara_state_file=/usr/lib/sysimage/libdnf5/$nobara_state_name.toml
    if [ -f "$nobara_state_file" ] && [ ! -L "$nobara_state_file" ]; then
        chmod 0644 "$nobara_state_file" || :
    fi
done
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files
%license %{_datadir}/licenses/nobara-updater/LICENSE
%{python3_sitelib}/nobara_updater/
%{_bindir}/nobara-sync
%{_bindir}/nobara-updater
%{_bindir}/nobara-codec-wizard
%{_datadir}/applications/nobara-codec-wizard.desktop
%{_datadir}/nobara-codec-wizard/
%dir %{_datadir}/nobara-updater
%doc %{_datadir}/nobara-updater/OFFLINE_UPDATES.md
%doc %{_datadir}/nobara-updater/RECOVERY.md
%doc %{_datadir}/nobara-updater/UPDATES.md
%{_libexecdir}/nobara-update-worker
%{_libexecdir}/nobara-update-reboot
%{_libexecdir}/nobara-codec-guard
%{_sysconfdir}/dnf/libdnf5-plugins/actions.d/nobara-codecs.actions
%{_libexecdir}/nobara-update-notice
%{_sysconfdir}/xdg/autostart/nobara-update-notice.desktop
%{_libexecdir}/nobara-eac-enroll-notice
%{_sysconfdir}/xdg/autostart/nobara-eac-enroll-notice.desktop
%{_datadir}/applications/nobara-update-recovery.desktop
%{_sysconfdir}/grub.d/42_nobara_update
%{_prefix}/lib/dracut/modules.d/91nobara-rollback/
%{_unitdir}/nobara-updater-*.service
%{_unitdir}/system-update.target.wants/nobara-updater-offline.service
%{_unitdir}/multi-user.target.wants/nobara-updater-confirm.service
%{_unitdir}/dnf5-offline-transaction.service.d/
%{_unitdir}/dnf5-offline-transaction-cleanup.service.d/
%{_unitdir}/dnf-system-upgrade.service.d/
%{_unitdir}/dnf-system-upgrade-cleanup.service.d/
%{_unitdir}/packagekit-offline-update.service.d/

%clean
rm -rf %{buildroot}

%changelog
* Thu Nov 12 2026 Nobara Project <support@nobaraproject.org> - 2.0.2-1
- Remove rsyslog and its rsyslog-* modules once, as with the move from SDDM:
  the journal keeps every message, and rsyslog's copies in /var/log grew
  without a size limit. After the update, delete the logs it wrote (messages,
  secure, maillog, cron, spooler and their rotated copies) and
  /var/lib/rsyslog. Recorded in /var/lib/nobara-updater/rsyslog-removal.json,
  so a reinstalled rsyslog is left alone; rsyslog also stays while another
  installed package requires it.
- Fix Btrfs recovery that could never be confirmed when the recovery entry's
  kernel has no modules in the recovered root (an earlier rollback left that
  kernel in the shared /boot). The recovered system started on another
  installed kernel through its normal entry was refused ("The recovery boot
  entry does not match the running kernel"). Recovery now confirms with that
  kernel when the recovered root has its complete module tree and its normal
  entry, and disables the entries of kernels the root has no modules for.
- Don't roll back an update because a DKMS module that no package provides
  fails to build for the new kernel (such as xone or xpad-noone installed
  with upstream's install.sh, which no longer build for 7.2). Skip it for
  that kernel and, once the update is confirmed, name it at the desktop with
  the command to remove it. Packaged DKMS modules still have to build.

* Wed Nov 11 2026 Nobara Project <support@nobaraproject.org> - 2.0.1-99
- Fix the move to the Nobara boot splash never happening: every standard
  install has gamescope-session-common (the Steam session), and was treated as
  an HTPC and put back on BGRT at every update. Only installs with both
  gamescope-htpc-common and gamescope-session-common are HTPC/handheld now and
  keep the SteamOS splash; all others follow the standard rule, and a selected
  Nobara or custom theme is no longer reverted to BGRT.
- A Theme= line naming a theme that is not installed (steamos left behind by a
  removed gamescope-htpc-common) counts as the default, as Plymouth treats it.

* Wed Nov 11 2026 Nobara Project <support@nobaraproject.org> - 2.0.1-96
- Move standard installs that still use the default BGRT boot splash, once, to
  the Nobara Plymouth theme from nobara-logos 44.0.0-2, rebuilding the boot
  images. Chosen themes, a later return to BGRT and HTPC/handheld (gamescope)
  installs are left alone; without the theme files the splash is kept and a
  later update tries again.

* Wed Nov 04 2026 Nobara Project <support@nobaraproject.org> - 2.0.1-94
- With Secure Boot on and the Easy Anti-Cheat kernel installed, offer at login
  to enroll the Nobara EAC CA: the user chooses the one-time MokManager password
  in a dialog, and nobara-eac-enroll queues the keys through pkexec.

* Mon Sep 28 2026 Nobara Project <support@nobaraproject.org> - 2.0.1-53
- Document immediate and offline updates, restart behavior, and recovery triggers.
- Explain supported filesystems and snapshot creation, promotion, and retirement.

* Mon Sep 28 2026 Nobara Project <support@nobaraproject.org> - 2.0.1-52
- Bundle user guidance for recovery, retries, and package origins.
- Include status-specific instructions in failure reports and offline bundles.

* Mon Sep 28 2026 Nobara Project <support@nobaraproject.org> - 2.0.1-51
- Preserve locally installed RPMs during distro-sync and migrations.
- Identify conflicting local and third-party packages and their repositories.
- Preserve origin diagnostics in preparation reports and recovery bundles.

* Mon Sep 28 2026 Nobara Project <support@nobaraproject.org> - 2.0.1-50
- Retire Btrfs rollback snapshots and recovery entries after boot confirmation.
- Preserve active recovered roots and referenced boot images.
- Retry interrupted cleanup without failing an already confirmed boot.

* Mon Sep 28 2026 Nobara Project <support@nobaraproject.org> - 2.0.1-49
- Keep DNF system-state files readable by ordinary users.
- Promote recovered Btrfs roots to normal kernel boot entries.
- Preserve active root arguments across later kernel and system updates.

* Mon Sep 28 2026 Nobara Project <support@nobaraproject.org> - 2.0.1-48
- Replay saved RPMs without remote repository objects and preflight native replay.
- Finish recovery before rebooting to avoid losing access to boot files.
- Preserve failure diagnostics across rollback and provide desktop recovery notices.
- Add offline support bundles and explicit pbcli log sharing.
- Report failures on bootable systems without snapshots while keeping partial updates blocked.

* Mon Sep 28 2026 Nobara Project <support@nobaraproject.org> - 2.0.1-47
- Revalidate scheduled jobs and repair missing offline boot triggers.
- Invalidate stale plans and report missed scheduling at startup.
- Prevent updater downgrades and guard other offline cleanup services.

* Mon Sep 28 2026 Nobara Project <support@nobaraproject.org> - 2.0.1-46
- Add ext4/XFS LVM rollback with a pre-update recovery initramfs.
- Arm GRUB fallback through installation and boot confirmation.
- Restore reserved storage after confirmation and preserve SSD TRIM support.

* Sun Sep 27 2026 Nobara Project <support@nobaraproject.org> - 2.0.1-45
- Package the offline update backend, systemd units, and documentation.
- Remove obsolete updater GUI and group inventory entries from the file list.
- Require the DNF5 backend version and codec wizard terminal dependency.

* Fri Jun 28 2024 Your Name <you@example.com> - 1.0-1
- Initial package

Name:          nobara-updater
Version:       2.0.1
Release:       70%{?dist}
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
%{_libexecdir}/nobara-codec-guard
%{_sysconfdir}/dnf/libdnf5-plugins/actions.d/nobara-codecs.actions
%{_libexecdir}/nobara-update-notice
%{_sysconfdir}/xdg/autostart/nobara-update-notice.desktop
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

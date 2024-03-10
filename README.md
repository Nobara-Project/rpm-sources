This repo contains the various .spec sheets, patches, and configurations Nobara applies to the modified packages it provides. You can use the config files in the mock folder to build the packages using mock.

Package building basics:

First, we need to create a .src.rpm from the .spec sheet and patches/files it uses. This will require some tools:

`sudo dnf install spectool fedpkg`

Next, open a terminal and navigate to the folder containing the spec sheet of the package you want to build:

`cd some-package-folder`

Download the sources listed in the spec sheet:

`spectool -g *.spec`

Make any modifications you want here. New patches, spec sheet modifications, etc.

After making your modifications, create a .src.rpm file from the spec sheet, sources, and patches/files in the folder. Replace '39' in f39 with whatever version you're building -- ie f38, f39, f40. The 'f' does not change for Nobara:

`fedpkg --release f39 srpm`

Now we're ready to build the resulting .src.rpm file.


LOCAL BUILD ONLY:
---
Install some dependencies:

`sudo dnf install mock pykickstart`

Add your user to the mock group:

`sudo usermod -aG mock $USER`
`su - $USER`

Use mock to build the rpm. Mock config files are in the mock folder. Most packages only need a 64 bit build:

64 bit package:
`mock -r /path/to/mock/folder/nobara-39-x86_64.cfg --rebuild --enable-network *.src.rpm`

32 bit package:
`mock -r /path/to/mock/folder/nobara-39-i686.cfg --rebuild --enable-network *.src.rpm`

Move the results folder to the current directory:

64 bit package:
`mv /var/lib/mock/nobara-39-x86_64/result .`

32 bit package:
`mv /var/lib/mock/nobara-39-i686/result .`

Optionally install or upgrade using the new rpms in the result folder:

`cd result`
`sudo dnf update *.rpm`
or
`sudo dnf install <some-rpm-name>.rpm`

When installing rpms instead of upgrading, specify all of the rpm file names you want. You do not need to install debug rpms, and doing so will bloat your system. Just install the ones you need, don't use a wildcard unless you are updating existing installed packages only.
---

Submit the build to a COPR repository:
---
go here, make an account:
https://copr.fedorainfracloud.org/

go here, generate an api token, copy the entire grey box:
https://copr.fedorainfracloud.org/api/

create a new file on your system at `~/.config/copr` with the pasted copr api grey box info

go here, make a new project:
https://copr.fedorainfracloud.org/coprs/USERNAME-GOES-HERE/

in the new project settings, check boxes of the chroots you want. for example `fedora-39-x86_64` and `fedora-39-i386`. check `enable internet access`. check `multilib support`. check `follow fedora branching`.

navigate to the folder containing your `.src.rpm` file you generated with `fedpkg`, and submit it.

Syntax:

copr-cli build <copr-repo-name> --nowait --chroot=<chroot-you-want> --timeout=36000 *.src.rpm

You can check the status of the build at:
https://copr.fedorainfracloud.org/coprs/YOUR-USER-NAME/YOUR-REPO-NAME/builds/

Examples:

All chroots:
copr-cli build nobara --nowait --timeout=36000 *.src.rpm

64 bit:
copr-cli build nobara --nowait --chroot=fedora-39-x86_64 --timeout=36000 *.src.rpm

32 bit:
copr-cli build nobara --nowait --chroot=fedora-39-i386 --timeout=36000 *.src.rpm

Once the build is finished you can install it from copr like any other copr repo:

`dnf copr enable username/reponame`
`dnf install -y some-package-name --refresh`
---



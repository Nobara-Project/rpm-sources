
Introduction to building packages for Nobara:
---

This repo contains the various .spec sheets, patches, and configurations Nobara applies to the modified packages it provides. You can use the config files in the mock folder to build the packages using mock.

Package building basics:
---

First, we need to create a .src.rpm from the .spec sheet and patches/files it uses. This will require some tools:

`sudo dnf install fedpkg`

Next, open a terminal and navigate to the folder containing the spec sheet of the package you want to build:

`cd some-package-folder`

Download the sources listed in the spec sheet:

`spectool -g *.spec`

Make any modifications you want here. New patches, spec sheet modifications, etc.

After making your modifications, create a .src.rpm file from the spec sheet, sources, and patches/files in the folder. Replace '39' in f39 with whatever version you're building -- ie f38, f39, f40. The 'f' does not change for Nobara:

`fedpkg --release f40 srpm`

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

`mock -r /path/to/mock/folder/nobara-40-x86_64.cfg --rebuild --enable-network *.src.rpm`

32 bit package:

`mock -r /path/to/mock/folder/nobara-40-i686.cfg --rebuild --enable-network *.src.rpm`


> Think you will be doing a lot of local builds? You can also move the  
> mock .cfg files for Nobara into the /etc/mock directory itself.
> This lets you simplify the .cfg names and pathing:
>
>64 bit package: 
>
>`mock -r nobara-40-x86_64 --rebuild --enable-network *.src.rpm`
>
>32 bit package: 
>
>`mock -r nobara-40-i686 --rebuild --enable-network *.src.rpm`

After the mock build finishes, move the results folder to the current directory:

64 bit package:

`mv /var/lib/mock/nobara-40-x86_64/result .`

32 bit package:

`mv /var/lib/mock/nobara-40-i686/result .`


Optionally install or upgrade using the new rpms in the result folder:

`cd result`

`sudo dnf update *.rpm`
or
`sudo dnf install <some-rpm-name>.rpm`

When installing rpms instead of upgrading, specify all of the rpm file names you want. You do not need to install debug rpms, and doing so will bloat your system. Just install the ones you need, don't use a wildcard unless you are updating existing installed packages only.
---

Submit the build to a COPR repository:
---
Go here, make an account:
https://copr.fedorainfracloud.org/

Go here, generate an api token, copy the entire grey box:
https://copr.fedorainfracloud.org/api/

Create a new file on your system at `~/.config/copr` with the pasted copr api grey box info

Go here, make a new project:
https://copr.fedorainfracloud.org/coprs/USERNAME-GOES-HERE/

On the new project settings, check boxes of the chroots you want. For example, `fedora-40-x86_64` and `fedora-40-i386`. Check `Enable internet access during builds`. Check `Follow Fedora branching`. Check `Multilib support`.

Navigate to the folder containing your `.src.rpm` file you generated with `fedpkg`, and submit it.

Syntax:

`copr-cli build <copr-repo-name> --nowait --chroot=<chroot-you-want> --timeout=36000 *.src.rpm`

You can check the status of the build at:
https://copr.fedorainfracloud.org/coprs/YOUR-USER-NAME/YOUR-REPO-NAME/builds/

Examples:

All chroots:

`copr-cli build nobara --nowait --timeout=36000 *.src.rpm`

64 bit:

`copr-cli build nobara --nowait --chroot=fedora-40-x86_64 --timeout=36000 *.src.rpm`

32 bit:

`copr-cli build nobara --nowait --chroot=fedora-40-i386 --timeout=36000 *.src.rpm`

Once the build is finished you can install it from copr like any other copr repo:

### `dnf copr enable username/reponame`
### `dnf install -y some-package-name --refresh`
---

Further reading:
---
Here are some helpful resources for packaging on Nobara: 
>Since Nobara is a Fedora-based distro, the documentation for Fedora's package build process typically applies to Nobara as well.

`mock` documentation: 

https://rpm-software-management.github.io/mock/

`rpm` documentation: 

https://asamalik.fedorapeople.org/tmp-docs-preview/quick-docs/creating-rpm-packages/

https://rpm-packaging-guide.github.io/

`copr` documentation:

https://docs.pagure.org/copr.copr/user_documentation.html

`fedpkg` documentation:

https://docs.fedoraproject.org/en-US/package-maintainers/Package_Maintenance_Guide/

https://docs.fedoraproject.org/en-US/package-maintainers/Packaging_Tutorial_GNU_Hello/

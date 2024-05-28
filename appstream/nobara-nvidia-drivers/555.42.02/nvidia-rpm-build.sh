#!/bin/bash

if [ ! $1 ] || [ ! $2 ]; then
	echo "Usage: ./nvidia-rpm-build.sh <release> <nvidia driver version>"
	exit 1;
else
	RELEASE="$1"
	NVVER="$2"
fi

MOCK64="mock -r /etc/mock/fedora-$RELEASE-x86_64.cfg --rebuild --enable-network *.src.rpm"
MOCK32="mock -r /etc/mock/fedora-$RELEASE-i386.cfg --rebuild --enable-network *.src.rpm"
FEDPKG="fedpkg --release f$RELEASE srpm"
MOVE64="mv /var/lib/mock/fedora-$RELEASE-x86_64/result/*.rpm ../RELEASE/$RELEASE/"
MOVE32="mv /var/lib/mock/fedora-$RELEASE-i686/result/*.rpm ../RELEASE/$RELEASE/"

# Clean out previous sources:
for i in $(ls)
do
	if [ -d "./$i" ] && [[ $i != "RELEASE" ]]; then
		cd "$i"
		# Remove pre-existing .src.rpms,.tar.xzs,.tar.gzs
		rm -Rf *.src.rpm
		rm -Rf *.tar.gz
		rm -Rf *.tar.xz
		cd ..
	fi
done
rm -Rf NVIDIA-Linux-x86_64-$NVVER.run

# Create new source tarballs:
sed -i "s|VERSION:-.*|VERSION:-$NVVER}|g" nvidia-generate-tarballs.sh
./nvidia-generate-tarballs.sh

# Download extras:
./nvidia-download-extras.sh $NVVER

# Move tarballs to appropriate subfolders:
mv nvidia-driver* driver/
mv nvidia-kmod-common* kmod-common/
cp nvidia-kmod* dkms/
mv nvidia-kmod* kmod/
mv nvidia-modprobe* modprobe/
mv nvidia-persistenced* persistenced/
mv nvidia-settings* settings/
mv nvidia-xconfig* xconfig/
cp open-gpu-kernel-modules* open-dkms/
mv open-gpu-kernel-modules* open-kmod/

# Prepare release folder:
rm -Rf RELEASE/$RELEASE
mkdir -p RELEASE/$RELEASE

# Build packages:
for i in $(ls) 
do
	if [ -d "./$i" ] && [[ $i != "RELEASE" ]]; then
		cd "$i"
		# Update the version in the spec sheet
		sed -i "s|Version:.*|Version:        $2|g" *.spec
		# Create new .src.rpm
		$FEDPKG
		# Build
		$MOCK64
		# Move to release folder
		$MOVE64
		if [[ $i == "driver" ]]; then
			echo "building 32 bit packages"
			# Build 32 bit packages
			$MOCK32
			# Move to release folder
			$MOVE32
		fi
		cd ..
	fi
done
echo "JOB DONE."

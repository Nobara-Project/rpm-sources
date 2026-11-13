#!/bin/bash

if [ ! $1 ] || [ ! $2 ]; then
	echo "Usage: ./nvidia-rpm-build.sh <release> <nvidia driver version> [arch ...]"
	echo "       arch: x86_64 and/or aarch64 (default: both)"
	exit 1;
else
	RELEASE="$1"
	NVVER="$2"
fi

# Architectures to build for. Foreign architectures are built by mock through
# qemu-user-static emulation, so expect those builds to be much slower.
ARCHES="${@:3}"
ARCHES="${ARCHES:-x86_64 aarch64}"
for ARCH in $ARCHES
do
	if [[ $ARCH != "x86_64" ]] && [[ $ARCH != "aarch64" ]]; then
		echo "Unsupported architecture: $ARCH (supported: x86_64 aarch64)"
		exit 1;
	fi
done
FIRSTARCH="${ARCHES%% *}"

FEDPKG="fedpkg --release f$RELEASE srpm"
OUTDIR="RELEASE/$RELEASE"
FAILED=""

# Rebuild the .src.rpm in the current folder and move the results to the
# release folder.
# $1 = arch in the mock config name, $2 = arch in the mock root name
mock_build()
{
	if ! mock -r /etc/mock/fedora-$RELEASE-$1.cfg --rebuild --enable-network *.src.rpm; then
		# Keep the log, the next build in the same mock root overwrites it
		FAILED="$FAILED $i/$2"
		mkdir -p ../$OUTDIR/failed
		cp /var/lib/mock/fedora-$RELEASE-$2/result/build.log ../$OUTDIR/failed/$i-$2-build.log
		return 1
	fi
	mv /var/lib/mock/fedora-$RELEASE-$2/result/*.rpm ../$OUTDIR/
}

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
rm -Rf NVIDIA-Linux-aarch64-$NVVER.run

# Create new source tarballs. This is always done for every architecture,
# the driver .src.rpm carries the i386, x86_64 and aarch64 tarballs:
sed -i "s|VERSION:-.*|VERSION:-$NVVER}|g" nvidia-generate-tarballs.sh
./nvidia-generate-tarballs.sh

# Download extras:
./nvidia-download-extras.sh $NVVER

# Move tarballs to appropriate subfolders:
mv nvidia-driver* driver/
mv nvidia-kmod-common* kmod-common/
cp $NVVER.tar.gz dkms/
mv $NVVER.tar.gz kmod/
mv nvidia-modprobe* modprobe/
mv nvidia-persistenced* persistenced/
mv nvidia-settings* settings/

# Prepare release folder:
rm -Rf $OUTDIR
mkdir -p $OUTDIR

# Build packages:
for i in $(ls)
do
	if [ -d "./$i" ] && [[ $i != "RELEASE" ]]; then
		cd "$i"
		# Update the version in the spec sheet
		sed -i "s|Version:.*|Version:        $NVVER|g" *.spec
		# Create new .src.rpm
		$FEDPKG
		if grep -q "^BuildArch:.*noarch" *.spec; then
			# noarch packages only need to be built once
			echo "building $i noarch packages"
			mock_build $FIRSTARCH $FIRSTARCH
		else
			for ARCH in $ARCHES
			do
				echo "building $i $ARCH packages"
				mock_build $ARCH $ARCH
				if [[ $i == "driver" ]] && [[ $ARCH == "x86_64" ]]; then
					echo "building 32 bit packages"
					# Build 32 bit packages
					mock_build i386 i686
				fi
			done
		fi
		cd ..
	fi
done

# Separate the packages by architecture:
#   RELEASE/<release>/<arch>/  packages for that architecture, plus a copy
#                              of the noarch packages. The 32 bit libraries
#                              go along with x86_64.
#   RELEASE/<release>/src/     source packages
mkdir -p $OUTDIR/src
mv $OUTDIR/*.src.rpm $OUTDIR/src/
for ARCH in $ARCHES
do
	mkdir -p $OUTDIR/$ARCH
	mv $OUTDIR/*.$ARCH.rpm $OUTDIR/$ARCH/
	if [[ $ARCH == "x86_64" ]]; then
		mv $OUTDIR/*.i686.rpm $OUTDIR/$ARCH/
	fi
	cp $OUTDIR/*.noarch.rpm $OUTDIR/$ARCH/
done
rm -f $OUTDIR/*.noarch.rpm

if [ -n "$FAILED" ]; then
	echo "FAILED BUILDS:$FAILED"
	echo "Build logs are in $OUTDIR/failed/"
	exit 1;
fi
echo "JOB DONE."

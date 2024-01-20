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

rm -Rf RELEASE/$RELEASE
mkdir -p RELEASE/$RELEASE

for i in $(ls) 
do
	if [ -d "./$i" ] && [[ $i != "RELEASE" ]]; then
		cd "$i"
		rm -Rf *.src.rpm
		sed -i "s|Version:.*|Version:        $2|g" *.spec
		$FEDPKG
		$MOCK64
		$MOVE64
		if [[ $i == "driver" ]]; then
			echo "building 32 bit packages"
			$MOCK32
			$MOVE32
		fi
		cd ..
	fi
done
echo "JOB DONE."

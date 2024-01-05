#!/bin/bash
HAS_PYSIDE=$(pip3 list installed | grep PySide6-Essentials)
if [[ -z $HAS_PYSIDE ]]; then
	pip3 install inputs PySide6-Essentials
fi
site_packages="$(python -c "import site; print(site.getsitepackages()[2])")"
cd "${site_packages}"
/usr/bin/python3 -m pupgui2


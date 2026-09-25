#!/bin/bash
# Finish the MITK build once the sid ITK with remote modules exists:
# install the whole local dependency chain, force a reconfigure (the cached
# configure predates the new ITK module set), then build and package.
# Log: ~/Workspace/mitk_build_final.log
set -u
W=/home/mhough/Workspace
ITK_RT=$(ls $W/_itk_sid_deb/libinsighttoolkit5.4_5.4.7-1+neuro1_amd64.deb 2>/dev/null)
ITK_DEV=$(ls $W/_itk_sid_deb/libinsighttoolkit5-dev_5.4.7-1+neuro1_amd64.deb 2>/dev/null)
[ -n "$ITK_RT" ] && [ -n "$ITK_DEV" ] || { echo "sid ITK +neuro1 debs not found"; exit 1; }
rm -f $W/_mitk_deb/mitk-2026.06/debian/debhelper-build-stamp
docker rm -f mitkbuild >/dev/null 2>&1
docker run --name mitkbuild --security-opt seccomp=unconfined \
  -v $W/_mitk_deb:/mitk -v $W/_ctk_deb:/ctk -v $W/_acvd_deb:/acvd -v $W/_itk_sid_deb:/itk neurodeb-sid bash -c '
  set -e
  apt-get update -qq 2>/dev/null
  apt-get install -y -qq /itk/libinsighttoolkit5.4_5.4.7-1+neuro1_amd64.deb /itk/libinsighttoolkit5-dev_5.4.7-1+neuro1_amd64.deb \
    /ctk/libctk0.1_2026.09.02-1+neuro6_amd64.deb /ctk/libctk-dev_2026.09.02-1+neuro6_amd64.deb \
    /acvd/libacvd4.0_4.0-1_amd64.deb /acvd/libacvd-dev_4.0-1_amd64.deb 2>&1 | grep -E "Setting up|E:" | tail -8
  echo "ITK GrowCut header: $(ls /usr/include/ITK-5.4/itkFastGrowCut.h 2>/dev/null || echo MISSING)"
  cd /mitk/mitk-2026.06
  apt-get build-dep -y -qq . 2>&1 | tail -1
  dpkg-checkbuilddeps && echo "build-deps satisfied"
  echo "=== build start $(date) ==="
  dpkg-buildpackage -us -uc -b -nc 2>&1; rc=$?
  echo "=== build end $(date) rc=$rc ==="
  chown -R 1001:1001 /mitk
  exit $rc
' > $W/mitk_build_final.log 2>&1
rc=$?; docker rm -f mitkbuild >/dev/null 2>&1
echo "container EXIT=$rc"
L=$W/mitk_build_final.log
echo "progress: $(grep -oE '^\[[0-9]+/[0-9]+\]' $L | tail -1)"
grep -nE 'CMake Error|^FAILED:| error: |dh_missing: (warning|error)|dpkg-deb: building|dpkg-buildpackage: error|patchelf|Error [0-9]' $L | tail -40
ls -la $W/_mitk_deb/*.deb 2>/dev/null | awk '{print "  "$5"  "$9}' || echo "  no debs"

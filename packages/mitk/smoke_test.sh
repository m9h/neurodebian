#!/bin/bash
# Smoke-test the built MITK debs in a fresh sid container. The logic lives in
# smoke_test_inner.sh (mounted in, no nested quoting). Usage: smoke_test.sh [secs]
W=/home/mhough/Workspace
docker run --rm --security-opt seccomp=unconfined \
  -v $W/_mitk_deb:/mitk -v $W/_ctk_deb:/ctk -v $W/_acvd_deb:/acvd -v $W/_itk_sid_deb:/itk \
  neurodeb-sid bash /mitk/smoke_test_inner.sh "${1:-90}"

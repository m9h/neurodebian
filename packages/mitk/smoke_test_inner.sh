#!/bin/bash
# Runs INSIDE the sid container (as root) with the package dirs mounted.
# Installs the MITK chain, launches MitkWorkbench under Xvfb as an unprivileged
# user, and greps for the failure signatures a successful build does not rule out.
SECS=${1:-90}
apt-get update -qq 2>/dev/null
apt-get install -y -qq xvfb xauth libgl1-mesa-dri libegl1 fonts-dejavu-core >/dev/null 2>&1
echo '=== install chain ==='
apt-get install -y -qq \
  $(ls /itk/libinsighttoolkit5.4_*neuro*_amd64.deb | tail -1) \
  $(ls /ctk/libctk0.1_*neuro6_amd64.deb | tail -1) \
  /acvd/libacvd4.0_4.0-1_amd64.deb \
  $(ls /mitk/mitk_2026.06-*_amd64.deb | tail -1) \
  $(ls /mitk/mitk-workbench_2026.06-*_amd64.deb | tail -1) \
  $(ls /mitk/python3-mitk_2026.06-*_amd64.deb | tail -1) 2>&1 | grep -E 'Setting up (mitk|libctk|libacvd|libinsight)|E:|not going|unmet' | tail -8
echo '=== files ==='
echo "  workbench: $(readlink -f /usr/bin/MitkWorkbench)"
echo "  plugins: $(ls /usr/lib/x86_64-linux-gnu/mitk/plugins/liborg_*.so 2>/dev/null | wc -l)"
echo "  provisioning: $(ls /usr/lib/x86_64-linux-gnu/mitk/*.provisioning 2>/dev/null)"
echo '=== ldd: missing libs across the tree ==='
find /usr/lib/x86_64-linux-gnu/mitk \( -name '*.so' -o -name MitkWorkbench \) | while read -r f; do
  ldd "$f" 2>/dev/null | grep 'not found' | sed "s|^|  $(basename "$f"): |"
done | sort -u | head -20
echo '=== python3-mitk imports? ==='
su builder -c 'python3 -c "import mitk; print(\"  import mitk OK:\", mitk.__file__)"' 2>&1 | tail -2
echo "=== launch MitkWorkbench under Xvfb for ${SECS}s (as builder, --no-sandbox) ==="
chmod 1777 /tmp
cat > /tmp/run_wb.sh <<EOF
export HOME=/home/builder QT_QPA_PLATFORM=offscreen QTWEBENGINE_CHROMIUM_FLAGS=--no-sandbox
timeout ${SECS} xvfb-run -a -s '-screen 0 1280x1024x24' MitkWorkbench
echo "WB_EXIT=\$?"
EOF
chmod 755 /tmp/run_wb.sh
su builder -c /tmp/run_wb.sh > /tmp/wb.log 2>&1
echo "  $(grep -oE 'WB_EXIT=[0-9]+' /tmp/wb.log | tail -1)   (124 = still running at timeout = launched OK; 134 = abort)"
echo '=== failure signatures ==='
for pat in 'could not be loaded' 'No application id' 'Resource not valid' 'State machine pattern not found' 'ctkPluginException' 'Segmentation fault' 'symbol lookup error' 'cannot open shared object' 'Aborted' 'Running as root'; do
  printf '  %-36s %s\n' "$pat" "$(grep -c "$pat" /tmp/wb.log)"
done
echo '=== workbench milestones ==='
for pat in 'PostWindowCreate' 'WorkbenchWindow::Open' 'Could not read :/' 'QResource'; do
  printf '  %-36s %s\n' "$pat" "$(grep -c "$pat" /tmp/wb.log)"
done
echo '=== last 15 lines ==='; tail -15 /tmp/wb.log | cut -c1-200

#!/usr/bin/env python3
"""Refresh the cross-channel version tracker for COPR + NeuroDebian packaging.

Columns tracked per package:
  upstream  - latest upstream release (GitHub API when --net, else known/manual)
  copr      - version in mhough/neurofedora COPR (from the .spec Version:)
  debian    - version in apt (Debian/Ubuntu/NeuroDebian), or '-' if unpackaged
  ours      - version we have built locally as a .deb, or '-'
  status    - SKIP / OURS / OUTDATED / PARTIAL / MISSING

Usage:
  python3 refresh_versions.py          # refresh copr (specs) + write tracker
  python3 refresh_versions.py --net    # also query GitHub for upstream latest
"""
import json, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SPECDIR = os.path.join(HERE, "neurofedora")
OUT = os.path.join(HERE, "versions.tsv")

# --- packages we build/maintain ourselves (local .deb versions) ---
OURS = {
    "liblsl": "1.17.7-1",
    "python-pylsl": "1.18.2-1",
    "python-pyxdf": "1.17.5-1",
    "InsightToolkit5": "5.4.6-1~noble2",  # batteries-included: +8 remote modules
    "ANTs": "2.6.5-1~noble1",
}

# --- apt mapping for packages already in Debian/Ubuntu/NeuroDebian ---
# pkg -> (debian_binary, debian_version, status)
DEBIAN = {
    "fcl": ("libfcl-dev", "0.7.0", "SKIP"),
    "ciftilib": ("libcifti-dev", "1.6.0", "SKIP"),
    "flann": ("libflann-dev", "1.9.2", "SKIP"),
    "gifticlib-cmake-devel": ("libgiftiio-dev", "1.0.9", "SKIP"),
    "tclap": ("libtclap-dev", "1.2.5", "SKIP"),
    "teem": ("libteem-dev", "1.12.0", "SKIP"),
    "freesurfer7": ("freesurfer", "8.2.0", "SKIP"),
    "freesurfer8": ("freesurfer", "8.2.0", "SKIP"),
    "libxdf": ("libxdf0", "0.99.8", "OUTDATED"),
    "biosig4c++": ("libbiosig3", "2.6.0", "OUTDATED"),
    "InsightToolkit5": ("libinsighttoolkit5-dev", "5.3.0", "OUTDATED"),
    "vtk": ("libvtk9-dev", "9.1.0", "OUTDATED"),
    "vtk-mpi": ("libvtk9-dev", "9.1.0", "OUTDATED"),
    "dlib": ("libdlib-dev", "19.24", "OUTDATED"),
    "dart": ("libdart-all-dev", "6.13.2", "OUTDATED"),
    "openigtlink": ("libopenigtlink-dev", "1.11.0", "OUTDATED"),
    "ismrmrd": ("libismrmrd-dev", "1.8.0", "OUTDATED"),
    "urdfdom": ("liburdfdom-dev", "4.0.0", "OUTDATED"),
    "urdfdom-headers": ("liburdfdom-headers-dev", "1.0.5", "OUTDATED"),
    "compat-libtiff5": ("libtiff5", "4.3.0", "OUTDATED"),
    "afni": ("afni-atlases", "(data)", "PARTIAL"),
    "fsl-first": ("fsl-first-data", "5.0.7", "PARTIAL"),
    "fsl-possum": ("fsl-possum-data", "5.0.7", "PARTIAL"),
    "freesurfer7-synth-tools": ("freesurfer", "8.2.0", "PARTIAL"),
    "freesurfer8-synth-tools": ("freesurfer", "8.2.0", "PARTIAL"),
    "freesurfer8-synthstrip": ("freesurfer", "8.2.0", "PARTIAL"),
    "python-pybids": ("python3-bids-validator", "1.14.1", "PARTIAL"),
}

# --- known upstream-latest (manually curated; refreshed by --net for GitHub) ---
UPSTREAM = {
    "vtk": "9.6.2",
    "InsightToolkit5": "5.4.6",
    "InsightToolkit6": "6.0.0b2",
    "ANTs": "2.6.5",
}

# COPR packaging helpers that are not real software (exclude from tracker)
NOT_SOFTWARE = {"freesurfer-common", "freesurfer-fspython"}


def spec_version_url(name):
    path = os.path.join(SPECDIR, name + ".spec")
    if not os.path.isfile(path):
        return "", ""
    txt = open(path, encoding="utf-8", errors="replace").read()
    def field(f):
        m = re.search(rf'^{f}:\s*(.+)$', txt, re.M | re.I)
        return m.group(1).strip() if m else ""
    return field("Version"), field("URL")


def _gh_api(path):
    """Query the GitHub API via the authenticated gh CLI (5000 req/hr)."""
    try:
        out = subprocess.run(["gh", "api", path], capture_output=True,
                             text=True, timeout=15)
        if out.returncode != 0:
            return None
        return json.loads(out.stdout)
    except Exception:
        return None


def github_latest(url):
    m = re.search(r'github\.com/([^/]+)/([^/#?]+)', url)
    if not m:
        return ""
    repo = f"{m.group(1)}/{m.group(2)}".rstrip(".git").removesuffix(".git")
    d = _gh_api(f"repos/{repo}/releases/latest")
    if d and d.get("tag_name"):
        return d["tag_name"].lstrip("v")
    # fall back to newest tag when the project cuts no GitHub "releases"
    tags = _gh_api(f"repos/{repo}/tags")
    if isinstance(tags, list) and tags:
        return tags[0].get("name", "").lstrip("v")
    return ""


def main():
    net = "--net" in sys.argv
    meta = json.load(open(os.path.join(HERE, "spec_meta.json")))
    rows = []
    for pkg, copr_ver, url, _summ in meta:
        if pkg in NOT_SOFTWARE:
            continue
        deb_pkg, deb_ver, status = DEBIAN.get(pkg, ("-", "-", "MISSING"))
        ours = OURS.get(pkg, "-")
        if ours != "-":
            status = "OURS"
        up = UPSTREAM.get(pkg, "")
        if net and not up:
            up = github_latest(url)
        rows.append((pkg, up or "-", copr_ver or "-", deb_ver, ours, status, deb_pkg, url))
    # stable sort: status priority then name
    order = {"OURS": 0, "OUTDATED": 1, "PARTIAL": 2, "SKIP": 3, "MISSING": 4}
    rows.sort(key=lambda r: (order.get(r[5], 9), r[0].lower()))
    with open(OUT, "w") as f:
        f.write("package\tupstream\tcopr\tdebian\tours\tstatus\tdebian_pkg\turl\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    from collections import Counter
    c = Counter(r[5] for r in rows)
    print(f"wrote {OUT}: {len(rows)} packages")
    print("  " + "  ".join(f"{k}={c[k]}" for k in ["OURS","OUTDATED","PARTIAL","SKIP","MISSING"]))


if __name__ == "__main__":
    main()

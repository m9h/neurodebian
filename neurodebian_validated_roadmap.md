# NeuroDebian packaging — validated target list (2026-06-23)

Re-validated all 166 COPR "missing" packages against apt (Ubuntu 24.04 noble +
NeuroDebian) by **homepage/description match**, version-compared, via 6 parallel
adjudicator agents. Supersedes the unreliable name-based /tmp/copr_missing.txt.

## SKIP — already packaged at matching version (8)
fcl (libfcl-dev 0.7.0) · ciftilib (libcifti 1.6.0) · flann (libflann 1.9.2) ·
gifticlib (libgiftiio 1.0.9) · tclap (libtclap 1.2.5) · teem (libteem 1.12.0) ·
freesurfer7 & freesurfer8 (freesurfer 8.2.0 suite)

## ALREADY DONE this effort (3)
liblsl 1.17.7 · python3-pylsl 1.18.2 · python3-pyxdf 1.17.5

## OUTDATED — packaged but apt older than COPR (refresh optional) (12)
| pkg | apt | copr |
|---|---|---|
| libxdf | 0.99.8 | 0.99.10 |
| biosig4c++ | libbiosig 2.6.0 | 3.9.4 |
| InsightToolkit5 | 5.3.0 | 5.4.6 |
| vtk / vtk-mpi | libvtk9 9.1.0 | 9.6.2 |
| dlib | 19.24 | 20.0.1 |
| dart | 6.13.2 | 6.18.0 |
| openigtlink | 1.11.0 | 3.1.0 (big gap) |
| ismrmrd | 1.8.0 | 1.15.0 |
| urdfdom | 4.0.0 | 4.0.2 |
| urdfdom-headers | 1.0.5 | 1.1.2 |
| compat-libtiff5 | libtiff5 4.3.0 | 4.4.0 |

## PARTIAL — only data/bundled sub-component in apt, core tool/module missing (7)
afni (afni-atlases only) · fsl-first (data) · fsl-possum (data) ·
freesurfer7-synth-tools / freesurfer8-synth-tools / freesurfer8-synthstrip
(bundled inside freesurfer suite) · python-pybids (only bids-validator)

## N/A — COPR packaging helpers, not real software (2)
freesurfer-common · freesurfer-fspython

## MISSING — genuine build targets (~134)

### LSL / electrophysiology
labrecorder · lsl-apps · App-AudioCapture · App-Gamepad · App-PupilLabs ·
App-SigVisualizer · App-XDFStreamer · brainflow · python-brainflow ·
python-ephyviewer · open-ephys-gui · openvibe · mne-cpp · python-pylsl(done)

### 3D Slicer stack
3dslicer · 3dslicer-elastix · 3dslicer-monailabel · 3dslicer-openlifu ·
3dslicer-totalsegmentator · SlicerExecutionModel · PythonQt · python-pythonqt ·
ctk · commontk-applauncher · qRestAPI · qttesting · vtkAddon · SPHARM-PDM ·
python-mcp-slicer

### Registration / segmentation / morphometry
ANTs · ANTs3 · niftyreg · niftyseg · greedy · c3d · itksnap · vmtk · TTK ·
RPI · anima · dtk · dtk-qt6 · medInria · mitk · InsightToolkit6 · laynii · palm

### FSL (all binary tools — NeuroDebian ships only data/atlases)
fsl · fsl-avwutils · fsl-bet2 · fsl-bianca · fsl-cluster · fsl-eddy ·
fsl-fabber-core · fsl-fabber-models-asl · fsl-fast4 · fsl-fdt · fsl-feat5 ·
fsl-film · fsl-filmbabe · fsl-flameo · fsl-flirt · fsl-fnirt · fsl-fugue ·
fsl-gps · fsl-libvis · fsl-mcflirt · fsl-melodic · fsl-mist · fsl-mm ·
fsl-oxford-asl · fsl-ptx2 · fsl-randomise · fsl-siena · fsl-slicetimer ·
fsl-susan · fsl-swe · fsl-tbss · fsl-topup · fsl-xtract · fsl-xtract-data ·
python-pyfix · python-file-tree

### FreeSurfer add-ons / segmentation ML
python-samseg · python-charm-gems · python-surfa · simnibs

### Diffusion / tractography
dsi-studio

### Physics / simulation / MC
geant4 · opentopas · jemris · babelbrain · python-babelviscofdtd · igsio ·
openigtlinkio · cmdstan · python-stanio

### Python scientific / web-viz (trame)
python-nilearn · python-monai · python-simpleitk · python-narwhals ·
python-formulaic · python-bsmschema · python-spectrum · python-pygpc ·
python-fmm3dpy · python-simservice · python-py-undo-stack ·
python-pillow-avif-plugin · python-trame · python-trame-client ·
python-trame-common · python-trame-rca · python-trame-server ·
python-trame-vtk · python-trame-vuetify · python-wslink

### CompuCell3D / robotics / misc
compucell3d · cc3d-player5 · cc3d-twedit5 · dart(OUTDATED) · urdfdom(OUTDATED) ·
rr-libstruct · vespa · viskores · libspm · ucsc-kent-utils · dicomanonymizer ·
python-OpenSeeFace · python-gaze-tracking · opentrack · quit · mricrogl ·
OrcaSlicer · xpra-html5 · iit-human-brain-atlas

"""
Standalone convpaint test: proves a trained model works outside napari and GA3.

Run inside the pixi environment:

    cd C:\\Convpaint
    pixi shell
    python scripts\\test_convpaint_standalone.py

Edit the settings block below first. Record the positive-pixel count it prints
for your reference image: the same model, image and napari-convpaint version
should give exactly the same number on any machine.
"""

import numpy as np
import nd2
import tifffile
from napari_convpaint import ConvpaintModel

# ----------------------------------------------------------------------
# EDIT THESE
MODEL_PATH = r"C:\Convpaint\models\my_model.pkl"
IMAGE_PATH = r"C:\Convpaint\test_image.nd2"      # or a .tif / .ome.tif
OUTPUT_PATH = r"C:\Convpaint\test_segmentation.tif"

TARGET_CLASS = 2      # label number of the structure you want (1 is usually background)
CHANNEL_INDEX = 0     # which channel to use if the file has several
# ----------------------------------------------------------------------

# --- Load image -------------------------------------------------------
if IMAGE_PATH.lower().endswith(".nd2"):
    img = nd2.imread(IMAGE_PATH)
else:
    img = tifffile.imread(IMAGE_PATH)

img = np.squeeze(img)
print(f"Image loaded: shape={img.shape}, dtype={img.dtype}")

if img.ndim == 3:
    img = img[CHANNEL_INDEX]
    print(f"Multi-channel input, took channel {CHANNEL_INDEX}: shape={img.shape}")

if img.ndim != 2:
    raise SystemExit(f"Expected a single 2D image, got shape {img.shape}.")

# --- Load model -------------------------------------------------------
cpm = ConvpaintModel(model_path=MODEL_PATH)
print("Model loaded.")
# The .pkl stores the training parameters, including downsampling.
try:
    print("Model params:", vars(cpm.get_params()))
except Exception:
    pass  # parameter introspection differs between versions; not critical

# --- Segment ----------------------------------------------------------
print("Segmenting (CPU, may take a couple of minutes)...")
labels = np.squeeze(cpm.segment(img))
print(f"Done: labels shape={labels.shape}, classes={np.unique(labels)}")

if labels.shape != img.shape:
    print(f"WARNING: label shape {labels.shape} != image shape {img.shape}.")

# --- Save outputs -----------------------------------------------------
tifffile.imwrite(OUTPUT_PATH, labels.astype(np.uint8))
print(f"Label image saved: {OUTPUT_PATH}")

binary = (labels == TARGET_CLASS).astype(np.uint8)
binary_path = OUTPUT_PATH.replace(".tif", "_binary.tif")
tifffile.imwrite(binary_path, binary * 255)
print(f"Binary saved: {binary_path}")

n_px = int(binary.sum())
print(f"Target-class pixels: {n_px} ({100 * n_px / binary.size:.2f}% of image)")
print("Open the outputs in Fiji or napari and compare against your napari prediction.")

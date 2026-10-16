# Installation

Build a Python environment that NIS-Elements can call, and prove the model works in it before involving GA3.

**Time:** about an hour on a fresh machine, roughly half of it package downloads.

> **Use the same folder path on every machine.** The node code and the GA3 recipe both store absolute paths. If the path is identical everywhere, a recipe can move between PCs with no edits. This guide uses `C:\Convpaint`.

## 1. Create the folders

```
C:\Convpaint\
├── scripts\     put test_convpaint_standalone.py here
├── models\      your trained .pkl file
└── logs\        the node writes python.log here (the folder must exist)
```

Avoid spaces in the folder name; they cause avoidable trouble when other software has to find your files.

## 2. Install pixi (once per machine)

Open PowerShell and run the Windows installer from the [pixi documentation](https://pixi.sh):

```powershell
powershell -ExecutionPolicy Bypass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

Restart the terminal, then check:

```cmd
pixi --version
```

## 3. Create the environment

```cmd
cd C:\Convpaint
pixi init
pixi add python=3.11 pip
```

## 4. Install the packages

```cmd
pixi shell
pip install napari-convpaint==1.1.0 matplotlib pyqt5 nd2 tifffile
```

| Package | Why it is needed |
|---|---|
| `napari-convpaint` | The model itself. **Pin the version used to train your `.pkl`.** |
| `matplotlib` | NIS-Elements needs it for the Python node to communicate. Without it the node fails. |
| `pyqt5` | convpaint's package imports its napari widget, which imports Qt. Without Qt bindings the import fails even though no window is ever shown. |
| `nd2` | Reads `.nd2` files in the standalone test script. The GA3 node itself does not need it. |
| `tifffile` | Writes the test output in the standalone script. |

napari itself is **not** needed on a deployment machine.

## 5. Confirm the interpreter

Check that this file exists:

```
C:\Convpaint\.pixi\envs\default\pythonw.exe
```

This is the interpreter GA3 will call. You will paste its path into the node.

## 6. Validate the model outside GA3

Never debug a model through GA3. Confirm it works headlessly first.

1. Copy `scripts/test_convpaint_standalone.py` to `C:\Convpaint\scripts\`, and your model to `C:\Convpaint\models\`.
2. Edit the paths at the top of the script (model, a test image, output name).
3. Run:

```cmd
cd C:\Convpaint
pixi shell
python scripts\test_convpaint_standalone.py
```

**What to expect** (numbers will differ):

```
Image loaded: shape=(H, W), dtype=uint16
Model loaded.
Model params: {...}
Segmenting (CPU, may take a couple of minutes)...
Done: labels shape=(H, W), classes=[1 2 3]
Target-class pixels: N (x.xx% of image)
```

**Checks:**

- The label image has the **same shape as the input**. Convpaint applies and reverses its internal downsampling automatically.
- Open the saved `*_binary.tif` and compare it visually with what you saw in napari.
- **Record `N`** for your reference image. This is your regression benchmark: the same model, image and convpaint version should give exactly the same count on any machine. Repeat the test on every new machine and compare.

Harmless messages: warnings that Cellpose or Ilastik are not installed (optional feature extractors), and the "imagenet normalization" warning for single-channel images. On first run the vgg16 weights (about 550 MB) are downloaded automatically.

**Do not continue until this step passes.**

Next: [Patch the NIS lim files](lim-file-patch.md).

# How it works

You can follow the other pages without this one. Read it if you want to understand why the steps are what they are, which makes problems much easier to diagnose.

## An environment is a folder

A Python environment is a folder containing a Python interpreter and a `site-packages` directory of installed libraries. Installing a package copies files into that `site-packages`. Isolation just means another folder with its own copies.

Yours is `C:\Convpaint\.pixi\envs\default\`. That is why napari-convpaint can be pinned to one version here without affecting anything else on the PC.

## What pixi does

Pixi builds and tracks that folder from a recipe:

- `pixi.toml` is what you ask for (Python 3.11, and so on).
- `pixi.lock` is what was actually resolved, with exact versions.
- `.pixi/` is the built result. It is machine-specific and should not be copied between PCs.

In this guide, pixi provides Python 3.11 and `pip`, and `pip` installs napari-convpaint and the rest.

## Activation is only a PATH change

`pixi shell` puts the environment's `python.exe` and DLL folders at the front of PATH, so typing `python` runs the right one. That is all.

## Why NIS-Elements needs special treatment

NIS-Elements never activates anything. It starts `pythonw.exe` directly, by the full path you gave in the node. Three things follow:

1. **The PATH patch.** Native libraries from conda-style packages live in `Library\bin`. Without activation that folder is not on PATH, so imports die at startup (`Exited code 1`). LIM's patched `limnode.py` adds the folder itself.
2. **Copying the lim files.** NIS has its own built-in Python with `limnode` in it. Your pixi Python is a separate interpreter and cannot see it, so you copy the files in.
3. **The version patch.** The stock `limnode.py` restricts which Python version it accepts; the patch lowers the requirement so Python 3.11 works.

## What "run out of process" means

With **Run out of process** on, NIS starts your interpreter as a child process. The child runs `limnode.child_main(run, output, build)` and exchanges images with GA3 over a pipe. Because the child is a separate process:

- `print` output never reaches the NIS log, so the node writes to a log file instead;
- the model is cached in a global so it loads once per child, not once per call;
- a crash in the child shows up in NIS only as a generic exit-code error, which is why the standalone test comes first.

## What convpaint does

Convpaint extracts features from the image using a pretrained network (VGG16 by default) at several scales, then trains a small classifier (CatBoost in the validated setup) on your sparse annotations to label every pixel. The saved `.pkl` bundles the classifier and the settings used, including the image downsampling. At inference it applies the same settings and returns a label image at the original size.

Because the features and classifier depend on the library version, **use the same napari-convpaint version for inference as for training.**

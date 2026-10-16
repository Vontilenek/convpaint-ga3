# Patching the NIS-Elements lim files

NIS-Elements 6.20 ships helper modules (`limnode.py`, `limtabledata.py`, `limreport.py`) that let a Python node exchange data with GA3. Laboratory Imaging publishes patched versions that fix problems this workflow runs into:

- the out-of-process Python version is restricted (the patch lowers the requirement to Python 3.10, so Python 3.11 works);
- `Library\bin` is not added to PATH, because NIS launches `pythonw.exe` directly without activating the environment;
- table data modified in an out-of-process node does not come back to NIS (a limitation, noted by LIM).

**Source (LIM):** <https://github.com/Laboratory-Imaging/GA3-examples/tree/main/NIS_v6.20/00-Fixing_Python_Issues>

The patched files are not copied into this repository; always take them from LIM so you get their current version.

**You need administrator rights** for steps 1 and 2.

## 1. Back up the originals

Open the NIS site-packages folder (adjust the path if NIS is installed elsewhere):

```
C:\Program Files\NIS-Elements\Python\Lib\site-packages
```

Rename:

- `limnode.py` to `limnode.py.backup`
- `limtabledata.py` to `limtabledata.py.backup`

Optionally also copy the originals somewhere outside Program Files so they survive a reinstall.

## 2. Install the patched files

Download `limnode.py` and `limtabledata.py` from the LIM link above. Use the **raw** file view, and make sure they save as `.py`, not `.py.txt`. Place both in the NIS site-packages folder, replacing the renamed originals.

## 3. Copy the lim files into the environment

Copy **three** files from the NIS site-packages folder:

- `limnode.py` (the patched one)
- `limtabledata.py` (the patched one)
- `limreport.py` (the unchanged original)

into your environment:

```
C:\Convpaint\.pixi\envs\default\Lib\site-packages
```

> **Check you are in the right folder.** That folder already holds hundreds of package folders (numpy, torch, napari_convpaint, and so on). If it looks empty, you are one level too high. The files must go inside `envs\default\Lib\site-packages`, not `envs\Lib\site-packages` and not the project root.

Without this step the node fails with `ModuleNotFoundError: No module named 'limnode'`.

## 4. Restart NIS-Elements

Required for the patched files to take effect.

Next: [Add the GA3 Python node](ga3-node.md).

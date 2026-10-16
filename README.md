# convpaint-ga3

Run a trained [napari-convpaint](https://github.com/guiwitz/napari-convpaint) pixel-classification model as a segmentation step inside a Nikon **NIS-Elements GA3** recipe, using the GA3 Python node.

Convpaint lets you train a segmentation model by painting a few annotations in napari, with no deep-learning setup. This repo covers the other half: getting that saved model to run inside GA3 on a Windows PC, so its output can feed the rest of a GA3 recipe (binary clean-up, measurement, JOBS acquisition targets).

## Status

| | |
|---|---|
| Validated on | NIS-Elements **6.20**, Windows, Python **3.11**, napari-convpaint **1.1.0** |
| Image type | **Single-channel only** (validated). Multichannel and RGB nodes are not yet developed or tested. |
| NIS-Elements 7.x | **Not tested.** LIM's 7.01 release added native conda/mamba environment support to the Python node, so the lim-file patching described here is specific to 6.20. See LIM's [GA3-examples](https://github.com/Laboratory-Imaging/GA3-examples) repo, including `NIS_v7.10/50-Troubleshooting_pyenvs`. |

## What you need

- A Windows PC with NIS-Elements 6.20 and **administrator rights** (one step patches files in the NIS install folder)
- A trained convpaint model saved as a `.pkl` file, trained on **single-channel** images (for example DAPI alone), and fed the same channel at inference
- The **same napari-convpaint version** that was used to train that model (convpaint models may not load across versions, and results can differ)
- About an hour, most of it package downloads

## Quickstart

1. **Build the environment**: pixi, Python 3.11, napari-convpaint 1.1.0. See [docs/installation.md](docs/installation.md).
2. **Validate the model outside GA3** with [`scripts/test_convpaint_standalone.py`](scripts/test_convpaint_standalone.py). Do not continue until this passes.
3. **Patch the NIS lim files** and copy them into the environment. See [docs/lim-file-patch.md](docs/lim-file-patch.md).
4. **Add the Python node** to a GA3 recipe using [`nodes/single_convpaint_node.py`](nodes/single_convpaint_node.py). See [docs/ga3-node.md](docs/ga3-node.md).

If something fails, start with [docs/troubleshooting.md](docs/troubleshooting.md). If you want to understand why the steps are what they are, read [docs/how-it-works.md](docs/how-it-works.md).

## Repository layout

```
convpaint-ga3/
├── README.md
├── LICENSE
├── docs/
│   ├── installation.md       environment + standalone validation
│   ├── lim-file-patch.md     patching NIS 6.20 so the Python node starts
│   ├── ga3-node.md           configuring and running the node
│   ├── troubleshooting.md
│   └── how-it-works.md       environments, activation, out-of-process nodes
├── scripts/
│   └── test_convpaint_standalone.py
└── nodes/
    └── single_convpaint_node.py
```

## Scope

This repo is about **deployment**: running an existing model in GA3. It does not cover training a model. For that, see the [napari-convpaint documentation](https://github.com/guiwitz/napari-convpaint).

## Credits

- [Laboratory Imaging](https://github.com/Laboratory-Imaging/GA3-examples) for the GA3 examples, in particular `NIS_v6.20/52-Python_cellpose` (the pattern this node follows) and `NIS_v6.20/00-Fixing_Python_Issues` (the lim-file patches this setup depends on).
- [napari-convpaint](https://github.com/guiwitz/napari-convpaint) and its authors.

## License

MIT. See [LICENSE](LICENSE). The patched lim files are LIM's and are not redistributed here; get them from the link above.

## Author

Shane Vontelin van Breda

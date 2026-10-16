# The GA3 Python node

Prerequisites: the environment is built and the model validated ([installation](installation.md)), the lim files are patched and copied ([lim-file-patch](lim-file-patch.md)), and NIS-Elements has been restarted.

Develop and test recipes on any PC with NIS-Elements and a saved image. You do not need the microscope until you run a live acquisition.

## 1. Add and configure the node

1. Open NIS-Elements with an image loaded, then open the GA3 editor.
2. Add a **Python** node: `ND Processing & Conversions` then `Python` (bottom of the list).
3. In the node panel, add one **colour input** and one **binary output**.
4. Switch **Run out of process** ON.
5. Click `...` next to the interpreter dropdown and select:

   ```
   C:\Convpaint\.pixi\envs\default\pythonw.exe
   ```

## 2. Paste the node code

Replace the entire default contents of the editor with [`nodes/single_convpaint_node.py`](../nodes/single_convpaint_node.py).

Edit the constants at the top of the file:

| Constant | Meaning |
|---|---|
| `MODEL_PATH` | Full path to your `.pkl` model |
| `LOG_PATH` | Where the node writes its progress log. The folder must already exist. |
| `TARGET_CLASS` | The label number of the structure you want. Class numbers are the ones you assigned when annotating (commonly 1 = background, 2 = target, 3 = debris). |
| `OUTPUT_NAME` | Label for the binary output layer |

## 3. Wire the input

Connect a single channel (for example from a **Channels** node) to the Python node's input.

> **Channel consistency is critical.** The model must receive the same channel, in the same order, that it was trained on. A model trained on DAPI alone produces meaningless output if fed another channel. If your image has several channels, select the correct one in the Channels node.

## 4. Run

Run the recipe. Expect several minutes of apparent inactivity on a large image; GA3 cannot show progress from inside the Python call.

**The log file is your progress indicator**, because `print` output from an out-of-process node does not reach the NIS log:

| In `python.log` | Meaning |
|---|---|
| `Model loaded`, no `Segmented` line yet | Still computing; wait |
| `Segmented: N positive px` | Finished. Compare `N` with your standalone benchmark. |
| No log file at all | The child process died before running. See [troubleshooting](troubleshooting.md). |

## What the code does

- `import limnode` must be written exactly like that: not `from limnode import ...`, and not `import limnode as ...`.
- Heavy imports (`numpy`, `napari_convpaint`) live inside `run()`, because `output()` is called far more often than `run()`.
- The model is cached in a global, so it loads once per child process instead of once per call.
- NIS passes image data as rank-4 arrays, `[z, y, x, channel]`, so `inp[0].data[0, :, :, 0]` extracts a 2D single-channel image.
- The result is cast to `uint8` (NIS will not accept convpaint's default integer label type).
- `limnode.separateLabeledImage()` turns a labelled image into a NIS binary. NIS distinguishes objects by connectivity, so touching objects would otherwise merge.
- Segmentation applies the model's saved settings, including any downsampling, and returns labels at the original image size.

## Using the result downstream

Convpaint output is a pixel classification, not tidy objects. Some general points when building the rest of the recipe:

- **Use Binary processing nodes**, not Image processing nodes. Image-processing nodes expect a channel and will not connect to a binary. If a node asks for a channel, it is from the wrong menu.
- Masks are often lace-like, because the class boundary follows internal texture. **Dilate** until each structure merges into one continuous mass, **then Fill Holes**. The order matters: holes open to the outside are not holes.
- **Choose filter thresholds from measured data, not by guessing.** Run once with an Object Measurement node and no filter, then look at the area distribution for the gap between real objects and debris.
- If something downstream (for example NIS-JOBS) consumes the **binary**, the selection step must reduce the binary. A node that only filters the results table leaves the binary untouched.
- **Tuning tip:** save the binary once, then build and tune the downstream nodes against the saved binary. Previews become instant, with no multi-minute Python-node runs and no broken pipes.
- If you add GA3 analysis to stitched or tiled data, run segmentation on the stitched output, because segmenting tiles separately breaks objects at tile edges.

## Moving a recipe to another machine

The GA3 recipe is portable; the environment is not. On the new machine, repeat [installation](installation.md) and [lim-file-patch](lim-file-patch.md), copy over the `.ga3` recipe and the `.pkl`, re-run the standalone test and compare the benchmark count, and only then run the recipe. If the folder path is identical to the source machine, no edits are needed. Otherwise update the interpreter path in the node and the two paths in the code.

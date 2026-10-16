# Troubleshooting

Always check `python.log` first (see [ga3-node.md](ga3-node.md)); it is the only view into what the out-of-process Python is doing.

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'limnode'` | The lim files are missing from the environment | Copy all three lim files into `.pixi\envs\default\Lib\site-packages` ([lim-file-patch, step 3](lim-file-patch.md)) |
| `CalledProcessError: Exited code 1` immediately on run | The child process died at startup, usually because the unpatched lim files reject your Python version or `Library\bin` is missing from PATH | Install the patched lim files and restart NIS-Elements |
| `QtBindingsNotFoundError: No Qt bindings could be found` | convpaint imports its napari widget, which needs Qt | `pip install pyqt5` inside the environment |
| `FileNotFoundError: ... python.log` | The log folder does not exist | Create the folder named in the log path in the node |
| `FileNotFoundError: ... .pkl` | Wrong model filename or path | Copy the exact name into the model path in the node |
| No log file and no error | The child process never started | Check the interpreter path points at `pythonw.exe` in `.pixi\envs\default`, and that NIS was restarted after patching |
| `BrokenPipeError: The pipe is being closed` during preview | The preview was cancelled or superseded while the child was still running | Usually cosmetic if a full Run succeeds. If `python.log` shows repeated `Model loaded` lines, the child is restarting often and may be running out of memory. |
| Process killed with no error | Out of memory during feature extraction on a large image | Retrain with a higher `image_downsample`, or crop the input |
| Segmentation differs from the machine where you trained | napari-convpaint version mismatch | `pip install napari-convpaint==<version used for training>` |
| Positive-pixel count differs from your benchmark | Version mismatch, or a different channel or image | Re-run `test_convpaint_standalone.py` on the reference image and compare |
| Binary is empty downstream | Filter threshold in the wrong units, or filtering before objects were consolidated | Preview the Python node output directly; check filter units against measured values |
| Binary is fragmented into thousands of objects | Lace-like convpaint output not consolidated | Increase Dilate, then Fill Holes |
| A binary-processing node will not connect to the Python node | Wrong node family | Use nodes from Binary processing, Binary operations or Measurement, not Image processing |
| Works in napari, fails in GA3 | Different channel input, or a different convpaint version | Check the channel wiring and version; run the standalone test |

**Harmless warnings:** messages that Cellpose or Ilastik are not installed, and the "FE model is designed for imagenet normalization" warning for single-channel images.

Still stuck? Open an issue and include the full error text and the contents of `python.log`.

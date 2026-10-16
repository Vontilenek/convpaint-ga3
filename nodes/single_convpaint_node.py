# Single-channel convpaint segmentation for a NIS-Elements GA3 Python node.
#
# Paste this whole file into the node editor (Run out of process = ON).
# Edit the four constants below, nothing else.
#
# Validated: NIS-Elements 6.20, Python 3.11, napari-convpaint 1.1.0.
import limnode

# ----------------------------------------------------------------------
# EDIT THESE
MODEL_PATH = r"C:\Convpaint\models\my_model.pkl"   # your trained model
LOG_PATH = r"C:\Convpaint\logs\python.log"         # folder must already exist
TARGET_CLASS = 2                                   # label number of the structure you want
OUTPUT_NAME = "segmentation"                       # name of the binary output layer
# ----------------------------------------------------------------------

model = None


def _log(message):
    # Out-of-process print output does not reach the NIS log, so write to a file.
    with open(LOG_PATH, "a") as f:
        f.write(f"{message}\n")


def output(inp, out):
    # One binary output layer, displayed in cyan.
    out[0].makeNew(OUTPUT_NAME, (0, 255, 255))


def build(loops):
    return None


def run(inp, out, ctx):
    # Heavy imports live here: output() is called far more often than run().
    import numpy
    from napari_convpaint import ConvpaintModel

    # Cache the model in a global so it loads once per child process.
    global model
    if model is None:
        model = ConvpaintModel(model_path=MODEL_PATH)
        _log("Model loaded")

    # Input and output data are always rank 4: [z, y, x, channel].
    img = inp[0].data[0, :, :, 0]

    labels = numpy.squeeze(model.segment(img))

    # Keep only the target class; cast to uint8 for NIS.
    binary = (labels == TARGET_CLASS).astype(numpy.uint8)

    out[0].data[0, :, :, 0] = limnode.separateLabeledImage(binary)
    _log(f"Segmented: {int(binary.sum())} positive px")


# Child process initialisation: required when "Run out of process" is set.
if __name__ == '__main__':
    limnode.child_main(run, output, build)

# Single-channel convpaint segmentation for a NIS-Elements GA3 Python node.
#
# Paste this whole file into the node editor (Run out of process = ON).
# Change only the two paths marked ">>>" (and the class number 2 if needed).
#
# Validated: NIS-Elements 6.20, Python 3.11, napari-convpaint 1.1.0.
import limnode

model = None

def _log(message):
    # Out-of-process print output does not reach the NIS log, so write to a file.
    # >>> log path (the folder must already exist)
    with open("C:\\Convpaint\\logs\\python.log", "a") as f:
        f.write(f"{message}\n")

def output(inp, out):
    # One binary output layer, displayed in cyan.
    out[0].makeNew("segmentation", (0, 255, 255))

def build(loops):
    return None

def run(inp, out, ctx):
    # Heavy imports live here: output() is called far more often than run().
    import numpy
    from napari_convpaint import ConvpaintModel

    # Cache the model in a global so it loads once per child process.
    global model
    if model is None:
        # >>> model path
        model = ConvpaintModel(
            model_path="C:\\Convpaint\\models\\my_model.pkl"
        )
        _log("Model loaded")

    # Input and output data are always rank 4: [z, y, x, channel].
    img = inp[0].data[0, :, :, 0]

    labels = numpy.squeeze(model.segment(img))

    # Keep only the target class (2 = the structure you trained for); cast to uint8 for NIS.
    binary = (labels == 2).astype(numpy.uint8)

    out[0].data[0, :, :, 0] = limnode.separateLabeledImage(binary)
    _log(f"Segmented: {int(binary.sum())} positive px")

# Child process initialisation — required when "Run out of process" is set.
if __name__ == '__main__':
    limnode.child_main(run, output, build)

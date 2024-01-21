# RNN-GUI-WAT

This application provides a GUI for the [torch-rnn](https://github.com/jcjohnson/torch-rnn) RNN implementation by jcjohnson.

# Installation and prerquisites

## System setup
You'll need to install the header files for Python 2.7 and the HDF5 library.

```bash
sudo apt-get -y install python2.7-dev
sudo apt-get install libhdf5-dev
```

## Python setup
The preprocessing script is written in Python 2.7; its dependencies are in the file `requirements.txt`.
You can install these dependencies in a virtual environment like this:

```bash
virtualenv .env                  # Create the virtual environment
source .env/bin/activate         # Activate the virtual environment
pip install -r requirements.txt  # Install Python dependencies
# Work for a while ...
deactivate                       # Exit the virtual environment
```

## Lua setup
The main modeling code is written in Lua using [torch](http://torch.ch); you can find installation instructions
[here](http://torch.ch/docs/getting-started.html#_). You'll need the following Lua packages:

- [torch/torch7](https://github.com/torch/torch7)
- [torch/nn](https://github.com/torch/nn)
- [torch/optim](https://github.com/torch/optim)
- [lua-cjson](https://luarocks.org/modules/luarocks/lua-cjson)
- [torch-hdf5](https://github.com/deepmind/torch-hdf5)

After installing torch, you can install / update these packages by running the following:

```bash
# Install most things using luarocks
luarocks install torch
luarocks install nn
luarocks install optim
luarocks install lua-cjson

# We need to install torch-hdf5 from GitHub
git clone https://github.com/deepmind/torch-hdf5
cd torch-hdf5
luarocks make hdf5-0-0.rockspec
```

### CUDA support (Optional)
To enable GPU acceleration with CUDA, you'll need to install CUDA 6.5 or higher and the following Lua packages:
- [torch/cutorch](https://github.com/torch/cutorch)
- [torch/cunn](https://github.com/torch/cunn)

You can install / update them by running:

```bash
luarocks install cutorch
luarocks install cunn
```

## OpenCL support (Optional)
To enable GPU acceleration with OpenCL, you'll need to install the following Lua packages:
- [distro-cl](https://github.com/hughperkins/distro-cl)

You can install / update them by running:

```bash
git clone --recursive https://github.com/hughperkins/distro -b distro-cl ~/torch-cl
cd ~/torch-cl
bash install-deps
./install.sh
```

# Usage


## Step 1: Preprocess the data
Currently, data preprocessing has do be done by hand as described by jcjohnson's [torch-rnn](https://github.com/jcjohnson/torch-rnn) page.

If you have training data stored in `my_data.txt`, you can run the script like this (in the torch-rnn directory):

```bash
python scripts/preprocess.py \
  --input_txt my_data.txt \
  --output_h5 my_data.h5 \
  --output_json my_data.json
```

This will produce files `my_data.h5` and `my_data.json` that will be passed to the training script.

## Step 2: Training the model

To train the model run the `main.py` file like this:

```bash
python3 main.py
```

This will bring up the gui application
![image.jpg](https://github.com/MiloszKahlan/RNN-GUI-WAT/blob/main/examples/RNN%20gui.png)

Then, fill out the labeled textboxes with the corresponding file names and desired parameters, you can use the same parameters as in the picture, but feel free to experiment.
Num layers: 3
RNN size: 512
Max Epochs: 12
GPU Backend : opencl  (this means that a AMD GPU was used)

Then Press 'Start" to start the training

Every 1000 iterations a validation is performed at which point, Validation Loss will be calculated and a checkpoint is generated, which will be used to sample the model.

## Step 3: Sampling the model

In order to sample from the model, switch to the sampling tab. There enter the name of the checkpoint you want to sample from (they are stored in the cv folder of torch-rnn), as well as the desired sample length and gpu backend type.

![Example](https://github.com/MiloszKahlan/RNN-GUI-WAT/blob/main/examples/sample.png)

The resulting sample will be saved to a file result.txt but you can also copy the result right from the text box and paste it to a file by your own.

## Step 4: Converting sample to music

The training data for this example was obtained by converting MIDI files into csv using [midicsv](https://www.fourmilab.ch/webtools/midicsv/)

Then, the csv files were further compressed using carykh's [caryCompressionMIDICSV](https://github.com/carykh/caryCompressionMIDICSV)

In order to convert the sample to music, revert the process: result.txt -> uncompressed CSV -> result.midi

# TODOs
1. Rewrite the MIDICSV compression and add the functionality to RNN-GUI-WAT
2. Incorporate the functionality of MIDICSV
3. Add input sanitizing to textboxes and handling for non-gpu cases
4. TBD

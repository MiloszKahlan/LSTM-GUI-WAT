# RNN-GUI-WAT

This application provides a GUI for preprocessing Kern datasets, training an LSTM model and generating Midi music.

# Installation and prerequisites

## System setup
You'll need to install the following dependencies

```bash
pip install tensorflow midi21 matplotlib pyqt5 numpy
```

### CUDA support (Optional)
To enable GPU acceleration with CUDA, you'll need drivers for you NVIDIA GPU


# Usage


## Step 1: Preprocess the data
Unpack your Kern dataset (files only) into data/dataset.

Launch main.py

![Preprocessing tab](https://github.com/MiloszKahlan/RNN-GUI-WAT/blob/master/Examples/preprocessing_tab.png)

In the preprocessing tab, press "Preprocess Data". Your Kern files will be preprocessedinto a single file dataset and a mapping file.

## Step 2: Training the model

Open the training tab

![Training Tab](https://github.com/MiloszKahlan/RNN-GUI-WAT/blob/master/Examples/training_tab.png)


Then, fill out the labeled textboxes with the desired parameters, you can use the same parameters as in the picture, but feel free to experiment.

*Important* - the Output units parameter must match the size of the generated vocabulary - the amount of items in your mapping.json file.

Then Press 'Start" to start the training

Every epoch the plots are updated with training/validation loss/accuracy values.

![Training Tab running](https://github.com/MiloszKahlan/RNN-GUI-WAT/blob/master/Examples/training.png)

## Step 3: Sampling the model

In order to generate music from the model, switch to the sampling tab. There enter desired parameters into the text boxes. 10 seed values are hardcoded. The number of steps indicates the max amount of symbols that might be generated. The temperature value indicates how randomly the model will be sampled (<1 - less random, >1 - more random).

![Example](https://github.com/MiloszKahlan/RNN-GUI-WAT/blob/master/Examples/sampling.png)

The resulting file will be saved as mel.mid. Have a listen!

# Examples
For examples of training data, training files and generated .midi files, refer to the examples folder of the repository

# Attributions

This project uses code from Valerio Velardo's ![repository](https://github.com/musikalkemist/generating-melodies-with-rnn-lstm) which is distributed under the MIT license.

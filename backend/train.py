import tensorflow.keras as keras
from .preprocess import generate_training_sequences, SEQUENCE_LENGTH
import os

NUM_UNITS = [256]
LOSS = "sparse_categorical_crossentropy"
LEARNING_RATE = 0.001
BATCH_SIZE = 64
SAVE_MODEL_DIR = "data/model"
SAVE_MODEL_PATH = os.path.join(SAVE_MODEL_DIR, "model_epoch_{epoch:02d}.h5")


class StopTrainingCallback(keras.callbacks.Callback):
    def __init__(self, stop_flag):
        super().__init__()
        self.stop_flag = stop_flag

    def on_batch_end(self, batch, logs=None):
        if self.stop_flag.is_set():
            self.model.stop_training = True
            print("Stopping training as requested.")

class PlotMetricsCallback(keras.callbacks.Callback):
    def __init__(self, update_plots_callback):
        super().__init__()
        self.update_plots_callback = update_plots_callback

    def on_epoch_end(self, epoch, logs=None):
        if logs is not None:
            train_loss = logs.get('loss')
            train_accuracy = logs.get('accuracy')
            val_loss = logs.get('val_loss')
            val_accuracy = logs.get('val_accuracy')
            self.update_plots_callback(epoch, train_loss, train_accuracy, val_loss, val_accuracy)

def build_model(output_units, num_units, loss, learning_rate):
    """Builds and compiles model

    :param output_units (int): Num output units
    :param num_units (list of int): Num of units in hidden layers
    :param loss (str): Type of loss function to use
    :param learning_rate (float): Learning rate to apply

    :return model (tf model): Where the magic happens :D
    """

    # create the model architecture
    input = keras.layers.Input(shape=(None, output_units))
    x = keras.layers.LSTM(num_units[0])(input)
    x = keras.layers.Dropout(0.2)(x)

    output = keras.layers.Dense(output_units, activation="softmax")(x)

    model = keras.Model(input, output)

    # compile model
    model.compile(loss=loss,
                  optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
                  metrics=["accuracy"])

    model.summary()

    return model


def train(output_units, num_units, epochs, stop_flag, update_plots_callback):
    """Train and save TF model.

    :param output_units (int): Num output units
    :param num_units (list of int): Num of units in hidden layers
    :param loss (str): Type of loss function to use
    :param learning_rate (float): Learning rate to apply
    :param epochs (int): Number of epochs for training
    :param stop_flag (threading.Event): Event to signal stopping the training
    :param update_plots_callback (function): Callback function to update plots
    """

    # generate the training and validation sequences
    x_train, x_val, y_train, y_val = generate_training_sequences(SEQUENCE_LENGTH)

    # build the network
    model = build_model(output_units, num_units, LOSS, LEARNING_RATE)

    # define the model checkpoint callback
    checkpoint_callback = keras.callbacks.ModelCheckpoint(filepath=SAVE_MODEL_PATH,
                                                          save_weights_only=False,
                                                          save_best_only=False,
                                                          save_freq='epoch')

    # define early stopping callback
    early_stopping_callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    # define stop training callback
    stop_training_callback = StopTrainingCallback(stop_flag)

    # define plot metrics callback
    plot_metrics_callback = PlotMetricsCallback(update_plots_callback)

    # train the model with all callbacks
    model.fit(x_train, y_train, epochs=epochs, batch_size=BATCH_SIZE,
              validation_data=(x_val, y_val), callbacks=[checkpoint_callback, early_stopping_callback, stop_training_callback, plot_metrics_callback])

    # save the model
    if not stop_flag.is_set():
        model.save(SAVE_MODEL_PATH)
        print("Model saved.")


if __name__ == "__main__":
    train()

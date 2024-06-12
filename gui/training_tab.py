import sys
import threading
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
from PyQt5.QtGui import QTextCursor
from backend.train import train as trainMain
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass

class TrainingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.stop_flag = threading.Event()  # Event to signal the stop of the training

        # Layout for the first tab
        tab_layout = QHBoxLayout(self)
        self.setLayout(tab_layout)

        # Left layout
        left_layout = QVBoxLayout()
        tab_layout.addLayout(left_layout)

        # TextEdit for logs
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        left_layout.addWidget(QLabel("Log output:"))
        left_layout.addWidget(self.textEdit)

        # Input fields for parameters
        self.output_units = QLineEdit(self)
        self.lstm_size = QLineEdit(self)
        self.max_epochs = QLineEdit(self)

        # Add input fields to the layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Output units (vocabulary size from mapping.json):"))
        input_layout.addWidget(self.output_units)
        input_layout.addWidget(QLabel("LSTM Size:"))
        input_layout.addWidget(self.lstm_size)
        input_layout.addWidget(QLabel("Max Epochs:"))
        input_layout.addWidget(self.max_epochs)

        # Add input layout to left layout
        left_layout.addLayout(input_layout)

        # Start and Stop buttons
        self.startButton = QPushButton('Start', self)
        self.startButton.clicked.connect(self.on_start_button_clicked)
        left_layout.addWidget(self.startButton)

        self.stopButton = QPushButton('Stop', self)
        self.stopButton.clicked.connect(self.on_stop_button_clicked)
        left_layout.addWidget(self.stopButton)

        # Add left layout to main layout
        tab_layout.addLayout(left_layout)

        # Right layout for plots
        right_layout = QVBoxLayout()
        tab_layout.addLayout(right_layout)

        # Create matplotlib figures for training and validation metrics
        self.train_fig = Figure()
        self.train_canvas = FigureCanvas(self.train_fig)
        right_layout.addWidget(self.train_canvas)

        self.val_fig = Figure()
        self.val_canvas = FigureCanvas(self.val_fig)
        right_layout.addWidget(self.val_canvas)

        # Create an EmittingStream for this tab
        self.stdout_stream = EmittingStream()
        self.stdout_stream.textWritten.connect(self.append_text)
        self.old_stdout = sys.stdout

        self.train_losses = []
        self.train_accuracies = []
        self.val_losses = []
        self.val_accuracies = []

    @pyqtSlot(str)
    def append_text(self, text):
        self.textEdit.moveCursor(QTextCursor.End)
        self.textEdit.insertPlainText(text)
        self.textEdit.moveCursor(QTextCursor.End)

    def on_start_button_clicked(self):
        # Reset the stop flag
        self.stop_flag.clear()
        self.thread = threading.Thread(target=self.run_train)
        self.thread.start()

    def on_stop_button_clicked(self):
        # Set the stop flag to signal the thread to stop
        if self.thread is not None:
            self.stop_flag.set()
            self.thread.join()
            self.thread = None

    def run_train(self):
        output_units = int(self.output_units.text())
        lstm_size = [int(self.lstm_size.text())]
        max_epochs = int(self.max_epochs.text())

        sys.stdout = self.stdout_stream
        try:
            trainMain(output_units=output_units, num_units=lstm_size, epochs=max_epochs, stop_flag=self.stop_flag, update_plots_callback=self.update_plots)
        finally:
            sys.stdout = self.old_stdout

    def update_plots(self, epoch, train_loss, train_accuracy, val_loss, val_accuracy):
        self.train_losses.append(train_loss)
        self.train_accuracies.append(train_accuracy)
        self.val_losses.append(val_loss)
        self.val_accuracies.append(val_accuracy)

        self.plot_metrics(self.train_fig, self.train_canvas, "Training Metrics", "Loss", "Accuracy", self.train_losses, self.train_accuracies)
        self.plot_metrics(self.val_fig, self.val_canvas, "Validation Metrics", "Loss", "Accuracy", self.val_losses, self.val_accuracies)

    def plot_metrics(self, fig, canvas, title, ylabel1, ylabel2, losses, accuracies):
        fig.clear()
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        ax1.plot(losses, 'g-')
        ax2.plot(accuracies, 'b-')

        ax1.set_xlabel('Epochs')
        ax1.set_ylabel(ylabel1, color='g')
        ax2.set_ylabel(ylabel2, color='b')

        ax1.set_title(title)
        canvas.draw()

    def __del__(self):
        # Restore stdout
        sys.stdout = self.old_stdout

# Don't forget to restore sys.stdout when the application exits
import atexit
atexit.register(lambda: sys.stdout.__setattr__('write', sys.__stdout__.write))

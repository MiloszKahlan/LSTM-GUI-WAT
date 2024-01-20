from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
import re
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from external_thread import External


class TrainingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.loss_values = []  # List to store loss values
        self.val_loss_values = []  # List to store val_loss values

        # Layout for the first tab
        tab1_layout = QVBoxLayout(self)
        self.setLayout(tab1_layout)

        # TextEdit for logs
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        left_layout = QVBoxLayout()
        tab1_layout.addWidget(self.textEdit)

        # Input fields for parameters
        self.input_h5 = QLineEdit(self)
        self.input_json = QLineEdit(self)
        self.model_type = QLineEdit(self)
        self.num_layers = QLineEdit(self)
        self.rnn_size = QLineEdit(self)
        self.max_epochs = QLineEdit(self)
        self.gpu_backend = QLineEdit(self)

        # Add input fields to the layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Input H5:"))
        input_layout.addWidget(self.input_h5)
        input_layout.addWidget(QLabel("Input JSON:"))
        input_layout.addWidget(self.input_json)
        input_layout.addWidget(QLabel("Model Type:"))
        input_layout.addWidget(self.model_type)
        input_layout.addWidget(QLabel("Num Layers:"))
        input_layout.addWidget(self.num_layers)
        input_layout.addWidget(QLabel("RNN Size:"))
        input_layout.addWidget(self.rnn_size)
        input_layout.addWidget(QLabel("Max Epochs:"))
        input_layout.addWidget(self.max_epochs)
        input_layout.addWidget(QLabel("GPU Backend:"))
        input_layout.addWidget(self.gpu_backend)

        # Add input layout to left layout
        tab1_layout.addLayout(input_layout)

        # Matplotlib figure
        self.figure = Figure(figsize=(10, 4))  # Adjust figure size
        self.canvas = FigureCanvas(self.figure)
        self.ax_loss = self.figure.add_subplot(121)
        self.ax_val_loss = self.figure.add_subplot(122)

        # Initialize both plots
        self.init_plots()

        # Adding canvas to the layout
        tab1_layout.addWidget(self.canvas)

        # Start and Stop buttons
        self.startButton = QPushButton('Start', self)
        self.startButton.clicked.connect(self.startSubprocess)
        left_layout.addWidget(self.startButton)

        self.stopButton = QPushButton('Stop', self)
        self.stopButton.clicked.connect(self.stopSubprocess)
        left_layout.addWidget(self.stopButton)

        # Add layouts to main layout
        tab1_layout.addLayout(left_layout)

    def init_plots(self):
        self.ax_loss.set_title('Loss Over Time')
        self.ax_loss.set_xlabel('Iteration')
        self.ax_loss.set_ylabel('Loss')
        self.ax_val_loss.set_title('Validation Loss Over Time')
        self.ax_val_loss.set_xlabel('Iteration')
        self.ax_val_loss.set_ylabel('Validation Loss')


    @pyqtSlot(str)
    def onCountChanged(self, value):
        self.textEdit.append(value)

        # Regex pattern to match the specific format of the Epoch lines
        epoch_pattern = r'Epoch (\d+(\.\d+)?) / (\d+), i = (\d+) / (\d+), loss = (\d+(\.\d+)?)'
        
        # Regex pattern for val_loss lines
        val_loss_pattern = r'val_loss =\s*(\d+(\.\d+)?)'

        # Check if the output line matches the Epoch format
        match = re.match(epoch_pattern, value)
        if match:
            # Extract the numbers
            epoch, _, total_epochs, iteration, total_iterations, loss, _ = match.groups()
            epoch = float(epoch)
            total_epochs = int(total_epochs)
            iteration = int(iteration)
            total_iterations = int(total_iterations)
            loss = float(loss)

            # Now you can use these variables as needed
            print(f"Epoch: {epoch}, Total Epochs: {total_epochs}, Iteration: {iteration}, Total Iterations: {total_iterations}, Loss: {loss}")

            # Check if the output line matches the val_loss format
        val_loss_match = re.match(val_loss_pattern, value)
        if val_loss_match:
            val_loss = float(val_loss_match.group(1))

            # Process the val_loss data
            print(f"Validation Loss: {val_loss}")

        # Update loss plot
        if 'loss' in locals():
            self.loss_values.append(loss)
            self.update_loss_plot()

        # Update val_loss plot
        if 'val_loss' in locals():
            self.val_loss_values.append(val_loss)
            self.update_val_loss_plot()


    def update_loss_plot(self):
        self.ax_loss.clear()
        self.ax_loss.plot(self.loss_values, label='Loss')
        self.init_plots()  # Reinitialize plot settings
        self.canvas.draw_idle()  # Use draw_idle for efficient updating

    def update_val_loss_plot(self):
        self.ax_val_loss.clear()
        self.ax_val_loss.plot(self.val_loss_values, label='Validation Loss')
        self.init_plots()  # Reinitialize plot settings
        self.canvas.draw_idle()  # Use draw_idle for efficient updating


    def startSubprocess(self):
        commandTrain = ['th', 'train.lua']
        commandTrain += ['-input_h5', self.input_h5.text()]
        commandTrain += ['-input_json', self.input_json.text()]
        commandTrain += ['-model_type', self.model_type.text()]
        commandTrain += ['-num_layers', self.num_layers.text()]
        commandTrain += ['-rnn_size', self.rnn_size.text()]
        commandTrain += ['-max_epochs', self.max_epochs.text()]
        commandTrain += ['-gpu_backend', self.gpu_backend.text()]

        # Disable input fields and start button
        self.input_h5.setEnabled(False)
        self.input_json.setEnabled(False)
        self.model_type.setEnabled(False)
        self.num_layers.setEnabled(False)
        self.rnn_size.setEnabled(False)
        self.max_epochs.setEnabled(False)
        self.gpu_backend.setEnabled(False)
        self.startButton.setEnabled(False)

        # Start the thread with the constructed command
        if not self.thread or not self.thread.isRunning():
            self.thread = External(commandTrain)
            self.thread.countChanged.connect(self.onCountChanged)
            self.thread.start()

    def stopSubprocess(self):

        # Re-enable input fields and start button
        self.input_h5.setEnabled(True)
        self.input_json.setEnabled(True)
        self.model_type.setEnabled(True)
        self.num_layers.setEnabled(True)
        self.rnn_size.setEnabled(True)
        self.max_epochs.setEnabled(True)
        self.gpu_backend.setEnabled(True)
        self.startButton.setEnabled(True)

        if self.thread is not None:
            self.thread.stop()

    def onErrorOccurred(self, error_message):
        # Handle the error, for example, display it in a dialog or append it to the textEdit
        self.textEdit.append("Error: " + error_message)
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QPushButton
from external_thread import External

class SamplingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.outputFile = None
        self.lineCounter = 0  # Initialize the line counter
        
        # Layout for the second tab
        tab2_layout = QVBoxLayout(self)
        self.setLayout(tab2_layout)
        
        # TextEdit for logs
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        left_layout = QVBoxLayout()
        tab2_layout.addWidget(self.textEdit)

        # Input fields for parameters
        self.checkpoint_file = QLineEdit(self)
        self.length = QLineEdit(self)
        self.gpu_backend = QLineEdit(self)

        # Add input fields to the layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Checkpoint file: (with cv/)"))
        input_layout.addWidget(self.checkpoint_file)
        input_layout.addWidget(QLabel("Sample length:"))
        input_layout.addWidget(self.length)
        input_layout.addWidget(QLabel("GPU Backend:"))
        input_layout.addWidget(self.gpu_backend)

        # Add input layout to left layout
        tab2_layout.addLayout(input_layout)

        # Sample button
        self.startButton = QPushButton('Sample', self)
        self.startButton.clicked.connect(self.startSubprocess)
        left_layout.addWidget(self.startButton)

        # Add layouts to main layout
        tab2_layout.addLayout(left_layout)


    def startSubprocess(self):
        commandSample = ['th', 'sample.lua']
        commandSample += ['-checkpoint', self.checkpoint_file.text()]
        commandSample += ['-length', self.length.text()]
        commandSample += ['-gpu_backend', self.gpu_backend.text()]
        print(f"Command: {commandSample}")
        self.outputFile = open('result.txt', 'w')

        # Start the thread with the constructed command
        if not self.thread or not self.thread.isRunning():
            self.thread = External(commandSample)
            self.thread.countChanged.connect(self.onCountChanged)
            self.thread.finished.connect(self.onThreadFinished)  # Connect to the finished signal
            self.thread.start()

    @pyqtSlot(str)
    def onCountChanged(self, value):
        self.textEdit.append(value)
        self.lineCounter += 1
        if self.outputFile and self.lineCounter > 3:  # Skip the first three lines
            self.outputFile.write(value + '\n')

    @pyqtSlot()
    def onThreadFinished(self):
        # This method is called when the thread finishes
        if self.outputFile:
            self.outputFile.close()
            self.outputFile = None
            self.textEdit.append("Result writtent to result.txt")

    def onErrorOccurred(self, error_message):
        # Handle the error, for example, display it in a dialog or append it to the textEdit
        self.textEdit.append("Error: " + error_message)

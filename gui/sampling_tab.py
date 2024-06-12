import sys
import threading
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
from PyQt5.QtGui import QTextCursor
from backend.melodygenerator import MelodyGenerator
from backend.melodygenerator import SEQUENCE_LENGTH

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass

class SamplingTab(QWidget):
    def __init__(self):
        super().__init__()
        

        # Layout for the tab
        tab_layout = QVBoxLayout(self)
        self.setLayout(tab_layout)

        # TextEdit for logs
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        left_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel("Log output:"))
        tab_layout.addWidget(self.textEdit)

        # Input fields for parameters
        self.seed = QLineEdit(self)
        self.num_steps = QLineEdit(self)
        self.temperature = QLineEdit(self)

        # Add input fields to the layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Seed (seed1 - seed10)"))
        input_layout.addWidget(self.seed)
        input_layout.addWidget(QLabel("Number of steps"))
        input_layout.addWidget(self.num_steps)
        input_layout.addWidget(QLabel("Temperature"))
        input_layout.addWidget(self.temperature)

        # Add input layout to left layout
        tab_layout.addLayout(input_layout)

        # Sample button
        self.startButton = QPushButton('Generate', self)
        self.startButton.clicked.connect(self.on_generate_button_clicked)
        left_layout.addWidget(self.startButton)

        # Add layouts to main layout
        tab_layout.addLayout(left_layout)

        # Redirect stdout to the QTextEdit
        self.stdout_stream = EmittingStream()
        self.stdout_stream.textWritten.connect(self.append_text)
        self.old_stdout = sys.stdout

    @pyqtSlot(str)
    def append_text(self, text):
        self.textEdit.moveCursor(QTextCursor.End)
        self.textEdit.insertPlainText(text)
        self.textEdit.moveCursor(QTextCursor.End)

    def on_generate_button_clicked(self):
        # Get the values from the input fields
        seed = self.seed.text()
        num_steps = int(self.num_steps.text())
        temperature = float(self.temperature.text())

        # Start a thread to run the melody generation
        self.thread = threading.Thread(target=self.run_generate_melody, args=(seed, num_steps, temperature))
        self.thread.start()

    def run_generate_melody(self, seed, num_steps, temperature):
        sys.stdout = self.stdout_stream
        try:
            mg = MelodyGenerator()
            melody = mg.generate_melody(seed, num_steps, SEQUENCE_LENGTH, temperature)
            print(melody)
            mg.save_melody(melody)
        finally:
            sys.stdout = self.old_stdout

    def __del__(self):
        # Restore stdout
        sys.stdout = self.old_stdout

# Don't forget to restore sys.stdout when the application exits
import atexit
atexit.register(lambda: sys.stdout.__setattr__('write', sys.__stdout__.write))
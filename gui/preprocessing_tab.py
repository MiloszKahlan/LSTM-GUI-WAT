import sys
import threading
from PyQt5.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
from PyQt5.QtGui import QTextCursor
from backend.preprocess import main as preprocessMain

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass

class PreprocessingTab(QWidget):
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
        tab2_layout.addWidget(QLabel("Log output:"))
        tab2_layout.addWidget(self.textEdit)

        # Sample button
        self.startButton = QPushButton('Preprocess Data', self)
        self.startButton.clicked.connect(self.on_preprocess_button_clicked)
        left_layout.addWidget(self.startButton)

        # Add layouts to main layout
        tab2_layout.addLayout(left_layout)

        # Create an EmittingStream for this tab
        self.stdout_stream = EmittingStream()
        self.stdout_stream.textWritten.connect(self.append_text)
        self.old_stdout = sys.stdout

    @pyqtSlot(str)
    def append_text(self, text):
        self.textEdit.moveCursor(QTextCursor.End)
        self.textEdit.insertPlainText(text)
        self.textEdit.moveCursor(QTextCursor.End)

    def on_preprocess_button_clicked(self):
        self.thread = threading.Thread(target=self.run_preprocess)
        self.thread.start()

    def run_preprocess(self):
        sys.stdout = self.stdout_stream
        try:
            preprocessMain()
        finally:
            sys.stdout = self.old_stdout

    def __del__(self):
        # Restore stdout
        sys.stdout = self.old_stdout

# Don't forget to restore sys.stdout when the application exits
import atexit
atexit.register(lambda: sys.stdout.__setattr__('write', sys.__stdout__.write))

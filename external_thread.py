import subprocess
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
import os
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

# Define the path to the directory containing the Lua script
script_directory = '/home/ubunciak/Downloads/torch-rnn-master'

# Change the current working directory to the script directory
os.chdir(script_directory)

# Define the command to run the Lua script with its arguments

class External(QThread):
    """
    Runs the subprocess in a separate thread.
    """

    countChanged = pyqtSignal(str)
    errorOccurred = pyqtSignal(str)

    def __init__(self, commandTrain = None, commandSample = None):
        super(External, self).__init__()
        self.process = None
        self.commandTrain = commandTrain
        self.commandSample = commandSample

    def run(self):
        if self.commandTrain:
            self.process = subprocess.Popen(self.commandTrain, 
                                            stdout=subprocess.PIPE, 
                                            stderr=subprocess.PIPE, 
                                            universal_newlines=True, 
                                            bufsize=1)               

        for line in iter(self.process.stdout.readline, ''):
            self.countChanged.emit(line.strip())

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None

from PyQt5.QtWidgets import QMainWindow, QTabWidget
from training_tab import TrainingTab
from sampling_tab import SamplingTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()        

        self.setWindowTitle('Training Monitor')
        self.setGeometry(10, 10, 1200, 600)  # Adjust the main window size

        # Create the tab widget
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Create the first tab for existing functionality
        self.trainingTab = TrainingTab()
        self.tabs.addTab(self.trainingTab, "Training")

        # Create the second tab for new functionality
        self.samplingTab = SamplingTab()
        self.tabs.addTab(self.samplingTab, "Sampling")
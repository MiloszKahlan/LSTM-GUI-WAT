from PyQt5.QtWidgets import QMainWindow, QTabWidget
from gui.training_tab import TrainingTab
from gui.sampling_tab import SamplingTab
from gui.preprocessing_tab import PreprocessingTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()        

        self.setWindowTitle('Training Monitor')
        self.setGeometry(10, 10, 1200, 600)  # Adjust the main window size

        # Create the tab widget
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Create the tab for preprocessing
        self.trainingTab = PreprocessingTab()
        self.tabs.addTab(self.trainingTab, "Preprocessing")

        # Create the tab for training
        self.samplingTab = TrainingTab()
        self.tabs.addTab(self.samplingTab, "Training")

        # Create the tab for sampling
        self.samplingTab = SamplingTab()
        self.tabs.addTab(self.samplingTab, "Sampling")
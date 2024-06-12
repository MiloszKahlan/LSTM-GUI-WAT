import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui.main_window import MainWindow

def main():
# Set the high DPI scaling attribute
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    

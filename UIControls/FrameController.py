from DataCollector.CollectDataWindow import CollectDataWindow
from StartMenu.StartWindow import StartWindow
import sys
from PySide2.QtWidgets import *

class FrameController():
    def __init__(self):
        self.startWindow = StartWindow(self)
        self.collectWindow = CollectDataWindow(self)

        self.startWindow.show()

        self.curHeight = 650
        self.curWidth = 1115

    def showStartMenu(self):
        self.collectWindow.close()
        self.loadDataWindow.close()
        self.startWindow.show()

    def showCollectData(self):
        self.startWindow.close()
        self.collectWindow.show()



def main():
    app = QApplication(sys.argv)
    controller = FrameController()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()





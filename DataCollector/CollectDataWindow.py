import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from DataCollector.CollectDataController import *
import tkinter as tk
from tkinter import filedialog
from Plotter import GenericPlot as gp

class CollectDataWindow(QWidget):
    def __init__(self,controller):
        QWidget.__init__(self)

        self.controller = controller
        self.buttonPanel = self.ButtonPanel()
        self.plotPanel = self.Plotter()
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.buttonPanel)
        self.splitter.addWidget(self.plotPanel)
        layout = QHBoxLayout()
        self.setStyleSheet("background-color:#3d4c51;")
        layout.addWidget(self.splitter)
        self.setLayout(layout)
        self.setWindowTitle("Collect Data Gui")

        self.CallbackConnector = PlottingManagement(self.plotCanvas)

# region Gui Components

    def ButtonPanel(self):
        buttonPanel = QWidget()
        buttonLayout = QVBoxLayout()

        self.connect_button = QPushButton('Connect', self)
        self.connect_button.setToolTip('Connect Base')
        self.connect_button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        self.connect_button.objectName = 'Connect'
        self.connect_button.clicked.connect(self.connect_callback)
        self.connect_button.setStyleSheet('QPushButton {color: white;}')
        buttonLayout.addWidget(self.connect_button)

        findSensor_layout = QHBoxLayout()

        self.pair_button = QPushButton('Pair', self)
        self.pair_button.setToolTip('Pair Sensors')
        self.pair_button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        self.pair_button.objectName = 'Pair'
        self.pair_button.clicked.connect(self.pair_callback)
        self.pair_button.setStyleSheet('QPushButton {color: white;}')
        self.pair_button.setEnabled(False)
        findSensor_layout.addWidget(self.pair_button)

        self.scan_button = QPushButton('Scan', self)
        self.scan_button.setToolTip('Scan for Sensors')
        self.scan_button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        self.scan_button.objectName = 'Scan'
        self.scan_button.clicked.connect(self.scan_callback)
        self.scan_button.setStyleSheet('QPushButton {color: white;}')
        self.scan_button.setEnabled(False)
        findSensor_layout.addWidget(self.scan_button)

        buttonLayout.addLayout(findSensor_layout)

        self.start_button = QPushButton('Start', self)
        self.start_button.setToolTip('Start Sensor Stream')
        self.start_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.start_button.objectName = 'Start'
        self.start_button.clicked.connect(self.start_callback)
        self.start_button.setStyleSheet('QPushButton {color: white;}')
        self.start_button.setEnabled(False)
        buttonLayout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.setToolTip('Stop Sensor Stream')
        self.stop_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.stop_button.objectName = 'Stop'
        self.stop_button.clicked.connect(self.stop_callback)
        self.stop_button.setStyleSheet('QPushButton {color: white;}')
        self.stop_button.setEnabled(False)
        buttonLayout.addWidget(self.stop_button)

        self.SensorModeList = QComboBox(self)
        self.SensorModeList.setToolTip('PlaceHolder 3')
        self.SensorModeList.objectName = 'PlaceHolder'
        self.SensorModeList.setStyleSheet('QComboBox {color: white;background: #848482}')
        self.SensorModeList.currentIndexChanged.connect(self.sensorModeList_callback)
        buttonLayout.addWidget(self.SensorModeList)

        self.SensorListBox = QListWidget(self)
        self.SensorListBox.setToolTip('PlaceHolder 4')
        self.SensorListBox.objectName = 'PlaceHolder'
        self.SensorListBox.setStyleSheet('QListWidget {color: white;background:#848482}')
        self.SensorListBox.clicked.connect(self.sensorList_callback)
        buttonLayout.addWidget(self.SensorListBox)

        button = QPushButton('Home', self)
        button.setToolTip('Return to Start Menu')
        button.objectName = 'Home'
        button.clicked.connect(self.home_callback)
        button.setStyleSheet('QPushButton {color: white;}')
        buttonLayout.addWidget(button)

        buttonPanel.setLayout(buttonLayout)

        return buttonPanel

    def Plotter(self):
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        plot_mode = 'windowed'
        pc = gp.GenericPlot(plot_mode)
        pc.native.objectName = 'vispyCanvas'
        pc.native.parent = self
        widget.layout().addWidget(pc.native)
        self.plotCanvas = pc
        return widget

# endregion

    def connect_callback(self):
        self.CallbackConnector.Connect_Callback()
        self.connect_button.setEnabled(False)

        self.pair_button.setEnabled(True)
        self.scan_button.setEnabled(True)

    def pair_callback(self):
        self.CallbackConnector.Pair_Callback()
        self.scan_callback()

    def scan_callback(self):
        sensorList = self.CallbackConnector.Scan_Callback()
        self.SensorListBox.clear()
        self.SensorListBox.addItems(sensorList)
        self.SensorListBox.setCurrentRow(0)

        if len(sensorList)>0:
            self.start_button.setEnabled(True)

    def start_callback(self):
        self.CallbackConnector.Start_Callback()
        self.stop_button.setEnabled(True)

    def stop_callback(self):
        self.CallbackConnector.Stop_Callback()

    def home_callback(self):
        self.controller.showStartMenu()

    def sensorList_callback(self):
        curItem = self.SensorListBox.currentRow()
        modeList = self.CallbackConnector.getSampleModes(curItem)
        curMode = self.CallbackConnector.getCurMode()

        self.SensorModeList.clear()
        self.SensorModeList.addItems(modeList)
        self.SensorModeList.setCurrentText(curMode[0])

    def sensorModeList_callback(self):
        curItem = self.SensorListBox.currentRow()
        selMode = self.SensorModeList.currentText()
        self.CallbackConnector.setSampleMode(curItem,selMode)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    CollectDataWindow = CollectDataWindow()
    CollectDataWindow.show()
    sys.exit(app.exec_())
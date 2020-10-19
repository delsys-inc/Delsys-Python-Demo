"""
Controller class for the Data Collector Gui
This is the GUI that lets you connect to a base, scan via rf for sensors, and stream data from them in real time
"""

from collections import deque
import threading
from Plotter.GenericPlot import *
from AeroPy.TrignoBase import *
from AeroPy.DataManager import *

clr.AddReference("System.Collections")
from System.Collections.Generic import List
from System import Int32

base = TrignoBase()
TrigBase = base.BaseInstance

app.use_app('PySide2')

class PlottingManagement():
    def __init__(self,EMGplot):
        self.EMGplot = EMGplot
        self.packetCount = 0
        self.pauseFlag = False
        self.numSamples = 10000
        self.DataHandler = DataKernel(TrigBase)

    def streaming(self):
        """This is the data processing thread"""
        self.emg_queue = deque()
        while self.pauseFlag is False:
            self.DataHandler.processData(self.emg_plot)
        print(self.DataHandler.getPacketCount())

    def vispyPlot(self):
        """Plot Thread"""
        while self.pauseFlag is False:
            if len(self.emg_plot) >= 1:
                incData = self.emg_plot.popleft()
                outData = list(np.asarray(incData)[tuple([self.dataStreamIdx])])
                self.EMGplot.plot_new_data(outData)

    def threadManager(self):
        """Handles the threads for the DataCollector gui"""
        self.emg_plot = deque()

        t1 = threading.Thread(target=self.streaming)
        t2 = threading.Thread(target=self.vispyPlot)

        t1.start()
        t2.start()

    def Connect_Callback(self):
        """Callback to connect to the base"""
        TrigBase.ValidateBase(key, license, "RF")

    def Pair_Callback(self):
        """Callback to tell the base to enter pair mode for new sensors"""
        TrigBase.PairSensors()

    def Scan_Callback(self):
        """Callback to tell the base to scan for any available sensors"""
        f = TrigBase.ScanSensors().Result
        self.nameList = TrigBase.ListSensorNames()
        self.SensorsFound = len(self.nameList)

        TrigBase.ConnectSensors()
        return self.nameList

    def Start_Callback(self):
        """Callback to start the data stream from Sensors"""

        self.pauseFlag = False
        newTransform = TrigBase.CreateTransform("raw")
        index = List[Int32]()

        TrigBase.ClearSensorList()

        for i in range(self.SensorsFound):
            selectedSensor = TrigBase.GetSensorObject(i)
            TrigBase.AddSensortoList(selectedSensor)
            index.Add(i)

        self.sampleRates = [[] for i in range(self.SensorsFound)]

        TrigBase.StreamData(index, newTransform, 2)

        self.dataStreamIdx = []
        plotCount = 0
        idxVal = 0
        for i in range(self.SensorsFound):
            selectedSensor = TrigBase.GetSensorObject(i)
            for channel in range(len(selectedSensor.TrignoChannels)):
                self.sampleRates[i].append((selectedSensor.TrignoChannels[channel].SampleRate,
                                           selectedSensor.TrignoChannels[channel].Name))
                if "EMG" in selectedSensor.TrignoChannels[channel].Name:
                    self.dataStreamIdx.append(idxVal)
                    plotCount+=1
                idxVal += 1

        self.EMGplot.initiateCanvas(None,None,plotCount,1,self.numSamples)

        self.threadManager()

    def Stop_Callback(self):
        """Callback to stop the data stream"""
        TrigBase.StopData()
        self.pauseFlag = True

    # Helper Functions
    def getSampleModes(self,sensorIdx):
        """Gets the list of sample modes available for selected sensor"""
        sampleModes = TrigBase.ListSensorModes(sensorIdx)
        return sampleModes

    def getCurMode(self):
        """Gets the current mode of the sensors"""
        curMode = TrigBase.GetSampleMode()
        return curMode

    def setSampleMode(self,curSensor,setMode):
        """Sets the sample mode for the selected sensor"""
        TrigBase.SetSampleMode(curSensor,setMode)
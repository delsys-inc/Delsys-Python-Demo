"""
This is the class that handles the data that is output from the Delsys Trigno Base
Create an instance of this and pass it a reference to the Trigno base for initialization
"""
import numpy as np

class DataKernel():
    def __init__(self,trigno_base):
        self.TrigBase = trigno_base
        self.packetCount = 0
        self.sampleCount = 0

    def processData(self,data_queue):
        """Processes the data from the Trignobase and places it in data_queue variable"""
        outArr = self.GetData()
        if outArr is not None:
            for i in range(len(outArr[0])):
                data_queue.append(list(np.asarray(outArr)[:, i]))
            try:
                self.packetCount += len(outArr[0])
                self.sampleCount += len(outArr[0][0])
            except:
                pass

    def GetData(self):
        """Callback to get the data from the streaming sensors"""
        dataReady = self.TrigBase.CheckDataQueue()
        if dataReady:
            DataOut = self.TrigBase.PollData()
            if len(DataOut) > 0:  # Check for lost Packets
                outArr = [[] for i in range(len(DataOut))]
                for j in range(len(DataOut)):
                    for k in range(len(DataOut[j])):
                        outBuf = DataOut[j][k]
                        outArr[j].append(np.asarray(outBuf))
                return outArr
            else:
                return None
        else:
            return None

# region Helpers
    def getPacketCount(self):
        return self.packetCount

    def resetPacketCount(self):
        self.packetCount = 0
        self.sampleCount = 0

    def getSampleCount(self):
        return self.sampleCount
#endregion
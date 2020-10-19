"""
Author: Chan
Last Edit: 3/24/2020

Summary:
This is a Python example gui that utilizes the Delsys API in order to demonstrate functionality that users can
implement in their own code. This example allows a user to connect to the base, scan for sensors, pair new sensors,
and then stream data from them to a plot.

Known Limitations:
-Button presses are not rate limited, so don't click things too quickly or you'll override the queue

TODO:
Only EMG data is being streamed currently, need to implement user options to stream things such as gyro and IMU data
"""

import tkinter as tk
from tkinter import Frame,ttk,filedialog
import clr
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Add the LodeStone Reference with PythonNet
clr.AddReference("/resources/DelsysAPI")
clr.AddReference("System.Collections")

# Import the Python Wrapper from LodeStone.dll
from LodeStone import PyStone
from System.Collections.Generic import List
from System import Int32

# Old licensing scheme for the Delsys API. May be retired in the future
key = "MIIBKjCB4wYHKoZIzj0CATCB1wIBATAsBgcqhkjOPQEBAiEA/////wAAAAEAAAAAAAAAAAAAAAD///////////////8wWwQg/////" \
      "wAAAAEAAAAAAAAAAAAAAAD///////////////wEIFrGNdiqOpPns+u9VXaYhrxlHQawzFOw9jvOPD4n0mBLAxUAxJ02CIbnBJNqZnjh" \
      "E50mt4GffpAEIQNrF9Hy4SxCR/i85uVjpEDydwN9gS3rM6D0oTlF2JjClgIhAP////8AAAAA//////////+85vqtpxeehPO5ysL8YyV" \
      "RAgEBA0IABH66ZuYrdjCXRvg1FNp1+YSdB8OmabrLEkFm6GzMFyUdT/vmPrjQxb6t+YL45vE1+HuLP1+PKGxFTMWa4EjUjfc="
license = "<License><Id>b8fc99f3-61de-4a9f-8bf8-173029dc2210</Id><Type>Trial</Type><Quantity>10</Quantity>" \
          "<LicenseAttributes><Attribute name=\"Software\">VS2012</Attribute></LicenseAttributes><ProductFeatures" \
          "><Feature name=\"Sales\">True</Feature><Feature name=\"Billing\">False</Feature></ProductFeatures>" \
          "<Customer><Name>John Doe</Name><Email>johndoe@delsys.test.com</Email></Customer><Expiration>Mon, " \
          "21 Nov 2107 05:00:00 GMT</Expiration><Signature>MEYCIQCCXA7WXdnalWOtQQBpOQxsg4mKO/SHkDU1AuLZBXYjWw" \
          "IhALCQgYSsyWF/6P6CsRJgIVqo1cWA4Y5O9WOp1zj5grLg</Signature></License>"

sns.set_style("darkgrid")

# Create a new instance of the Python wrapper
TrigBase = PyStone()

# Set the number of samples for the data buffer (Default is 20000)
numSample = 20000

# create the data buffer
outList = [[np.nan]*numSample]

# Set the default axis for the plots. (Default is 5)
yLim = 5

class Window(tk.PanedWindow):
    """Define the main window of the gui"""
    def __init__(self, master = None):
        tk.PanedWindow.__init__(self,master)
        self.master = master
        self.init_window()
        self.config(orient="horizontal", background = '#3d4c51')

    def init_window(self):
        """Sets up the main gui window based on the user selection in StartMenu"""

        self.master.title('Data Stream Example')

        sidebar = tk.Frame(self,width=200, height=400)

        self.wtitle = tk.Label(sidebar, text="Base Comms", fg='white')
        self.wtitle.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        self.connectButton = tk.Button(sidebar, height=5, width=20, text="Connect", command=self.connect_callback,
                                       fg='white')
        self.connectButton.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        self.sensorFrame = tk.Frame(sidebar,width=20, height=5)
        self.sensorFrame.grid(row=2, column=0, sticky=tk.W + tk.E + tk.N + tk.S,rowspan=3)
        self.sensorFrame.columnconfigure(0, weight=1)
        self.sensorFrame.columnconfigure(1, weight=1)
        self.sensorFrame.rowconfigure(0, weight=1)

        self.PairButton = tk.Button(self.sensorFrame, height=10, width=10, text="Pair", command=self.pair_callback,
                                    fg='white')
        self.PairButton.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
        self.ScanButton = tk.Button(self.sensorFrame, height=10, width=10, text="Scan", command=self.scan_callback,
                                    fg='white')
        self.ScanButton.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)

        self.StartButton = tk.Button(sidebar, height=5, width=20, text="Start", command=self.start_callback,fg='white')
        self.StartButton.grid(row=5, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
        self.StopButton = tk.Button(sidebar, height=5, width=20, text="Stop", command=self.stop_callback,fg='white')
        self.StopButton.grid(row=6, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        sidebar.tk_setPalette(background='#3d4c51', foreground='#848482',
                              activeBackground='#848482', activeForeground='#3d4c51')

        self.SensorListbox = tk.Listbox(sidebar, height=10, width=20,background = '#848482',fg = 'white')
        self.SensorListbox.grid(row=7, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
        self.SensorListbox.bind('<<ListboxSelect>>', self.SensorList_callback)

        self.SensorModeList = ttk.Combobox(sidebar, background = '#848482')
        self.SensorModeList.grid(row=8, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
        self.SensorModeList.bind("<<ComboboxSelected>>", self.sensorMode_callback)


        plotWindow = tk.Frame(self, width=400, height=400,background = '#3d4c51')

        self.fig = plt.figure(facecolor='#808080')
        # self.xs = list(range(0, numSample))

        self.plotLabel = tk.Label(plotWindow, text="Plot View", fg='white')
        self.plotLabel.grid(row=0, column=2, sticky=tk.W + tk.E + tk.N + tk.S)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plotWindow)
        self.canvas.get_tk_widget().grid(row=1, column=2, columnspan=1, rowspan=8, sticky=tk.W + tk.E + tk.N + tk.S,
                                         padx=5, pady=5)

        # Code for resizing the window capabilities
        sidebar.columnconfigure(0, weight=1)
        sidebar.rowconfigure(0, weight=1)
        sidebar.rowconfigure(1, weight=1)
        sidebar.rowconfigure(2, weight=1)
        sidebar.rowconfigure(3, weight=1)
        sidebar.rowconfigure(4, weight=1)
        sidebar.rowconfigure(5, weight=1)
        sidebar.rowconfigure(6, weight=1)
        sidebar.rowconfigure(7, weight=1)
        sidebar.rowconfigure(8, weight=1)

        plotWindow.rowconfigure(1, weight=1)
        plotWindow.rowconfigure(3, weight=1)
        plotWindow.rowconfigure(4, weight=1)
        plotWindow.columnconfigure(2, weight=1)

        # Zoom/Pan
        self.press = None
        self.cur_xlim = [0,20000]
        self.cur_ylim = [-yLim,yLim]
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.sampleRates = None

        # add the paned window to the root
        self.pack(fill="both", expand=True)

        # add the sidebar and plotWindow area to the main paned window
        self.add(sidebar)
        self.add(plotWindow)
        self.pauseFlag = False
        self.sidebar = sidebar
        self.curTime = 0
        self.tot_samples=0
        self.plot_sensors = None


    # Callbacks
    def sensorMode_callback(self,instance):
        """Callback to set the current sensormode of the selected sensor"""
        cursel = self.SensorModeList.get()
        curSensor = self.selectedSensor
        TrigBase.SetSampleMode(curSensor,cursel)


    def SensorList_callback(self,instance):
        """Callback for the listbox of sensors, polls the base and loads in the available modes for the currently
        Selected Sensor"""
        sensorSelected = self.SensorListbox.curselection()

        if len(sensorSelected)==0:
            return

        self.selectedSensor = sensorSelected[0]
        sampleModes = TrigBase.ListSensorModes(sensorSelected[0])
        curMode = TrigBase.GetSampleMode()
        setVal = 1
        modeBuf = []

        for i in range(len(sampleModes)):
            modeBuf.append(sampleModes[i])
            if str(curMode[sensorSelected[0]]) in str(sampleModes[i]):
                setVal = i

        self.SensorModeList['values'] = modeBuf
        self.SensorModeList.current(newindex=setVal)


    def connect_callback(self):
        """Callback to connect to the base"""
        TrigBase.ValidateBase(key, license)


    def pair_callback(self):
        """Callback to tell the base to enter pair mode for new sensors"""
        TrigBase.PairSensors()
        self.scan_callback()


    def scan_callback(self):
        """Callback to tell the base to scan for any available sensors"""
        self.SensorListbox.delete(0,tk.END)
        f = TrigBase.ScanSensors().Result
        self.nameList = TrigBase.ListSensorNames()
        for i in range(len(self.nameList)):
            self.SensorListbox.insert(tk.END,self.nameList[i])
        self.SensorsFound = len(self.nameList)
        self.init_callback()


    def init_callback(self):
        """Callback to connect the base to the sensors"""
        TrigBase.ConnectSensors()


    def PreparePlot(self):
        """Method to prepare the number of plots according to the number of sensors found"""
        self.fig.clear()

        axbuf = []
        linebuf = []

        # NumPlots = self.SensorsFound
        self.plot_sensors = []
        self.plot_totsamples = []
        self.sensorId = []

        # Find all the EMG channels and their sampling rates
        i = 0
        for sensors in range(len(self.sampleRates)):
            for channels in range(len(self.sampleRates[sensors])):
                if 'EMG' in self.sampleRates[sensors][channels]:
                    self.plot_sensors.append(self.sampleRates[sensors][channels][0])
                    self.plot_totsamples.append(0)
                    self.sensorId.append(i)
                i = i + 1

        num_plots = len(self.plot_sensors)
        self.timeSpan = numSample / max(self.plot_sensors)

        for i in range(num_plots):

            ax = self.fig.add_subplot(num_plots, 1, i + 1)
            ax.set_ylim(self.cur_ylim)
            self.cur_xlim[0] = -self.timeSpan
            self.cur_xlim[1] = 0
            ax.set_xlim(self.cur_xlim)
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            axbuf.append(ax)

            if i >= 1:
                outList.append([np.nan] * numSample)

            # xs = list(np.linspace(self.timeSpan,0, numSample))
            xs = [np.nan] * numSample
            line, = axbuf[i].plot(xs, outList[i], lw=2)
            linebuf.append(line,)
        plt.draw()
        self.axes = self.fig.axes

        self.ax = axbuf
        self.line = linebuf
        self.fig.canvas.mpl_connect('scroll_event',self.scrollCallback)
        self.fig.canvas.mpl_connect('button_press_event', self.onPress)
        self.fig.canvas.mpl_connect('button_release_event', self.onRelease)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onMotion)


    def onPress(self,event):
        if event.inaxes != event.inaxes: return
        if event.inaxes is None: return

        self.cur_xlim = event.inaxes.get_xlim()
        self.cur_ylim = event.inaxes.get_ylim()
        self.press = self.x0, self.y0, event.xdata, event.ydata
        self.x0, self.y0, self.xpress, self.ypress = self.press
        fig = event.inaxes.get_figure()
        fig.canvas.mpl_connect('button_press_event', self.onPress)


    def onRelease(self,event):
        self.press = None
        # event.inaxes.figure.canvas.draw()
        if event.inaxes is None: return
        fig = event.inaxes.get_figure()
        fig.canvas.mpl_connect('button_release_event', self.onRelease)


    def onMotion(self,event):
        """Callback for panning functionality, current implementation only allows for panning within current plot
        boundaries"""

        if self.press is None: return
        if event.inaxes != event.inaxes: return
        if event.xdata is None: return
        if event.ydata is None: return

        dx = event.xdata - self.xpress
        dy = event.ydata - self.ypress
        self.cur_xlim -= dx
        self.cur_ylim -= dy
        if self.cur_xlim[0]<self.cur_time-self.timeSpan:
            self.cur_xlim[0] = self.cur_time-self.timeSpan
        if self.cur_xlim[1]> self.cur_time:
            self.cur_xlim[1] = self.cur_time
        if (self.cur_ylim[0]<-yLim):
            self.cur_ylim[0] = -yLim
        if (self.cur_ylim[1]>yLim):
            self.cur_ylim[1] = yLim
        event.inaxes.set_xlim(self.cur_xlim)
        event.inaxes.set_ylim(self.cur_ylim)

        plt.draw()

        fig = event.inaxes.get_figure()
        fig.canvas.mpl_connect('motion_notify_event', self.onMotion)

    def scrollCallback(self,event):
        """Callback for zooming functionality. Current implementation: Zooms to max x and y set by boundaries"""

        if event.inaxes is None: return

        base_scale=2.0
        if event.button =='down':
            scale_factor = base_scale
        else:
            scale_factor = 1 / base_scale

        xdata = event.xdata  # get event x location
        ydata = event.ydata  # get event y location

        cur_xlim = event.inaxes.get_xlim()
        cur_ylim = event.inaxes.get_ylim()

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

        new_xMin = xdata - new_width * (1 - relx)
        new_xMax = xdata + new_width * (relx)

        new_yMin = ydata - new_height * (1 - rely)
        new_yMax = ydata + new_height * (rely)

        if (new_xMin< self.cur_time-self.timeSpan):
            new_xMin = self.cur_time-self.timeSpan
        if (new_xMax> self.cur_time):
            new_xMax = self.cur_time

        if (new_yMin<-yLim):
            new_yMin = -yLim
        if (new_yMax>yLim):
            new_yMax = yLim

        event.inaxes.set_xlim([new_xMin, new_xMax])
        event.inaxes.set_ylim([new_yMin, new_yMax])

        self.cur_xlim = [new_xMin, new_xMax]
        self.cur_ylim = [new_yMin, new_yMax]

        plt.draw()

        fig = event.inaxes.get_figure()
        fig.canvas.mpl_connect('scroll_event', self.scrollCallback)


    def start_callback(self):
        """Callback to start data streaming and sets up plot"""
        plt.clf()
        global outList

        self.pauseFlag = False

        outList = [[float(0)] * numSample]

        newTransform = TrigBase.createTransform("raw")

        index = List[Int32]()

        TrigBase.ClearSensorList()

        for i in range(self.SensorsFound):
            selectedSensor = TrigBase.getSensorObject(i)
            TrigBase.AddSensortoList(selectedSensor)
            index.Add(i)

        self.sampleRates = [ [] for i in range(self.SensorsFound)]


        TrigBase.StreamData(index,newTransform,2)
        collecting = True

        for i in range(self.SensorsFound):
            selectedSensor = TrigBase.getSensorObject(i)
            for channel in range(len(selectedSensor.TrignoChannels)):
                self.sampleRates[i].append((selectedSensor.TrignoChannels[channel].SampleRate,
                                           selectedSensor.TrignoChannels[channel].Name))

        self.PreparePlot()

        self.ani = animation.FuncAnimation(self.fig,
                                      self.animate,
                                      fargs=(outList,),
                                      interval=20, #ms
                                      blit=False)
        self.ani._start()


    def GetData(self):
        """Callback to get the data from the streaming sensor"""

        if not self.pauseFlag:
            dataReady = TrigBase.CheckDataQueue()
            if dataReady:
                DataOut = TrigBase.PollData()
                outArr = []
                if len(DataOut) > 0:  # Check for lost Packets
                    for j in range(len(DataOut)):
                        outBuf = DataOut[j]
                        outArr.append(np.asarray(outBuf))
                return outArr
        else:
            return None


    def animate(self, i, outList):
        """Callback event: Polls the base for new data, if there is new data, adds it to the plot"""

        self.update()
        # Collect the Data to be plotted from the base
        outArr = self.GetData()
        if outArr is not None:
            if len(outArr) > 0:  # Check for lost Packets
                outBuf = outArr
                # Append data to plot
                count = 0
                for k in range(len(outBuf)):
                    if k in self.sensorId:
                        self.plot_totsamples[count] += len(outBuf[k])

                        for j in range(len(outBuf[k])):
                            outList[count].insert(0,outBuf[k][j])
                            outList[count].pop()

                        # calculates the current time based on sample count and sets the time accordingly
                        self.cur_time = self.plot_totsamples[count] / self.plot_sensors[count]
                        self.ax[count].set_xlim(self.cur_time-self.timeSpan,self.cur_time)
                        self.line[count].set_ydata(outList[count])
                        self.line[count].set_xdata(list(np.linspace(self.cur_time,self.cur_time-self.timeSpan,numSample)))
                        count = count+1
        # Create the line to plot
        return self.line,


    def stop_callback(self):
        """Callback that stops data collection"""
        ret = TrigBase.StopData()
        try:
            self.ani._stop()
            self.pauseFlag = True
        except:
            return


    def enableSideBar(self):
        """Method that enables the sidebar buttons"""
        for child in self.sidebar.winfo_children():
            child["state"]="normal"
        self.update()


    def disableSideBar(self):
        """Method that disables the sidebar buttons"""
        for child in self.sidebar.winfo_children():
            child["state"]="disabled"
        self.update()

# THIS IS THE MAIN CODE THAT RUNS
def main():
    root = tk.Tk()
    root.geometry('800x750+0+0')
    app = Window(root)
    root.mainloop()

if __name__== "__main__":
    main()
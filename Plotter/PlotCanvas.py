"""
This is the constructor for users to create their own custom plot canvases

They can add axis, titles, grids, etc to their plot objects here

Should return a widget that they can just add into their gui by default

For now, just one plot per plot object
"""
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCharts import *
import Plotter.GenericPlot as gp
import sys

class PlotCanvas(QWidget):
    def __init__(self,plot_widget=None):
        QWidget.__init__(self)

        if plot_widget is None:
            plot = gp.GenericPlot()
            # #This should be passed in as a plot widget they created or automated
            plot_widget = QWidget()
            plot_widget.setLayout(QVBoxLayout())
            plot_widget.layout().addWidget(plot.native)

        self.plot_widget = plot_widget

        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignCenter)

        self.y_axis_label = QLabel(self)
        self.y_axis_label.setAlignment(Qt.AlignCenter)

        self.x_axis_label = QLabel(self)
        self.x_axis_label.setAlignment(Qt.AlignCenter)

        # Axis Labels
        self.y_axis = QLabel(self)
        self.y_axis.setAlignment(Qt.AlignCenter)

        self.x_axis = QLabel(self)
        self.x_axis.setAlignment(Qt.AlignCenter)

        #Create the vertical component
        self.VComp = QWidget(self)
        self.VGrid = QGridLayout()
        self.VGrid.setSpacing(0)
        self.VGrid.setMargin(0)

        self.VGrid.addWidget(self.title)
        self.VGrid.addWidget(self.plot_widget)
        # self.VSplitter.addWidget(self.x_axis) #Commenting this out for now until axis question can be solved
        # self.VGrid.addWidget(self.x_axis_label)
        self.VComp.setLayout(self.VGrid)

        #Add in the horizontal components
        self.HComp = QWidget(self)
        self.HGrid = QGridLayout()
        self.HGrid.setSpacing(0)
        self.HGrid.setMargin(0)
        # self.HGrid.addWidget(self.y_axis_label)
        # self.HSplitter.addWidget(self.y_axis) #Commenting this out for now until axis question can be solved
        self.HGrid.addWidget(self.VComp)
        self.HComp.setLayout(self.HGrid)
        
        

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.HComp)
        self.setLayout(layout)

    def set_title(self,title_string):
        self.title.setText(title_string)

    def set_y_label(self,title_string):
        self.y_axis_label.setText(title_string)

    def set_x_label(self,title_string):
        self.x_axis_label.setText(title_string)

## FIX THIS
# class Vertical_Label(QWidget):
#     def __init__(self,parent, text=None):
#         QWidget.__init__(self,parent=parent)
#         self.text = text
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setPen(Qt.black)
#         painter.translate(20,100)
#         painter.rotate(-90)
#         if self.text:
#             painter.drawText(0, 0, self.text)
#         painter.end()
#
#     def setText(self,text):
#         self.text = text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    PlotCanvas = PlotCanvas()
    PlotCanvas.set_title("Test Title")
    PlotCanvas.set_x_label("Test x Title")
    # PlotCanvas.set_y_label("Test y Title")
    PlotCanvas.show()
    sys.exit(app.exec_())








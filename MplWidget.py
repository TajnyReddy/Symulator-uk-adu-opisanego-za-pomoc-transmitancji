from matplotlib.backends.backend_qtagg import (NavigationToolbar2QT as NavigationToolbar,FigureCanvasQTAgg)
import matplotlib.pyplot as plt
from gui import *

#tworzenie "plotna" mpl
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(1, 1, figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)

#nadpisywanie QWidgetu przez MplWidget
class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)  # Inherit from QWidget
        self.canvas = MplCanvas()  # Create canvas object
        self.vbl = QVBoxLayout()  # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(NavigationToolbar(self.canvas, self))  # add a toolbar
        self.setLayout(self.vbl)

        self.resize(620, 285)  # resize needed to have a visible plot
        self.vbl.setSizeConstraint

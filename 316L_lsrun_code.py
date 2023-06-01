from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolBar, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QUrl, QDir
from PyQt5.QtWebEngineWidgets import QWebEngineView
from lasso.dyna import D3plot, ArrayType

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Add a button
        self.button = QPushButton('Load Simulation')
        self.button.clicked.connect(self.load_simulation)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.browser)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.showMaximized()

    def load_simulation(self):
        d3plot = D3plot("d3plot")
        print(d3plot)
        pstrain = d3plot.arrays[ArrayType.element_shell_bending_moment]
        pstrain = pstrain.mean(axis = 2)
       
        # Save the plot as a HTML file
        export_filepath = 'plot.html'
        d3plot.plot(3, field = pstrain[3], fringe_limits= (0, 0.6), export_filepath= export_filepath)
        self.browser.load(QUrl.fromLocalFile(QDir.current().absoluteFilePath(export_filepath)))

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
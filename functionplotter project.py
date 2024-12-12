import sys
import numpy as np
from sympy import sympify, lambdify, Symbol, sin, cos, tan, cot
from PySide6 import QtWidgets
from PySide6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.setWindowTitle("Function Plotter")
        self.layout = QtWidgets.QGridLayout(self._main)

        # Create Labels and Textboxes
        self.label1 = QtWidgets.QLabel(self._main)
        self.label1.setText("Enter the function equation:")
        self.label1.setFont(QFont('Arial', 13))

        self.textBox1 = QtWidgets.QLineEdit(self._main)
        self.textBox1.setFont(QFont('Arial', 13))
        self.textBox1.setToolTip("Equation must be a function of x.")

        self.label2 = QtWidgets.QLabel(self._main)
        self.label2.setText("Enter the minimum value:")
        self.label2.setFont(QFont('Arial', 13))

        self.textBox2 = QtWidgets.QLineEdit(self._main)
        self.textBox2.setFont(QFont('Arial', 13))

        self.label3 = QtWidgets.QLabel(self._main)
        self.label3.setText("Enter the maximum value:")
        self.label3.setFont(QFont('Arial', 13))

        self.textBox3 = QtWidgets.QLineEdit(self._main)
        self.textBox3.setFont(QFont('Arial', 13))
        
if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec()

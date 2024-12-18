import sys
import numpy as np
from sympy import sympify, lambdify, Symbol, sin, cos, tan, cot, E
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
        self.plot_type_label = QtWidgets.QLabel(self._main)
        self.plot_type_label.setText("Select Plot Type:")
        self.plot_type_label.setFont(QFont('Arial', 13))

        self.plot_type_dropdown = QtWidgets.QComboBox(self._main)
        self.plot_type_dropdown.addItems(["Continuous", "Discrete"])
        self.plot_type_dropdown.setFont(QFont('Arial', 13))
        self.plot_type_dropdown.currentIndexChanged.connect(self.toggle_plot_type)

        self.label1 = QtWidgets.QLabel(self._main)
        self.label1.setText("Enter the function equation:")
        self.label1.setFont(QFont('Arial', 13))

        self.textBox1 = QtWidgets.QLineEdit(self._main)
        self.textBox1.setFont(QFont('Arial', 13))
        self.textBox1.setToolTip("Equation must be a function of x or n. Supported operators: + - / * ^, trig functions, and e.")

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

        # Create button
        self.button = QtWidgets.QPushButton('Plot', self._main)
        self.button.setFont(QFont('Arial', 13))
        self.button.setToolTip('Press to plot')
        self.button.clicked.connect(self.on_click)

        # Create MessageBox for errors
        self.mbox = QtWidgets.QMessageBox()

        # Create Figure and Toolbar
        self.static_canvas = FigureCanvas(Figure(figsize=(8, 5)))
        self._static_ax = self.static_canvas.figure.subplots()
        self.toolbar = NavigationToolbar(self.static_canvas, self._main)

        # Add Widgets
        self.layout.addWidget(self.plot_type_label, 0, 0)
        self.layout.addWidget(self.plot_type_dropdown, 0, 1)
        self.layout.addWidget(self.label1, 1, 0)
        self.layout.addWidget(self.textBox1, 1, 1)
        self.layout.addWidget(self.label2, 2, 0)
        self.layout.addWidget(self.textBox2, 2, 1)
        self.layout.addWidget(self.label3, 3, 0)
        self.layout.addWidget(self.textBox3, 3, 1)
        self.layout.addWidget(self.button, 4, 0, 1, 2)
        self.layout.addWidget(self.static_canvas, 5, 0, 1, 2)
        self.layout.addWidget(self.toolbar, 6, 0, 1, 2)

    def toggle_plot_type(self):
        plot_type = self.plot_type_dropdown.currentText()
        if plot_type == "Continuous":
            self.label1.setText("Enter the function equation (in terms of x):")
        else:
            self.label1.setText("Enter the function equation (in terms of n):")

    def dialog(self, msg):
        self.mbox.setText(msg)
        self.mbox.setWindowTitle("Error")
        self.mbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.mbox.exec_()

    def on_click(self):
        plot_type = self.plot_type_dropdown.currentText()
        equation = self.textBox1.text()
        if not equation:
            self.dialog("Please enter a function equation.")
            return

        try:
            initial = int(self.textBox2.text())
            end = int(self.textBox3.text())
        except ValueError:
            self.dialog("Minimum and maximum values must be integers.")
            return

        if initial >= end:
            self.dialog("The minimum value must be less than the maximum value.")
            return

        self._static_ax.clear()

        if plot_type == "Continuous":
            t = np.linspace(initial, end, 500)
            expr = sympify(equation.replace('^', '**'), {'sin': sin, 'cos': cos, 'tan': tan, 'cot': cot, 'E': E})
            f = lambdify(Symbol('x'), expr, 'numpy')
            result = f(t)
            self._static_ax.plot(t, result, label=equation, color="blue")
        else:
            n = np.arange(initial, end + 1)
            expr = sympify(equation.replace('^', '**'), {'sin': sin, 'cos': cos, 'tan': tan, 'cot': cot, 'E': E})
            f = lambdify(Symbol('n'), expr, 'numpy')
            result = f(n)
            self._static_ax.stem(n, result, linefmt='blue', markerfmt='bo', basefmt="black")

        self._static_ax.axhline(0, color='black', linewidth=1)
        self._static_ax.axvline(0, color='black', linewidth=1)
        self._static_ax.set(title=f"{plot_type} Signal Plotting", xlabel="x" if plot_type == "Continuous" else "n", ylabel="f(x)" if plot_type == "Continuous" else "f(n)")
        self._static_ax.legend()
        self.static_canvas.figure.tight_layout()
        self.static_canvas.draw()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec()

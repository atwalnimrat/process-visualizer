from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QTimer

import sys

app = QApplication(sys.argv)
label = QLabel("Process Visualizer GUI Prototype")

label.show()
sys.exit(app.exec_())

from PyQt5.QtWidgets import QApplication, QLabel

import sys

app = QApplication(sys.argv)
label = QLabel("Process Visualizer GUI Prototype")

label.show()
sys.exit(app.exec_())

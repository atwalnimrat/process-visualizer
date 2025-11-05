from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QTimer

import sys

from cli.processes import system_stats, process_stats
from cli.format import generate_table

app = QApplication(sys.argv)

label = QLabel()
label.setText(generate_table(system_stats(), process_stats()))
label.setStyleSheet("font-size: 16px; padding: 10px;")
label.show()

def update_label():
    global label
    label.setText(generate_table(system_stats(), process_stats()))

timer = QTimer()
timer.timeout.connect(update_label())
timer.start(1000)

sys.exit(app.exec_())

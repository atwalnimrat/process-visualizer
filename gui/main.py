from PyQt5.QtWidgets import QApplication

import sys

from gui.ssv import StatsVisualizer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StatsVisualizer()
    window.show()
    sys.exit(app.exec_())

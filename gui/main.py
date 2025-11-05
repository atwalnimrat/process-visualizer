from PyQt5.QtWidgets import QApplication

import sys

from gui.pv import ProcessVisualizer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProcessVisualizer()
    window.show()
    sys.exit(app.exec_())

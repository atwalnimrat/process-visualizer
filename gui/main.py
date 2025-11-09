from PyQt5.QtWidgets import QApplication

import sys

from gui.bubbles import BubbleOverlay
from gui.ssv import StatsVisualizer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = BubbleOverlay()
    overlay.show()
    sys.exit(app.exec())

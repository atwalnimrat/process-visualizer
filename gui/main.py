from PyQt5.QtWidgets import QApplication

import sys

from gui.bubbles import BubbleOverlay
from gui.ssv import StatsVisualizer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    overlay = BubbleOverlay()
    stats_window = StatsVisualizer()

    overlay.set_stats_window(stats_window)

    overlay.show()
    sys.exit(app.exec())

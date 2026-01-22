from PyQt5.QtWidgets import QApplication

import sys

from gui.bubbles import BubbleOverlay
from gui.ssv import StatsVisualizer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    screen = QApplication.primaryScreen()
    size = screen.availableGeometry()
    dpi_scale = screen.logicalDotsPerInch() / 96            # 96 = baseline DPI


    overlay = BubbleOverlay(size, dpi_scale)
    stats_window = StatsVisualizer(size, dpi_scale)

    overlay.setWindowTitle("Process Visualizer")
    overlay.set_stats_window(stats_window)

    overlay.show()
    sys.exit(app.exec())

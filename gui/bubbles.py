from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor

import sys
import random

from cli.processes import process_stats

class Bubble:
    def __init__(self, name, cpu):
        self.name = name
        self.cpu = cpu
        self.x = random.randint(50, 450)
        self.y = random.randint(50, 450)
        self.dx = random.choice([-2, 2])
        self.dy = random.choice([-2, 2])
        self.radius = max(10, cpu * 3)           # scale size by CPU%

class BubbleOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(800, 500)
        self.move_to_bottom_right()
        
        self.bubbles = []
        self.update_processes()

        # Refresh processes 
        self.process_timer = QTimer(self)
        self.process_timer.timeout.connect(self.update_processes)
        self.process_timer.start(3000)      # every 3s

        # Animate bubbles
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.animate)
        self.anim_timer.start(16)       # 16ms (~60fps)

    def move_to_bottom_right(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.width() - 20
        y = screen.bottom() - self.height() - 20
        self.move(x, y)

    def update_processes(self):
        procs = process_stats()
        seen = set()
        self.bubbles = [Bubble(p['name'], p['cpu_percent'])for p in procs if not (p['name'] in seen or seen.add(p['name']))][:5]      # top 5

    def animate(self):
        for b in self.bubbles:
            b.x += b.dx
            b.y += b.dy
            if b.x - b.radius < 0 or b.x + b.radius > self.width():
                b.dx *= -1
            if b.y - b.radius < 0 or b.y + b.radius > self.height():
                b.dy *= -1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for b in self.bubbles:
            color = QColor(random.randint(100,255), random.randint(100,255), random.randint(100,255), 150)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(b.x, b.y), b.radius, b.radius)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = BubbleOverlay()
    overlay.show()
    sys.exit(app.exec())

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QFont

import sys
import random
import hashlib

from cli.processes import process_stats

class Bubble:
    def __init__(self, name, cpu, x=None, y=None):
        self.name = name
        self.cpu = cpu
        self.x = x if x is not None else random.randint(50, 450)
        self.y = y if y is not None else random.randint(50, 450)
        self.dx = random.choice([-2, 2])
        self.dy = random.choice([-2, 2])
        self.radius = max(10, cpu * 3)           # scale size by CPU%
        self.color = self.get_color_from_name(name)

    def get_color_from_name(self, name):
        hash_val = int(hashlib.md5(name.encode()).hexdigest(), 16)
        r = (hash_val & 0xFF0000) >> 16
        g = (hash_val & 0x00FF00) >> 8
        b = (hash_val & 0x0000FF)
        return QColor(r, g, b, 180)

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
        
        self.bubbles = {}
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
        current_names = self.bubbles.keys()
        seen = set()
        bubbles_now = [Bubble(p['name'], p['cpu_percent'])for p in procs if not (p['name'] in seen or seen.add(p['name']))][:5]      # top 5
        for b in bubbles_now:
            if b.name in current_names:
                bubble = self.bubbles[b.name]
                bubble.cpu = b.cpu
                bubble.radius = max(10, b.cpu * 3)
            else:
                self.bubbles[b.name] = b
        
        # Remove bubbles not in top 5
        for name in list(current_names):
            if name not in [x.name for x in bubbles_now]:
                del self.bubbles[name]

    def animate(self):
        for b in self.bubbles.values():
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
        
        font = QFont("Arial")
        painter.setFont(font)

        for bubble in self.bubbles.values():
            # Draw bubble
            painter.setBrush(bubble.color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(bubble.x, bubble.y), bubble.radius, bubble.radius)

            # Bubble name
            painter.setPen(Qt.white)

            text = bubble.name[:15]
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(text)
            text_height = fm.height()
            
            # Text font
            font.setPointSizeF(max(6, bubble.radius * 0.4))

            x = bubble.x - text_width / 2
            y = bubble.y + text_height / 4  

            painter.drawText(QPointF(x, y), text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = BubbleOverlay()
    overlay.show()
    sys.exit(app.exec())

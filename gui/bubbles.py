from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QFont

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
        self.radius = min(max(10, self.cpu * 3), 220)          # scale size by CPU%
        self.color = self.get_color_from_name(name)
        self.font = QFont("Arial")

    def get_color_from_name(self, name):
        hash_val = int(hashlib.md5(name.encode()).hexdigest(), 16)
        r = (hash_val & 0xFF0000) >> 16
        g = (hash_val & 0x00FF00) >> 8
        b = (hash_val & 0x0000FF)
        return QColor(r, g, b, 180)

class BubbleOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(800, 500)
        self.move_to_bottom_right()

        # Processes
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

        # Stats Window
        self.stats_window = None

        self.stats_button = QPushButton("Stats", self)
        self.stats_button.setFixedSize(60, 30)
        self.stats_button.move(10, 10)          # top-left corner
        self.stats_button.clicked.connect(self.toggle_stats)

        self.stats_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 80);
                border: none;
                border-radius: 5px;
                color: black;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 150);
            }
        """)

    def set_stats_window(self, stats_window):
        self.stats_window = stats_window

    def toggle_stats(self):
        if self.stats_window is not None:
            if self.stats_window.isVisible():
                self.stats_window.hide()
            else:
                self.stats_window.show()
                self.stats_window.raise_()

    def closeEvent(self, event):        
        event.ignore()      # hides
        self.hide()

    def move_to_bottom_right(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.width() - 20
        y = screen.bottom() - self.height() - 20
        self.move(x, y)

    def update_processes(self):
        procs = process_stats()
        current_names = self.bubbles.keys()

        # Update bubbles
        seen = set()
        bubbles_now = [Bubble(p['name'], p['cpu_percent'])for p in procs if not (p['name'] in seen or seen.add(p['name']))][:5]      # top 5
        for b in bubbles_now:
            if b.name in current_names:
                bubble = self.bubbles[b.name]
                bubble.cpu = b.cpu
                bubble.radius = min(max(10, b.cpu * 3), 220)
            else:
                self.bubbles[b.name] = b
        
        # Remove bubbles not in top 5
        for name in list(current_names):
            if name not in [x.name for x in bubbles_now]:
                del self.bubbles[name]

    def animate(self):
        for bubble in self.bubbles.values():
            bubble.x += bubble.dx
            bubble.y += bubble.dy

            # Bounce inside bounds
            if bubble.x - bubble.radius < 0:
                bubble.x = bubble.radius
                bubble.dx *= -1
            elif bubble.x + bubble.radius > self.width():
                bubble.x = self.width() - bubble.radius
                bubble.dx *= -1

            if bubble.y - bubble.radius < 0:
                bubble.y = bubble.radius
                bubble.dy *= -1
            elif bubble.y + bubble.radius > self.height():
                bubble.y = self.height() - bubble.radius
                bubble.dy *= -1

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for bubble in self.bubbles.values():
            painter.setFont(bubble.font)
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
            bubble.font.setPointSizeF(max(10, bubble.radius * 0.15))

            x = bubble.x - text_width / 2
            y = bubble.y + text_height / 4  

            painter.drawText(QPointF(x, y), text)

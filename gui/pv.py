from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer

import pyqtgraph as pg

from cli.processes import system_stats, process_stats

class ProcessVisualizer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Process Visualizer - Prototype")
        self.resize(800, 500)

        # Layouts
        layout = QVBoxLayout()
        stats_layout = QHBoxLayout()

        # Gauges (CPU, Memory, Temp)
        self.cpu_label = QLabel("CPU: 0%")
        self.mem_label = QLabel("Memory: 0%")
        self.temp_label = QLabel("Temp: 0°C")

        for lbl in (self.cpu_label, self.mem_label, self.temp_label):
            lbl.setStyleSheet("font-size: 18px; padding: 8px;")

        stats_layout.addWidget(self.cpu_label)
        stats_layout.addWidget(self.mem_label)
        stats_layout.addWidget(self.temp_label)

        # Realtime Graph
        self.plot = pg.PlotWidget(title="CPU Usage Over Time")
        self.plot.showGrid(x=True, y=True)
        self.data_x = list(range(60))
        self.data_y = [0]*60
        self.curve = self.plot.plot(self.data_x, self.data_y, pen=pg.mkPen(width=2))

        layout.addLayout(stats_layout)
        layout.addWidget(self.plot)

        self.setLayout(layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def update_data(self):
            cpu, cores, memory, temp = system_stats()

            self.cpu_label.setText(f"CPU: {cpu:.1f}%")
            self.mem_label.setText(f"Memory: {memory:.1f}%")
            self.temp_label.setText(f"Temp: {temp:.1f}°C")

            # Shift data for the chart
            self.data_y = self.data_y[1:] + [cpu]
            self.curve.setData(self.data_x, self.data_y)

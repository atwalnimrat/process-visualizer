from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer
from plyer import notification

import pyqtgraph as pg

from cli.processes import system_stats

class StatsVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self._force_close = False

        self.setWindowTitle("System Stats Visualizer")
        self.resize(1000, 1500)

        self.time = 60      #over a minute

        # Layouts
        layout = QVBoxLayout()
        stats_cpu_layout = QHBoxLayout()
        stats_memory_layout = QHBoxLayout()
        stats_temp_layout = QHBoxLayout()

        # Gauges (CPU, Memory, Temp)
        self.cpu_label = QLabel("CPU: 0%")
        self.mem_label = QLabel("Memory: 0%")
        self.temp_label = QLabel("Temp: 0°C")
        self.cores_label = QLabel("Cores: 0%")

        for lbl in (self.cpu_label, self.mem_label, self.temp_label, self.cores_label):
            lbl.setStyleSheet("font-size: 24px; padding: 5px;")

        # CPU stats
        stats_cpu_layout.addWidget(self.cpu_label)
        stats_cpu_layout.addWidget(self.cores_label)

        # Realtime CPU Graph
        self.cpu_plot = pg.PlotWidget(title="CPU Usage Over Time")
        self.cpu_plot.showGrid(x=True, y=True)
        self.data_cpu_x = list(range(self.time))
        self.data_cpu_y = [0]*self.time
        self.cpu_curve = self.cpu_plot.plot(self.data_cpu_x, self.data_cpu_y, pen=pg.mkPen(width=2, color='r'))

        layout.addLayout(stats_cpu_layout)
        layout.addWidget(self.cpu_plot)

        # Memory stats
        stats_memory_layout.addWidget(self.mem_label)

        # Realtime Memory Graph
        self.memory_plot = pg.PlotWidget(title="Memory Usage Over Time")
        self.memory_plot.showGrid(x=True, y=True)
        self.data_memory_x = list(range(self.time))
        self.data_memory_y = [0]*self.time
        self.memory_curve = self.memory_plot.plot(self.data_memory_x, self.data_memory_y, pen=pg.mkPen(width=2, color='g'))

        layout.addLayout(stats_memory_layout)
        layout.addWidget(self.memory_plot)

        # Temp stats
        stats_temp_layout.addWidget(self.temp_label)

        # Realtime Temp Graph
        self.temp_plot = pg.PlotWidget(title="Temperature Over Time")
        self.temp_plot.showGrid(x=True, y=True)
        self.data_temp_x = list(range(self.time))
        self.data_temp_y = [0]*self.time
        self.temp_curve = self.temp_plot.plot(self.data_temp_x, self.data_temp_y, pen=pg.mkPen(width=2))

        layout.addLayout(stats_temp_layout)
        layout.addWidget(self.temp_plot)

        self.setLayout(layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def closeEvent(self, event):
        if self._force_close:
            event.accept()
        else:
            event.ignore()          
            self.hide()
    
    def update_data(self):
        cpu, cores, memory, temp = system_stats()
        strcores = "% | ".join(map(str, cores))

        # Check for notification
        self.check_data(cpu, memory, temp)

        self.cpu_label.setText(f"<b><u>CPU:</u></b> {cpu:.1f}%")
        self.mem_label.setText(f"<b><u>Memory:</u></b> {memory:.1f}%")
        self.temp_label.setText(f"<b><u>Temp:</u></b> {temp:.1f}°C")
        self.cores_label.setText(f"<b><u>Cores:</u></b> {strcores}%")

        # Shift data for the charts
        self.data_cpu_y = self.data_cpu_y[1:] + [cpu]
        self.cpu_curve.setData(self.data_cpu_x, self.data_cpu_y)

        self.data_memory_y = self.data_memory_y[1:] + [memory]
        self.memory_curve.setData(self.data_memory_x, self.data_memory_y)

        self.data_temp_y = self.data_temp_y[1:] + [temp]
        self.temp_curve.setData(self.data_temp_x, self.data_temp_y)     

    def check_data(self, cpu, memory, temp):
        # THRESHOLDS
        CPU_USAGE_THRESHOLD = 80
        MEMORY_USAGE_THRESHOLD = 80
        CPU_TEMP_THRESHOLD = 100  

        # Flags
        alerts = {
            "cpu": False,
            "memory": False,
            "temp": False,
        }

        def notify(title, message):
            notification.notify(title=title, message=message, timeout=5)

        # CPU check
        if cpu > CPU_USAGE_THRESHOLD and not alerts["cpu"]:
            notify("Warning ⚠️: High CPU Usage", f"CPU usage at {cpu:.1f}%")
            alerts["cpu"] = True
        elif cpu <= CPU_USAGE_THRESHOLD:
            alerts["cpu"] = False

        # Memory check
        if memory > MEMORY_USAGE_THRESHOLD and not alerts["memory"]:
            notify("Warning ⚠️: High Memory Usage", f"Memory usage at {memory:.1f}%")
            alerts["memory"] = True
        elif memory <= MEMORY_USAGE_THRESHOLD:
            alerts["memory"] = False

        # Temperature check
        if temp > CPU_TEMP_THRESHOLD and not alerts["temp"]:
            notify("Warning ⚠️: High CPU Temperature", f"CPU temp at {temp:.1f}°C")
            alerts["temp"] = True
        elif temp <= CPU_TEMP_THRESHOLD:
            alerts["temp"] = False


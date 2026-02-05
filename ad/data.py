import psutil
import numpy as np

data = []

while True:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    net = psutil.net_io_counters()
    sent = net.bytes_sent / 1024
    recv = net.bytes_recv / 1024

    data.append([cpu, ram, sent, recv])

    print(data[-1])

    if len(data) >= 2000:  # ~30 mins
        break

np.save("normal_usage.npy", np.array(data))

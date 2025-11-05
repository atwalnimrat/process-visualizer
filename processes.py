import psutil

def system_stats():
    cpu = psutil.cpu_percent(percpu=False)
    cores = psutil.cpu_percent(percpu=True)
    memory = psutil.virtual_memory().percent
    cpu_temp = psutil.sensors_temperatures(fahrenheit=False)['thinkpad'][0].current
    return [cpu, cores,  memory, cpu_temp]

def process_stats():
    processes = []
    for pro in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(pro.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        processes.sort(key=lambda p: p['cpu_percent'], reverse=True)
    return processes[:15]

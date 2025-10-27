import psutil
from rich.table import Table

def system_stats():
    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory().percent
    cpu_temp = psutil.sensors_temperatures(fahrenheit=False)['thinkpad'][0].current
    return [cpu, memory, cpu_temp]

def process_stats():
    processes = []
    for pro in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(pro.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        processes.sort(key=lambda p: p['cpu_percent'], reverse=True)
    return processes[:15]

# For terminal output
def generate_table(sys_stats, processes):
    cpu, memory, cpu_temp = sys_stats
    table = Table(title=f"System Monitor \nCPU: {cpu:.2f}% | Memory: {memory:.2f}% | Temp: {cpu_temp}°C")
    
    table.add_column("PID", justify="right")
    table.add_column("Name", justify="left", no_wrap=True)
    table.add_column("CPU%", justify="right")
    table.add_column("Memory%", justify="right")

    for process in processes:
        table.add_row(str(process["pid"]), process["name"], f"{process['cpu_percent']:.2f}", f"{process['memory_percent']:.3f}")

    return table

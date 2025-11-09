from rich.table import Table

# For terminal output
def generate_table(sys_stats, processes):
    cpu, cores, memory, cpu_temp = sys_stats
    strcores = "%|".join(map(str, cores)) + "%"
    table = Table(title=f"System Monitor \nCPU: {cpu:.2f}% | Memory: {memory:.2f}% | Temp: {cpu_temp}°C \nCPU Cores: {strcores}")

    table.add_column("PID", justify="right")
    table.add_column("Name", justify="left", no_wrap=True)
    table.add_column("CPU%", justify="right")
    table.add_column("Memory%", justify="right")

    for process in processes:
        table.add_row(str(process["pid"]), process["name"], f"{process['cpu_percent']:.2f}", f"{process['memory_percent']:.3f}")

    return table
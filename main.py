import os
import time

from processes import system_stats, process_stats

while True:
    os.system('clear')

    total_cpu_usage_percent, total_memory_usage_percent, cpu_temp = system_stats()
    all_processes = process_stats()

    print(f"CPU usage: {total_cpu_usage_percent:.3f}%")
    print(f"Memory usage: {total_memory_usage_percent:.3f}% \n")
    print(f"CPU temperature: {cpu_temp}°C \n\n")

    print("\n pid \t name \t \t cpu \t memory")
    for process in all_processes:
        print(f"{process['pid']}\t{process['name'][:15]}\t\t{process['cpu_percent']}\t{process['memory_percent']:.3f}")
    
    time.sleep(1)

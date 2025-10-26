import psutil

from processes import sort_processes

total_cpu_usage_percent = psutil.cpu_percent()
total_memory_usage_percent = psutil.virtual_memory().percent

all_processes = list(psutil.process_iter())
running_processes, idle_processes, sleeping_processes, terminated_processes, other_processes = sort_processes(all_processes)

#all_processes.sort(reverse=True)

cpu_temp, gpu_temp = psutil.sensors_temperatures(fahrenheit=False)['thinkpad'][:2]

print(other_processes)

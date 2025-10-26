import psutil

from processes import sort_processes

total_cpu_usage_percent = psutil.cpu_percent(interval=1)
total_memory_usage_percent = psutil.virtual_memory().percent

all_processes = psutil.process_iter()
running_processes, idle_processes, sleeping_processes, stopped_processes, terminated_processes, other_processes = sort_processes(all_processes)

cpu_temp = psutil.sensors_temperatures(fahrenheit=False)['thinkpad'][0]

#print(running_processes[0].cpu_percent())
#print(running_processes[0].memory_percent())

print(total_cpu_usage_percent)

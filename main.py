import psutil

from processes import sort_processes

total_cpu_usage_percent = psutil.cpu_percent(interval=0.1)
total_memory_usage_percent = psutil.virtual_memory().percent

cpu_temp = psutil.sensors_temperatures(fahrenheit=False)['thinkpad'][0]

all_processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
#running_processes, idle_processes, sleeping_processes, 
# stopped_processes, terminated_processes, other_processes = sort_processes(all_processes)


#print(running_processes[0].cpu_percent())
#print(running_processes[0].memory_percent())


print(" pid","name", "\t cpu\t", "\tmemory")
for process in all_processes:
    memory = process.info['memory_percent']
    if memory > 0:
        cpu = process.cpu_percent(interval=0.1)
        if cpu > 0:
            print(process.pid, process.name(), cpu, memory)

print("\n\nCPU usage:", total_cpu_usage_percent, "%")
print("Memory usage:", total_memory_usage_percent, "%")
print("CPU temperature:", cpu_temp.current, "C")

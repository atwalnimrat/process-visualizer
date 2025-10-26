def sort_processes(all_processes):

    running_processes, idle_processes, sleeping_processes, stopped_processes, terminated_processes, other_processes = [], [], [], [], [], []
    
    for item in all_processes:
        if item.status() == 'running':
            running_processes.append(item)
        elif item.status() == 'idle':
            idle_processes.append(item)
        elif item.status() == 'sleeping':
            sleeping_processes.append(item)
        elif item.status() == 'stopped':
            stopped_processes.append(item)
        elif item.status() in ['terminated', 'dead']:
            terminated_processes.append((item.pid, item.name()))
        else:
            other_processes.append(item)

    return [running_processes, idle_processes, sleeping_processes, stopped_processes, terminated_processes, other_processes]

            
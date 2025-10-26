def sort_processes(all_processes):

    running_processes, idle_processes, sleeping_processes, terminated_processes, other_processes = [], [], [], [], []
    
    for item in all_processes:
        if item.status() == 'running':
            running_processes.append((item.pid, item.name()))
        elif item.status() == 'idle':
            idle_processes.append((item.pid, item.name()))
        elif item.status() == 'sleeping':
            sleeping_processes.append((item.pid, item.name()))
        elif item.status() == 'terminated':
            terminated_processes.append((item.pid, item.name()))
        else:
            other_processes.append((item.pid, item.name()))

    return [running_processes, idle_processes, sleeping_processes, terminated_processes, other_processes]

            
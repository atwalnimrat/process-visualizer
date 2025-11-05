import time
from rich.live import Live

from processes import system_stats, process_stats
from format import generate_table

with Live(generate_table(system_stats(), process_stats()), refresh_per_second=1, screen=True) as live:
    while True:
        time.sleep(1)
        live.update(generate_table(system_stats(), process_stats()))

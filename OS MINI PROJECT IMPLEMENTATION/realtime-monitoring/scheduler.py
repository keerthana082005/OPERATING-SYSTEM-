import psutil

def run_scheduler():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        processes.append(proc.info)
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)  # Highest CPU first
    return processes[:5]  # Show top 5 CPU-consuming processes

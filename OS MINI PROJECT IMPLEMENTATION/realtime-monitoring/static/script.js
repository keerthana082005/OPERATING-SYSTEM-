def get_processes():
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
        try:
            processes.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "cpu": proc.info['cpu_percent']  # Correctly fetch CPU usage
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes

@app.route('/run_scheduler')
def run_scheduler():
    processes = get_processes()
    return render_template("run_scheduler.html", processes=processes)
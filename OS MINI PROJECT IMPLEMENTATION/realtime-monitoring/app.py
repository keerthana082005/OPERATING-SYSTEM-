from flask import Flask, render_template, jsonify
import psutil
import random
import time

app = Flask(__name__)

# Home Page - Displays CPU usage graph
@app.route("/")
def home():
    return render_template("index.html")

# Load Processes - Categorizes processes into "App" and "Background"
@app.route("/load_processes")
def load_processes():
    apps, background = [], []
    for process in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
        try:
            if process.info['cpu_percent'] > 5:  # Assume apps use more CPU
                apps.append(process.info)
            else:
                background.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return render_template("load_processes.html", apps=apps, background=background)

# Run Scheduler - Implements First-Come, First-Serve (FCFS)
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
# Check Anomalies - Detects high CPU usage processes
@app.route("/check_anomalies")
def check_anomalies():
    anomalies = []
    for process in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
        try:
            if process.info['cpu_percent'] > 50:  # Threshold for high usage
                anomalies.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return render_template("check_anomalies.html", anomalies=anomalies)

@app.route("/cpu_usage")
def cpu_usage():
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
        try:
            processes.append({
                "name": proc.info['name'],
                "cpu": proc.info['cpu_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return jsonify({"cpu": psutil.cpu_percent(interval=1), "processes": processes})
if __name__ == "__main__":
    app.run(debug=True)

import random

def detect_anomalies():
    anomalies = []
    for _ in range(5):
        anomalies.append({
            "pid": random.randint(1000, 9999),
            "name": f"Process_{random.randint(1,10)}",
            "cpu": random.uniform(50, 99)  # Simulated high CPU usage
        })
    return anomalies

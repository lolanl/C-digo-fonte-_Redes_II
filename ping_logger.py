import csv
import os
from datetime import datetime

def log_rtt(dest, rtt):
    os.makedirs("resultados:", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"resultados:{timestamp}.csv"

    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Host Destino", "RTT (ms)"])

    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([dest, rtt])

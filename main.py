import multiprocessing
import subprocess
from app import app
from waitress import serve

def run_flask():
    serve(app, host="0.0.0.0", port=8080)

def run_monitor():
    subprocess.call(["python", "email_monitor.py"])

if __name__ == "__main__":
    flask_process = multiprocessing.Process(target=run_flask)
    monitor_process = multiprocessing.Process(target=run_monitor)

    flask_process.start()
    monitor_process.start()

    flask_process.join()
    monitor_process.join()

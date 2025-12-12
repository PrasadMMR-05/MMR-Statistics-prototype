import os
import sys
import subprocess
import webbrowser
import time
import threading

def main():
    # Ensure we are in the script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    print("--- 1. Running Data Ingestion ---")
    try:
        subprocess.run([sys.executable, "ingest.py"], check=True)
    except subprocess.CalledProcessError:
        print("Ingestion failed. Please check your MongoDB connection and settings.")
        return

    print("--- 2. Starting FastAPI Server ---")
    
    def open_swagger():
        # Wait a moment for the server to start
        time.sleep(2)
        print("Opening Swagger UI...")
        webbrowser.open("http://127.0.0.1:8000/docs")

    threading.Thread(target=open_swagger, daemon=True).start()

    subprocess.run([sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"])

if __name__ == "__main__":
    main()
import subprocess
import threading

def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py"])

def run_fastapi():
    subprocess.run(["uvicorn", "api:app", "--reload"])

if __name__ == "__main__":
    t1 = threading.Thread(target=run_fastapi)
    t2 = threading.Thread(target=run_streamlit)
    t1.start()
    t2.start()
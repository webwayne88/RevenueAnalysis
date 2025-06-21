import subprocess
import atexit
import signal
import sys
import shutil
import os


BACKEND_PATH = "backend/api.py"
FRONTEND_PATH = "frontend/app.py"

def cleanup_pycache():
    """Рекурсивно удаляет все __pycache__ директории в проекте."""
    print("Очистка __pycache__...")
    for root, dirs, files in os.walk(os.getcwd()):  
        for dir_name in dirs:
            if dir_name == "__pycache__":
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"Удалено: {dir_path}")
                except Exception as e:
                    print(f"Ошибка при удалении {dir_path}: {e}")


def terminate_processes():
    """Завершает все запущенные процессы (FastAPI и Streamlit)."""
    print("Завершение процессов...")
    if 'fastapi_process' in globals() and fastapi_process.poll() is None:
        fastapi_process.terminate()
    if 'streamlit_process' in globals() and streamlit_process.poll() is None:
        streamlit_process.terminate()


def exit_handler():
    """Вызывается при завершении программы (нормальном или по Ctrl+C)."""
    terminate_processes()
    cleanup_pycache()


def signal_handler(sig, frame):
    """Обрабатывает Ctrl+C и другие сигналы завершения."""
    print("\nПолучен сигнал прерывания, завершение работы...")
    exit_handler()
    sys.exit(0)


def start_fastapi():
    """Запускает FastAPI с autoreload."""
    return subprocess.Popen(["uvicorn", "api:app", "--reload", "--app-dir", "backend"])


def start_streamlit():
    """Запускает Streamlit."""
    return subprocess.Popen(["streamlit", "run", FRONTEND_PATH])


atexit.register(exit_handler)
signal.signal(signal.SIGINT, signal_handler)  
signal.signal(signal.SIGTERM, signal_handler)  

print("Запуск FastAPI...")
fastapi_process = start_fastapi()

print("Запуск Streamlit...")
streamlit_process = start_streamlit()

print("Серверы запущены. Для выхода нажмите Ctrl+C")


fastapi_process.wait()
streamlit_process.wait()
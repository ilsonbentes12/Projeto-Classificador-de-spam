"""Inicia a API e a pagina Streamlit."""
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent
PYTHON = Path(sys.executable)


def main() -> None:
    load_dotenv(ROOT / ".env")

    api = subprocess.Popen(
        [
            str(PYTHON),
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            os.getenv("API_HOST", "127.0.0.1"),
            "--port",
            os.getenv("API_PORT", "8000"),
        ],
        cwd=ROOT,
    )

    page = subprocess.Popen(
        [
            str(PYTHON),
            "-m",
            "streamlit",
            "run",
            str(ROOT / "app" / "page.py"),
            "--server.headless",
            "true",
        ],
        cwd=ROOT,
        env={**os.environ, "API_URL": os.getenv("API_URL", "http://127.0.0.1:8000")},
    )

    try:
        api.wait()
        page.wait()
    except KeyboardInterrupt:
        print("\nEncerrando a API e a pagina...")
    finally:
        for process in (page, api):
            if process.poll() is None:
                process.terminate()
        for process in (page, api):
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()


if __name__ == "__main__":
    main()

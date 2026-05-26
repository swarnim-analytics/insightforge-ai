import os
import shutil
import subprocess
import requests
from datetime import datetime

BOT_TOKEN = "8223599519:AAEoydidjo7GgjG3nq752uXDwbisAumIigg"
CHAT_ID = "1352120330"

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def get_disk_usage():

    total, used, free = shutil.disk_usage("/")

    return {
        "total": round(total / (1024**3), 2),
        "used": round(used / (1024**3), 2),
        "free": round(free / (1024**3), 2),
    }


def get_ram_usage():

    result = subprocess.check_output(
        "free -h",
        shell=True
    ).decode()

    return result


def get_uptime():

    uptime = subprocess.check_output(
        "uptime -p",
        shell=True
    ).decode().strip()

    return uptime


def get_docker_status():

    docker_ps = subprocess.check_output(
        "docker ps --format '{{.Names}} - {{.Status}}'",
        shell=True
    ).decode()

    return docker_ps


def build_report():

    disk = get_disk_usage()

    report = f"""
🖥️ Home Server Status Report
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📦 Storage
Total: {disk['total']} GB
Used: {disk['used']} GB
Free: {disk['free']} GB

🧠 RAM
{get_ram_usage()}

⏳ Uptime
{get_uptime()}

🐳 Docker Containers
{get_docker_status()}
"""

    return report


def send_telegram_message(message):

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(
        TELEGRAM_URL,
        json=payload
    )

    return response.json()


if __name__ == "__main__":

    report = build_report()

    result = send_telegram_message(report)

    print(result)
import shutil
import subprocess
import socket
from datetime import datetime
import sys
import os

sys.path.append(
    "/server/projects/insightforge-ai"
)
from app.services.market.market_monitor import analyze_stock
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = "8223599519:AAEoydidjo7GgjG3nq752uXDwbisAumIigg"


# -------------------------
# SYSTEM INFORMATION
# -------------------------

def get_disk_usage():

    total, used, free = shutil.disk_usage("/")

    used_percent = round((used / total) * 100, 2)

    return f"""
📦 STORAGE

Total: {round(total / (1024**3), 2)} GB
Used: {round(used / (1024**3), 2)} GB
Free: {round(free / (1024**3), 2)} GB
Usage: {used_percent}%
"""


def get_ram_usage():

    ram = subprocess.check_output(
        "free -h",
        shell=True
    ).decode()

    return f"""
🧠 RAM USAGE

{ram}
"""


def get_uptime():

    uptime = subprocess.check_output(
        "uptime -p",
        shell=True
    ).decode().strip()

    return f"""
⏳ UPTIME

{uptime}
"""


def get_ip():

    ip = subprocess.check_output(
        "hostname -I",
        shell=True
    ).decode().strip()

    return f"""
🌐 NETWORK

IP Address:
{ip}
"""


# -------------------------
# TEMPERATURE
# -------------------------

def get_temperature():

    try:

        temp = subprocess.check_output(
            "sensors",
            shell=True
        ).decode()

        return f"""
🌡️ TEMPERATURE

{temp[:1000]}
"""

    except Exception:

        return """
🌡️ TEMPERATURE

lm-sensors not installed.
"""


# -------------------------
# DOCKER MONITORING
# -------------------------

def get_docker_status():

    try:

        running = subprocess.check_output(
            "docker ps --format '{{.Names}} - {{.Status}}'",
            shell=True
        ).decode()

        stopped = subprocess.check_output(
            "docker ps -a --filter status=exited --format '{{.Names}} - STOPPED'",
            shell=True
        ).decode()

        restarting = subprocess.check_output(
            "docker ps -a --filter status=restarting --format '{{.Names}} - RESTARTING'",
            shell=True
        ).decode()

        result = "🐳 DOCKER STATUS\n\n"

        if running.strip():
            result += "✅ RUNNING:\n"
            result += running + "\n"

        if stopped.strip():
            result += "\n❌ STOPPED:\n"
            result += stopped + "\n"

        if restarting.strip():
            result += "\n⚠️ RESTARTING:\n"
            result += restarting + "\n"

        return result

    except Exception as e:

        return f"Docker Error: {str(e)}"


# -------------------------
# NEXTCLOUD
# -------------------------

def get_nextcloud_status():

    try:

        nextcloud = subprocess.check_output(
            "docker ps --filter name=nextcloud",
            shell=True
        ).decode()

        if nextcloud.strip():

            return """
☁️ NEXTCLOUD

✅ Nextcloud container is running
"""

        return """
☁️ NEXTCLOUD

❌ Nextcloud container not running
"""

    except Exception as e:

        return f"Nextcloud Error: {str(e)}"


# -------------------------
# OLLAMA
# -------------------------

def get_ollama_status():

    try:

        ollama = subprocess.check_output(
            "docker ps --filter name=ollama",
            shell=True
        ).decode()

        if ollama.strip():

            return """
🤖 OLLAMA

✅ Ollama AI service running
"""

        return """
🤖 OLLAMA

❌ Ollama service offline
"""

    except Exception as e:

        return f"Ollama Error: {str(e)}"


# -------------------------
# HEALTH SUMMARY
# -------------------------

def get_health_summary():

    return f"""
🖥️ HOME SERVER HEALTH

📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ Server reachable
✅ Monitoring active
✅ Telegram bot online

{get_disk_usage()}

{get_uptime()}

{get_nextcloud_status()}

{get_ollama_status()}
"""


# -------------------------
# TELEGRAM COMMANDS
# -------------------------

async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = f"""
🖥️ FULL SERVER STATUS

{get_disk_usage()}

{get_ram_usage()}

{get_uptime()}

{get_ip()}

{get_temperature()}

{get_docker_status()}
"""

    await update.message.reply_text(message[:4000])


async def health(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        get_health_summary()
    )


async def storage(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        get_disk_usage()
    )


async def docker(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        get_docker_status()
    )


async def nextcloud(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        get_nextcloud_status()
    )


async def ollama(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        get_ollama_status()
    )


async def uptime(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        get_uptime()
    )


async def temperature(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        get_temperature()
    )


# -------------------------
# MAIN BOT
# -------------------------
async def stock(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        ticker = context.args[0]

        if not ticker.endswith(".NS"):
            ticker += ".NS"

        result = analyze_stock(ticker)

        await update.message.reply_text(result)

    except Exception as e:

        await update.message.reply_text(
            f"Error: {str(e)}"
        )

def main():

    app = ApplicationBuilder().token(
        BOT_TOKEN
    ).build()

    app.add_handler(
        CommandHandler("status", status)
    )

    app.add_handler(
        CommandHandler("health", health)
    )

    app.add_handler(
        CommandHandler("storage", storage)
    )

    app.add_handler(
        CommandHandler("docker", docker)
    )

    app.add_handler(
        CommandHandler("nextcloud", nextcloud)
    )

    app.add_handler(
        CommandHandler("ollama", ollama)
    )

    app.add_handler(
        CommandHandler("uptime", uptime)
    )

    app.add_handler(
        CommandHandler("temperature", temperature)
    )
    app.add_handler(
    CommandHandler("stock", stock)
    )

    print("🚀 Telegram Monitoring Bot Started")

    app.run_polling()


if __name__ == "__main__":

    main()
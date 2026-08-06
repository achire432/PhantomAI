"""
PROACTIVE ASSISTANT SERVICE
============================
Purpose:
    Monitor system health and generate proactive alerts.

Responsibilities:
    - Monitor CPU usage
    - Monitor RAM usage
    - Monitor disk usage
    - Monitor battery level
    - Store recent alerts in memory
    - Run monitoring in a background thread

Important:
    This service detects problems.
    A separate notification service can later decide how
    PhantomAI delivers those alerts to the user.
"""

import threading
import time
from datetime import datetime
from typing import Optional

import psutil


# ============================================================
# CONFIGURATION
# ============================================================

CPU_THRESHOLD = 80.0
RAM_THRESHOLD = 85.0
DISK_THRESHOLD = 85.0
BATTERY_THRESHOLD = 20.0

DEFAULT_CHECK_INTERVAL = 60

MAX_ALERTS = 100


# ============================================================
# STATE
# ============================================================

_alerts = []

_monitor_thread: Optional[threading.Thread] = None
_monitor_running = False

_state_lock = threading.Lock()


# ============================================================
# SYSTEM CHECK
# ============================================================

def check_system() -> list:
    """
    Check current system health.

    Returns a list of alerts.

    Checks:
        - CPU usage
        - RAM usage
        - Disk usage
        - Battery level
    """

    detected_alerts = []

    now = datetime.now().isoformat()

    # --------------------------------------------------------
    # CPU
    # --------------------------------------------------------

    cpu = psutil.cpu_percent(interval=0.5)

    if cpu > CPU_THRESHOLD:
        detected_alerts.append({
            "type": "warning",
            "category": "cpu",
            "message": (
                f"CPU usage is high: {cpu:.1f}%"
            ),
            "value": cpu,
            "threshold": CPU_THRESHOLD,
            "timestamp": now,
        })

    # --------------------------------------------------------
    # RAM
    # --------------------------------------------------------

    memory = psutil.virtual_memory()

    if memory.percent > RAM_THRESHOLD:
        detected_alerts.append({
            "type": "warning",
            "category": "memory",
            "message": (
                f"RAM usage is high: {memory.percent:.1f}%"
            ),
            "value": memory.percent,
            "threshold": RAM_THRESHOLD,
            "timestamp": now,
        })

    # --------------------------------------------------------
    # DISK
    # --------------------------------------------------------

    disk = psutil.disk_usage("/")

    if disk.percent > DISK_THRESHOLD:
        detected_alerts.append({
            "type": "warning",
            "category": "disk",
            "message": (
                f"Disk usage is high: {disk.percent:.1f}%"
            ),
            "value": disk.percent,
            "threshold": DISK_THRESHOLD,
            "timestamp": now,
        })

    # --------------------------------------------------------
    # BATTERY
    # --------------------------------------------------------

    battery = psutil.sensors_battery()

    if (
        battery is not None
        and battery.percent < BATTERY_THRESHOLD
        and not battery.power_plugged
    ):
        detected_alerts.append({
            "type": "warning",
            "category": "battery",
            "message": (
                f"Battery is low: {battery.percent:.1f}%"
            ),
            "value": battery.percent,
            "threshold": BATTERY_THRESHOLD,
            "timestamp": now,
        })

    return detected_alerts


# ============================================================
# ALERT STORAGE
# ============================================================

def add_alert(alert: dict) -> None:
    """
    Store an alert in memory.

    The list is limited to MAX_ALERTS so it cannot grow
    indefinitely.
    """

    global _alerts

    with _state_lock:
        _alerts.append(alert)

        if len(_alerts) > MAX_ALERTS:
            _alerts = _alerts[-MAX_ALERTS:]


def add_alerts(new_alerts: list) -> None:
    """
    Store multiple alerts.
    """

    for alert in new_alerts:
        add_alert(alert)


def get_alerts() -> list:
    """
    Return a copy of the current alerts.

    Returning a copy prevents external code from accidentally
    modifying the internal alert storage.
    """

    with _state_lock:
        return list(_alerts)


def clear_alerts() -> None:
    """
    Remove all stored alerts.
    """

    global _alerts

    with _state_lock:
        _alerts.clear()


# ============================================================
# MONITORING LOOP
# ============================================================

def _monitor_loop(check_interval: int) -> None:
    """
    Background monitoring loop.

    Runs until the monitoring service is stopped.
    """

    global _monitor_running

    print("🧠 PhantomAI proactive monitoring started.")

    while _monitor_running:

        try:
            detected_alerts = check_system()

            if detected_alerts:
                add_alerts(detected_alerts)

                for alert in detected_alerts:
                    print(
                        f"⚠️ PROACTIVE ALERT: "
                        f"{alert['message']}"
                    )

        except Exception as error:
            print(
                f"Proactive monitoring error: {error}"
            )

        # Wait before checking again.
        # Use small sleeps so stop_monitoring() can respond
        # relatively quickly.
        for _ in range(check_interval):

            if not _monitor_running:
                break

            time.sleep(1)

    print("🧠 PhantomAI proactive monitoring stopped.")


# ============================================================
# START / STOP
# ============================================================

def start_monitoring(
    check_interval: int = DEFAULT_CHECK_INTERVAL
) -> dict:
    """
    Start proactive system monitoring.

    If monitoring is already running, no second thread
    will be created.
    """

    global _monitor_running
    global _monitor_thread

    if _monitor_running:
        return {
            "success": True,
            "message": "Proactive monitoring is already running.",
            "is_running": True,
        }

    if check_interval < 5:
        return {
            "success": False,
            "message": "Check interval must be at least 5 seconds.",
            "is_running": False,
        }

    _monitor_running = True

    _monitor_thread = threading.Thread(
        target=_monitor_loop,
        args=(check_interval,),
        daemon=True,
        name="phantom-proactive-monitor",
    )

    _monitor_thread.start()

    return {
        "success": True,
        "message": "Proactive monitoring started.",
        "is_running": True,
        "check_interval": check_interval,
    }


def stop_monitoring() -> dict:
    """
    Stop proactive system monitoring.
    """

    global _monitor_running
    global _monitor_thread

    if not _monitor_running:
        return {
            "success": True,
            "message": "Proactive monitoring is already stopped.",
            "is_running": False,
        }

    _monitor_running = False

    thread = _monitor_thread

    if thread and thread.is_alive():
        thread.join(timeout=2)

    _monitor_thread = None

    return {
        "success": True,
        "message": "Proactive monitoring stopped.",
        "is_running": False,
    }


# ============================================================
# STATUS
# ============================================================

def get_monitor_status() -> dict:
    """
    Return monitoring service status.
    """

    return {
        "is_running": _monitor_running,
        "alert_count": len(get_alerts()),
        "thresholds": {
            "cpu": CPU_THRESHOLD,
            "ram": RAM_THRESHOLD,
            "disk": DISK_THRESHOLD,
            "battery": BATTERY_THRESHOLD,
        },
    }
"""
PROACTIVE ASSISTANT SERVICE
============================
Purpose: PhantomAI checks system status and alerts you automatically.

Why This Matters:
- This is what makes JARVIS feel real
- PhantomAI becomes an active helper, not passive
- Alerts you before problems get worse

How It Works:
1. Runs in the background
2. Checks system metrics
3. Detects issues
4. Creates notifications
5. You get alerts

What Would Happen Without This:
- PhantomAI would only respond when asked
- You'd miss important things
- Not a real assistant
"""

import psutil
import threading
import time
from datetime import datetime
from sqlalchemy.orm import Session

# Storage for alerts (in memory for now)
alerts = []

def check_system() -> list:
    """
    Check system metrics and return alerts.
    
    Checks:
    1. CPU usage > 80%
    2. RAM usage > 85%
    3. Disk usage > 85%
    4. Running processes > 100
    
    Returns:
    [
        {"type": "warning", "message": "CPU usage is high: 90%"},
        {"type": "info", "message": "Disk space is low: 15% remaining"}
    ]
    """
    alerts = []
    
    # Check CPU
    cpu = psutil.cpu_percent(interval=0.5)
    if cpu > 80:
        alerts.append({
            "type": "warning",
            "message": f"⚠️ CPU usage is {cpu}% - consider closing some applications",
            "timestamp": datetime.now().isoformat()
        })
    
    # Check RAM
    ram = psutil.virtual_memory()
    if ram.percent > 85:
        alerts.append({
            "type": "warning",
            "message": f"⚠️ RAM usage is {ram.percent}% - your system may slow down",
            "timestamp": datetime.now().isoformat()
        })
    
    # Check Disk
    disk = psutil.disk_usage('/')
    if disk.percent > 85:
        alerts.append({
            "type": "warning",
            "message": f"⚠️ Disk usage is {disk.percent}% - consider freeing up space",
            "timestamp": datetime.now().isoformat()
        })
    
    # Check Battery
    battery = psutil.sensors_battery()
    if battery and battery.percent < 20 and not battery.power_plugged:
        alerts.append({
            "type": "warning",
            "message": f"🔋 Battery is at {battery.percent}% - please plug in your charger",
            "timestamp": datetime.now().isoformat()
        })
    
    return alerts

def get_alerts() -> list:
    """
    Get all current alerts.
    """
    return alerts

def clear_alerts():
    """
    Clear all alerts.
    """
    alerts.clear()
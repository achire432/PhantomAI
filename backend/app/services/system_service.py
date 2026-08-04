"""
SYSTEM SERVICE
===============
Purpose: Provide system information.
"""

import psutil
import platform

def get_system_info() -> dict:
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_cores = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        battery = psutil.sensors_battery()
        
        return {
            "cpu": {
                "percent": cpu_percent,
                "cores": cpu_cores,
                "frequency": cpu_freq.current if cpu_freq else None
            },
            "memory": {
                "total": mem.total,
                "available": mem.available,
                "percent": mem.percent
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent
            },
            "battery": {
                "percent": battery.percent if battery else None,
                "charging": battery.power_plugged if battery else None
            },
            "os": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine()
            }
        }
    except Exception as e:
        return {"error": str(e), "success": False}
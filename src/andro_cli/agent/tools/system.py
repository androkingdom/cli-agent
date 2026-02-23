"""System diagnostic tools for the agent"""
import platform
import os
import subprocess
from typing import Any


def get_system_info() -> dict[str, Any]:
    """Get basic system information."""
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "hostname": platform.node(),
        "python_version": platform.python_version(),
    }


def check_disk() -> dict[str, Any]:
    """Check disk space usage."""
    if platform.system() == "Windows":
        try:
            result = subprocess.run(
                ["wmic", "logicaldisk", "get", "size,freespace,caption"],
                capture_output=True,
                text=True,
            )
            return {"output": result.stdout}
        except Exception as e:
            return {"error": str(e)}
    else:
        try:
            result = subprocess.run(
                ["df", "-h"],
                capture_output=True,
                text=True,
            )
            return {"output": result.stdout}
        except Exception as e:
            return {"error": str(e)}


def check_processes() -> dict[str, Any]:
    """List running processes."""
    if platform.system() == "Windows":
        try:
            result = subprocess.run(
                ["tasklist", "/fo", "table"],
                capture_output=True,
                text=True,
            )
            return {"output": result.stdout}
        except Exception as e:
            return {"error": str(e)}
    else:
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True,
            )
            return {"output": result.stdout}
        except Exception as e:
            return {"error": str(e)}


def check_network() -> dict[str, Any]:
    """Check network connectivity."""
    results = {}
    
    # Check internet connectivity
    if platform.system() == "Windows":
        ping_target = "8.8.8.8"
    else:
        ping_target = "8.8.8.8"
    
    try:
        result = subprocess.run(
            ["ping", "-n", "1", ping_target],
            capture_output=True,
            text=True,
            timeout=5,
        )
        results["ping"] = "OK" if result.returncode == 0 else "Failed"
    except Exception as e:
        results["ping"] = f"Error: {e}"
    
    # Get network interfaces
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["ipconfig"],
                capture_output=True,
                text=True,
            )
            results["interfaces"] = result.stdout
        else:
            result = subprocess.run(
                ["ip", "addr"],
                capture_output=True,
                text=True,
            )
            results["interfaces"] = result.stdout
    except Exception as e:
        results["interfaces"] = f"Error: {e}"
    
    return results

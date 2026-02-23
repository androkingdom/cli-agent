"""Tools for the agent - exports all available tools"""
from .system import (
    get_system_info,
    check_disk,
    check_processes,
    check_network,
)

from .network import (
    ping,
    check_dns,
    get_local_ip,
    check_port,
    traceroute,
)


def run_command(command: str) -> dict:
    """Execute a shell command (use with caution!)."""
    import subprocess
    import platform
    
    try:
        # Determine shell based on OS
        if platform.system() == "Windows":
            shell = True
        else:
            shell = True
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=shell,
            timeout=60,
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}


# Export all tools in a dictionary for easy access
AVAILABLE_TOOLS = {
    # System tools
    "get_system_info": get_system_info,
    "check_disk": check_disk,
    "check_processes": check_processes,
    "check_network": check_network,
    # Network tools
    "ping": ping,
    "check_dns": check_dns,
    "get_local_ip": get_local_ip,
    "check_port": check_port,
    "traceroute": traceroute,
    # Command execution
    "run_command": run_command,
}


__all__ = [
    # System
    "get_system_info",
    "check_disk", 
    "check_processes",
    "check_network",
    # Network
    "ping",
    "check_dns",
    "get_local_ip",
    "check_port",
    "traceroute",
    # Command
    "run_command",
    # Export
    "AVAILABLE_TOOLS",
]

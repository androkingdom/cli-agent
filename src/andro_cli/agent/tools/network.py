"""Network diagnostic tools for the agent"""
import socket
import subprocess
import platform
from typing import Any


def ping(host: str = "8.8.8.8", count: int = 1) -> dict[str, Any]:
    """Ping a host to check connectivity."""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["ping", "-n", str(count), host],
                capture_output=True,
                text=True,
                timeout=10,
            )
        else:
            result = subprocess.run(
                ["ping", "-c", str(count), host],
                capture_output=True,
                text=True,
                timeout=10,
            )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "host": host,
        }
    except Exception as e:
        return {"error": str(e)}


def check_dns(domain: str = "google.com") -> dict[str, Any]:
    """Check DNS resolution for a domain."""
    try:
        ip = socket.gethostbyname(domain)
        return {"domain": domain, "ip": ip, "success": True}
    except socket.gaierror as e:
        return {"domain": domain, "error": str(e), "success": False}


def get_local_ip() -> dict[str, Any]:
    """Get the local IP address."""
    try:
        # Create a socket to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return {"ip": local_ip, "success": True}
    except Exception as e:
        return {"error": str(e)}


def check_port(host: str, port: int) -> dict[str, Any]:
    """Check if a port is open on a host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        
        return {
            "host": host,
            "port": port,
            "open": result == 0,
        }
    except Exception as e:
        return {"error": str(e)}


def traceroute(host: str = "google.com") -> dict[str, Any]:
    """Perform a traceroute to a host."""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["tracert", host],
                capture_output=True,
                text=True,
                timeout=30,
            )
        else:
            result = subprocess.run(
                ["traceroute", host],
                capture_output=True,
                text=True,
                timeout=30,
            )
        
        return {
            "host": host,
            "output": result.stdout,
            "success": result.returncode == 0,
        }
    except Exception as e:
        return {"error": str(e)}

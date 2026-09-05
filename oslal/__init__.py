import ctypes
import os
import socket
from sys import platform

if not platform.startswith("linux"):
    raise OSError("OS-LAL requires Linux network kernel features.")

_lib_dir = os.path.dirname(__file__)
_lib_path = None

for file in os.listdir(_lib_dir):
    if file.startswith("_oslal") and file.endswith(".so"):
        _lib_path = os.path.join(_lib_dir, file)
        break

if _lib_path:
    _lib = ctypes.CDLL(_lib_path)
else:
    _lib = None

class OslalPolicy(ctypes.Structure):
    _fields_ = [
        ("priority", ctypes.c_double),
        ("req_bandwidth_mbps", ctypes.c_double),
        ("max_latency_ms", ctypes.c_double),
    ]

if _lib:
    _lib.oslal_init.restype = ctypes.c_int
    _lib.oslal_bind_socket.argtypes = [ctypes.c_int, OslalPolicy]
    _lib.oslal_bind_socket.restype = ctypes.c_int

def init():
    if not _lib:
        raise RuntimeError("OS-LAL C extension binary missing.")
    return _lib.oslal_init()

def bind_socket(sock: socket.socket, priority: float, req_bandwidth: float, max_latency: float) -> int:
    if not _lib:
        raise RuntimeError("OS-LAL C extension binary missing.")
    
    policy = OslalPolicy(priority, req_bandwidth, max_latency)
    return _lib.oslal_bind_socket(sock.fileno(), policy)

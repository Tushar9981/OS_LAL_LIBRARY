import socket
import oslal

# Initialize scheduler core
oslal.init()

# Create a network socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket according to process policy constraints:
# Priority = 10.0, Required Bandwidth = 20.0 Mbps, Max Allowable Latency = 12.0 ms
status = oslal.bind_socket(
    sock=sock, priority=10.0, req_bandwidth=20.0, max_latency=12.0
)

if status == 0:
    print("Socket bound to optimal interface.")
else:
    print("Binding failed or insufficient permissions.")

sock.close()
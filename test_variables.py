import socket
import oslal

oslal.init()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Pass live dynamic metrics for testing
dynamic_ifaces = [
    {"name": "eth0", "capacity_mbps": 100.0, "latency_ms": 5.0, "drop_rate": 0.001},
    {"name": "wlan0", "capacity_mbps": 300.0, "latency_ms": 25.0, "drop_rate": 0.02}
]

# Weights tuple: (W_p, W_l, W_b, W_d)
# Prioritize bandwidth heavily (W_b = 3.0) vs latency (W_l = 0.5)
print("\n[Test 1] Prioritizing Bandwidth Weight (W_b=3.0)")
oslal.bind_socket(
    sock=sock,
    priority=5.0,
    req_bandwidth=50.0,
    max_latency=30.0,
    weights=(1.0, 0.5, 3.0, 1.0),
    custom_interfaces=dynamic_ifaces
)

# Prioritize low latency heavily (W_l = 5.0) vs bandwidth (W_b = 0.5)
print("\n[Test 2] Prioritizing Low Latency Weight (W_l=5.0)")
oslal.bind_socket(
    sock=sock,
    priority=5.0,
    req_bandwidth=50.0,
    max_latency=30.0,
    weights=(1.0, 5.0, 0.5, 1.0),
    custom_interfaces=dynamic_ifaces
)

sock.close()

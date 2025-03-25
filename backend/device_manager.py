import socket
import threading
import json
import time

# Device registry
devices = {}

# Multicast settings
MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 5007

def discover_devices():
    """
    Broadcasts on LAN to discover other devices
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    # Broadcast device info
    while True:
        msg = json.dumps({
            'name': socket.gethostname(),
            'ip': socket.gethostbyname(socket.gethostname()),
            'cpu': 8,  # Example CPU core count
            'gpu': 1,  # Example GPU count
            'ram': 32  # Example RAM in GB
        })
        sock.sendto(msg.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
        time.sleep(5)

def listen_for_devices():
    """
    Listens for device broadcasts and registers them
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((MULTICAST_GROUP, MULTICAST_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        device_info = json.loads(data.decode())
        devices[addr[0]] = device_info
        print(f"Discovered Device: {device_info}")

# Start device discovery
threading.Thread(target=discover_devices).start()
threading.Thread(target=listen_for_devices).start()

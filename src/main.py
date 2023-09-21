import pyfiglet
import socket
from datetime import datetime

ascii_banner = pyfiglet.figlet_format("G-Scanner")

print("-" * 50)
print(ascii_banner)
print("-" * 50)

NUMBER_OF_THREADS = 40
open_ports = []
closed_ports = 0

HOST = socket.gethostbyname(input("Host(Ipv4): "))
STARTING_PORT = int(input("Starting port: "))
ENDING_PORT = int(input("Ending port: "))
print(f"Scanning started at: {datetime.now().strftime('%H:%M:%S')}.")
print("-" * 50)


for port in range(STARTING_PORT, ENDING_PORT + 1):
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCKET.settimeout(0.2)
    result = SOCKET.connect_ex((HOST, port))
    if result == 0:
        print(f"Port {port} is open.")
        open_ports.append(port)
    else:
        closed_ports += 1
    SOCKET.close()


print(f"Scanning was finished at: {datetime.now().strftime('%H:%M:%S')}.")
print(f"Out of all the ports you scanned {len(open_ports)} ports were open and {closed_ports} were closed.")

import sys
import pyfiglet
import socket
from datetime import datetime
from threading import Lock, Thread
from queue import Queue

class PortScanner:

    def __init__(self):
        """
        Initialize an instance of the PortScanner class.
        Creates empty lists to store open and closed ports.
        """
        self.open_ports = []  # List to store open ports
        self.closed_ports = 0  # Counter for closed ports
        self.thread_lock = Lock()  # Thread lock for synchronization
        self.number_of_threads = 10  # Number of threads to use for scanning
        self.q = Queue()  # Queue for storing ports to be scanned

    def print_banner(self):
        """
        Print a banner with ASCII art for the Port Scanner.
        """
        ascii_banner = pyfiglet.figlet_format("Port-Scanner")
        print("-" * 70)
        print(ascii_banner)
        print("-" * 70)

    def select_option(self):
        """
        Display a menu and get the user's choice for port scanning options.
        Returns:
            int: The selected option.
        """
        print("[+] Select 1 to scan a single port")
        print("[+] Select 2 to scan all ports(1-65535)")
        print("[+] Select 3 to scan all registered ports(1024-49151)")
        print("[+] Select 4 to scan all well-known ports(1-1023)")
        print("[+] Select 5 to scan all dynamic and private ports(49152–65535)")
        print("[+] Select 6 to scan a custom range")
        print("[+] Select 7 to exit")
        option = int(input("Select an option(1-7): "))
        return option

    def get_host(self):
        """
        Get the target host's IPv4 address.
        Returns:
            str: The IPv4 address of the target host.
        """
        host = socket.gethostbyname(input("Host(Ipv4): "))
        return host

    def scan_ports(self, host, starting_port, ending_port):
        """
        Scan a range of ports on the target host using multiple threads.
        Args:
            host (str): The target host's IPv4 address.
            starting_port (int): The first port in the range to scan.
            ending_port (int): The last port in the range to scan.
        """
        print(f"Scanning started at: {datetime.now().strftime('%H:%M:%S')}.")
        print("-" * 70)

        # Populate the queue with ports to scan
        for port in range(starting_port, ending_port + 1):
            self.q.put(port)

        # Create and start threads for port scanning
        threads = []
        for _ in range(self.number_of_threads):
            thread = Thread(target=self.scan_ports_thread, args=(host,))
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        print(f"Scanning was finished at: {datetime.now().strftime('%H:%M:%S')}.")
        print(f"Out of all the ports you scanned {len(self.open_ports)} ports were open and {self.closed_ports} were "
              f"closed.")

    def scan_ports_thread(self, host):
        """
        Scan ports in a separate thread.
        Args:
            host (str): The target host's IPv4 address.
        """
        while not self.q.empty():
            port = self.q.get()
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.2)
                result = sock.connect_ex((host, port))

                if result == 0:
                    with self.thread_lock:
                        print(f"Port {port} is open.")
                        self.open_ports.append(port)
                else:
                    with self.thread_lock:
                        self.closed_ports += 1
                sock.close()
            except OSError as error:
                sys.exit(f"Socket error occurred. Error: {error}")

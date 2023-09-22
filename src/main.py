import sys
import PortScanner

# Create an instance of the PortScanner class
scanner = PortScanner.PortScanner()

# Print the banner from the PortScanner class
print(scanner.print_banner())

# Ask the user to select an option
option = scanner.select_option()

# Handle different scanning options based on the user's choice
if option == 1:
    host = scanner.get_host()
    port = int(input("Enter port to scan: "))
    if port < 1 or port > 65535:
        print(f"The port must be in the following range: 1-65535. You chose: {port}")
    else:
        # Scan a single specified port
        scanner.scan_ports(host, port, port)
elif option == 2:
    host = scanner.get_host()
    # Scan all ports (1-65535)
    scanner.scan_ports(host, 1, 65535)
elif option == 3:
    host = scanner.get_host()
    # Scan registered ports (1024-49151)
    scanner.scan_ports(host, 1024, 49151)
elif option == 4:
    host = scanner.get_host()
    # Scan well-known ports (0-1023)
    scanner.scan_ports(host, 1, 1023)
elif option == 5:
    host = scanner.get_host()
    # Scan dynamic and private ports (49152–65535)
    scanner.scan_ports(host, 49152, 65535)
elif option == 6:
    host = scanner.get_host()
    starting_port = int(input("Enter a starting port for a custom scan(1-65535): "))
    ending_port = int(input("Enter an ending port for a custom scan(1-65535): "))
    if not starting_port < 1 or not starting_port > 65535:
        # Scan a custom range of ports
        scanner.scan_ports(host=host, starting_port=starting_port, ending_port=ending_port)
    else:
        sys.exit("Invalid port range. Exiting program...")
elif option == 7:
    sys.exit("Exiting program...")

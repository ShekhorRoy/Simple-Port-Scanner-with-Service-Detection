import socket
import threading
import sys
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for cross-platform terminal color support
init(autoreset=True)

class PortScanner:
    """
    A concurrent TCP port scanner with basic service detection (banner grabbing).
    """

    def __init__(self, target):
        """Initializes the scanner with the target IP."""
        self.target = target
        self.open_ports = []
        self.lock = threading.Lock()
        
    def get_service_banner(self, sock):
        """
        Attempts to receive a service banner from the open port.
        """
        try:
            # Send a simple HTTP GET request or just wait for data
            sock.send(b'HEAD / HTTP/1.0\r\n\r\n') 
            sock.settimeout(1.0) # Lower timeout for banner reading
            banner = sock.recv(1024).decode(errors='ignore').strip().split('\n')[0]
            if banner:
                return banner
        except socket.timeout:
            return "No Banner (Timeout)"
        except Exception:
            return "Unknown Service"
        return "Unknown Service"

    def scan_port(self, port):
        """
        Attempts to connect to a single port on the target.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5) # Connection timeout

        try:
            # Attempt TCP handshake
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                service_info = self.get_service_banner(sock)
                
                with self.lock:
                    self.open_ports.append(port)
                    print(f"{Fore.GREEN}[+] Port {port:<5} is OPEN. {Style.BRIGHT}{service_info}{Style.RESET_ALL}{Fore.GREEN}")
            else:
                # Optional: print closed/filtered status for debugging
                pass 
                
        except socket.gaierror:
            print(f"{Fore.RED}[ERROR] Hostname could not be resolved.")
            sys.exit()
        except socket.error as e:
            # Handle general socket errors
            print(f"{Fore.RED}[ERROR] Could not connect to server: {e}")
            sys.exit()
        finally:
            sock.close()

    def start_scan(self, start_port, end_port):
        """
        Manages the concurrent scanning of the port range using threads.
        """
        
        t1 = datetime.now()
        print(f"\n{Fore.CYAN}--- Starting scan on target: {Style.BRIGHT}{self.target}{Style.RESET_ALL}{Fore.CYAN} ---")
        print(f"Scanning ports {start_port} through {end_port}...")
        
        threads = []
        
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            
        t2 = datetime.now()
        total_time = t2 - t1

        print(f"\n{Fore.YELLOW}--- Scan Finished ---")
        print(f"{Fore.YELLOW}Total open ports found: {Style.BRIGHT}{len(self.open_ports)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Time taken: {total_time}")
        print("-" * 30 + Style.RESET_ALL)

def resolve_target(target):
    """Utility function to validate and resolve the hostname/IP."""
    try:
        # Resolve target to an IP address
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(f"{Fore.RED}[FATAL] Cannot resolve hostname: {target}. Please check the address.")
        sys.exit(1)

def print_usage():
    """Prints usage instructions."""
    print(f"\n{Fore.BLUE}=================================================")
    print(f"{Style.BRIGHT}  Python Port Scanner v1.0{Style.RESET_ALL}")
    print(f"{Fore.BLUE}=================================================")
    print(f"\n{Fore.YELLOW}Usage: python {sys.argv[0]} <target_ip_or_hostname> <start_port> <end_port>")
    print("\nExamples:")
    print(f"  {Style.BRIGHT}python {sys.argv[0]} 127.0.0.1 1 1000{Style.RESET_ALL}")
    print(f"  {Style.BRIGHT}python {sys.argv[0]} scanme.nmap.org 80 443{Style.RESET_ALL}")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print_usage()
        
    try:
        target_input = sys.argv[1]
        start_port = int(sys.argv[2])
        end_port = int(sys.argv[3])
    except ValueError:
        print(f"{Fore.RED}[ERROR] Port numbers must be valid integers.")
        sys.exit(1)
    
    if not (0 <= start_port <= 65535 and 0 <= end_port <= 65535 and start_port <= end_port):
        print(f"{Fore.RED}[ERROR] Invalid port range. Ports must be between 0 and 65535, and start_port must be less than or equal to end_port.")
        sys.exit(1)

    # Resolve target before starting the concurrent threads
    target_ip = resolve_target(target_input)
    
    scanner = PortScanner(target_ip)
    scanner.start_scan(start_port, end_port)

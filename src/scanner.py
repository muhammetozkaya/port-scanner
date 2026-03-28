#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Professional Port Scanner Tool
Author: Muhammet Özkaya
Description: Asynchronous and threaded network port scanner with banner grabbing and JSON export.
"""

import socket
import threading
import argparse
import sys
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

try:
    from colorama import init, Fore, Style
    # Initialize colorama
    init(autoreset=True)
except ImportError:
    print("Error: colorama module is not installed. Please run 'pip install colorama' or install from requirements.txt")
    sys.exit(1)

# Common Ports Mapping for quick identification
COMMON_PORTS = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP",
    68: "DHCP",
    80: "HTTP",
    110: "POP3",
    111: "RPCBind",
    135: "MSRPC",
    139: "NetBIOS",
    143: "IMAP",
    161: "SNMP",
    443: "HTTPS",
    445: "SMB",
    514: "Syslog",
    1433: "MSSQL",
    1521: "Oracle",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Proxy",
    8443: "HTTPS-Alt",
    27017: "MongoDB"
}

# Thread Lock for writing outputs without overlap
print_lock = threading.Lock()

class PortScanner:
    def __init__(self, targets, start_port, end_port, threads, timeout, output_file=None, scan_type='TCP'):
        self.targets = targets
        self.start_port = start_port
        self.end_port = end_port
        self.threads = threads
        self.timeout = timeout
        self.output_file = output_file
        self.scan_type = scan_type.upper()
        self.results = {}
        for target in targets:
             self.results[target] = []

    def print_message(self, message, m_type="info"):
        """Thread-safe printing function with colors"""
        with print_lock:
            if m_type == "success":
                print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")
            elif m_type == "error":
                print(f"{Fore.RED}[-] {message}{Style.RESET_ALL}")
            elif m_type == "warning":
                print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}[*] {message}{Style.RESET_ALL}")

    def grab_banner(self, s):
        """Attempts to grab a banner from the service"""
        try:
            # Send a dummy payload to trigger a response from some services (like HTTP)
            s.send(b'HEAD / HTTP/1.0\r\n\r\n')
            banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            # Clean up the banner string
            banner = banner.replace('\r', '').replace('\n', ' ')
            return banner[:50] + "..." if len(banner) > 50 else banner
        except:
             return "No banner available"

    def scan_tcp(self, target, port):
        """Scans a single TCP port"""
        try:
            # Create a socket
             # AF_INET for IPv4, SOCK_STREAM for TCP
            s = socket.socket(socket.AF_INET, socket.socket.SOCK_STREAM)
            socket.setdefaulttimeout(self.timeout)

            # Returns 0 if successful
            result = s.connect_ex((target, port))
            
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                banner = self.grab_banner(s)
                
                scan_res = {
                    "port": port,
                    "service": service,
                    "state": "open",
                    "protocol": "TCP",
                    "banner": banner
                }
                
                self.results[target].append(scan_res)
                self.print_message(f"{target}:{port}/tcp - {Fore.GREEN}OPEN{Style.RESET_ALL} - Service: {service} - Banner: {banner}", "success")
            s.close()
        except KeyboardInterrupt:
             sys.exit(0)
        except Exception as e:
            pass

    def scan_udp(self, target, port):
        """Scans a single UDP port (basic check)
           Note: UDP scanning is notoriously unreliable without specific payloads.
           This is a very simplistic implementation.
        """
        try:
           # AF_INET for IPv4, SOCK_DGRAM for UDP
           s = socket.socket(socket.AF_INET, socket.socket.SOCK_DGRAM)
           socket.setdefaulttimeout(self.timeout)

           # Send empty packet
           s.sendto(b'', (target, port))
           
           try:
              data, addr = s.recvfrom(1024)
              service = COMMON_PORTS.get(port, "Unknown")
              
              scan_res = {
                  "port": port,
                  "service": service,
                  "state": "open",
                  "protocol": "UDP",
                  "banner": "Received Response"
              }
              self.results[target].append(scan_res)
              self.print_message(f"{target}:{port}/udp - {Fore.GREEN}OPEN{Style.RESET_ALL} - Service: {service}", "success")
           except socket.timeout:
              # Timeout usually means the packet was dropped (port might be closed or filtered)
              pass
           s.close()
        except Exception as e:
             pass

    def worker(self, target_queue):
         """Thread worker function"""
         while not target_queue.empty():
             target, port = target_queue.get()
             if self.scan_type == 'TCP':
                 self.scan_tcp(target, port)
             elif self.scan_type == 'UDP':
                 self.scan_udp(target, port)
             target_queue.task_done()

    def run(self):
        """Main execution method"""
        
        # Resolve hostnames to IP addresses
        resolved_targets = []
        for target in self.targets:
             try:
                 ip = socket.gethostbyname(target)
                 resolved_targets.append(ip)
                 self.print_message(f"Resolved {target} to -> {ip}", "info")
                 if target != ip and target not in self.results:
                    self.results[ip] = self.results.pop(target)
             except socket.gaierror:
                  self.print_message(f"Could not resolve hostname: {target}", "error")
        
        if not resolved_targets:
            self.print_message("No valid targets to scan. Exiting.", "error")
            return

        self.print_message("=" * 60)
        self.print_message(f"Starting Scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.print_message(f"Targets: {', '.join(resolved_targets)}")
        self.print_message(f"Ports: {self.start_port} - {self.end_port}")
        self.print_message(f"Protocol: {self.scan_type}")
        self.print_message(f"Threads: {self.threads}")
        self.print_message("=" * 60)

        # Build Queue
        q = Queue()
        for target in resolved_targets:
            for port in range(self.start_port, self.end_port + 1):
                q.put((target, port))

        # Start Threads
        threads_list = []
        for _ in range(self.threads):
             t = threading.Thread(target=self.worker, args=(q,))
             t.daemon = True
             t.start()
             threads_list.append(t)
        
        # Wait for queue to empty
        q.join()

        self.print_message("=" * 60)
        self.print_message("Scan Completed!")
        
        # Save to JSON if requested
        if self.output_file:
            self.save_results()

    def save_results(self):
        """Saves scan results to a JSON file"""
        try:
             with open(self.output_file, 'w', encoding='utf-8') as f:
                 json.dump(self.results, f, indent=4, ensure_ascii=False)
             self.print_message(f"Results successfully saved to {self.output_file}", "success")
        except IOError as e:
             self.print_message(f"Error saving results: {e}", "error")

def parse_ip_range(ip_str):
    """
    Parses IPs. Currently supports single IPs or comma separated.
    TODO: Add support for CIDR notation (e.g., 192.168.1.0/24)
    """
    return [ip.strip() for ip in ip_str.split(',')]

def parse_port_range(port_str):
     """Parses port range strings like '80', '1-1000' """
     if '-' in port_str:
         start, end = port_str.split('-')
         return int(start), int(end)
     else:
         return int(port_str), int(port_str)

def main():
    parser = argparse.ArgumentParser(description="Professional Port Scanner by Muhammet Özkaya",
                                     formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("-t", "--target", dest="target", required=True,
                        help="Target IP/Hostname or comma separated list (e.g., 192.168.1.1,example.com)")
    
    parser.add_argument("-p", "--ports", dest="ports", default="1-1024",
                        help="Port(s) to scan. Single port (80) or range (1-1000). Default: 1-1024")
    
    parser.add_argument("--protocol", dest="protocol", choices=['TCP', 'UDP'], default="TCP",
                        help="Protocol to scan (TCP or UDP). Default: TCP")
    
    parser.add_argument("--threads", dest="threads", type=int, default=100,
                        help="Number of threads to use for scanning. Default: 100")
    
    parser.add_argument("--timeout", dest="timeout", type=float, default=1.0,
                         help="Socket timeout in seconds. Default: 1.0")
    
    parser.add_argument("-o", "--output", dest="output",
                        help="Filename to save results in JSON format (e.g., results.json)")

    args = parser.parse_args()

    targets = parse_ip_range(args.target)
    try:
        start_port, end_port = parse_port_range(args.ports)
        if start_port < 1 or end_port > 65535 or start_port > end_port:
             print("[!] Error: Invalid port range. Ports must be between 1 and 65535.")
             sys.exit(1)
    except ValueError:
        print("[!] Error: Invalid port format. Use single port (80) or range (1-1000).")
        sys.exit(1)

    # ASCII Art Header
    print(Fore.CYAN + r"""
    ================================================
     _____           _     _____                                
    |  __ \         | |   / ____|                               
    | |__) |__  _ __| |_ | (___   ___ __ _ _ __  _ __   ___ _ __ 
    |  ___/ _ \| '__| __| \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
    | |  | (_) | |  | |_  ____) | (_| (_| | | | | | | |  __/ |   
    |_|   \___/|_|   \__||_____/ \___\__,_|_| |_|_| |_|\___|_|   
                                                                 
    Professional Network Scanner v1.0
    Author: Muhammet Özkaya
    ================================================
    """ + Style.RESET_ALL)

    scanner = PortScanner(targets=targets,
                          start_port=start_port,
                          end_port=end_port,
                          threads=args.threads,
                          timeout=args.timeout,
                          output_file=args.output,
                          scan_type=args.protocol)
    
    try:
         scanner.run()
    except KeyboardInterrupt:
         print(f"\n{Fore.YELLOW}[!] Scanning interrupted by user.{Style.RESET_ALL}")
         sys.exit(0)

if __name__ == "__main__":
    main()

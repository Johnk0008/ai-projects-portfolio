#!/usr/bin/env python3
"""
Network Sniffer - Basic Packet Capture and Analysis Tool
Author: AI/ML Engineer
Description: Captures and analyzes network traffic packets
"""

import socket
import struct
import time
from datetime import datetime
from typing import Dict, List, Optional
import threading
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class BasicSniffer:
    def __init__(self, interface: Optional[str] = None):
        """
        Initialize the network sniffer
        
        Args:
            interface: Network interface to sniff on (None for default)
        """
        self.interface = interface
        self.is_running = False
        self.packet_count = 0
        self.captured_packets = []
        self.start_time = None
        
    def start_sniffing(self, packet_count: int = 0, timeout: int = 30):
        """
        Start packet capture
        
        Args:
            packet_count: Number of packets to capture (0 for unlimited)
            timeout: Timeout in seconds
        """
        print(f"{Fore.GREEN}Starting network sniffer...")
        print(f"{Fore.CYAN}Interface: {self.interface or 'Default'}")
        print(f"{Fore.CYAN}Packet Count: {packet_count if packet_count > 0 else 'Unlimited'}")
        print(f"{Fore.CYAN}Timeout: {timeout} seconds")
        print(f"{Fore.YELLOW}Press Ctrl+C to stop\n")
        
        self.is_running = True
        self.start_time = datetime.now()
        
        try:
            # Create raw socket
            if socket.has_IPPROTO_IP:
                sniffer_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            else:
                # Fallback for different OS
                sniffer_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            
            # Bind to interface
            sniffer_socket.bind(('0.0.0.0', 0))
            
            # Include IP headers
            sniffer_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            # Set timeout
            sniffer_socket.settimeout(1)
            
            end_time = time.time() + timeout
            
            while self.is_running:
                if time.time() > end_time and timeout > 0:
                    print(f"{Fore.YELLOW}Timeout reached. Stopping capture.")
                    break
                    
                if packet_count > 0 and self.packet_count >= packet_count:
                    print(f"{Fore.YELLOW}Packet count reached. Stopping capture.")
                    break
                    
                try:
                    # Receive packet
                    packet, addr = sniffer_socket.recvfrom(65535)
                    self._process_packet(packet, addr)
                    
                except socket.timeout:
                    continue
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Interrupted by user.")
                    break
                except Exception as e:
                    print(f"{Fore.RED}Error receiving packet: {e}")
                    continue
                    
        except PermissionError:
            print(f"{Fore.RED}Error: Root/Administrator privileges required for raw socket access!")
            return
        except Exception as e:
            print(f"{Fore.RED}Error creating socket: {e}")
            return
        finally:
            self.stop_sniffing()
            
    def _process_packet(self, packet: bytes, addr: tuple):
        """Process and analyze captured packet"""
        self.packet_count += 1
        current_time = datetime.now()
        
        # Parse IP header (first 20 bytes)
        ip_header = packet[0:20]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
        
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        
        ttl = iph[5]
        protocol = iph[6]
        src_ip = socket.inet_ntoa(iph[8])
        dest_ip = socket.inet_ntoa(iph[9])
        
        # Extract protocol name
        protocol_name = self._get_protocol_name(protocol)
        
        # Extract payload
        data = packet[iph_length:]
        data_hex = data.hex()[:64]  # First 32 bytes in hex
        data_ascii = ''.join([chr(byte) if 32 <= byte <= 126 else '.' for byte in data[:32]])
        
        packet_info = {
            'timestamp': current_time,
            'src_ip': src_ip,
            'dest_ip': dest_ip,
            'protocol': protocol,
            'protocol_name': protocol_name,
            'ttl': ttl,
            'length': len(packet),
            'data_hex': data_hex,
            'data_ascii': data_ascii,
            'raw_data': packet
        }
        
        self.captured_packets.append(packet_info)
        self._display_packet(packet_info)
        
    def _get_protocol_name(self, protocol_num: int) -> str:
        """Convert protocol number to name"""
        protocol_map = {
            1: 'ICMP',
            6: 'TCP',
            17: 'UDP',
            2: 'IGMP',
            41: 'IPv6',
            89: 'OSPF'
        }
        return protocol_map.get(protocol_num, f'Unknown({protocol_num})')
    
    def _display_packet(self, packet_info: Dict):
        """Display packet information in colored format"""
        timestamp = packet_info['timestamp'].strftime("%H:%M:%S.%f")[:-3]
        src_ip = packet_info['src_ip']
        dest_ip = packet_info['dest_ip']
        protocol = packet_info['protocol_name']
        length = packet_info['length']
        
        # Color coding based on protocol
        if protocol == 'TCP':
            color = Fore.BLUE
        elif protocol == 'UDP':
            color = Fore.GREEN
        elif protocol == 'ICMP':
            color = Fore.YELLOW
        else:
            color = Fore.MAGENTA
            
        print(f"{color}[{timestamp}] #{self.packet_count:04d} | "
              f"{src_ip:15} -> {dest_ip:15} | "
              f"{protocol:8} | {length:4} bytes")
        
        # Show first few bytes of data
        if packet_info['data_hex']:
            print(f"    Data (hex): {packet_info['data_hex']}")
            print(f"    Data (asc): {packet_info['data_ascii']}")
        
    def stop_sniffing(self):
        """Stop the packet capture"""
        self.is_running = False
        duration = datetime.now() - self.start_time if self.start_time else 0
        
        print(f"\n{Fore.GREEN}Capture Summary:")
        print(f"{Fore.CYAN}Total Packets: {self.packet_count}")
        print(f"{Fore.CYAN}Duration: {duration}")
        print(f"{Fore.CYAN}Packets per second: {self.packet_count / duration.total_seconds():.2f}" if duration.total_seconds() > 0 else "N/A")
        
    def get_statistics(self) -> Dict:
        """Get capture statistics"""
        protocols = {}
        for packet in self.captured_packets:
            proto = packet['protocol_name']
            protocols[proto] = protocols.get(proto, 0) + 1
            
        return {
            'total_packets': self.packet_count,
            'protocols': protocols,
            'duration': datetime.now() - self.start_time if self.start_time else 0
        }
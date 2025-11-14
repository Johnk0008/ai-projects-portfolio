#!/usr/bin/env python3
"""
Advanced Packet Analyzer using Scapy
"""

from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import json
from datetime import datetime
from colorama import Fore, Style
from prettytable import PrettyTable

class AdvancedSniffer:
    def __init__(self, interface: str = None):
        """
        Initialize advanced sniffer using Scapy
        
        Args:
            interface: Network interface to sniff on
        """
        self.interface = interface
        self.packets = []
        self.is_running = False
        
    def start_capture(self, count: int = 0, filter_str: str = None, timeout: int = 30):
        """
        Start packet capture with Scapy
        
        Args:
            count: Number of packets to capture (0 for unlimited)
            filter_str: BPF filter string
            timeout: Timeout in seconds
        """
        print(f"{Fore.GREEN}Starting advanced packet capture with Scapy...")
        print(f"{Fore.CYAN}Interface: {self.interface or 'Default'}")
        print(f"{Fore.CYAN}Filter: {filter_str or 'None'}")
        print(f"{Fore.CYAN}Count: {count if count > 0 else 'Unlimited'}")
        print(f"{Fore.YELLOW}Press Ctrl+C to stop\n")
        
        self.is_running = True
        
        try:
            # Start sniffing
            sniff(
                iface=self.interface,
                prn=self._process_packet_scapy,
                count=count,
                filter=filter_str,
                timeout=timeout,
                stop_filter=lambda x: not self.is_running
            )
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Capture interrupted by user.")
        except Exception as e:
            print(f"{Fore.RED}Error during capture: {e}")
        finally:
            self.stop_capture()
            
    def _process_packet_scapy(self, packet):
        """Process packet captured by Scapy"""
        packet_info = self._analyze_packet(packet)
        self.packets.append(packet_info)
        self._display_packet_scapy(packet_info)
        
    def _analyze_packet(self, packet) -> Dict:
        """Analyze packet using Scapy"""
        packet_info = {
            'timestamp': datetime.now(),
            'layers': [],
            'summary': packet.summary(),
            'raw': packet
        }
        
        # Ethernet layer
        if Ether in packet:
            eth = packet[Ether]
            packet_info['src_mac'] = eth.src
            packet_info['dst_mac'] = eth.dst
            packet_info['layers'].append('Ethernet')
            
        # IP layer
        if IP in packet:
            ip = packet[IP]
            packet_info['src_ip'] = ip.src
            packet_info['dst_ip'] = ip.dst
            packet_info['protocol'] = ip.proto
            packet_info['ttl'] = ip.ttl
            packet_info['length'] = len(packet)
            packet_info['layers'].append('IP')
            
        # Transport layers
        if TCP in packet:
            tcp = packet[TCP]
            packet_info['src_port'] = tcp.sport
            packet_info['dst_port'] = tcp.dport
            packet_info['flags'] = str(tcp.flags)
            packet_info['layers'].append('TCP')
            
        elif UDP in packet:
            udp = packet[UDP]
            packet_info['src_port'] = udp.sport
            packet_info['dst_port'] = udp.dport
            packet_info['layers'].append('UDP')
            
        elif ICMP in packet:
            icmp = packet[ICMP]
            packet_info['type'] = icmp.type
            packet_info['code'] = icmp.code
            packet_info['layers'].append('ICMP')
            
        # Payload analysis
        if packet.payload:
            payload = bytes(packet.payload)
            packet_info['payload_hex'] = payload.hex()[:64]
            packet_info['payload_ascii'] = ''.join([
                chr(byte) if 32 <= byte <= 126 else '.' for byte in payload[:32]
            ])
            packet_info['payload_size'] = len(payload)
            
        return packet_info
    
    def _display_packet_scapy(self, packet_info: Dict):
        """Display packet information with Scapy"""
        timestamp = packet_info['timestamp'].strftime("%H:%M:%S.%f")[:-3]
        
        # Determine color based on protocol
        if 'TCP' in packet_info['layers']:
            color = Fore.BLUE
            proto = 'TCP'
        elif 'UDP' in packet_info['layers']:
            color = Fore.GREEN
            proto = 'UDP'
        elif 'ICMP' in packet_info['layers']:
            color = Fore.YELLOW
            proto = 'ICMP'
        else:
            color = Fore.MAGENTA
            proto = 'Other'
            
        print(f"{color}[{timestamp}] | "
              f"{packet_info.get('src_ip', 'N/A'):15} -> "
              f"{packet_info.get('dst_ip', 'N/A'):15} | "
              f"{proto:6} | "
              f"{packet_info.get('length', 0):4} bytes")
              
        # Show port information if available
        if 'src_port' in packet_info:
            print(f"    Ports: {packet_info['src_port']} -> {packet_info['dst_port']}")
            
        # Show payload preview
        if 'payload_ascii' in packet_info and packet_info['payload_ascii']:
            print(f"    Payload: {packet_info['payload_ascii']}")
    
    def stop_capture(self):
        """Stop packet capture"""
        self.is_running = False
        print(f"\n{Fore.GREEN}Advanced capture stopped.")
        print(f"{Fore.CYAN}Total packets captured: {len(self.packets)}")
        
    def show_statistics(self):
        """Display detailed statistics"""
        if not self.packets:
            print(f"{Fore.YELLOW}No packets captured.")
            return
            
        # Protocol statistics
        protocols = {}
        for packet in self.packets:
            for layer in packet.get('layers', []):
                if layer in ['TCP', 'UDP', 'ICMP']:
                    protocols[layer] = protocols.get(layer, 0) + 1
                    break
                    
        # Create table
        table = PrettyTable()
        table.field_names = ["Metric", "Value"]
        table.add_row(["Total Packets", len(self.packets)])
        
        for proto, count in protocols.items():
            table.add_row([f"{proto} Packets", count])
            
        # Top talkers
        src_ips = {}
        for packet in self.packets:
            src_ip = packet.get('src_ip')
            if src_ip:
                src_ips[src_ip] = src_ips.get(src_ip, 0) + 1
                
        if src_ips:
            top_talker = max(src_ips.items(), key=lambda x: x[1])
            table.add_row(["Top Source IP", f"{top_talker[0]} ({top_talker[1]} packets)"])
            
        print(f"\n{Fore.CYAN}Capture Statistics:")
        print(table)
        
    def save_packets(self, filename: str):
        """Save captured packets to file"""
        try:
            # Save as pcap
            wrpcap(filename, [pkt['raw'] for pkt in self.packets])
            print(f"{Fore.GREEN}Packets saved to {filename}")
        except Exception as e:
            print(f"{Fore.RED}Error saving packets: {e}")
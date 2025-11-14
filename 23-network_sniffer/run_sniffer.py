#!/usr/bin/env python3
"""
Main runner for Network Sniffer
"""

import argparse
import sys
import os
from sniffer import BasicSniffer
from packet_analyzer import AdvancedSniffer
from colorama import Fore, Style

def display_banner():
    """Display application banner"""
    banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════════════╗
║                   NETWORK SNIFFER TOOL                      ║
║                 AI/ML Engineer - Basic Sniffer              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def main():
    display_banner()
    
    parser = argparse.ArgumentParser(description='Network Packet Sniffer')
    parser.add_argument('-m', '--mode', choices=['basic', 'advanced'], 
                       default='advanced', help='Sniffer mode (basic/advanced)')
    parser.add_argument('-c', '--count', type=int, default=0,
                       help='Number of packets to capture (0 for unlimited)')
    parser.add_argument('-t', '--timeout', type=int, default=30,
                       help='Capture timeout in seconds')
    parser.add_argument('-i', '--interface', type=str,
                       help='Network interface to use')
    parser.add_argument('-f', '--filter', type=str,
                       help='BPF filter string (for advanced mode)')
    parser.add_argument('-o', '--output', type=str,
                       help='Output file to save packets (for advanced mode)')
    
    args = parser.parse_args()
    
    try:
        if args.mode == 'basic':
            print(f"{Fore.YELLOW}Using Basic Sniffer (Raw Sockets)")
            sniffer = BasicSniffer(args.interface)
            sniffer.start_sniffing(packet_count=args.count, timeout=args.timeout)
            
        else:  # advanced mode
            print(f"{Fore.YELLOW}Using Advanced Sniffer (Scapy)")
            sniffer = AdvancedSniffer(args.interface)
            sniffer.start_capture(count=args.count, filter_str=args.filter, 
                                timeout=args.timeout)
            
            # Show statistics
            sniffer.show_statistics()
            
            # Save packets if requested
            if args.output:
                sniffer.save_packets(args.output)
                
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Application terminated by user.")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
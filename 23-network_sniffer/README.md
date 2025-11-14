# Network Sniffer Tool

A comprehensive Python-based network packet sniffer for educational purposes and network analysis.

## Features

- **Basic Sniffer**: Uses raw sockets for packet capture
- **Advanced Sniffer**: Uses Scapy library for detailed analysis
- **Real-time Display**: Colored output with packet details
- **Protocol Analysis**: Supports TCP, UDP, ICMP protocols
- **Payload Inspection**: Hex and ASCII representation of data
- **Statistics**: Capture statistics and protocol distribution
- **Filter Support**: BPF filter support in advanced mode

## Requirements

- Python 3.9+
- Required packages in `requirements.txt`

## Installation & Setup

### Method 1: Using VS Code with Python 3.9 Virtual Environment

1. **Clone/Download the project files**
   ```bash
   mkdir network_sniffer
   cd network_sniffer
   # Copy all the Python files here
# Advanced Web Scraping Project

A comprehensive web scraping solution built with Python for extracting data from websites.

## Features

- **Multiple Website Support**: Scrape books and quotes from demo websites
- **Respectful Scraping**: Follows robots.txt and implements rate limiting
- **Error Handling**: Robust error handling with retry logic
- **Multiple Output Formats**: CSV, JSON, Excel
- **Data Analysis**: Basic data analysis and cleaning
- **Configurable**: YAML-based configuration

## Installation

1. Clone the repository
2. Create virtual environment
3. Install dependencies

## Usage

### Basic Usage
```bash
python main.py --website books --output csv
python main.py --website quotes --output json
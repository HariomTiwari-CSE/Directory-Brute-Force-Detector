# 📁 Directory Discovery Tool

A Python tool to discover common directories and files on web servers for educational security testing. This helps understand information disclosure vulnerabilities.

> **⚠️ Authorization Required:** Use only on websites you own or have explicit written permission to test.

## ✨ Features
- Checks 30+ common directories and admin panels
- Shows HTTP status codes (200, 403, 301, etc.)
- Includes file size for found resources
- Polite scanning with delays
- Wordlist-based approach

## 🚀 Quick Start

### Prerequisites
- Python 3.x
- `requests` library

### Installation
```bash
# Clone repository
git clone https://github.com/HariomTiwari-CSE/directory-checker.git
cd directory-checker

# Install dependency
pip install -r requirements.txt

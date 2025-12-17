#!/usr/bin/env python3

import requests

def check_directory(url, wordlist_file):
    """Check for common directories on a web server."""
    
    # Common directories to check (small list for demo)
    common_dirs = ["admin", "login", "wp-admin", "backup", "images", "css", "js"]
    
    print(f"[*] Testing: {url}")
    
    for directory in common_dirs:
        test_url = f"{url}/{directory}"
        
        try:
            response = requests.get(test_url, timeout=3)
            
            if response.status_code == 200:
                print(f"[+] FOUND: {test_url} (Status: {response.status_code})")
            elif response.status_code == 403:
                print(f"[!] RESTRICTED: {test_url} (Status: 403 - Forbidden)")
                
        except requests.exceptions.RequestException:
            continue 

if __name__ == "__main__":
    # Use a test site or your own local server
    target_url = input("Enter target URL (e.g., http://testphp.vulnweb.com): ") or "http://testphp.vulnweb.com"
    check_directory(target_url, None)

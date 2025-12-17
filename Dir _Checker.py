import requests
import sys
import time
from urllib.parse import urljoin

def load_wordlist(wordlist_file="common_dirs.txt"):
    """Load directories from wordlist file"""
    try:
        with open(wordlist_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        # Default common directories if file not found
        return [
            "admin", "login", "wp-admin", "dashboard", "backup",
            "images", "css", "js", "uploads", "downloads",
            "config", "private", "secret", "test", "debug",
            "phpmyadmin", "server-status", "cgi-bin", "tmp"
        ]

def check_directory(url, directory, timeout=3):
    """Check if a directory exists on the web server"""
    target_url = urljoin(url + "/", directory)
    
    try:
        response = requests.get(target_url, timeout=timeout)
        
        if response.status_code == 200:
            return "FOUND", response.status_code, len(response.content)
        elif response.status_code == 403:
            return "FORBIDDEN", response.status_code, 0
        elif response.status_code == 301 or response.status_code == 302:
            return "REDIRECT", response.status_code, 0
        else:
            return "NOT FOUND", response.status_code, 0
            
    except requests.exceptions.Timeout:
        return "TIMEOUT", 0, 0
    except requests.exceptions.ConnectionError:
        return "CONN ERROR", 0, 0
    except requests.exceptions.RequestException:
        return "ERROR", 0, 0

def main():
    """Main function"""
    print("\n" + "="*60)
    print("        DIRECTORY DISCOVERY TOOL")
    print("="*60)
    
    # Get target URL
    default_url = "http://testphp.vulnweb.com"  # Test site
    url = input(f"Enter target URL [default: {default_url}]: ").strip()
    
    if not url:
        url = default_url
    
    # Ensure URL has protocol
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    
    print(f"\nTarget: {url}")
    print("Loading wordlist...")
    
    # Load directories to check
    directories = load_wordlist()
    print(f"Loaded {len(directories)} directories to check")
    
    print("\n" + "-"*60)
    print("Starting scan... (Ctrl+C to stop)")
    print("-"*60)
    
    found_count = 0
    
    for i, directory in enumerate(directories, 1):
        status, code, size = check_directory(url, directory)
        
        # Show progress
        progress = f"[{i}/{len(directories)}]"
        
        if status == "FOUND":
            print(f"{progress} ✓ {directory:20} -> {code} ({size} bytes)")
            found_count += 1
        elif status == "FORBIDDEN":
            print(f"{progress} ! {directory:20} -> {code} (Forbidden)")
        elif status == "REDIRECT":
            print(f"{progress} → {directory:20} -> {code} (Redirect)")
        # Uncomment to see all results:
        # else:
        #     print(f"{progress}   {directory:20} -> Not found")
        
        # Small delay to be polite
        time.sleep(0.1)
    
    # Results summary
    print("\n" + "-"*60)
    print("SCAN COMPLETE")
    print("-"*60)
    print(f"Target: {url}")
    print(f"Directories checked: {len(directories)}")
    print(f"Interesting findings: {found_count}")
    print("\nLegend: ✓ = Found, ! = Forbidden, → = Redirect")
    
    if found_count == 0:
        print("\n⚠ No accessible directories found in common list.")
    else:
        print("\n💡 Found directories may indicate:")
        print("  • Admin interfaces (login, admin, wp-admin)")
        print("  • Configuration files (config, backup)")
        print("  • Development files (test, debug)")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")

import os
from dotenv import load_dotenv
from datetime import datetime
import argparse
import logging
import subprocess

# Load environment variables from .env
load_dotenv()

# Config from .env
BLOCKED_SITES = os.getenv("BLOCKED_SITES", "").split(',')
BLOCK_DAYS = os.getenv("BLOCK_DAYS", "MON,TUE,WED,THU,FRI").split(',')
BLOCK_START = os.getenv("BLOCK_START", "23:00")
BLOCK_END = os.getenv("BLOCK_END", "09:00")

# System constants
HOSTS_PATH = "/etc/hosts"
REDIRECT_IP = "127.0.0.1"
LOG_FILE = "blockbuddy.log"

# Logging setup
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def generate_hosts_entries(sites):
    entries = []
    for site in sites:
        site = site.strip()
        if site:
            entries.append(f"{REDIRECT_IP} {site}")
            entries.append(f"{REDIRECT_IP} www.{site}")
    return entries

def is_block_time():
    now = datetime.now()
    current_day = now.strftime('%a').upper()  # MON, TUE, etc.
    current_time = now.strftime('%H:%M')

    if current_day[:3] not in BLOCK_DAYS:
        return False

    # Handle overnight time range (e.g., 23:00 - 09:00)
    if BLOCK_START > BLOCK_END:
        return current_time >= BLOCK_START or current_time <= BLOCK_END
    return BLOCK_START <= current_time <= BLOCK_END

def notify_user(message):
    try:
        subprocess.run(['osascript', '-e', f'display notification "{message}" with title "BlockBuddy"'])
    except Exception as e:
        print(f"Notification failed: {e}")

def block_sites(dry_run=False):
    if not is_block_time():
        print("✅ Not in block time. No action taken.")
        logging.info("Skipped blocking: outside of block time.")
        return

    entries = generate_hosts_entries(BLOCKED_SITES)

    with open(HOSTS_PATH, 'r+') as file:
        content = file.read()
        if dry_run:
            print("🧪 [Dry Run] These entries would be added:")
            for entry in entries:
                if entry not in content:
                    print(entry)
            logging.info("Dry run executed.")
            return

        for entry in entries:
            if entry not in content:
                file.write(f"\n{entry}")
                logging.info(f"Blocked: {entry}")

    os.system("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder")
    notify_user("🔒 BlockBuddy is active. Let’s stay focused.")
    print("🚫 Websites blocked.")

def unblock_sites():
    entries_to_remove = generate_hosts_entries(BLOCKED_SITES)

    with open(HOSTS_PATH, 'r') as file:
        lines = file.readlines()

    with open(HOSTS_PATH, 'w') as file:
        for line in lines:
            if not any(entry in line for entry in entries_to_remove):
                file.write(line)

    os.system("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder")
    notify_user("✅ All websites unblocked.")
    logging.info("Unblocked all websites.")
    print("✅ Websites unblocked.")

def main():
    parser = argparse.ArgumentParser(description="🛡️ BlockBuddy - Your Friendly Focus Partner")
    parser.add_argument("--block", action="store_true", help="Block distracting websites")
    parser.add_argument("--unblock", action="store_true", help="Unblock all websites")
    parser.add_argument("--dry-run", action="store_true", help="Preview block entries without modifying /etc/hosts")

    args = parser.parse_args()

    if args.block:
        block_sites(dry_run=args.dry_run)
    elif args.unblock:
        unblock_sites()
    elif args.dry_run:
        block_sites(dry_run=True)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

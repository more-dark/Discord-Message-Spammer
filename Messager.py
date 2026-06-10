import requests
import time
import os
import json
import threading
from concurrent.futures import ThreadPoolExecutor

CONFIG_FILE = "accounts.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                                                                        ║
    ║   ███╗   ███╗███████╗███████╗███████╗ █████╗  ██████╗ ███████╗ ██████╗  
    ║   ████╗ ████║██╔════╝██╔════╝██╔════╝██╔══██╗██╔════╝ ██╔════╝ ██╗╗╗██╗ 
    ║   ██╔████╔██║█████╗  ███████╗███████╗███████║██║  ███╗█████╗   ██████╗  
    ║   ██║╚██╔╝██║██╔══╝  ╚════██║╚════██║██╔══██║██║   ██║██╔══╝   ██╗  ██╗ 
    ║   ██║ ╚═╝ ██║███████╗███████║███████║██║  ██║╚██████╔╝███████╗ ██║  ██║ 
    ║   ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚══════╝ 
    ║                                                                        ║
    ║         Discord Message Auto-Sender - Multiple Accounts Support        ║
    ║                    v2.0 | Self-Bot | T-D Organisation                  ║
    ╚════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_status(status, message):
    if status == "info":
        print(f"  ┌─[ℹ️ INFO]─────────────────────────────────────────┐")
        print(f"  │  {message}")
        print(f"  └──────────────────────────────────────────────────┘")
    elif status == "success":
        print(f"  ┌─[✅ SUCCESS]──────────────────────────────────────┐")
        print(f"  │  {message}")
        print(f"  └──────────────────────────────────────────────────┘")
    elif status == "error":
        print(f"  ┌─[❌ ERROR]────────────────────────────────────────┐")
        print(f"  │  {message}")
        print(f"  └──────────────────────────────────────────────────┘")
    elif status == "warning":
        print(f"  ┌─[⚠️ WARNING]──────────────────────────────────────┐")
        print(f"  │  {message}")
        print(f"  └──────────────────────────────────────────────────┘")

def save_accounts(accounts):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(accounts, f, indent=4)
    print_status("success", f"{len(accounts)} accounts saved to {CONFIG_FILE}")

def load_accounts():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                accounts = json.load(f)
                return accounts if isinstance(accounts, list) else []
        except:
            return []
    return []

def get_multiple_accounts():
    clear_screen()
    print_banner()
    
    # Check if saved accounts exist
    saved_accounts = load_accounts()
    
    if saved_accounts and len(saved_accounts) > 0:
        print("\n" + "═" * 60)
        print_status("info", f"Found {len(saved_accounts)} saved account(s) in accounts.json")
        print("\n  ╭─[OPTIONS]────────────────────────────────────╮")
        print("  │  1. Use saved accounts                       │")
        print("  │  2. Enter new accounts                       │")
        print("  │  3. Add more accounts to existing            │")
        print("  ╰──────────────────────────────────────────────╯")
        
        choice = input("\n  ╰─➤ Choose (1/2/3): ")
        if choice == '1':
            return saved_accounts
        elif choice == '3':
            accounts = saved_accounts
        else:
            accounts = []
    else:
        accounts = []
    
    # Get number of accounts
    print("\n" + "═" * 60)
    while True:
        try:
            num_accounts = int(input("\n  🔢 How many Discord accounts do you want to use? "))
            if num_accounts > 0:
                break
            else:
                print("  ❌ Please enter at least 1 account!")
        except ValueError:
            print("  ❌ Please enter a valid number!")
    
    # Get credentials for each account
    for i in range(num_accounts):
        print("\n" + "═" * 60)
        print(f"\n  ╭─[👤 ACCOUNT {i+1} OF {num_accounts}]──────────────────────────────╮")
        print("  │  Please enter credentials for this account:      │")
        print("  ╰──────────────────────────────────────────────────╯")
        
        # Token input
        while True:
            token = input(f"\n  🔑 Account {i+1} Token: ").strip()
            if token:
                break
            else:
                print_status("error", "Token cannot be empty!")
        
        # Channel ID input
        while True:
            try:
                channel_id = input(f"\n  📢 Account {i+1} Channel ID: ").strip()
                if channel_id:
                    int(channel_id)  # Validate
                    break
                else:
                    print_status("error", "Channel ID cannot be empty!")
            except ValueError:
                print_status("error", "Invalid Channel ID! Must be numbers only.")
        
        accounts.append({
            "token": token,
            "channel_id": channel_id,
            "enabled": True
        })
        print_status("success", f"Account {i+1} added successfully!")
    
    # Save accounts
    if accounts:
        save_accounts(accounts)
    
    return accounts

def send_message(token, channel_id, message):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "content": message,
        "nonce": str(int(time.time() * 1000)),
        "tts": False
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        return None

def send_message_for_account(account, message, account_index, stats, interval, spam_count, messages, mode):
    """Send message for a single account"""
    token = account["token"]
    channel_id = account["channel_id"]
    
    # Select message based on mode
    if mode == '1':
        current_msg = messages[0]
    else:
        current_msg = messages[stats['count'] % len(messages)]
    
    response = send_message(token, channel_id, current_msg)
    timestamp = time.strftime("%H:%M:%S")
    
    if response and response.status_code == 200:
        stats['success'] += 1
        print(f"  [ACC{account_index+1}] {timestamp} ✅ {current_msg[:35]}...")
        return True
    elif response and response.status_code == 401:
        print(f"  [ACC{account_index+1}] {timestamp} ❌ Token invalid!")
        account['enabled'] = False
        return False
    elif response and response.status_code == 403:
        print(f"  [ACC{account_index+1}] {timestamp} ❌ Permission denied!")
        account['enabled'] = False
        return False
    elif response and response.status_code == 429:
        print(f"  [ACC{account_index+1}] {timestamp} ⚠️ Rate limit! Skipping...")
        return False
    else:
        stats['error'] += 1
        print(f"  [ACC{account_index+1}] {timestamp} ❌ Error: {response.status_code if response else 'No response'}")
        return False

def send_messages_round_robin(accounts, messages, interval, spam_count, mode):
    """Send messages in round-robin fashion across all accounts"""
    
    # Filter enabled accounts
    enabled_accounts = [acc for acc in accounts if acc.get('enabled', True)]
    
    if not enabled_accounts:
        print_status("error", "No enabled accounts found!")
        return
    
    print_status("info", f"Starting spam with {len(enabled_accounts)} accounts in round-robin mode")
    print_status("info", f"Each account will send messages in sequence")
    print_status("info", "Stop karne ke liye Ctrl+C press karo")
    
    print("\n  🚀 STARTING MULTI-ACCOUNT SPAMMER IN 3 SECONDS...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    total_sent = 0
    round_num = 0
    message_index = 0
    
    try:
        while True:
            # Check if we've reached the limit
            if spam_count > 0 and total_sent >= spam_count:
                print("\n" + "═" * 60)
                print_status("success", f"✅ Spam complete! Total messages sent: {total_sent}")
                break
            
            round_num += 1
            print(f"\n  ┌─[ROUND {round_num}]─────────────────────────────────────┐")
            
            # Send one message from each account
            for idx, account in enumerate(enabled_accounts):
                # Select message based on mode
                if mode == '1':
                    current_msg = messages[0]
                else:
                    current_msg = messages[message_index % len(messages)]
                
                response = send_message(account["token"], account["channel_id"], current_msg)
                timestamp = time.strftime("%H:%M:%S")
                
                if response and response.status_code == 200:
                    total_sent += 1
                    print(f"  │  [ACC{idx+1}] {timestamp} ✅ {current_msg[:35]}...")
                elif response and response.status_code == 401:
                    print(f"  │  [ACC{idx+1}] {timestamp} ❌ Token invalid - Disabling account")
                    account['enabled'] = False
                elif response and response.status_code == 403:
                    print(f"  │  [ACC{idx+1}] {timestamp} ❌ Permission denied - Disabling account")
                    account['enabled'] = False
                elif response and response.status_code == 429:
                    print(f"  │  [ACC{idx+1}] {timestamp} ⚠️ Rate limit!")
                else:
                    print(f"  │  [ACC{idx+1}] {timestamp} ❌ Error: {response.status_code if response else 'No response'}")
                
                # Small delay between accounts to avoid rate limiting
                time.sleep(0.5)
                
                # Update message index for next round
                if mode != '1':
                    message_index += 1
            
            # Remove disabled accounts
            enabled_accounts = [acc for acc in enabled_accounts if acc.get('enabled', True)]
            
            if not enabled_accounts:
                print_status("error", "All accounts disabled due to errors!")
                break
            
            print(f"  └─────────────────────────────────────────────────────┘")
            print(f"  📊 Total sent so far: {total_sent} | Active accounts: {len(enabled_accounts)}")
            
            # Wait for next round
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n" + "═" * 60)
        print_status("info", f"👋 Stopped by user!")
        print_status("success", f"📊 Total messages sent: {total_sent}")
        print("═" * 60 + "\n")

def send_messages_parallel(accounts, messages, interval, spam_count, mode):
    """Send messages in parallel from all accounts simultaneously"""
    
    enabled_accounts = [acc for acc in accounts if acc.get('enabled', True)]
    
    if not enabled_accounts:
        print_status("error", "No enabled accounts found!")
        return
    
    print_status("info", f"Starting parallel spam with {len(enabled_accounts)} accounts")
    print_status("info", f"All accounts will send messages simultaneously")
    print_status("info", "Stop karne ke liye Ctrl+C press karo")
    
    print("\n  🚀 STARTING PARALLEL SPAMMER IN 3 SECONDS...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    total_sent = 0
    round_num = 0
    message_index = 0
    
    try:
        while True:
            if spam_count > 0 and total_sent >= spam_count:
                print("\n" + "═" * 60)
                print_status("success", f"✅ Spam complete! Total messages sent: {total_sent}")
                break
            
            round_num += 1
            print(f"\n  ┌─[ROUND {round_num} - PARALLEL]─────────────────────────┐")
            
            # Send messages in parallel using threads
            def send_for_account(account, idx):
                nonlocal message_index
                if mode == '1':
                    current_msg = messages[0]
                else:
                    current_msg = messages[message_index % len(messages)]
                
                response = send_message(account["token"], account["channel_id"], current_msg)
                timestamp = time.strftime("%H:%M:%S")
                
                if response and response.status_code == 200:
                    print(f"  │  [ACC{idx+1}] {timestamp} ✅ {current_msg[:35]}...")
                    return True
                elif response and response.status_code == 401:
                    print(f"  │  [ACC{idx+1}] {timestamp} ❌ Token invalid")
                    account['enabled'] = False
                    return False
                elif response and response.status_code == 403:
                    print(f"  │  [ACC{idx+1}] {timestamp} ❌ Permission denied")
                    account['enabled'] = False
                    return False
                else:
                    print(f"  │  [ACC{idx+1}] {timestamp} ❌ Error")
                    return False
            
            # Run all accounts in parallel
            with ThreadPoolExecutor(max_workers=len(enabled_accounts)) as executor:
                futures = []
                for idx, account in enumerate(enabled_accounts):
                    future = executor.submit(send_for_account, account, idx)
                    futures.append(future)
                
                # Wait for all to complete
                results = [f.result() for f in futures]
                round_success = sum(results)
                total_sent += round_success
            
            if mode != '1':
                message_index += 1
            
            # Remove disabled accounts
            enabled_accounts = [acc for acc in enabled_accounts if acc.get('enabled', True)]
            
            if not enabled_accounts:
                print_status("error", "All accounts disabled due to errors!")
                break
            
            print(f"  └──────────────────────────────────────────────────┘")
            print(f"  📊 Round {round_num}: {round_success} messages sent | Total: {total_sent}")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n" + "═" * 60)
        print_status("info", f"👋 Stopped by user!")
        print_status("success", f"📊 Total messages sent: {total_sent}")
        print("═" * 60 + "\n")

def main():
    # Get multiple accounts
    accounts = get_multiple_accounts()
    
    if not accounts:
        print_status("error", "No accounts configured! Exiting...")
        return
    
    clear_screen()
    print_banner()
    
    print_status("warning", "Using Self-Bot is against Discord ToS!")
    print_status("warning", "Account ban ho sakta hai! Risk aapki apni hai.")
    print_status("info", f"Total accounts loaded: {len(accounts)}")
    
    print("\n" + "═" * 60)
    
    # Time interval
    while True:
        try:
            print("\n  ╭─[⏱️ TIME INTERVAL SETUP]────────────────────────╮")
            print("  │  Examples:                                     │")
            print("  │  - 5 = 5 seconds                               │")
            print("  │  - 0.5 = 500 milliseconds                      │")
            print("  │  - 0.1 = 100 milliseconds (Fast spam)          │")
            print("  ╰────────────────────────────────────────────────╯")
            
            interval_input = input("\n  ╰─➤ Enter time between rounds (seconds): ")
            interval = float(interval_input)
            
            if interval <= 0:
                print("  ❌ Positive number daalo!")
                continue
            
            if interval >= 1:
                print(f"\n  ✅ Round interval: {interval} seconds")
            else:
                print(f"\n  ✅ Round interval: {interval} seconds ({interval * 1000:.0f}ms)")
            print("  ╰──────────────────────────────────────────────────╯")
            break
            
        except ValueError:
            print("  ❌ Valid number daalo!")
    
    print("\n" + "═" * 60)
    
    # Multi-Account Mode Selection
    print("\n  ╭─[👥 MULTI-ACCOUNT MODE]──────────────────────────╮")
    print("  │  1. Round-Robin (One account after another)      │")
    print("  │  2. Parallel (All accounts send simultaneously)  │")
    print("  ╰──────────────────────────────────────────────────╯")
    
    while True:
        multi_mode = input("\n  ╰─➤ Select mode (1/2): ")
        if multi_mode in ['1', '2']:
            break
        print("  ❌ Invalid choice! Choose 1 or 2")
    
    print("\n" + "═" * 60)
    
    # Spam Mode Selection
    print("\n  ╭─[🎯 SPAM MODE]────────────────────────────╮")
    print("  │  1. Single Message (Ek hi message)        │")
    print("  │  2. Rotating Messages (Message rotate)    │")
    print("  ╰───────────────────────────────────────────╯")
    
    while True:
        spam_mode = input("\n  ╰─➤ Select mode (1/2): ")
        if spam_mode in ['1', '2']:
            break
        print("  ❌ Invalid choice! Choose 1 or 2")
    
    print("\n" + "═" * 60)
    
    # Get messages
    messages = []
    
    if spam_mode == '1':
        # Single message
        print("\n  ╭─[📝 SINGLE MESSAGE]────────────────────────╮")
        msg = input("  │  Enter your message: ")
        if msg.strip():
            messages.append(msg)
            print(f"  │  ✅ Message saved: {msg[:50]}")
            print("  ╰──────────────────────────────────────────────╯")
        else:
            print_status("error", "Message cannot be empty!")
            return
            
    else:
        # Multiple messages
        print("\n  ╭─[📝 MULTIPLE MESSAGES]─────────────────────────╮")
        print("  │  Apne messages likho (type 'done' to finish)   │")
        print("  ╰────────────────────────────────────────────────╯")
        
        while True:
            msg = input(f"\n  📌 Message {len(messages)+1}: ")
            if msg.lower() == 'done':
                if len(messages) > 0:
                    break
                else:
                    print("  ❌ Kam se kam ek message daalo!")
                    continue
            if msg.strip():
                messages.append(msg)
                print(f"  ✅ Added: {msg[:50]}{'...' if len(msg) > 50 else ''}")
            else:
                print("  ❌ Empty message not allowed!")
    
    # Spam Count
    print("\n" + "═" * 60)
    while True:
        try:
            print("\n  ╭─[🔢 SPAM COUNT]────────────────────────────╮")
            print("  │  0 = Infinite spam (until Ctrl+C)          │")
            print("  │  10 = Send 10 rounds                       │")
            print("  │  100 = Send 100 rounds                     │")
            print("  ╰────────────────────────────────────────────╯")
            
            spam_count = int(input("\n  ╰─➤ How many rounds to send? (0 for infinite): "))
            if spam_count >= 0:
                break
            print("  ❌ Enter 0 or positive number!")
        except ValueError:
            print("  ❌ Enter valid number!")
    
    print("\n" + "═" * 60)
    print_status("success", f"{len(messages)} messages loaded!")
    print_status("info", f"{len(accounts)} accounts configured!")
    print_status("info", f"Round interval: {interval} seconds")
    print_status("info", f"Multi-account mode: {'Round-Robin' if multi_mode == '1' else 'Parallel'}")
    print_status("info", f"Will send: {'Infinite' if spam_count == 0 else spam_count} rounds")
    
    # Test connections
    print("\n" + "═" * 60)
    print("\n  🔍 Testing connections for all accounts...")
    
    active_accounts = []
    for idx, account in enumerate(accounts):
        test_response = send_message(account["token"], account["channel_id"], "Make me Stop!")
        if test_response and test_response.status_code == 200:
            print(f"  ✅ Account {idx+1}: Connected successfully!")
            active_accounts.append(account)
        else:
            print(f"  ❌ Account {idx+1}: Connection failed!")
            account['enabled'] = False
    
    if not active_accounts:
        print_status("error", "No working accounts found! Exiting...")
        return
    
    accounts = active_accounts
    
    # Start spamming
    if multi_mode == '1':
        send_messages_round_robin(accounts, messages, interval, spam_count, spam_mode)
    else:
        send_messages_parallel(accounts, messages, interval, spam_count, spam_mode)

if __name__ == "__main__":
    main()

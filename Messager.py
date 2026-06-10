import requests
import time
import os
import json

CONFIG_FILE = "token.txt"

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
    ║            Discord Message Auto-Sender By T-D Organisation             ║
    ║                         v2.0 | Self-Bot                                ║
    ╚════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_status(status, message):
    if status == "info":
        print(f"  ┌─[ℹ️ INFO]────────────────────────────────────────┐")
        print(f"  │  {message}")
        print(f"  └──────────────────────────────────────────────────┘")
    elif status == "success":
        print(f"  ┌─[✅ SUCCESS]─────────────────────────────────────┐")
        print(f"  │  {message}")
        print(f"  └──────────────────────────────────────────────────┘")
    elif status == "error":
        print(f"  ┌─[❌ ERROR]───────────────────────────────────────┐")
        print(f"  │  {message}")
        print(f"  └──────────────────────────────────────────────────┘")
    elif status == "warning":
        print(f"  ┌─[⚠️ WARNING]─────────────────────────────────────┐")
        print(f"  │  {message}")
        print(f"  └──────────────────────────────────────────────────┘")

def save_config(token, channel_id):
    config = {
        "token": token,
        "channel_id": channel_id
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
    print_status("success", f"Config saved to {CONFIG_FILE}")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get("token", ""), config.get("channel_id", "")
        except:
            return "", ""
    return "", ""

def get_token_and_channel():
    clear_screen()
    print_banner()
    
    # Check if config exists
    saved_token, saved_channel = load_config()
    
    if saved_token and saved_channel:
        print("\n" + "═" * 60)
        print_status("info", "Previous config found in token.txt")
        print(f"\n  Token: {saved_token[:20]}...{saved_token[-10:]}")
        print(f"  Channel ID: {saved_channel}")
        print("\n  ╭─[OPTIONS]────────────────────────────────────╮")
        print("  │  1. Use saved config                         │")
        print("  │  2. Enter new config                         │")
        print("  ╰──────────────────────────────────────────────╯")
        
        choice = input("\n  ╰─➤ Choose (1/2): ")
        if choice == '1':
            return saved_token, saved_channel
    
    # Get new credentials
    print("\n" + "═" * 60)
    print("\n  ╭─[🔐 DISCORD CREDENTIALS]────────────────────────╮")
    print("  │  Please enter your Discord credentials:         │")
    print("  ╰─────────────────────────────────────────────────╯")
    
    # Token input
    while True:
        token = input("\n  🔑 Enter your Discord User Token: ").strip()
        if token:
            # Basic validation
            if len(token) > 50 and '.' in token:
                print_status("success", "Token accepted!")
                break
            else:
                print_status("warning", "Token looks invalid! Still saving but may not work.")
                break
        else:
            print_status("error", "Token cannot be empty!")
    
    # Channel ID input
    while True:
        try:
            channel_id = input("\n  📢 Enter Channel ID: ").strip()
            if channel_id:
                # Convert to int to validate
                int(channel_id)
                print_status("success", "Channel ID accepted!")
                break
            else:
                print_status("error", "Channel ID cannot be empty!")
        except ValueError:
            print_status("error", "Invalid Channel ID! Must be numbers only.")
    
    # Save config
    save_config(token, channel_id)
    
    return token, channel_id

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
    response = requests.post(url, headers=headers, json=data)
    return response

def main():
    # Get token and channel ID from user
    USER_TOKEN, CHANNEL_ID = get_token_and_channel()
    
    clear_screen()
    print_banner()
    
    print_status("warning", "Using Self-Bot is against Discord ToS!")
    print_status("warning", "Account ban ho sakta hai! Risk aapki apni hai.")
    
    print("\n" + "═" * 60)
    
    # Time interval lena (Seconds ya Milliseconds)
    while True:
        try:
            print("\n  ╭─[⏱️ TIME INTERVAL SETUP]───────────────────────╮")
            print("  │  Examples:                                     │")
            print("  │  - 5 = 5 seconds                               │")
            print("  │  - 0.5 = 500 milliseconds                      │")
            print("  │  - 0.1 = 100 milliseconds (Fast spam)          │")
            print("  │  - 0.05 = 50 milliseconds (Ultra fast)         │")
            print("  ╰────────────────────────────────────────────────╯")
            
            interval_input = input("\n  ╰─➤ Enter time (seconds): ")
            interval = float(interval_input)
            
            if interval <= 0:
                print("  ❌ Positive number daalo!")
                continue
            
            # Display interval
            if interval >= 1:
                print(f"\n  ✅ Interval set to {interval} seconds")
                print(f"  📊 That is {interval * 1000} milliseconds")
            else:
                print(f"\n  ✅ Interval set to {interval} seconds")
                print(f"  📊 That is {interval * 1000:.0f} milliseconds")
            print("  ╰──────────────────────────────────────────────────╯")
            break
            
        except ValueError:
            print("  ❌ Valid number daalo!")
    
    print("\n" + "═" * 60)
    
    # Spam Mode Selection
    print("\n  ╭─[🎯 SPAM MODE]────────────────────────────╮")
    print("  │  1. Single Message (Ek hi message)        │")
    print("  │  2. Multiple Messages (Rotate)            │")
    print("  │  3. List Messages (Sequential)            │")
    print("  ╰───────────────────────────────────────────╯")
    
    while True:
        mode = input("\n  ╰─➤ Select mode (1/2/3): ")
        if mode in ['1', '2', '3']:
            break
        print("  ❌ Invalid choice! Choose 1, 2, or 3")
    
    print("\n" + "═" * 60)
    
    messages = []
    
    if mode == '1':
        # Single message
        print("\n  ╭─[📝 SINGLE MESSAGE]────────────────────────╮")
        msg = input("  │  Enter your message: ")
        if msg.strip():
            messages.append(msg)
            print(f"  │  ✅ Message saved: {msg[:50]}")
            print("  ╰──────────────────────────────────────────────────╯")
        else:
            print_status("error", "Message cannot be empty!")
            return
            
    elif mode == '2':
        # Multiple messages (Rotate)
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
                
    elif mode == '3':
        # Sequential list
        print("\n  ╭─[📝 SEQUENTIAL MODE]─────────────────────────╮")
        print("  │  Messages will send in order: 1,2,3,1,2,3... │")
        print("  ╰──────────────────────────────────────────────╯")
        
        while True:
            msg = input(f"\n  📌 Message {len(messages)+1} (or 'done'): ")
            if msg.lower() == 'done':
                if len(messages) > 0:
                    break
                else:
                    print("  ❌ Kam se kam ek message daalo!")
                    continue
            if msg.strip():
                messages.append(msg)
                print(f"  ✅ Added: {msg[:50]}")
            else:
                print("  ❌ Empty message not allowed!")
    
    # Spam Count
    print("\n" + "═" * 60)
    while True:
        try:
            print("\n  ╭─[🔢 SPAM COUNT]────────────────────────────╮")
            print("  │  0 = Infinite spam (until Ctrl+C)          │")
            print("  │  10 = Send 10 times                        │")
            print("  │  100 = Send 100 times                      │")
            print("  │  1000 = Send 1000 times                    │")
            print("  ╰────────────────────────────────────────────╯")
            
            spam_count = int(input("\n  ╰─➤ How many messages to send? (0 for infinite): "))
            if spam_count >= 0:
                break
            print("  ❌ Enter 0 or positive number!")
        except ValueError:
            print("  ❌ Enter valid number!")
    
    print("\n" + "═" * 60)
    print_status("success", f"{len(messages)} messages loaded!")
    print_status("info", f"Interval: {interval} seconds" if interval >= 1 else f"Interval: {interval * 1000:.0f} milliseconds")
    print_status("info", f"Will send: {'Infinite' if spam_count == 0 else spam_count} messages")
    print_status("info", "Stop karne ke liye Ctrl+C press karo")
    
    # Test connection first
    print("\n" + "═" * 60)
    print("\n  🔍 Testing connection...")
    test_response = send_message(USER_TOKEN, CHANNEL_ID, "🟢 Spammer connected! Starting in 3 seconds...")
    if test_response.status_code == 200:
        print_status("success", "Connection successful!")
    else:
        print_status("error", f"Connection failed! Error {test_response.status_code}")
        print_status("error", "Please check your token and channel ID")
        return
    
    print("\n  🚀 STARTING SPAMMER IN 3 SECONDS...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    count = 0
    error_count = 0
    success_count = 0
    
    try:
        while True:
            # Check if we've reached the limit
            if spam_count > 0 and count >= spam_count:
                print("\n" + "═" * 60)
                print_status("success", f"✅ Spam complete! Sent {success_count} messages")
                if error_count > 0:
                    print_status("warning", f"⚠️ Errors: {error_count}")
                break
            
            # Select current message
            current_msg = messages[count % len(messages)]
            
            # Send message with timestamp
            timestamp = time.strftime("%H:%M:%S")
            response = send_message(USER_TOKEN, CHANNEL_ID, current_msg)
            
            # Progress calculation
            if spam_count > 0:
                percentage = (count / spam_count) * 100
                bar_length = 30
                filled = int(bar_length * count / spam_count)
                bar = '█' * filled + '░' * (bar_length - filled)
                progress_text = f"{percentage:.1f}% {bar}"
            else:
                progress_text = "INFINITE MODE"
            
            if response.status_code == 200:
                success_count += 1
                print(f"  [{count+1:04d}] {timestamp} ✅ {current_msg[:35]}... | {progress_text}")
                
            elif response.status_code == 401:
                print_status("error", "Token invalid! Please check your token.")
                break
                
            elif response.status_code == 403:
                print_status("error", "Permission denied in this channel!")
                break
                
            elif response.status_code == 429:
                error_count += 1
                print_status("warning", f"Rate limit! Waiting 5 seconds... (Error #{error_count})")
                time.sleep(5)
                continue
                
            elif response.status_code == 400:
                print_status("error", "Bad request! Message might be empty or too long")
                break
                
            else:
                error_count += 1
                print(f"  [{count+1:04d}] ❌ Error {response.status_code} | {progress_text}")
                if error_count > 10:
                    print_status("error", "Too many errors! Stopping...")
                    break
            
            count += 1
            
            # Wait for next message
            if interval < 0.05:
                time.sleep(0.05)  # Minimum 50ms delay to prevent crash
            else:
                time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n" + "═" * 60)
        print_status("info", f"👋 Stopped by user!")
        print_status("success", f"📊 Total sent: {success_count} | Errors: {error_count}")
        print("═" * 60 + "\n")

if __name__ == "__main__":
    main()

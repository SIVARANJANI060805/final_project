import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"   # LAN access
PORT = 5000

clients = {}
muted_users = set()
log_file = "chat_logs.txt"


def log_message(message):
    with open(log_file, "a") as f:
        f.write(message + "\n")


def broadcast(message, sender=None):
    for client, username in list(clients.items()):
        if username != sender and username not in muted_users:
            try:
                client.send(message.encode())
            except:
                pass


def handle_client(client):
    username = None
    try:
        username = client.recv(1024).decode()
        if not username:
            return

        clients[client] = username

        join_msg = f"[{datetime.now()}] {username} joined the chat"
        print(join_msg)
        log_message(join_msg)
        broadcast(join_msg)

        while True:
            msg = client.recv(1024).decode()
            if not msg or msg == "/exit":
                break

            elif msg.startswith("/mute"):
                muted_users.add(username)
                client.send("You are muted".encode())

            else:
                full_msg = f"{username}: {msg}"
                print(full_msg)
                log_message(full_msg)
                broadcast(full_msg, username)

    except:
        pass
    finally:
        if username:
            leave_msg = f"{username} left the chat"
            print(leave_msg)
            log_message(leave_msg)
            broadcast(leave_msg)

        if client in clients:
            del clients[client]

        client.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    server.settimeout(1)   # allows CTRL+C to work on Windows

    print("Server started...")

    try:
        while True:
            try:
                client, addr = server.accept()
                threading.Thread(
                    target=handle_client,
                    args=(client,),
                    daemon=True
                ).start()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("\nServer stopped safely")
    finally:
        server.close()


# ⭐ THIS WAS MISSING (VERY IMPORTANT)
if __name__ == "__main__":
    start_server()


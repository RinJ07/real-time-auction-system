import socket
import threading

# Global variables
clients = []
current_bid = 0
highest_bidder = "No one yet"
auction_item = "Antique Vase"

def broadcast(message):
    """Broadcasts messages to all connected clients."""
    for client in clients:
        try:
            client.send(message.encode())
        except:
            clients.remove(client)

def handle_client(client_socket, address):
    """Handles client interactions."""
    global current_bid, highest_bidder

    client_socket.send(f"Welcome to the auction for '{auction_item}'!\n".encode())
    client_socket.send(f"Current highest bid: ${current_bid} by {highest_bidder}\n".encode())
    broadcast(f"New participant joined: {address}")

    while True:
        try:
            bid_message = client_socket.recv(1024).decode()
            if not bid_message:
                break

            # Process the bid
            try:
                bid = int(bid_message.strip())
                if bid > current_bid:
                    current_bid = bid
                    highest_bidder = f"{address[0]}:{address[1]}"
                    broadcast(f"New highest bid: ${current_bid} by {highest_bidder}")
                else:
                    client_socket.send("Bid too low! Place a higher bid.\n".encode())
            except ValueError:
                client_socket.send("Invalid input! Please enter a numeric value for your bid.\n".encode())
        except:
            print(f"Client {address} disconnected.")
            clients.remove(client_socket)
            break

    client_socket.close()

def start_server(host='127.0.0.1', port=5555):
    """Starts the auction server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Auction server started for '{auction_item}' on {host}:{port}\n")

    while True:
        client_socket, address = server_socket.accept()
        print(f"New connection from {address}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    start_server()

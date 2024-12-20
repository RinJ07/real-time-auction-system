import socket
import threading
import time

# Global variables
clients = []
current_bid = 0
highest_bidder = "No one yet"
auction_item = "Antique Vase"
auction_running = True

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

            # Check for winner acknowledgment
            if not auction_running and f"{address[0]}:{address[1]}" == highest_bidder:
                if bid_message.strip().lower() == "yes":
                    client_socket.send("Thank you for confirming your purchase. The item is now yours!\n".encode())
                    print(f"Winner {highest_bidder} confirmed their purchase.")
                else:
                    client_socket.send("Please type 'yes' to confirm your purchase.\n".encode())
                continue

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

def close_auction():
    """Ends the auction and announces the winner."""
    global auction_running
    auction_running = False
    broadcast(f"\nAuction closed! Winner: {highest_bidder} with a bid of ${current_bid}.")

    # Notify the winner individually
    for client in clients:
        if f"{client.getpeername()[0]}:{client.getpeername()[1]}" == highest_bidder:
            try:
                client.send("Congratulations! You are the winner. Please confirm your purchase by typing 'yes'.\n".encode())
            except:
                print(f"Could not notify the winner: {highest_bidder}")
    print("Auction ended.")

def auction_timer(duration):
    """Closes the auction after a specific duration."""
    time.sleep(duration)
    close_auction()

def start_server(host='127.0.0.1', port=5555):
    """Starts the auction server."""
    global auction_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Auction server started for '{auction_item}' on {host}:{port}\n")

    # Timer thread for auction closure
    threading.Thread(target=auction_timer, args=(300,)).start()  # Auction ends in 300 seconds (5 minutes)

    while auction_running:
        try:
            client_socket, address = server_socket.accept()
            print(f"New connection from {address}")
            clients.append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket, address)).start()
        except:
            break

    close_auction()
    server_socket.close()

if __name__ == "__main__":
    start_server()

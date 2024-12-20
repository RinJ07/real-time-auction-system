import socket
import threading

def listen_for_updates(sock):
    """Listens for messages from the server."""
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            print(f"\n{message}")

            # Handle auction closure and winner confirmation
            if "Auction closed!" in message:
                print("The auction has ended.")
                if "Congratulations! You are the winner." in message:
                    while True:
                        confirmation = input("Type 'yes' to confirm your purchase: ")
                        sock.send(confirmation.encode())
                        if confirmation.lower() == "yes":
                            print("Thank you for confirming your purchase!")
                            break
                print("Exiting as auction has ended.")
                sock.close()
                break

        except:
            print("Disconnected from the server.")
            break

def start_client(host='127.0.0.1', port=5555):
    """Starts the auction client."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Connected to auction server at {host}:{port}\n")
    except:
        print("Failed to connect to the server. Please check the server status.")
        return

    # Start a thread to listen for updates
    threading.Thread(target=listen_for_updates, args=(client_socket,), daemon=True).start()

    while True:
        try:
            bid = input("Enter your bid (or type 'exit' to leave): ")
            if bid.lower() == "exit":
                print("Exiting the auction...")
                client_socket.close()
                break
            client_socket.send(bid.encode())
        except:
            print("Error occurred. Exiting...")
            break

if __name__ == "__main__":
    start_client()

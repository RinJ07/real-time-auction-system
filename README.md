```markdown

# Real-Time Auction System

## Overview

This is a simple, real-time auction application 
built with Python, demonstrating network programming 
concepts using sockets and threading. Multiple clients can 
connect to a central server and participate in a live 
auction by placing bids.


## Prerequisites

- Python 3.7+

- Standard Python libraries(socket,threading)


## Project Structure

real-time-auction-system/
│
├── auction_server.py     # Server-side application
├── auction_client.py     # Client-side application
└── README.md             # This documentation file

## Installation
- Clone the repository

````bash
    git clone https://github.com/RinJ07/real-time-auction-system.git

navigate the project
````bash
    cd auction-project
    
- No additional dependencies are 
    required beyond standard Python 
    libraries.

## Running the Application


-Start the Server

````bash
    python auction_server.py

-Start Clients

````bash
    python auction_client.py


### How to use 

- Run the server first

- Connect multiple clients

- Enter numeric bids when prompted

- Type 'exit' to leave the auction



## Bidding Rules

- Bids must be higher than the current highest bid

- Bids are numeric values

- The highest bidder is updated in real-time across all clients


## Current Auction Item

- The default auction item is an "Antique Vase"

## Costumization

- To change the host, port, or auction item, modify the respective variables in "auction_server.py"

## Troubleshooting

- Ensure Python 3.7+ is installed
- Check network connectivity
- Verify no other applications are using port 5555
- Restart the server if connection issues occur

## Future Improvements

- Add user authentication
- Implement persistent auction state
- Create a graphical user interface
- Add more robust error handling
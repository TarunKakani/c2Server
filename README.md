# Basic C2 Server

This repository contains a simple implementation of a Command and Control (C2) Server, designed for educational and conceptual understanding purposes only. The project demonstrates fundamental networking and concurrency concepts using Python sockets and multithreading. Additionally, the `client.py` script can be run as a background process (using fork) to simulate multiple clients for testing the server's handling of concurrent connections.

## Features

- **Socket Programming:**  
  - Establishes a TCP server using Python's socket library.
  - Enables multiple clients to connect to the server via sockets.

- **Multi-Threading:**  
  - Each client connection is handled in a separate thread, allowing simultaneous communication with multiple clients.

- **Background Client Process:**  
  - The `client.py` script can be forked to run as a background process, useful for simulating real-world scenarios and testing server concurrency.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

### Usage

#### 1. Start the C2 Server

Run the server script to start listening for incoming client connections:

```bash
python3 server.py
```

#### 2. Start Clients

You can start one or more clients to connect to the server. To simulate background processes, you can fork the client script using the `os.fork()` method inside `client.py` or run in the background from your shell:

```bash
python3 client.py &
```

Or, inside `client.py`, use `os.fork()` to spawn multiple background clients for testing.

#### 3. Observe Server Output

The server will display logs for each client connection and handle their messages concurrently.

## File Structure

```
.
├── server.py   # The main C2 server implementation
├── client.py     # The client implementation; can be run as background process
└── README.md     # This documentation
```

## How It Works

- **Server** (`server.py`):
  - Listens on a specified port for incoming TCP connections.
  - For each new client, spawns a new thread for communication, ensuring multiple clients can be connected and managed simultaneously.

- **Client** (`client.py`):
  - Connects to the server and sends/receives messages.
  - Can be run in multiple instances or as background processes to test server concurrency.

## Disclaimer

> **This project is for educational and conceptual demonstration purposes only.**
> Do **NOT** use this code for any unauthorized or malicious activities. The author is not responsible for any misuse of this code.

## License

This repository is licensed under the MIT License.

---

Feel free to open issues or PRs for suggestions and improvements!

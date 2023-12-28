import socket
import time

# Set up the socket and bind it to a port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 12345))

# Set up the initial sequence and acknowledgement numbers
seq = 0
ack = 0
step = 0

mode = int(input("Manual or Auto?: 0 ve 1" ))

while True:
    # Receive a message from the client
    data, addr = sock.recvfrom(1024)

    # Convert the received bytes-like object to a string
    data = data.decode()

    # Extract the client's sequence and acknowledgement numbers and packet length from the message
    client_seq, client_ack, clientLength = data.split(',')
    client_seq = int(client_seq)
    client_ack = int(client_ack)
    clientLength = int(clientLength)

    if clientLength > 0:
        print("Incoming data")
        print(client_seq, client_ack, clientLength)
        # Calculate the next sequence and acknowledgement numbers for the server's response
        seq = client_ack
        ack = client_seq + clientLength

    else:
        print("No data from client. Server may send.")
        serverLength = 164
        seq = client_ack
        ack = client_seq + serverLength

    if(mode == 0):
        seq, ack, clientLength = input("Enter the ACK, SEQ, and length values: ").split(',')

    # Send a message with the server's sequence and acknowledgement numbers and packet length
    message = f"{seq},{ack},{clientLength}"
    # Convert the message to a bytes-like object before sending it
    message = message.encode()
    
    sock.sendto(message, addr)
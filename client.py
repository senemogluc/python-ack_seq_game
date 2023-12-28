import socket

# Set up the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set up the initial sequence and acknowledgement numbers
seq = 0
ack = 0

while True:
    # Get the input from the user as a string
    input_string = input("Enter the ACK, SEQ, and length values: ")

    # Split the input string on the comma delimiter to get the individual values
    seq, ack, length = input_string.split(',')

    # Convert the values to the desired data type
    seq = int(seq)
    ack = int(ack)
    length = int(length)

    # Get the packet length from the user
    #length = int(input("Enter the packet length: "))

    # Calculate the next sequence and acknowledgement numbers for the client's message
    #seq += length
    #ack += length

    # Send a message with the client's sequence and acknowledgement numbers and packet length
    message = f"{seq},{ack},{length}"

    # Convert the message to a bytes-like object before sending it
    message = message.encode()
    sock.sendto(message, ('localhost', 12345))
    
    # Receive a message from the server
    data, _ = sock.recvfrom(1024)

    # Convert the received bytes-like object to a string
    data = data.decode()

    # Extract the server's sequence and acknowledgement numbers and packet length from the message
    server_seq, server_ack, _ = data.split(',')
    server_seq = int(server_seq)
    server_ack = int(server_ack)

    # Print the server's response
    print(f"Server response: seq={server_seq}, ack={server_ack}")

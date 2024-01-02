import socket

def send_message(sock, seq, ack, length, addr = ('localhost', 12345)):
    message = f"{seq} {ack} {length}"
    print(f"Sent: {message} to {addr}")
    message = message.encode()
    sock.sendto(message, addr)
    seq += length

def receive_message(sock):
    data, addr = sock.recvfrom(1024)
    data = data.decode()
    print(f"Received: {data} from {addr}")
    received_seq, received_ack, received_len = list(map(int, data.split(" ")))


    return received_seq, received_ack, received_len, addr

def check_lost(received_seq, ack):
        return received_seq != ack  

def main():   
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 12345))

    iteration = 0
    seq = 0
    while True:

        received_seq, received_ack, received_len, addr = receive_message(sock)
        if iteration == 0:
            ack = received_seq
        if check_lost(received_seq, ack):
            print(f"Packet lost!")

        ack = received_seq + received_len
        seq = received_ack
        
        send_message(sock, seq, ack, 10, addr)
        iteration += 1
        print("Iteration: ", iteration)

if __name__ == "__main__":
    main()
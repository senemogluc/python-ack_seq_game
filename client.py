import socket

def send_message(sock, seq, ack, length=10, addr = ('localhost', 12345)):
    message = f"{seq} {ack} {length}"
    message = message.encode()
    sock.sendto(message, addr)

def receive_message(sock):
    data, addr = sock.recvfrom(1024)
    data = data.decode()
    print(f"Received: {data} from {addr}")
    received_seq, received_ack, received_len = data.split(' ')
    received_seq = int(received_seq)
    received_ack = int(received_ack)
    received_len = int(received_len)

    return received_seq, received_ack, received_len, addr

def check_lost(received_seq, ack):
        return received_seq != ack  

def main():   
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    iteration = 0
    while True:
        input_string = input("Enter the SEQ, ACK, and length values: ")
        seq, ack, length = list(map(int, input_string.split(' ')))

        send_message(sock, seq, ack, length)
        received_seq, received_ack, received_len, addr = receive_message(sock)
        if check_lost(received_seq, ack):
            print("Packet lost!")
        iteration += 1
        print("Iteration: ", iteration)

if __name__ == "__main__":
    main()
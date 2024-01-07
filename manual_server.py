import socket
import pandas as pd

def send_message(sock, seq, ack, length, addr = ('localhost', 12345)):
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

def append_data(seq, ack, length, dataframe):
    data = [seq, ack, length]
    dataframe.loc[len(dataframe)] = data
    print(dataframe)
    return dataframe

def main():   
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 12345))

    server_df = pd.DataFrame(columns=['seq', 'ack', 'length'])

    iteration = 0
    while True:
        print("Iteration: ", iteration)

        if iteration != 0 and seq != received_ack and not corrupted:
            ack = received_seq

        corrupted = False
        received_seq, received_ack, received_len, addr = receive_message(sock)
        if iteration != 0 and check_lost(received_seq, ack):
            print("Recieved wrong packet sequence! Please resend the packet")
            corrupted = True

        input_string = input("Enter the SEQ, ACK, and length values: ")
        seq, ack, length = list(map(int, input_string.split(' ')))

        send_message(sock, seq, ack, length, addr)
        append_data(seq, ack, length, server_df)
        
        iteration += 1
        
if __name__ == "__main__":
    main()
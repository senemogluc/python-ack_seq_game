import socket
import random
import pandas as pd

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
    seq = 0
    while True:
        print("Iteration: ", iteration)
        

        received_seq, received_ack, received_len, addr = receive_message(sock)
        if iteration == 0:
            ack = received_seq

        if check_lost(received_seq, ack):
            print(f"Packet lost!")
            send_message(sock, seq, ack, corrupted_rate*10, addr)
            append_data(seq, ack, corrupted_rate*10, server_df)
            received_seq, received_ack, received_len, addr = receive_message(sock)

        ack = received_seq + received_len
        seq = received_ack
        
        corrupted_rate = random.randint(1, 11)
        if corrupted_rate % 3 == 0:
            print("Sending corrupted packet...", corrupted_rate)

            send_message(sock, seq+corrupted_rate, ack, corrupted_rate*10, addr)
            append_data(seq+corrupted_rate, ack, corrupted_rate*10, server_df)

            iteration += 1
            print("Iteration: ", iteration)

            received_seq, received_ack, received_len, addr = receive_message(sock)
            ack = received_seq + received_len
            seq = received_ack

        send_message(sock, seq, ack, corrupted_rate*10, addr)
        append_data(seq, ack, corrupted_rate*10, server_df)
        iteration += 1

if __name__ == "__main__":
    main()
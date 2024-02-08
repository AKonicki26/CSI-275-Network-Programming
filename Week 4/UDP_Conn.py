import socket
import time

if __name__ == "__main__":

    #UDP connection this time
    udp_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    data = "Hey there, Scott's Server!"
    send_address = ("216.93.148.124", 54810)

    # udp connections use sendto()
    udp_conn.sendto(data.encode('ascii'), send_address)

    print("Sent message")
    MAX_TIMEOUT = 10
    wait_time = 1
    udp_conn.settimeout(wait_time)
    while True:
        try:
            udp_conn.sendto(data.encode("ascii"), send_address)
            response, address = udp_conn.recvfrom(4096)
            print(f"'{response.decode()}' received from {address}")
            time.sleep(0.75)
        except socket.timeout:
            print("Connection timed out")
            wait_time *= 2
            if wait_time >= MAX_TIMEOUT:
                print("Exceeded max wait time")
                break
            udp_conn.settimeout(wait_time)
            # If we exceed our max wait time,
            # break the loop

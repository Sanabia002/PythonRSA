import socket
import sys
import math
import rsa
import os
import tqdm
# generate key pair
(pub_key, priv_key) = rsa.newkeys(2048)
# device's IP address
HOST = "169.254.123.111"
PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
s = socket.socket()
# bind the socket to our local address
s.bind((HOST, PORT))
s.listen(5)
print(f"[*] Listening as {HOST}:{PORT}")
# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename_2)
# convert to integer
filesize = int(filesize)
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))


#read in public keys
with open('client_pub_key.pem', 'rb') as f:
    pub_key = rsa.PublicKey.load_pkcs1(f.read())
 
# read in encrypted file
with open('encrypted_file.txt', 'rb') as f:
    encrypted = f.read()
def decrypt(encrypted, priv_key):
    try:
        return rsa.decrypt(encrypted, priv_key).decode('ascii')
    except:
        return False
plaintext = decrypt(encrypted, priv_key)
# read in signed file
with open('signed_file.txt', 'rb') as f:
    signed = f.read()
 
# verify file
rsa.verify(data, signed, pub_key)

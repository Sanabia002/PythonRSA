import socket
import math
import sys
import os
import rsa
import threading
import tqdm 
# generate key pair
(pub_key, priv_key) = rsa.newkeys(2048)
# export public key
with open('client_pub_key.pem', 'wb') as f:
    f.write(pub_key.save_pkcs1())
with open('client_priv_key.pem', 'wb') as f:
    f.write(priv_key.save_pkcs1())
# read in file to be sent
with open('plaintext.txt', 'rb') as f:
    data = f.read()
# encrypt file
encrypted = rsa.encrypt(data, pub_key)
# save encrypted file
with open('encrypted_file.txt', 'wb') as f:
    f.write(encrypted)
# sign file
signed = rsa.sign(data, priv_key, 'SHA-256')
# save signed file
with open('signed_file.txt', 'wb') as f:
    f.write(signed)
# open socket
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
host = "169.254.123.111"
port = 5001
filename = "encrypted_file.txt"
filesize = os.path.getsize('encrypted_file.txt')
s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")
s.send (f"{filename}{SEPARATOR}{filesize}".encode())
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# read in file to be sent
with open('signed_file.txt', 'rb') as f:
    data = f.read()
filesize = os.path.getsize('signed_file.txt')
filename = "signed_file.txt"
s.send (f"{filename}{SEPARATOR}{filesize}".encode())
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
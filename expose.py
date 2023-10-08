import cv2
import socket
import pickle
import struct

# Set up camera capture
camera = cv2.VideoCapture(0)  # Replace 0 with the camera index if multiple cameras are connected

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'  # Replace with the desired host IP address
port = 8000  # Replace with the desired port number
server_socket.bind((host, port))
server_socket.listen(1)
print('Waiting for a client to connect...')

# Accept a client connection
client_socket, client_address = server_socket.accept()
print('Client connected:', client_address)

# Stream camera frames to the client
while True:
    # Read frame from the camera
    ret, frame = camera.read()

    # Encode frame as JPEG
    _, encoded_frame = cv2.imencode('.jpg', frame)
    data = pickle.dumps(encoded_frame)
    message_size = struct.pack("L", len(data))  # Pack message size as 4 bytes

    # Send message size first
    client_socket.sendall(message_size)
    # Send the frame data
    client_socket.sendall(data)

# Close the socket and release the camera
client_socket.close()
server_socket.close()
camera.release()

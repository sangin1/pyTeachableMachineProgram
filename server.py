import socket, threading
from keras.models import load_model
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientSocket):
        threading.Thread.__init__(self)
        self.csocket = clientSocket
        np.set_printoptions(suppress=True)
        model = tensorflow.keras.models.load_model('keras_model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        size = (224, 224)      
        
    def run(self):
        while True:
            data = self.scoket.recv()
            image = data.decode()
            image = ImageOps.fit(image, size, Image.ANTIALIAS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            prediction = model.predict(data)

            sendString = prediction[0]+'-'+prediction[1]
            
            if not data:
                connections.remove(c)
                c.close()
                break

host = "127.0.0.1"
port = 5000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server.bind((host,port))

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()

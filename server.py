import socket
import threading
from keras.models import load_model
import tensorflow.keras
from PIL import Image, ImageOps
import PIL
import numpy as np
import numpy
import socket
import cv2
import base64
import os

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientSocket):
        threading.Thread.__init__(self)
        self.csocket = clientSocket
        np.set_printoptions(suppress=True)
              
    def run(self):
        while True:
            length = self.csocket.recv(64)
            length1 = length.decode('utf-8')
            stringData = self.csocket.recv(int(length1))
            data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)
            decimg = cv2.imdecode(data, 1)

            model = tensorflow.keras.models.load_model('keras_model.h5')               
            data2 = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            image_array = np.asarray(decimg)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data2[0] = normalized_image_array
            prediction = model.predict(data2)

            sendString = str(round(prediction[0][0]*100,2))+'-'+str(round(prediction[0][1]*100,2))
            self.csocket.send(sendString.encode('utf-8'))
            

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

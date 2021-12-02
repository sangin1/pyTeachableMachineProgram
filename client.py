import tkinter.messagebox
from tkinter import *
from PIL import Image,ImageTk
from tkinter import filedialog 
import socket
import PIL
from PIL import Image, ImageOps
import cv2
import numpy
import base64

def open():
    global photo
    filename = filedialog.askopenfilename(initialdir='', title='파일선택', filetypes=(
    ('png files', '*.png'), ('jpg files', '*.jpg')))
    
    image = Image.open(filename)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    canvas.delete("all")
    canvas.create_image(0,0,anchor='nw',image=photo)
    canvas.image = photo

    rgb_image = cv2.imread(filename)
    dst = cv2.resize(rgb_image, dsize=(224, 224), interpolation=cv2.INTER_AREA)

    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv2.imencode('.jpg', dst, encode_param)
    data = numpy.array(imgencode)
    stringData = base64.b64encode(data)
    length = str(len(stringData))
    
    sock.sendall(length.encode('utf-8').ljust(64))
    sock.send(stringData)
    
    a = sock.recv(1024)
    a = a.decode('utf-8')
    
    water = a.split('-')[0]
    melon = a.split('-')[1]
    label2.configure(text = "수박"+water+"% 일치")
    label3.configure(text = "멜론"+melon+"% 일치")
 
    
def on_closing():
    sock.close()
    root.destroy()

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('localhost',5000));

root = Tk()

root.title("수박,멜론구별 프로그램")
root.geometry("600x400+300+300")

label1 = Label(root,text = "수박, 멜론사진을 올리면 판별합니다")
label1.pack()

canvas = Canvas(height=224,width=224)
canvas.pack()
label2 = Label(root,text = "")
label2.pack()
label3 = Label(root,text = "")
label3.pack()
my_btn = Button(root, text='파일열기', command=open).pack()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

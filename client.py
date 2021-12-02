import tkinter.messagebox
from tkinter import *
from PIL import Image,ImageTk
from tkinter import filedialog
import PIL
import socket
import numpy

def open():
    global photo
    filename = filedialog.askopenfilename(initialdir='', title='파일선택', filetypes=(
    ('png files', '*.png'), ('jpg files', '*.jpg')))
    
    image = Image.open(filename)
    image = image.resize((224,224),PIL.Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    Label(root,image=photo).pack()

    sock.send(photo.encode())

    a = sock.recv(1024).decode()
    water = a.split('-')[0]
    melon = a.split('-')[1]

    Label(root,text="수박"+water+"% 일치").pack()
    Label(root,text="멜론"+water+"% 일치").pack()
    
def on_closing():
    socket.close()
    root.destroy()

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('localhost',5000));

root = Tk()

root.title("수박,멜론구별 프로그램")
root.geometry("600x400+300+300")

label1 = Label(root,text = "수박, 멜론사진을 올리면 판별합니다")
label1.pack()

 
my_btn = Button(root, text='파일열기', command=open).pack()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

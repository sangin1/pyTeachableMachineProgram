from tkinter import *
from PIL import Image,ImageTk
from tkinter import filedialog
import PIL

def open():
    global photo # 함수에서 이미지를 기억하도록 전역변수 선언 (안하면 사진이 안보임)
    filename = filedialog.askopenfilename(initialdir='', title='파일선택', filetypes=(
    ('png files', '*.png'), ('jpg files', '*.jpg')))
    
    image = Image.open(filename)
    image = image.resize((224,224),PIL.Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    Label(root,image=photo).pack() 
 

root = Tk()

root.title("수박,멜론구별 프로그램")
root.geometry("600x400+300+300")

label1 = Label(root,text = "수박, 멜론사진을 올리면 판별합니다")
label1.pack()

 
my_btn = Button(root, text='파일열기', command=open).pack()


root.mainloop()

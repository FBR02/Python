import PIL
from PIL import Image, ImageTk
#import pytesseract
import cv2
from tkinter import *

width, height = 1920, 1080
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = Tk()
root.configure(height=height, width=width)
root.bind('<Escape>', lambda e: root.quit())

video_frame = LabelFrame(height=800, width=800, text="View", fg="white")
controls_frame = LabelFrame(height=800, width=200, text="Controls", fg="white")
lmain = Label(video_frame, text="IMAGE", fg="White")

video_frame.grid(row=0,column=0, padx=15, pady=15)
lmain.grid(row=0, column=0)
controls_frame.grid(row=0, column=1, padx=15, pady=15)

def show_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (780, 880)) #Resizes image
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converts color space
        frame = cv2.bitwise_not(frame) #Inverts colors
        (thresh, frame) = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img = PIL.Image.fromarray(frame) #Converts CV image to PIL iamge
        imgtk = PIL.ImageTk.PhotoImage(image=img) #Converts PIL to tkImage
        lmain.imgtk = imgtk #Assigns image to labe-imgtk name
        lmain.configure(image=imgtk) #Applys image to label
        lmain.after(50, show_frame)

show_frame()
root.mainloop()
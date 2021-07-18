import PIL
from PIL import Image, ImageTk
#import pytesseract
import cv2
import tkinter as tk
from Settings import *

class Viewer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.cap = cv2.VideoCapture(0)
        self.width, self.height = 1920, 1080
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.parent = parent  # self.parent.title is similar to root.title
        self.parent.configure(bg=BG)
        self.parent.title(TITLE)
    # Tkinter Variables
        self.freeze = tk.BooleanVar()
        self.gray_on = tk.BooleanVar()
        self.invert_on = tk.BooleanVar()
        self.bw_on = tk.BooleanVar()
    # Frames and Labels
        self.video_frame = tk.LabelFrame(height=800, width=800, text="View", fg=FG, bg=BG, font=INFOLBLFONT)
        self.controls_frame = tk.LabelFrame(text="Controls", fg=FG, bg=BG, font=INFOLBLFONT)
        self.controls_frame.configure(height=925, width=400)
        self.controls_frame.grid_propagate(0)
        self.lmain = tk.Label(self.video_frame, text="IMAGE", fg="White")
    # Var controls
        self.thresh_slide = tk.Scale(self.controls_frame, from_=0, to=255, orient="horizontal", label="Threshold", width=30, length=300)
        self.thresh_slide.set(150)
        self.invert_check = tk.Checkbutton(self.controls_frame, text="Invert", variable=self.invert_on, onvalue=True, offvalue=False, font=INFOLBLFONT)
        self.gray_check = tk.Checkbutton(self.controls_frame, text="Grayscale", variable=self.gray_on, onvalue=True, offvalue=False, font=INFOLBLFONT)
        self.bw_check = tk.Checkbutton(self.controls_frame, text="Blk/Wht", variable=self.bw_on, onvalue=True, offvalue=False, font=INFOLBLFONT)
        self.freeze_button = tk.Button(self.controls_frame, text="Freeze", command=self.freeze_command, bg=BG, fg=FG, font=BTNFONT)
    # Grid
        self.video_frame.grid(row=0, column=0, padx=15, pady=15)
        self.lmain.grid(row=0, column=0)
        self.controls_frame.grid(row=0, column=1, padx=15, pady=15)
        self.invert_check.grid(row=0, column=0)
        self.gray_check.grid(row=1, column=0)
        self.bw_check.grid(row=2, column=0)
        self.thresh_slide.grid(row=3, column=0, padx=15, pady=15)
        self.freeze_button.grid(row=4, column=0)


        self.show_frame()

    # Methods
    def freeze_command(self): #Sets freeze var to opposite of current
        self.freeze.set(not self.freeze.get())


    def show_frame(self):
        ret, frame = self.cap.read() # Pulls frame from device
        if ret: #If there is a frame
            if not self.freeze.get(): #If the user hasnt opted to freeze video capture
                frame = cv2.flip(frame, 1) #Grab the next video rame
                frame = cv2.resize(frame, (780, 880)) #Resizes image
                if self.gray_on.get(): #If grayscale is selected
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converts color space
                if self.invert_on.get(): #If invert is selected
                    frame = cv2.bitwise_not(frame) #Inverts colors
                if self.bw_on.get(): #If black white is selected
                    if not self.gray_on: #Check/set grapyscale on, fixes bug where BW only works with gray on
                        self.gray_on.set(True)
                        pass #Restart function call so that BW never attempts without gray on
                    frame = cv2.threshold(frame, self.thresh_slide.get(), 255, cv2.THRESH_BINARY)[1] #Drops image to threshold
                img = PIL.Image.fromarray(frame) #Converts CV image to PIL iamge
                imgtk = PIL.ImageTk.PhotoImage(image=img) #Converts PIL to tkImage
                self.lmain.imgtk = imgtk #Assigns image to label-imgtk name
                self.lmain.configure(image=imgtk) #Applys image to label
            self.lmain.after(50, self.show_frame) #Restarts function call making a updating loop



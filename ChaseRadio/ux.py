import tkinter as tk
from Settings import *
from datetime import datetime as dt
from datetime import timedelta as td
import requests
from bs4 import BeautifulSoup as bs
import urllib.request as ur
import urllib.error as ure

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.tx = False
        self.rmloc = 1
        self.curspeed = 1
        self.chaseloc = 100
        self.lastupdate = dt.now()
        self.theoloc = 1
        self.eta = 1
        self.estdist = 1

        self.parent = parent #self.parent.title is similar to root.title
        self.parent.configure(bg=BG)
        self.parent.geometry(RES)
        self.parent.title(TITLE)
#Radio Frame
        self.radioFrame = tk.LabelFrame(master=self.parent, bg=BG, text="Radio Control", fg=FG)
        self.radioFrame.grid(row=0, column=0, padx=30, pady=30, sticky="n")
    #Switches
        self.station1 = tk.Button(self.radioFrame, text="Switch", bg=BG, fg=FG, font=BTNFONT, padx=10, pady=5)
        self.station1.grid(row=0, column=0, padx=FRMPADX, pady=FRMPADY)
        self.station2 = tk.Button(self.radioFrame, text="Switch", bg=BG, fg=FG, font=BTNFONT, padx=10, pady=5)
        self.station2.grid(row=1, column=0, padx=FRMPADX, pady=FRMPADY)
        self.station3 = tk.Button(self.radioFrame, text="Switch", bg=BG, fg=FG, font=BTNFONT, padx=10, pady=5)
        self.station3.grid(row=2, column=0, padx=FRMPADX, pady=FRMPADY)
        self.transmitBtn = tk.Button(self.radioFrame, text="TX", bg=BG, fg=FG, font=BTNFONT, padx=10, pady=5)
        self.transmitBtn.grid(row=3, column=0, columnspan=2, padx=FRMPADX, pady=FRMPADY)
    #Radio Labels
        self.station1_label = tk.Label(self.radioFrame, text="Race Comms", font=BTNFONT, bg=BG, fg=FG)
        self.station1_label.grid(column=1, row=0, padx=FRMPADX, pady=FRMPADY)
        self.station2_label = tk.Label(self.radioFrame, text="Race Comms 2", font=BTNFONT, bg=BG, fg=FG)
        self.station2_label.grid(column=1, row=1, padx=FRMPADX, pady=FRMPADY)
        self.station3_label = tk.Label(self.radioFrame, text="Race Comms 3", font=BTNFONT, bg=BG, fg=FG)
        self.station3_label.grid(column=1, row=2, padx=FRMPADX, pady=FRMPADY)
#Sat Frames
        self.satFrame = tk.LabelFrame(master=self.parent, bg=BG, text="Live Info", fg=FG)
        self.satFrame.grid(row=0, column=1, padx=30, pady=30, sticky="n")
        self.satParam = tk.Frame(self.satFrame, bg=BG)
        self.satParam.grid(column=0, row=0)
        self.satValue = tk.Frame(self.satFrame, bg=BG)
        self.satValue.grid(column=1, row=0)
    #Sat Labels
        self.lstUpd_label = tk.Label(self.satParam, text="Last Update:", font=INFOLBLFONT, bg=BG, fg=FG)
        self.lstUpd_label.grid(column=0, row=0, padx=FRMPADX, pady=FRMPADY, sticky="w")
        self.curSpeed_label = tk.Label(self.satParam, text="Last Speed:", font=INFOLBLFONT, bg=BG, fg=FG)
        self.curSpeed_label.grid(column=0, row=1, padx=FRMPADX, pady=FRMPADY, sticky="w")
        self.curRM_label = tk.Label(self.satParam, text="Last RM:", font=INFOLBLFONT, bg=BG, fg=FG)
        self.curRM_label.grid(column=0, row=2, padx=FRMPADX, pady=FRMPADY, sticky="w")
        self.estLoc_label = tk.Label(self.satParam, text="Est. Loc:", font=INFOLBLFONT, bg=BG, fg=FG)
        self.estLoc_label.grid(column=0, row=3, padx=FRMPADX, pady=FRMPADY, sticky="w")
        self.estETA_label = tk.Label(self.satParam, text="Est. ETA:", font=INFOLBLFONT, bg=BG, fg=FG)
        self.estETA_label.grid(column=0, row=4, padx=FRMPADX, pady=FRMPADY, sticky="w")
        self.estDist_label = tk.Label(self.satParam, text="Est. Dist:", font=INFOLBLFONT, bg=BG, fg=FG)
        self.estDist_label.grid(column=0, row=5, padx=FRMPADX, pady=FRMPADY, sticky="w")
    #Sat Values
        self.lstUpd_v = tk.Label(self.satValue, text="00min", font=INFOLBLFONT, bg=BG, fg=FG)
        self.lstUpd_v.grid(column=0, row=0, padx=FRMPADX, pady=FRMPADY, sticky="e")
        self.curSpeed_v = tk.Label(self.satValue, text="00mph", font=INFOLBLFONT, bg=BG, fg=FG)
        self.curSpeed_v.grid(column=0, row=1, padx=FRMPADX, pady=FRMPADY, sticky="e")
        self.curRM_v = tk.Label(self.satValue, text="RM00", font=INFOLBLFONT, bg=BG, fg=FG)
        self.curRM_v.grid(column=0, row=2, padx=FRMPADX, pady=FRMPADY, sticky="e")
        self.estLoc_v = tk.Label(self.satValue, text="RM00", font=INFOLBLFONT, bg=BG, fg=FG)
        self.estLoc_v.grid(column=0, row=3, padx=FRMPADX, pady=FRMPADY, sticky="e")
        self.estETA_v = tk.Label(self.satValue, text="00mins", font=INFOLBLFONT, bg=BG, fg=FG)
        self.estETA_v.grid(column=0, row=4, padx=FRMPADX, pady=FRMPADY, sticky="e")
        self.estDist_v = tk.Label(self.satValue, text="00miles", font=INFOLBLFONT, bg=BG, fg=FG)
        self.estDist_v.grid(column=0, row=5, padx=FRMPADX, pady=FRMPADY, sticky="e")
#Chase Location Frame
        self.chaseRMFrame = tk.LabelFrame(master=self.parent, text="Chase Location", fg=FG, bg=BG)
        self.chaseRMFrame.grid(row=1, column=0, sticky="w", padx=30, pady=0)
    #Chase Location
        self.chaseLocLabel = tk.Label(master=self.chaseRMFrame, text="Chase RM location:", bg=BG, fg=FG, font=INFOLBLFONT)
        self.chaseLocLabel.grid(row=0, column=0, sticky="w", padx=FRMPADX, pady=FRMPADY)
        self.chaseInput = tk.Entry(master=self.chaseRMFrame, text="Enter location", width=10, bg=BG, fg=FG, font=INFOLBLFONT)
        self.chaseInput.grid(row=0, column=1, sticky="e", padx=40, pady=FRMPADY)


#Methods
    def start_tx(self, event):
        self.tx = True
        print("Transmit Start")

    def stop_tx(self, event):
        self.tx = False
        print("Transmit off")

    def update_stats(self):
        print("Updating stats")
        self.request_update()
        try:
            self.chaseloc = int(self.chaseInput.get())
        except:
            pass
    #Calculate amount of time since last succesful update
        diff_time = dt.now() - self.lastupdate
    #Converts time since last update into a floating number
        time_float = diff_time.total_seconds() / 3600
    #Calculates theoretical location
        self.theoloc = round(self.rmloc + (time_float * self.curspeed), 1)
    #Calculate distance to arrival
        self.estdist = round(self.chaseloc - self.theoloc, 1)
    #Calculate ETA
        if self.curspeed > 0:
            eta_time = self.estdist / self.curspeed
            self.eta = str(td(hours=eta_time))
            self.eta = str(self.eta).split(".")[0]
        else:
            self.eta = "Not Moving"

    #Prints the dta to the frame
        self.lstUpd_v.config(text=str(diff_time).split(".")[0])
        self.curSpeed_v.config(text=f"{self.curspeed}mph")
        self.curRM_v.config(text=f"{self.rmloc}RM")
        self.estLoc_v.config(text=f"{self.theoloc}RM")
        self.estDist_v.config(text=f"{self.estdist}mi")
        self.estETA_v.config(text=self.eta)
        self.after(1000, self.update_stats)

    def request_update(self):
        print("Requesting data from web")
        if self.check_internet() == True:
            try:
                page = requests.get(URL)
                print(page)
            except:
                pass
            else:
                site = page.text
                html = bs(site, "html.parser")
                self.lastupdate = dt.now()
                stats = html.find_all("td")
                info = {stats[i].getText(): stats[i + 1].getText() for i in range(0, len(stats), 2)}
                self.curspeed = float(info["Current speed"].split(" ")[0])
                self.rmloc = float(info["Route mile"].split(" ")[0])

    def check_internet(self):
        try:
            req = ur.Request(URL)
            response = ur.urlopen(req, timeout=2)
            print(response)
            return True
        except ure.URLError as err:
            return False









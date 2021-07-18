from tkinter import *
from tkinter import filedialog as fd
from csv import DictReader
import subprocess, signal, os, time, requests, json
import liveTracking

def liveUpdate(link):
    liveUpdateDict = liveTracking.getTracking(liveUpdateDict)
    print(text)
    trackerlText.configure(state='normal')
    trackerlText.delete(1.0, END)
    trackerlText.insert(END, text)
    trackerlText.configure(state='disabled')
    root.after(15000, liveUpdate, liveUpdateDict)

def newstation(station, sr, gn, sq):
    global process, stnum
    rate = round(sr / 2)
    # create a rtl_fm command line string and insert the new freq
    part1 = "rtl_fm -M fm -f "
    part2 = "e6 -s " + str(sr) + " -r " + str(rate) + " -g " + str(gn) + " -l " + str(sq) + "| aplay -r " + str(rate) +" -f S16_LE"
    cmd = part1 + str(station) + part2
    print ('\nChanging station :', station)
    print ("Sample Rate: " + str(sr))
    print ("Gain: " + str(gn))
    print ("Squelch: " + str(sq), "\n")
    # kill the old fm connection if it was running
    if process != 0:
        try:
            process = int(subprocess.check_output(["pidof","rtl_fm"]))
        except:
            print('Process not found')
            process = 0
        print ("Process pid = ", process)
        if process != 0:
            os.kill(process,signal.SIGINT)
            time.sleep(2) # wait 2 seconds to restart rtl_fm
    # start the new fm connection
    print (cmd)
    #process = subprocess.Popen(cmd, shell=True)#takes all inputs and executes rtl_fm with args

def clickb1():
    b1.configure(bg="red", fg="black", text="Listen")
    b2.configure(bg="black", fg="white", text="Switch")
    b3.configure(bg="black", fg="white", text="Switch")
    print("BEGIN DEBUG")
    newstation(channel1Dict.get('Freq'), samVar.get(), gnVar.get(), sqVar.get())#Dials to new channel based on corresponding drop down
    channelText.configure(state='normal')
    channelText.delete(1.0, END)
    channelText.insert(END, getCallInfo(channel1Dict))
    channelText.configure(state='disabled')
    liveUpdateDict["link"] = channel1Dict["Link"]
    liveUpdate(liveUpdateDict)

def clickb2():
    b1.configure(bg="black", fg="white", text="Switch")
    b2.configure(bg="red", fg="black", text="Listen")
    b3.configure(bg="black", fg="white", text="Switch")
    newstation(channel2Dict.get("Freq"), samVar.get(), gnVar.get(), sqVar.get())#Dial
    channelText.configure(state='normal')
    channelText.delete(1.0, END)
    channelText.insert(END, getCallInfo(channel2Dict))
    channelText.configure(state='disabled')

def clickb3():
    b1.configure(bg="black", fg="white", text="Switch")
    b2.configure(bg="black", fg="white", text="Switch")
    b3.configure(bg="red", fg="black", text="Listen")
    newstation(channel3Dict.get("Freq"), samVar.get(), gnVar.get(), sqVar.get())#Dial    channelText.configure(state='normal')
    channelText.configure(state='normal')
    channelText.delete(1.0, END)
    channelText.insert(END, getCallInfo(channel3Dict))
    channelText.configure(state='disabled')

def opmenu1(dial):
    global channel1Dict
    for ch in channelList:
        if ch.get("Name") == dial:
            channel1Dict = ch
            channel1.set(ch.get("Name"))
            b1l.configure(text=ch.get("Freq"))#Changes label next to drop down to selected channel name

def opmenu2(dial):
    global channel2Dict
    for ch in channelList:
        if ch.get("Name") == dial:
            channel2Dict = ch
            channel2.set(ch.get("Name"))
            b2l.configure(text=ch.get("Freq"))

def opmenu3(dial):
    global channel3Dict
    for ch in channelList:
        if ch.get("Name") == dial:
            channel3Dict = ch
            channel3.set(ch.get("Name"))
            b3l.configure(text=ch.get("Freq"))#C

def kill():
    global process
    try:
        process = int(subprocess.check_output(["pidof","rtl_fm"]))
    except:
        print('\nProcess not found\n')
        process = 0
    if process != 0:
        print('\nrtl_fm found, killing\n')
        os.kill(process, signal.SIGINT)
        time.sleep(2)
    b1.configure(bg="black", fg="white", text="Switch")
    b2.configure(bg="black", fg="white", text="Switch")
    b3.configure(bg="black", fg="white", text="Switch")#Kills rtl_fm if running

def returnChannelList(list):
    chs = []
    for ch in list:
        chs.append(ch.get('Name'))
    return chs#Feed channel list, return just the names of channels

def loadchannels():
    global channelList
    filename = fd.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    with open(filename, 'r') as read_obj:
        dict_reader = DictReader(read_obj)
        list_of_dict = list(dict_reader)
        channelList = list_of_dict
    drop1.children["menu"].delete(0, "end")
    drop2.children["menu"].delete(0, "end")
    drop3.children["menu"].delete(0, "end")
    for value in returnChannelList(channelList):
        drop1.children["menu"].add_command(label=value, command=lambda v=value: opmenu1(v))
        drop2.children["menu"].add_command(label=value, command=lambda v=value: opmenu2(v))
        drop3.children["menu"].add_command(label=value, command=lambda v=value: opmenu3(v))

def getCallInfo(dictItem):
    if dictItem.get("chanType") == "R":
        try:
            query = {'searchValue':'', 'format' : 'json'}
            query['searchValue'] = dictItem.get("Name")
            data2 = requests.get('https://www.repeaterbook.com/api/export.php?country=United%20States&callsign=' + query['searchValue']).text
            data2 = json.loads(data2)
            cs = 'Call Sign: ' + data2['results'][0]['Callsign']
            st = '\nState: ' + data2['results'][0]['State']
            ct = '\nCounty: ' + data2['results'][0]['County']
            oFreq = '\nListen Freq: ' + data2['results'][0]['Frequency']
            iFreq = '\nTalk Freq: ' + data2['results'][0]['Input Freq']
            lat = '\nLattitude: ' + data2['results'][0]['Lat']
            long = '\nLongitude: ' + data2['results'][0]['Long']
            return (cs + st + ct + oFreq + iFreq + lat + long)
        except:
            return "Information not found in repeater book API"
    if dictItem.get("chanType") == "B":
        return "This is a broadcast FM station, currently no data available"
    if dictItem.get("chanType") == "C":
        info = ""
        try:
            for key in dictItem:
                if key != "chanType" and key != "Link":
                    info = info + key + ": " + dictItem[key] + "\n"
            return info
        except:
            return "Error retrieving car information"

    return "Invalid CSV channel type selection"
#==========================================
process = 0#Init process as 0 as placeholder

print('\nStarted application, waiting for input\n')

liveUpdateDict = {
    "link" : "",
    "nextLoc" : "",
    "Last Sat Update" : "",
    "Current Speed" : "",
    "Current Location" : ""
    "Distance to Next" : ""
}

channelList = [
    {'name' : 'None Loaded', 'freq' : ''}]

root = Tk()
root.configure(bg='#333300')
root.title('Radio App')
#Open channel CSV list
topmenu = Menu(root, bg='black', fg='white')
fileMenu = Menu(topmenu)
fileMenu.add_command(label="Load Channels", command = loadchannels)
topmenu.add_cascade(label = "File", menu = fileMenu)

channel1 = StringVar()
channel2 = StringVar()
channel3 = StringVar()
channel1.set("None")
channel2.set("None")
channel3.set("None")

channel1Dict = {}
channel2Dict = {}
channel3Dict = {}

samVar = IntVar()
gnVar = IntVar()
sqVar = IntVar()

channelInfoFrame = LabelFrame(root, text='Channel Info', padx=5, pady=5, bg='black', fg='white')
channelInfoFrame.grid_propagate(0)
channelInfoFrame.grid(row=0, column=3, rowspan=6, padx=15)

carTrackerFrame = LabelFrame(root, text='Live Info', padx=5, pady=5, bg='black', fg='white')
carTrackerFrame.grid_propagate(0)
carTrackerFrame.grid(row=0, column=4, rowspan=6, padx=15)

channelText = Text(channelInfoFrame, bg='black', fg='white', state='disabled')
channelText.grid_propagate(0)
channelText.configure(width=25, height=18)
channelText.pack()

trackerlText = Text(carTrackerFrame, bg='black', fg='white', state='disabled')
trackerlText.grid_propagate(0)
trackerlText.configure(width=25, height=18)
trackerlText.pack()


#Init all the drop down menus
drop1 = OptionMenu(root, channel1, *returnChannelList(channelList), command=opmenu1)
drop1.configure(bg='black', fg='white')
drop1.grid(row=0, column=2)

drop2 = OptionMenu(root, channel2, *returnChannelList(channelList), command=opmenu2)
drop2.configure(bg='black', fg='white')
drop2.grid(row=1, column=2)

drop3 = OptionMenu(root, channel3, *returnChannelList(channelList), command=opmenu3)
drop3.configure(bg='black', fg='white')
drop3.grid(row=2, column=2)
#Init all the buttons
b1l = Label(root, text = "None Selected")
b1l.configure(bg='#333300', fg='white', font=24, padx=25, pady=25)
b1l.grid(row=0, column=1)

b2l = Label(root, text = "None Selected")
b2l.configure(bg='#333300', fg='white', font=24, padx=25, pady=25)
b2l.grid(row=1, column=1)

b3l = Label(root, text = "None Selected")
b3l.configure(bg='#333300', fg='white', font=24, padx=25, pady=25)
b3l.grid(row=2, column=1)
#Init all buttons
b1 = Button(root, text = 'Switch', bg = "black", fg= "white", command = clickb1)
b1.grid(row=0, column=0, padx=10)

b2 = Button(root, text = 'Switch', bg = "black", fg= "white", command = clickb2)
b2.grid(row=1, column=0, padx=10)

b3 = Button(root, text = 'Switch', bg = "black", fg= "white", command = clickb3)
b3.grid(row=2, column=0, padx=10)

killSta = Button(root, padx=10, pady=10, text = 'Close Radio Connections', bg = "black", fg= "white", command=kill)
killSta.grid(row=3, column=1, pady=10)
#Init lower entry fields
settingsFrame = LabelFrame(root,  text='Settings', padx=5, pady=5, bg='black', fg='white')
settingsFrame.grid(row=4 ,column=0, columnspan=3, pady=10)

sampleRate = Entry(settingsFrame,width=8, bg='black', fg='white', text='12500', textvariable=samVar)
sampleRate.insert(0, "1250")
srLbl = Label(settingsFrame, bg='black', fg='white', font=24, padx=5, pady=5, text='Samples/s')
sampleRate.grid(row=1, column=0, padx=10, pady=1)
srLbl.grid(row=0, column=0)

gain = Entry(settingsFrame, width=8, bg='black', fg='white', text='Gain', textvariable=gnVar)
gainLbl = Label(settingsFrame, bg='black', fg='white', font=24, padx=5, pady=5, text='Gain')
gain.grid(row=1, column=1, padx=10, pady=1)
gainLbl.grid(row=0, column=1)

squelch = Entry(settingsFrame, width=8, bg='black', fg='white', text='Squelch', textvariable=sqVar)
sqLbl = Label(settingsFrame, bg='black', fg='white', font=24, padx=5, pady=5, text='Squelch')
squelch.grid(row=1, column=2, padx=10, pady=1)
sqLbl.grid(row=0, column=2)

root.config(menu=topmenu)
root.mainloop()

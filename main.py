import tkinter as tk
from tkinter import *
import sys
import datetime
import time
import csv
import tkFont

from dronekit import connect, VehicleMode, Command, LocationGlobal
from pymavlink import mavutil


#set up csv file
global csvtog
csvtog = False

global csvfile
timename = time.strftime('%y-%m-%d___%H_%M_%S')
csvfile = open('SAE_Data_' + timename + '.csv','wb')

thiswriter = csv.writer(csvfile, delimiter = ' ', quoting=csv.QUOTE_MINIMAL)
thiswriter.writerow(['Time:             ' , 'Ground speed:        ', 'Roll:               ', 'Pitch:                  ', 'Altitude:               '])

# Connect to vehicle
connectionString = "com4"
print "Connecting on: ",connectionString
vehicle = connect(connectionString, wait_ready=["groundspeed","attitude","location.global_relative_frame"], baud=57600)

window = tk.Tk()

window.title('LMU AirLions')
#You can set the geometry attribute to change the root windows size
window.geometry("1540x840") #You want the size of the app to be 500x500

back = tk.Frame(window,bg='black')
window.configure(background='black')

helv46 = tkFont.Font(family='Verdana', size=120)
helv = tkFont.Font(family='Verdana', size= 55)
data_x = 1010
data_y = 165

label_x = 925
label_y = 100

verd24 = tkFont.Font(family='Verdana', size=24)


# gets the altitude information
alt_label = Label(text = "Altitude (ft)", font = verd24, bg = 'black', fg = 'white')
alt_label.place(x=label_x,y=label_y)
alt1 = ''
telem = Label(window, font = helv46, bg = 'black', fg = 'yellow')
telem.pack(fill= BOTH, expand = 1)
telem.place(x=data_x-60, y=label_y+40)


# gets the grounding speed information
speed_label = Label(text = "Speed (ft/s)", font = verd24 ,bg = 'black', fg = 'white')
speed_label.place(x = label_x+300, y = label_y)
speed1 = ''
speed_text = Label(window, font = helv46, bg = 'black', fg = 'orange')
speed_text.pack(fill= BOTH, expand = 1)
speed_text.place(x=data_x+300-40, y=label_y+40)


# get latitude
lat_label = Label(text = " Latitude", font = verd24, bg = 'black', fg = 'white')
lat_label.place(x = label_x, y=label_y+180+60)
lat1 = ''
lat_info = Label(window, font = helv, bg = 'black', fg = 'lime green')
lat_info.pack(fill= BOTH, expand = 1)
lat_info.place(x= data_x-150, y=label_y+180+65+60)


# get longitude
long_label = Label(text = " Longitude", font = verd24, bg = 'black', fg = 'white')
long_label.place(x=label_x + 300, y=label_y+180+60)
long1 = ''
long_info = Label(window, font = helv, bg = 'black', fg = 'red2')
long_info.pack(fill= BOTH, expand = 1)
long_info.place(x=data_x+120, y=label_y+180+65+60)


# make a time stamp
global time1
time1 = ''
global clock
clock = Label(window, font=('Verdana', 26), bg='black', fg = 'white')
clock.pack(fill=BOTH, expand=1)
clock.place(x=1100,y=20)


#If you have a large number of widgets, like it looks like you will for your
#game you can specify the attributes for all widgets simply like this.
window.option_add("*Button.Background", "white")
window.option_add("*Button.Foreground", "red")

# create font size
helv36 = tkFont.Font(family='Verdana', size=16)
btn_x = 30
btn_y = 740


#Main loop, calls every 
#
#

def tick():
    global time1
    global clock
    # get the current local time from the PC
    time2 = time.strftime('%y-%m-%d %H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    getFlightData()
    clock.after(200,tick)
    


# get flight data
def getFlightData():
    groundSpeed = vehicle.groundspeed
    groundSpeed = int(groundSpeed*3.28084)
    roll = vehicle.attitude.roll
    pitch = vehicle.attitude.pitch
    altitude = vehicle.location.global_relative_frame.alt
    altitude = int(altitude*3.28084)


    lat2 = round(vehicle.location.global_frame.lat, 3)
    long2 = round(vehicle.location.global_frame.lon, 3)

    
    if altitude < 0:    # Dont let the dropTime become imaginary
        altitude = 0

    global csvtog

    if csvtog:
        timeNow = time.strftime('%y-%m-%d %H:%M:%S')
        global csvfile
        thiswriter = csv.writer(csvfile, delimiter = ' ', quoting=csv.QUOTE_MINIMAL)
        thiswriter.writerow([timeNow ,'____', groundSpeed,'_____', roll,'_____', pitch,'_____', altitude])

    updateHUD(groundSpeed, roll, pitch, altitude,lat2,long2)

    return (groundSpeed, roll, pitch, altitude,lat2,long2)


def updateHUD(groundSpeed, roll, pitch, altitude,lat2,long2):
    telem.config(text = altitude)

    speed_text.config(text = groundSpeed)
    
    lat_info.config(text = lat2)
    
    long_info.config(text = long2)

    return
    
# create the functions that display which payload was dropped
def CDA():    
    CDA_label = Label(text = "CDA", font = ('Verdana', 100), fg = 'white', bg = 'black').place(x=100,y=150)
    return

def supply():
    supply_label = Label(text = "Supplies", font = ('Verdana', 100), fg = 'white', bg = 'black').place(x = 100,y=150)
    return        

def habitat():
    habitat_label = Label(text = altitude, font = ('Verdana', 100), fg = 'white', bg = 'black').place(x=100,y=150)
    return

def toggleCSV():
    global csvtog
    csvtog = not csvtog
    if csvtog:
        #global CSV_button
        CSV_button.config(text = 'Stop Logging')
    else:
        CSV_button.config(text = 'Log Data')
    return

def quitcommand():
    global csvfile
    csvfile.close()
    window.destroy()
    return


# create buttons for dropping the payloads
CDA_button = tk.Button(window, text = "CDA", command = CDA, font = helv36, height = 2, width = 12, fg = "white", borderwidth = 0, bg = 'grey30')
CDA_button.place(x = btn_x, y = btn_y)

CSV_button = tk.Button(window, text = "Log Data", command = toggleCSV, font = helv36, height = 2, width = 12, fg = "white", borderwidth = 0, bg = 'grey30')
CSV_button.place(x = btn_x, y = btn_y-175)

supply_button = Button(window, text = "Supplies", command = supply, font = helv36, height = 2, width = 12, fg = "white", borderwidth = 0, bg = 'grey30')
supply_button.place(x = btn_x + 175, y = btn_y)

habitat_button = Button(window, text = "Habitat", command = habitat, font = helv36, height = 2, width = 12, fg = "white", borderwidth = 0, bg = 'grey30')
habitat_button.place(x = btn_x + 175+175, y = btn_y)

stop = Button(window, text = "Quit", command = quitcommand, font = helv36, height = 2, width = 12, fg = "red", borderwidth = 0, bg = 'grey30')
stop.place(x = btn_x+3*175, y = btn_y)




tick()

window.mainloop()

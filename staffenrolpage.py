import random
import time
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from PIL import ImageTk, Image
from tkinter import PhotoImage
import tkinter.filedialog
import pandas as pd
import numpy as np
import re
import os
import math
import sys
import smtplib
import matplotlib.pyplot as plt
from uuid import uuid4
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.scrolledtext import ScrolledText

import sqlite3

window = Tk()
window.title("Staff Enrollment Page")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

#=============================Window setting=========================================================

window.resizable(0, 0)  # Delete the restore button
window_height = 750
window_width = 1350

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

#==============================Database==============================================================
conn = sqlite3.connect("SE Project.unknown")
cursor = conn.cursor()

cursor.execute("SELECT Training_Venue, Date, Time, Department FROM Add_Training")
training_data = cursor.fetchone()  # Fetches the first row of data



#===========================Set Frame==================================================================



staff_emroll_page = Frame(window)  # Renamed frame

for frame in (staff_emroll_page,):  # Added staff_emroll_page frame
    frame.grid(row=0, column=0, sticky='nsew')



def show_frame(frame):
    frame.tkraise()

show_frame(staff_emroll_page)

staff_emroll_page.config()

st_transFrame = Frame(staff_emroll_page, bg='white', highlightthickness=1)
st_transFrame.place(x=150, y=20, height=715, width=1200)

# Create the label
trainlabel = Label(st_transFrame, text='TRAINING', font=('Arial', 35), fg='#2181AA', bg='white')
trainlabel.place(x=0, y=15, width=400)


# Extract the values from the training_data tuple
venue_ep = training_data[0]
date_ep = training_data[1]
time_ep = training_data[2]
department_ep = training_data[3]



venue_label = Label(st_transFrame, text='Venue:', font=('Arial', 20), fg='#2181AA', bg='white')
venue_label.place(x=50, y=100)

venue_value_label = Label(st_transFrame, text=venue_ep, font=('Arial', 19), fg='#2181AA', bg='white')
venue_value_label.place(x=220, y=103)

date_label = Label(st_transFrame, text='Date:', font=('Arial', 20), fg='#2181AA', bg='white')
date_label.place(x=50, y=150)

date_value_label = Label(st_transFrame, text=date_ep, font=('Arial', 19), fg='#2181AA', bg='white')
date_value_label.place(x=220, y=150)

time_label = Label(st_transFrame, text='Time:', font=('Arial', 20), fg='#2181AA', bg='white')
time_label.place(x=50, y=200)

time_value_label = Label(st_transFrame, text=time_ep, font=('Arial', 19), fg='#2181AA', bg='white')
time_value_label.place(x=220, y=200)

department_label = Label(st_transFrame, text='Department:', font=('Arial', 20), fg='#2181AA', bg='white')
department_label.place(x=50, y=250)

department_value_label = Label(st_transFrame, text=department_ep, font=('Arial', 19), fg='#2181AA', bg='white')
department_value_label.place(x=220, y=253)




program_flow_label = Label(st_transFrame, text='Program Flow:', font=('Arial', 20), fg='#2181AA', bg='white')
program_flow_label.place(x=50, y=300)



# Create a box under the program flow label
box_canvas_ep = Canvas(st_transFrame, width=800, height=250, bg='white', highlightthickness=1, highlightbackground='black')
box_canvas_ep.place(x=250, y=350)


# Create a new frame for the Register button
register_button_frame_ep = Frame(st_transFrame, bg='#7AB8F0')
register_button_frame_ep.place(x=500, y=650, width=120, height=30)

# Function to handle the register button click
def register_button_ep_clicked():
    message = "You have been registered to this training"
    messagebox.showinfo("Registration Successful", message)


# Add the register button
register_button_ep = Button(register_button_frame_ep, text="Register", bg='#2181AA', fg='white', font=('Arial', 12), relief='flat', command=register_button_ep_clicked)
register_button_ep.pack(fill=BOTH, expand=True)

#placing frame for menu bar left
menuFrame = Frame(staff_emroll_page, bg='#2181AA', width=170, height=715, highlightbackground='black', highlightthickness=1)
menuFrame.place(x=0, y=20)

# Defining the buttons for menu bar in Home page left
home_icon = PhotoImage(file="images/home_icon.png")
train_sch_icon = PhotoImage(file="images/ts_icon.png")
train_list_icon = PhotoImage(file="images/ls_icon.png")
logout_icon = PhotoImage(file="images/logout_icon.png")

home_b = Button(
    menuFrame, text="Home", image=home_icon, compound=TOP, bg='#2181AA', relief='flat', fg='white',
    font=('yu gothic ui', 13))


Training_Sch_b = Button(
    menuFrame, text="Training \nSchedule", image=train_sch_icon, compound=TOP, bg='#2181AA', relief='flat',
    fg='white', font=('yu gothic ui', 13))

train_list_b = Button(
    menuFrame, text="List of Training", image=train_list_icon, compound=TOP, bg='#2181AA',
    relief='flat', fg='white', font=('yu gothic ui', 13))

logout_b = Button(
    menuFrame, text="Log Out", image=logout_icon, compound=TOP, bg='#2181AA', relief='flat', fg='white',
    font=('yu gothic ui', 13))

# Placing buttons in menu bar Home Page
home_b.place(x=11, y=20, width=150)
train_list_b.place(x=11, y=130, width=150)
Training_Sch_b.place(x=11, y=240, width=150)
logout_b.place(x=11, y=370, width=150)

conn.close()

window.mainloop()
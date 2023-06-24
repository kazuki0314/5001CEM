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
window.title("HR Home Page")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

# =============================Window setting=========================================================

window.resizable(0, 0)  # Delete the restore button
window_height = 750
window_width = 1350

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


# ==============================Database==============================================================
conn = sqlite3.connect("SE Project.unknown")  # Replace "your_database.db" with your actual database file name
cursor = conn.cursor()

# ===========================Set Frame==================================================================

hrhomepage = Frame(window)
hrhomepage.grid(row=0, column=0, sticky='nsew')


def show_frame(frame):
    frame.tkraise()


show_frame(hrhomepage)

hrhomepage.config()

hrhome = Frame(hrhomepage, bg='white', highlightthickness=1)
hrhome.place(x=150, y=20, height=715, width=1200)

# Create the label
hplabel = Label(hrhome, text='Hello, Person', font=('Arial', 40), fg='#E84966', bg='white')
hplabel.place(x=400, y=15, width=400)

twlabel = Label(text='This Week', font=('Arial', 15, 'bold'), fg='#E84966', bg='white')
twlabel.place(x=198, y=115)

hrbackframe = Frame(hrhome, bg='white')
hrbackframe.place(x=40, y=85, height=600, width=1115)

# Table

# Add some style
style = ttk.Style()

style.theme_use("clam")
style.configure("Treeview.Heading", background="#E84966", foreground='white', rowheight=100)

hrhometree = ttk.Treeview(
    hrbackframe,
    selectmode="extended",
    show='headings',
    columns=('Training Name', 'Venue', 'Date', 'Time', 'No. Participants'),
    style="style1.Treeview"
)
hrhometree.place(x=20, y=60, relwidth=0.97, relheight=0.82)

# Configure horizontal and vertical scrollbar for treeview
x_scroller = Scrollbar(hrhometree, orient=HORIZONTAL, command=hrhometree.xview)
y_scroller = Scrollbar(hrhometree, orient=VERTICAL, command=hrhometree.yview)
x_scroller.pack(side=BOTTOM, fill=X)
y_scroller.pack(side=RIGHT, fill=Y)
hrhometree.config(yscrollcommand=y_scroller.set, xscrollcommand=x_scroller.set)

# Set heading name for treeview column
hrhometree.heading('Training Name', text='Training Name', anchor=CENTER)
hrhometree.heading('Venue', text='Venue', anchor=CENTER)
hrhometree.heading('Date', text='Date', anchor=CENTER)
hrhometree.heading('Time', text='Time', anchor=CENTER)
hrhometree.heading('No. Participants', text='No. Participants', anchor=CENTER)

hrhometree.column("Training Name", anchor=CENTER, width=100)
hrhometree.column("Venue", anchor=CENTER, width=100)
hrhometree.column("Date", anchor=CENTER, width=100)
hrhometree.column("Time", anchor=CENTER, width=100)
hrhometree.column("No. Participants", anchor=CENTER, width=100)

# Retrieve data from the database
cursor.execute("SELECT Traning_Name,Training_Venue, Date, Time, No_Of_Participant FROM Add_Training")
training_data = cursor.fetchall()  # Fetches all the rows of data

# Insert data into the treeview
for row in training_data:
    hrhometree.insert('', 'end', values=row)


# Placing frame for menu bar left
menuFrame = Frame(hrhomepage, bg='#E84966', width=170, height=715, highlightthickness=1)
menuFrame.place(x=0, y=20)

# Defining the buttons for menu bar in Home page left
home_icon = PhotoImage(file="images/home_icon.png")
add_train_icon = PhotoImage(file="images/at_icon.png")
train_sch_icon = PhotoImage(file="images/ts_icon.png")
list_staff_icon = PhotoImage(file="images/ls_icon.png")
enrol_req_icon = PhotoImage(file="images/er_icon.png")
logout_icon = PhotoImage(file="images/logout_icon.png")

home_b = Button(
    menuFrame,
    text="Home",
    image=home_icon,
    compound=TOP,
    bg='#E84966',
    relief='flat',
    fg='white',
    font=('yu gothic ui', 13),
    activebackground='#74bc94'
)
add_training_b = Button(
    menuFrame,
    text="Add Training",
    image=add_train_icon,
    compound=TOP,
    bg='#E84966',
    relief='flat',
    fg='white',
    font=('yu gothic ui', 13),
    activebackground='#74bc94'
)
Training_Sch_b = Button(
    menuFrame,
    text="Training \nSchedule",
    image=train_sch_icon,
    compound=TOP,
    bg='#E84966',
    relief='flat',
    fg='white',
    font=('yu gothic ui', 13),
    activebackground='#74bc94'
)
list_staff_b = Button(
    menuFrame,
    text="List of Staff",
    image=list_staff_icon,
    compound=TOP,
    bg='#E84966',
    relief='flat',
    fg='white',
    font=('yu gothic ui', 13),
    activebackground='#74bc94'
)
Enrollment_req_b = Button(
    menuFrame,
    text="Enrollment \nRequest",
    image=enrol_req_icon,
    compound=TOP,
    bg='#E84966',
    relief='flat',
    fg='white',
    font=('yu gothic ui', 13),
    activebackground='#74bc94'
)
logout_b = Button(
    menuFrame,
    text="Log Out",
    image=logout_icon,
    compound=TOP,
    bg='#E84966',
    relief='flat',
    fg='white',
    font=('yu gothic ui', 13),
    activebackground='#74bc94'
)

# Placing buttons in menu bar Home Page
home_b.place(x=11, y=20, width=150)
add_training_b.place(x=11, y=110, width=150)
Training_Sch_b.place(x=11, y=220, width=150)
list_staff_b.place(x=11, y=350, width=150)
Enrollment_req_b.place(x=11, y=440, width=150)
logout_b.place(x=11, y=570, width=150)

window.mainloop()

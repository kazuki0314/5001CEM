import random
import time
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from PIL import ImageTk, Image  # pip install pillow
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
window.title("Staff Training List Page")
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
conn = sqlite3.connect("SE Project.unknown")  # Replace "your_database.db" with your actual database file name
cursor = conn.cursor()

#===========================Set Frame==================================================================

staff_training_list = Frame(window)

for frame in (staff_training_list,):
    frame.grid(row=0, column=0, sticky='nsew')


def show_frame(frame):
    frame.tkraise()


show_frame(staff_training_list)

staff_training_list.config()

sftrainlist = Frame(staff_training_list, bg='white', highlightthickness=1)
sftrainlist.place(x=150, y=20, height=715, width=1200)

# Create the label
tl_label = Label(sftrainlist, text='TRAINING LIST', font=('Arial', 35), fg='#2181AA', bg='white')
tl_label.place(x=30, y=15, width=400)

# Search area
search_area_frame = Frame(sftrainlist, bg='#7AB8F0')
search_area_frame.place(x=60, y=80, width=300, height=40)

search_icon = PhotoImage(file="images/search_icon_2.png")
search_label = Label(search_area_frame, image=search_icon, bg='#7AB8F0')
search_label.pack(side=RIGHT, padx=5)

search_textlsp = Entry(search_area_frame, bg='#7AB8F0', font=('Arial', 12), relief='flat')
search_textlsp.pack(side=LEFT, padx=5)

# Create a new frame for the search button
search_button_frame = Frame(sftrainlist, bg='#7AB8F0')
search_button_frame.place(x=400, y=85, width=80, height=30)


def search_button_lps_clicked():
    search_text_value = search_textlsp.get().lower()  # Get the search text from the entry and convert to lowercase

    # Retrieve data from the database
    cursor.execute("SELECT Traning_Name,Training_Venue, Date, Time, No_Of_Participant FROM Add_Training")
    training_data = cursor.fetchall()  # Fetch all the rows of data

    # Filter the data based on the search text
    filtered_data = []
    for row in training_data:
        if (
            search_text_value in str(row[0]).lower()  # Convert row[0] to string and then apply lower()
            or search_text_value in str(row[1]).lower()
            or search_text_value in str(row[2]).lower()
            or search_text_value in str(row[3]).lower()
            or search_text_value in str(row[4]).lower()
        ):
            filtered_data.append(row)

    # Clear the Treeview
    sttranstree.delete(*sttranstree.get_children())

    # Insert the filtered data into the Treeview
    for row in filtered_data:
        sttranstree.insert("", "end", values=row)


search_button_lps = Button(
    search_button_frame, text="Search", bg='#2181AA', fg='white', font=('Arial', 12), relief='flat',
    command=search_button_lps_clicked)
search_button_lps.pack(fill=BOTH, expand=True)


def search_button_lps_clicked():
    search_text_value = search_textlsp.get().lower()  # Get the search text from the entry and convert to lowercase

    # Retrieve data from the database
    cursor.execute("SELECT Traning_Name,Training_Venue, Date, Time, No_Of_Participant FROM Add_Training")
    training_data = cursor.fetchall()  # Fetch all the rows of data

    # Filter the data based on the search text
    filtered_data = []
    for row in training_data:
        if (
            search_text_value in str(row[0]).lower()  # Convert row[0] to string and then apply lower()
            or search_text_value in str(row[1]).lower()
            or search_text_value in str(row[2]).lower()
            or search_text_value in str(row[3]).lower()
            or search_text_value in str(row[4]).lower()
        ):
            filtered_data.append(row)

    # Clear the Treeview
    sttranstree.delete(*sttranstree.get_children())

    # Insert the filtered data into the Treeview
    for row in filtered_data:
        sttranstree.insert("", "end", values=row)


# Create a new frame for the select button
lspselect_button_frame = Frame(sftrainlist, bg='#7AB8F0')
lspselect_button_frame.place(x=950, y=80, width=95, height=30)

# Add the select button
select_button_stl = Button(lspselect_button_frame, text="Select", bg='#2181AA', fg='white', font=('Arial', 12), relief='flat')
select_button_stl.pack(fill=BOTH, expand=True)

backfram = Frame(sftrainlist, bg='white')
backfram.place(x=40, y=130, height=555, width=1115)

# Table
# Add some style:
style = ttk.Style()
style.configure("style1.Treeview", borderwidth=0, relief="flat", background="white")
style.theme_use("clam")
style.configure("style1.Treeview.Heading", background="#2181AA", foreground='white', rowheight=100)

sttranstree = ttk.Treeview(
    backfram,
    selectmode="extended",
    show='headings',
    columns=('Training Name', 'Venue', 'Date', 'Time', 'No. Participants'),
    style="style1.Treeview"
)
sttranstree.place(x=20, y=0, relwidth=0.97, relheight=1)

# configure horizontal and vertical scrollbar for treeview
x_scroller = Scrollbar(sttranstree, orient=HORIZONTAL, command=sttranstree.xview)
y_scroller = Scrollbar(sttranstree, orient=VERTICAL, command=sttranstree.yview)
x_scroller.pack(side=BOTTOM, fill=X)
y_scroller.pack(side=RIGHT, fill=Y)
sttranstree.config(yscrollcommand=y_scroller.set, xscrollcommand=x_scroller.set)

# set heading name for treeview column
sttranstree.heading('Training Name', text='Training Name', anchor=CENTER)
sttranstree.heading('Venue', text='Venue', anchor=CENTER)
sttranstree.heading('Date', text='Date', anchor=CENTER)
sttranstree.heading('Time', text='Time', anchor=CENTER)
sttranstree.heading('No. Participants', text='No. Participants', anchor=CENTER)

sttranstree.column("Training Name", anchor=CENTER, width=100)
sttranstree.column("Venue", anchor=CENTER, width=100)
sttranstree.column("Date", anchor=CENTER, width=100)
sttranstree.column("Time", anchor=CENTER, width=100)
sttranstree.column("No. Participants", anchor=CENTER, width=50)

# Retrieve data from the database
cursor.execute("SELECT Traning_Name,Training_Venue, Date, Time, No_Of_Participant FROM Add_Training")
training_data = cursor.fetchall()  # Fetches all the rows of data

# Insert data into the treeview
for row in training_data:
    sttranstree.insert('', 'end', values=row)


# Create a new frame for the select button
lspselect_button_frame = Frame(sftrainlist, bg='#7AB8F0')
lspselect_button_frame.place(x=950, y=80, width=95, height=30)

# Add the select button
select_button_stl = Button(lspselect_button_frame, text="Select", bg='#2181AA', fg='white', font=('Arial', 12), relief='flat')
select_button_stl.pack(fill=BOTH, expand=True)

backfram = Frame(sftrainlist, bg='white')
backfram.place(x=40, y=130, height=555, width=1115)

#Table

#Add some style:
style = ttk.Style()
style.configure("Search.TEntry", borderwidth=0, relief="flat", background="#7AB8F0")
style.theme_use("clam")
style.configure("Treeview.Heading", background="#2181AA", foreground='white', rowheight=100)

sttranstree = ttk.Treeview(
    backfram,
    selectmode="extended",
    show='headings',
    columns=('Training Name', 'Venue', 'Date', 'Time', 'No. Participants'),
    style="style1.Treeview"
)
sttranstree.place(x=20, y=0, relwidth=0.97, relheight=1)

#configure horizontal and vertical scrollbar for treeview
x_scroller = Scrollbar(sttranstree, orient=HORIZONTAL, command=sttranstree.xview)
y_scroller = Scrollbar(sttranstree, orient=VERTICAL, command=sttranstree.yview)
x_scroller.pack(side=BOTTOM, fill=X)
y_scroller.pack(side=RIGHT, fill=Y)
sttranstree.config(yscrollcommand=y_scroller.set, xscrollcommand=x_scroller.set)

#set heading name for treeview column
sttranstree.heading('Training Name', text='Training Name', anchor=CENTER)
sttranstree.heading('Venue', text='Venue', anchor=CENTER)
sttranstree.heading('Date', text='Date', anchor=CENTER)
sttranstree.heading('Time', text='Time', anchor=CENTER)
sttranstree.heading('No. Participants', text='No. Participants', anchor=CENTER)

sttranstree.column("Training Name", anchor=CENTER, width=100)
sttranstree.column("Venue", anchor=CENTER, width=100)
sttranstree.column("Date", anchor=CENTER, width=100)
sttranstree.column("Time", anchor=CENTER, width=100)
sttranstree.column("No. Participants", anchor=CENTER, width=50)

# Retrieve data from the database
cursor.execute("SELECT Traning_Name,Training_Venue, Date, Time, No_Of_Participant FROM Add_Training")
training_data = cursor.fetchall()  # Fetches all the rows of data

# Insert data into the treeview
for row in training_data:
    sttranstree.insert('', 'end', values=row)


#placing frame for menu bar left
menuFrame = Frame(staff_training_list, bg='#2181AA', width=170, height=715, highlightthickness=1)
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
    menuFrame, text="List of Staff", image=train_list_icon, compound=TOP, bg='#2181AA',
    relief='flat', fg='white', font=('yu gothic ui', 13))

logout_b = Button(
    menuFrame, text="Log Out", image=logout_icon, compound=TOP, bg='#2181AA', relief='flat', fg='white',
    font=('yu gothic ui', 13))

# Placing buttons in menu bar Home Page
home_b.place(x=11, y=20, width=150)
train_list_b.place(x=11, y=130, width=150)
Training_Sch_b.place(x=11, y=240, width=150)
logout_b.place(x=11, y=370, width=150)



window.mainloop()

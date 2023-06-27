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
window.title("List of Staff Page")
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

# ==============================Database==============================================================
conn = sqlite3.connect("SE Project.unknown")  # Replace "your_database.db" with your actual database file name
cursor = conn.cursor()

#===========================Set Frame==================================================================

listofstaff_page = Frame(window)



for frame in (listofstaff_page,):
    frame.grid(row=0, column=0, sticky='nsew')


def show_frame(frame):
    frame.tkraise()

show_frame(listofstaff_page)

listofstaff_page.config()

lstaff = Frame(listofstaff_page, bg='white', highlightthickness=1)
lstaff.place(x=150, y=20, height=715, width=1200)

# Create the label
loslabel = Label(lstaff, text='LIST OF STAFF', font=('Arial', 35), fg='#E84966', bg='white')
loslabel.place(x=30, y=15, width=400)

# Search area
search_area_frame = Frame(lstaff, bg='#F5C8D0')
search_area_frame.place(x=60, y=80, width=300, height=40)

search_icon = PhotoImage(file="images/search_icon.png")
search_label = Label(search_area_frame, image=search_icon, bg='#F5C8D0')
search_label.pack(side=RIGHT, padx=5)


search_text = Entry(search_area_frame, bg='#F5C8D0', font=('Arial', 12), relief='flat')
search_text.pack(side=LEFT, padx=5)

# Create a new frame for the search button
search_button_frame = Frame(lstaff, bg='#F5C8D0')
search_button_frame.place(x=400, y=85, width=80, height=30)

# Add the search button
search_button_ls = Button(search_button_frame, text="Search", bg='#E84966', fg='white', font=('Arial', 12), relief='flat')
search_button_ls.pack(fill=BOTH, expand=True)

def search_button_ls_clicked():
    search_text_value = search_text.get().lower()  # Get the search text from the entry and convert to lowercase

    # Retrieve data from the database
    cursor.execute("SELECT Staff_Name, Gender, Staff_ID, Department, Phone_Number, Email FROM Staff_Information")
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
            or search_text_value in str(row[5]).lower()
        ):
            filtered_data.append(row)

    # Clear the Treeview
    lsttree.delete(*lsttree.get_children())

    # Insert the filtered data into the Treeview
    for row in filtered_data:
        lsttree.insert("", "end", values=row)

# Configure the search button command
search_button_ls.config(command=search_button_ls_clicked)


backlsframe = Frame(lstaff, bg='white')
backlsframe.place(x=40, y=130, height=555, width=1115)

#Table

#Add some style:
style = ttk.Style()

style.theme_use("clam")
style.configure("Treeview.Heading", background="#E84966", foreground='white', rowheight=100)

lsttree = ttk.Treeview(
    backlsframe,
    selectmode="extended",
    show='headings',
    columns=('Name', 'Gender', 'Staff ID', 'Department', 'Phone No', 'Email'),
    style="style1.Treeview"
)
lsttree.place(x=20, y=0, relwidth=0.97, relheight=1)

#configure horizontal and vertical scrollbar for treeview
x_scroller = Scrollbar(lsttree, orient=HORIZONTAL, command=lsttree.xview)
y_scroller = Scrollbar(lsttree, orient=VERTICAL, command=lsttree.yview)
x_scroller.pack(side=BOTTOM, fill=X)
y_scroller.pack(side=RIGHT, fill=Y)
lsttree.config(yscrollcommand=y_scroller.set, xscrollcommand=x_scroller.set)

#set heading name for treeview column
lsttree.heading('Name', text='Name', anchor=CENTER)
lsttree.heading('Gender', text='Gender', anchor=CENTER)
lsttree.heading('Staff ID', text='Staff ID', anchor=CENTER)
lsttree.heading('Department', text='Department', anchor=CENTER)
lsttree.heading('Phone No', text='Phone No', anchor=CENTER)
lsttree.heading('Email', text='Email', anchor=CENTER)

lsttree.column("Name", anchor=CENTER, width=100)
lsttree.column("Gender", anchor=CENTER, width=100)
lsttree.column("Staff ID", anchor=CENTER, width=100)
lsttree.column("Department", anchor=CENTER, width=100)
lsttree.column("Phone No", anchor=CENTER, width=100)
lsttree.column("Email", anchor=CENTER, width=100)


# Retrieve data from the database
cursor.execute("SELECT Staff_Name, Gender, Staff_ID, Department, Phone_Number, Email FROM Staff_Information")
training_data = cursor.fetchall()  # Fetches all the rows of data

# Insert data into the treeview
for row in training_data:
    lsttree.insert('', 'end', values=row)

#placing frame for menu bar left
menuFrame = Frame(listofstaff_page, bg='#E84966', width=170, height=715, highlightthickness=1)
menuFrame.place(x=0, y=20)

# Defining the buttons for menu bar in Home page left
home_icon = PhotoImage(file="images/home_icon.png")
add_train_icon = PhotoImage(file="images/at_icon.png")
train_sch_icon = PhotoImage(file="images/ts_icon.png")
list_staff_icon = PhotoImage(file="images/ls_icon.png")
enrol_req_icon = PhotoImage(file="images/er_icon.png")
logout_icon = PhotoImage(file="images/logout_icon.png")

home_b = Button(
    menuFrame, text="Home", image=home_icon, compound=TOP, bg='#E84966', relief='flat', fg='white',
    font=('yu gothic ui', 13), activebackground='#74bc94'
)
add_training_b = Button(
    menuFrame, text="Add Training", image=add_train_icon, compound=TOP, bg='#E84966', relief='flat', fg='white',
    font=('yu gothic ui', 13), activebackground='#74bc94'
)
Training_Sch_b = Button(
    menuFrame, text="Training \nSchedule", image=train_sch_icon, compound=TOP, bg='#E84966', relief='flat',
    fg='white', font=('yu gothic ui', 13), activebackground='#74bc94'
)
list_staff_b = Button(
    menuFrame, text="List of Staff", image=list_staff_icon, compound=TOP, bg='#E84966',
    relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94'
)
Enrollment_req_b = Button(
    menuFrame, text="Enrollment \nRequest", image=enrol_req_icon, compound=TOP, bg='#E84966',
    relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94'
)
logout_b = Button(
    menuFrame, text="Log Out", image=logout_icon, compound=TOP, bg='#E84966', relief='flat', fg='white',
    font=('yu gothic ui', 13), activebackground='#74bc94'
)

# Placing buttons in menu bar Home Page
home_b.place(x=11, y=20, width=150)
add_training_b.place(x=11, y=110, width=150)
Training_Sch_b.place(x=11, y=220, width=150)
list_staff_b.place(x=11, y=350, width=150)
Enrollment_req_b.place(x=11, y=440, width=150)
logout_b.place(x=11, y=570, width=150)


window.mainloop()

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

staff_training_list = Frame(window)



#===========================Set Frame==================================================================



for frame in (staff_training_list,):
    frame.grid(row=0, column=0, sticky='nsew')


def show_frame(frame):
    frame.tkraise()


show_frame(staff_training_list)

staff_training_list.config()



st_transFrame = Frame(staff_training_list, bg='white', highlightthickness=1)
st_transFrame.place(x=150, y=20, height=715, width=1200)

# Create the label
main_frame = tk.Frame(st_transFrame)
main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

my_canvas = tk.Canvas(main_frame)
my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

second_frame = tk.Frame(my_canvas, background='white')
second_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
my_canvas.create_window((0, 0), window=second_frame, anchor="nw", width=window.winfo_screenwidth(), height=window.winfo_screenheight())

# Create the label
trainlabel = tk.Label(second_frame, text='TRAINING', font=('Arial', 35), fg='#2181AA', bg='white')
trainlabel.place(x=10, y=20)



venue_static_label = tk.Label(second_frame, text='Venue:', font=('Arial', 20), fg='#2181AA', bg='white')
venue_static_label.place(x=10, y=100)

venue_value_label = tk.Label(second_frame, fg='black', bg='white')
venue_value_label.place(x=100, y=103)

date_static_label = tk.Label(second_frame, text='Date:', font=('Arial', 20), fg='#2181AA', bg='white')
date_static_label.place(x=10, y=150)

date_value_label = tk.Label(second_frame, fg='black', bg='white')
date_value_label.place(x=80, y=152)

time_static_label = tk.Label(second_frame, text='Time:', font=('Arial', 20), fg='#2181AA', bg='white')
time_static_label.place(x=10, y=200)

time_value_label = tk.Label(second_frame, fg='black', bg='white')
time_value_label.place(x=80, y=203)

department_static_label = tk.Label(second_frame, text='Department:', font=('Arial', 20), fg='#2181AA', bg='white')
department_static_label.place(x=10, y=250)

department_value_label = tk.Label(second_frame, fg='black', bg='white')
department_value_label.place(x=170, y=253)

program_flow_label = tk.Label(second_frame, text='Program Flow:', font=('Arial', 20), fg='#2181AA', bg='white')
program_flow_label.place(x=10, y=300)


#Create a box under the program flow label
box_canvas_ep = Canvas(second_frame, width=1150, height=650, bg='white', highlightthickness=1, highlightbackground='black')
box_canvas_ep.place(x=10, y=350)


#Add some style:
stylesfp = ttk.Style()
stylesfp.configure("Search.TEntry", borderwidth=0, relief="flat", background="#7AB8F0")
stylesfp.theme_use("classic")
stylesfp.configure("Treeview", background="#D6EAF8", fieldbackground="#D6EAF8", foreground="black", font=('times', 13))
stylesfp.configure("Treeview.Heading", font=('times', 15, 'bold'), background='#2181AA', foreground='white')
stylesfp.map("Treeview", foreground=[('selected', 'white')])

open_tree = ttk.Treeview(
    second_frame,
    selectmode="extended",
    show='headings',
    columns=('Anything'),
    style="Treeview"
)


#configure horizontal and vertical scrollbar for treeview
x_scrollersfp = Scrollbar(open_tree, orient=HORIZONTAL, command=open_tree.xview)
y_scrollersfp = Scrollbar(open_tree, orient=VERTICAL, command=open_tree.yview)
x_scrollersfp.pack(side=BOTTOM, fill=X)
y_scrollersfp.pack(side=RIGHT, fill=Y)


# Create a new frame for the Register button
register_button_frame_ep = Frame(second_frame, bg='#7AB8F0')
register_button_frame_ep.place(x=500, y=1045, width=120, height=30)

# Function to handle the register button click
def register_button_ep_clicked():
    message = "You have been registered to this training"
    messagebox.showinfo("Registration Successful", message)


# Add the register button
register_button_ep = Button(register_button_frame_ep, text="Register", bg='#2181AA', fg='white', font=('Arial', 12), relief='flat', command=register_button_ep_clicked)
register_button_ep.pack(fill=BOTH, expand=True)



#==========================================================================================================================================================================
#=============================STAFF TRAIN LIST=============================================================================================================================
#==========================================================================================================================================================================

sftrainlist = Frame(staff_training_list, bg='white', highlightthickness=1)
sftrainlist.place(x=150, y=20, height=715, width=1200)

# Create the label
tl_label = Label(sftrainlist, text='TRAINING LIST', font=('Arial', 35), fg='#2181AA', bg='white')
tl_label.place(x=0, y=15, width=400)

# Search area
search_area_framesft = Frame(sftrainlist, bg='#7AB8F0')
search_area_framesft.place(x=45, y=80, width=300, height=40)

search_icon_sft = PhotoImage(file="images/search_icon_2.png")
search_label_sft = Label(search_area_framesft, image=search_icon_sft, bg='#7AB8F0')
search_label_sft.pack(side=RIGHT, padx=5)

search_textlsp = Entry(search_area_framesft, bg='#7AB8F0', font=('Arial', 12), relief='flat')
search_textlsp.pack(side=LEFT, padx=5)

# Create a new frame for the search button
search_button_framesft = Frame(sftrainlist, bg='#7AB8F0')
search_button_framesft.place(x=400, y=85, width=80, height=30)


def search_button_lps_clicked():
    search_text_value_sft = search_textlsp.get().lower()  # Get the search text from the entry and convert to lowercase

    if not search_text_value_sft:
        messagebox.showinfo("Validation", "Please enter a search keyword.")
        return

    # Retrieve data from the database
    cursor.execute("SELECT Training_Name, Training_Venue, Date, Time, No_Of_Participant FROM Add_Training")
    training_datasfp = cursor.fetchall()  # Fetch all the rows of data

    # Filter the data based on the search text
    filtered_data = []
    for row in training_datasfp:
        if (
            search_text_value_sft in str(row[0]).lower()  # Convert row[0] to string and then apply lower()
            or search_text_value_sft in str(row[1]).lower()
            or search_text_value_sft in str(row[2]).lower()
            or search_text_value_sft in str(row[3]).lower()
            or search_text_value_sft in str(row[4]).lower()
        ):
            filtered_data.append(row)

    if not filtered_data:
        messagebox.showinfo("Validation", "No matching records found.")
        search_textlsp.delete(0, 'end')  # Clear the search text
        return

    # Clear the Treeview
    sttranstree.delete(*sttranstree.get_children())

    # Insert the filtered data into the Treeview
    for row in filtered_data:
        sttranstree.insert("", "end", values=row)


def clear_table(event):
    # Retrieve data from the database
    cursor.execute("SELECT Training_Name, Training_Venue, Department, Date, Time, No_Of_Participant FROM Add_Training")
    training_datast = cursor.fetchall()  # Fetches all the rows of data

    # Clear the Treeview
    sttranstree.delete(*sttranstree.get_children())

    # Insert data into the Treeview
    for row in training_datast:
        sttranstree.insert("", "end", values=row)

# Bind the backspace key to the clear_table function
window.bind("<BackSpace>", clear_table)




search_button_lps = Button(search_button_framesft, text="Search", bg='#2181AA', fg='white', font=('Arial', 12), relief='flat',command=search_button_lps_clicked)
search_button_lps.pack(fill=BOTH, expand=True)

def select_button_clicked():
    # Get the selected item from the Treeview
    selected_item = sttranstree.selection()

    if not selected_item:
        messagebox.showerror("Error", "No item selected.")
        return

    # Get the values of the selected item
    values_sep = sttranstree.item(selected_item, 'values')

    # Get the necessary information from the values (assuming Staff ID is the second column and Training ID is the third column)

    venue_value_label.config(text=values_sep[1], font=('Arial', 19))
    date_value_label.config(text=values_sep[3], font=('Arial', 19))
    time_value_label.config(text=values_sep[4], font=('Arial', 19))
    department_value_label.config(text=values_sep[2], font=('Arial', 19))

    # Show the desired page using the show_frame method
    show_frame(st_transFrame)

# Create a new frame for the select button
lspselect_button_frame = Frame(sftrainlist, bg='#7AB8F0')
lspselect_button_frame.place(x=950, y=80, width=95, height=30)

# Add the select button
select_button_stl = Button(lspselect_button_frame, text="Select", bg='#2181AA', fg='white', font=('Arial', 12),
                           relief='flat',command=select_button_clicked )
select_button_stl.pack(fill=BOTH, expand=True)

backframsfp = Frame(sftrainlist, bg='white')
backframsfp.place(x=40, y=130, height=555, width=1120)

#Table

#Add some style:
stylesfp = ttk.Style()
stylesfp.configure("Search.TEntry", borderwidth=0, relief="flat", background="#7AB8F0")
stylesfp.theme_use("classic")
stylesfp.configure("Treeview", background="#D6EAF8", fieldbackground="#D6EAF8", foreground="black", font=('times', 13))
stylesfp.configure("Treeview.Heading", font=('times', 15, 'bold'), background='#2181AA', foreground='white')
stylesfp.map("Treeview", foreground=[('selected', 'white')])

sttranstree = ttk.Treeview(
    backframsfp,
    selectmode="extended",
    show='headings',
    columns=('Training Name', 'Venue','Department','Date', 'Time', 'No. Participants'),
    style="Treeview"
)
sttranstree.place(x=5, y=0, relwidth=0.99, relheight=1)

#configure horizontal and vertical scrollbar for treeview
x_scrollersfp = Scrollbar(sttranstree, orient=HORIZONTAL, command=sttranstree.xview)
y_scrollersfp = Scrollbar(sttranstree, orient=VERTICAL, command=sttranstree.yview)
x_scrollersfp.pack(side=BOTTOM, fill=X)
y_scrollersfp.pack(side=RIGHT, fill=Y)
sttranstree.config( xscrollcommand=x_scrollersfp.set, yscrollcommand=y_scrollersfp)

#set heading name for treeview column
sttranstree.heading('Training Name', text='Training Name', anchor=CENTER)
sttranstree.heading('Venue', text='Venue', anchor=CENTER)
sttranstree.heading('Department', text='Department', anchor=CENTER)
sttranstree.heading('Date', text='Date', anchor=CENTER)
sttranstree.heading('Time', text='Time', anchor=CENTER)
sttranstree.heading('No. Participants', text='No. Participants', anchor=CENTER)

sttranstree.column("Training Name", anchor=CENTER, width=50)
sttranstree.column("Venue", anchor=CENTER, width=50)
sttranstree.column("Department", anchor=CENTER, width=50)
sttranstree.column("Date", anchor=CENTER, width=50)
sttranstree.column("Time", anchor=CENTER, width=50)
sttranstree.column("No. Participants", anchor=CENTER, width=50)

# Retrieve data from the database
cursor.execute("SELECT Training_Name,Training_Venue, Department,Date, Time, No_Of_Participant FROM Add_Training")
training_datast = cursor.fetchall()  # Fetches all the rows of data

# Insert data into the treeview
for row in training_datast:
    sttranstree.insert('', 'end', values=row)






#placing frame for menu bar left
menuFrame = Frame(staff_training_list,bg='#2181AA', width=170, height=715, highlightthickness=1)
menuFrame.place(x=0, y=20)

#Defining the buttons for menu bar in Home page left
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

window.mainloop()
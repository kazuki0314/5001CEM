import random
import time
from datetime import datetime
from datetime import date
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
window.title("Staff Training Tracking System")
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
conn = sqlite3.connect("C:\Program Files\SQLiteStudio\SE Project")
cursor = conn.cursor()

# ===========================Set Frame==================================================================
login = Frame(window)
hrhomepage = Frame(window)
staffhomepage = Frame(window)


for frame in(login, hrhomepage,staffhomepage ):
    frame.grid(row=0,column=0,sticky='nsew')

def show_frame(frame):
    frame.tkraise()


show_frame(login)
def on_enter():
    conn = sqlite3.connect("C:\Program Files\SQLiteStudio\SE Project")
    cursor = conn.cursor()

    # Retrieve data from the database
    cursor.execute("SELECT Role FROM Staff_Information WHERE User_name=? AND Password=?", (usernameEntry.get(), passwordEntry.get()))
    role = cursor.fetchone()
    if role:
        if role[0]=="staff":
            messagebox.showinfo('Success', 'Login Successful')
            usernameEntry.delete(0, END)
            passwordEntry.delete(0, END)
            show_frame(staffhomepage)
        elif role[0]=="HR":
            messagebox.showinfo('Success', 'Login Successful')
            usernameEntry.delete(0, END)
            passwordEntry.delete(0, END)
            show_frame(hrhomepage)

    elif usernameEntry.get() == "" or passwordEntry.get() == "":
        messagebox.showinfo('No blank spaces', 'Please fill up the details.')

    else:
        messagebox.showinfo('Failed', 'Try Again')
        usernameEntry.delete(0, END)
        passwordEntry.delete(0, END)

#==================================================Login===============================================================
login.configure(bg='white')
frame1 = Frame(login,bg="white")
heading=Label(frame1,text='Sign In', font=('Regular', 25,'bold'), bg='white',fg='Black')
heading.place(x=269,y=124)
frame1.pack(expand=True,fill=BOTH,side=LEFT)

subframe = Frame(login, bg="#E84966")
heading2=Label(subframe,text='Welcome to ', font=('Regular', 50,'bold'), bg="#E84966",fg="white")
heading2.place(x=125,y=364)
heading3=Label(subframe,text='Login ', font=('Regular', 50,'bold'), bg="#E84966",fg="white")
heading3.place(x=225,y=464)
subframe.pack(expand=True, fill=BOTH, side=RIGHT)

usernameHeading=Label(login,text='Username',font=('Regular', 20,'bold'),bg='white', fg='Black')
usernameHeading.place(x=116,y=268)
usernameEntry = Entry(login,width=30,font=('Microsoft Yahei UI light', 14,'normal'), highlightbackground = "black",
                         highlightthickness = 2,bd=0,bg='Grey',fg='black')
usernameEntry.place(x=116,y=341)

passwordHeading=Label(login,text='Password',font=('Regular', 20,'bold'),bg='white', fg='Black')
passwordHeading.place(x=116,y=469)
passwordEntry = Entry(login,width=30,font=('Microsoft Yahei UI light', 14,'normal'),highlightbackground = "black",
                         highlightthickness = 2,bd=0,bg='Grey',fg='black')
passwordEntry.place(x=116,y=533)

loginButton=Button(login, text='Sign in',font=('Regular',20,'bold'),
                   fg='white',bg='#E84966', highlightbackground = "black",
                         highlightthickness = 2, cursor='hand2',width=19, command=on_enter)
loginButton.place(x=116,y=664)

#==========================================Logout======================================================================
def logout_system():
    answer = messagebox.askyesno(title='Confirmation',
                                 message='Are you sure that you want to logout?')
    if answer:
        show_frame(login)
        messagebox.showinfo('Logout', 'You have successfully Logged Out!')


hrhomepage.config()

#=========================================list of staff=================================================================

lstaff = Frame(hrhomepage, bg='white', highlightthickness=1)
lstaff.place(x=150, y=20, height=715, width=1200)

# Create the label
loslabel = Label(lstaff, text='LIST OF STAFF', font=('Arial', 35), fg='#E84966', bg='white')
loslabel.place(x=30, y=15, width=400)

# Search area
lssearch_area_frame = Frame(lstaff, bg='#F5C8D0')
lssearch_area_frame.place(x=60, y=80, width=300, height=40)

lssearch_icon = PhotoImage(file="images/search_icon.png")
lssearch_label = Label(lssearch_area_frame, image=lssearch_icon, bg='#F5C8D0')
lssearch_label.pack(side=RIGHT, padx=5)


lssearch_text = Entry(lssearch_area_frame, bg='#F5C8D0', font=('Arial', 12), relief='flat')
lssearch_text.pack(side=LEFT, padx=5)

# Create a new frame for the search button
lssearch_button_frame = Frame(lstaff, bg='#F5C8D0')
lssearch_button_frame.place(x=400, y=85, width=80, height=30)

# Add the search button
search_button_ls = Button(lssearch_button_frame, text="Search", bg='#E84966', fg='white', font=('Arial', 12), relief='flat')
search_button_ls.pack(fill=BOTH, expand=True)

def search_button_ls_clicked():
    lssearch_text_value = lssearch_text.get().lower()  # Get the search text from the entry and convert to lowercase

    # Retrieve data from the database
    cursor.execute("SELECT Staff_Name, Gender, Staff_ID, Department, Phone_Number, Email FROM Staff_Information")
    training_data = cursor.fetchall()  # Fetch all the rows of data

    # Filter the data based on the search text
    filtered_data = []
    for row in training_data:
        if (
            lssearch_text_value in str(row[0]).lower()  # Convert row[0] to string and then apply lower()
            or lssearch_text_value in str(row[1]).lower()
            or lssearch_text_value in str(row[2]).lower()
            or lssearch_text_value in str(row[3]).lower()
            or lssearch_text_value in str(row[4]).lower()
            or lssearch_text_value in str(row[5]).lower()
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
lsstyle = ttk.Style()

lsstyle.theme_use("clam")
lsstyle.configure("Treeview.Heading", background="#E84966", foreground='white', rowheight=100)

lsttree = ttk.Treeview(
    backlsframe,
    selectmode="extended",
    show='headings',
    columns=('Name', 'Gender', 'Staff ID', 'Department', 'Phone No', 'Email'),
    style="style1.Treeview"
)
lsttree.place(x=20, y=0, relwidth=0.97, relheight=1)

#configure horizontal and vertical scrollbar for treeview
lsx_scroller = Scrollbar(lsttree, orient=HORIZONTAL, command=lsttree.xview)
lsy_scroller = Scrollbar(lsttree, orient=VERTICAL, command=lsttree.yview)
lsx_scroller.pack(side=BOTTOM, fill=X)
lsy_scroller.pack(side=RIGHT, fill=Y)
lsttree.config(yscrollcommand=lsy_scroller.set, xscrollcommand=lsx_scroller.set)

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


#======================================Enrollment request==============================================================
EnrollFrame = Frame(hrhomepage, bg='white', highlightthickness=1)
EnrollFrame.place(x=150, y=20, height=715, width=1200)

# Create the label
EnrollTopLabel = Label(EnrollFrame, text='ENROLLMENT REQUEST', font=('Arial', 35), fg='#E84966', bg='white')
EnrollTopLabel.place(x=30, y=15, width=600)

# Search area
Enrollsearch_area_frame = Frame(EnrollFrame, bg='#F5C8D0')
Enrollsearch_area_frame.place(x=60, y=80, width=300, height=40)

Enrollsearch_icon = PhotoImage(file="images/search_icon.png")
Enrollsearch_label = Label(Enrollsearch_area_frame, image=Enrollsearch_icon, bg='#F5C8D0')
Enrollsearch_label.pack(side=RIGHT, padx=5)


Enrollsearch_text = Entry(Enrollsearch_area_frame, bg='#F5C8D0', font=('Arial', 12), relief='flat')
Enrollsearch_text.pack(side=LEFT, padx=5)

# Create a new frame for the search button
Enrollsearch_button_frame = Frame(EnrollFrame, bg='#F5C8D0')
Enrollsearch_button_frame.place(x=400, y=85, width=80, height=30)

Enrollreject_button_frame = Frame(EnrollFrame, bg='#F5C8D0')
Enrollreject_button_frame.place(x=800, y=85, width=80, height=30)

Enrollapprove_button_frame = Frame(EnrollFrame, bg='#F5C8D0')
Enrollapprove_button_frame.place(x=900, y=85, width=80, height=30)
# Add the search button
Enrollsearch_button = Button(Enrollsearch_button_frame, text="Search", bg='#E84966', fg='white', font=('Arial', 12),
                             relief='flat')
Enrollsearch_button.pack(fill=BOTH, expand=True)

Enrollreject_button = Button(Enrollreject_button_frame, text="Reject", bg='#E84966', fg='white', font=('Arial', 12),
                             relief='flat')
Enrollreject_button.pack(fill=BOTH, expand=True)

Enrollapprove_button = Button(Enrollapprove_button_frame, text="Approve", bg='#E84966', fg='white', font=('Arial', 12),
                              relief='flat')
Enrollapprove_button.pack(fill=BOTH, expand=True)

# Function to handle the search button click event
def Enrollsearch_button_clicked():
    Enrollsearch_text_value = Enrollsearch_text.get()  # Get the search text from the entry
    # Implement your search functionality here
    # Update the Treeview based on the search results

Enrollsearch_button.config(command=Enrollsearch_button_clicked)

EnrollBottomFrame = Frame(EnrollFrame, bg='white')
EnrollBottomFrame.place(x=40, y=130, height=555, width=1115)


#Table

#Add some style:
Enrollstyle = ttk.Style()

Enrollstyle.theme_use("clam")
Enrollstyle.configure("Treeview.Heading", background="#E84966", foreground='white', rowheight=100)

EnrollTree = ttk.Treeview(
    EnrollBottomFrame,
    selectmode="extended",
    show='headings',
    columns=('Name', 'Gender', 'Staff ID', 'Department', 'Email'),
    style="style1.Treeview"
)
EnrollTree.place(x=20, y=0, relwidth=0.97, relheight=1)

#configure horizontal and vertical scrollbar for treeview
Enrollx_scroller = Scrollbar(EnrollTree, orient=HORIZONTAL, command=EnrollTree.xview)
Enrolly_scroller = Scrollbar(EnrollTree, orient=VERTICAL, command=EnrollTree.yview)
Enrollx_scroller.pack(side=BOTTOM, fill=X)
Enrolly_scroller.pack(side=RIGHT, fill=Y)
EnrollTree.config(yscrollcommand=Enrolly_scroller.set, xscrollcommand=Enrollx_scroller.set)

#set heading name for treeview column
EnrollTree.heading('Name', text='Name', anchor=CENTER)
EnrollTree.heading('Gender', text='Gender', anchor=CENTER)
EnrollTree.heading('Staff ID', text='Staff ID', anchor=CENTER)
EnrollTree.heading('Department', text='Department', anchor=CENTER)
EnrollTree.heading('Email', text='Email', anchor=CENTER)

EnrollTree.column("Name", anchor=CENTER, width=100)
EnrollTree.column("Gender", anchor=CENTER, width=100)
EnrollTree.column("Staff ID", anchor=CENTER, width=100)
EnrollTree.column("Department", anchor=CENTER, width=100)
EnrollTree.column("Email", anchor=CENTER, width=100)

# Create striped row tags
EnrollTree.tag_configure('oddrow', background="white")
EnrollTree.tag_configure('evenrow', background="#E84966")

conn = sqlite3.connect("C:\Program Files\SQLiteStudio\SE Project")
cursor = conn.cursor()
cursor.execute("SELECT Staff_Name, Gender, Staff_ID, Department, Email FROM Staff_Information")
Enrollmentdata = cursor.fetchall()

# Clear the existing data in the Treeview
EnrollTree.delete(*EnrollTree.get_children())

# Iterate over the fetched data and insert into the Treeview
for row in Enrollmentdata:
    staff_id = row[2]
    # Check if the staff ID exists in the Enrollment_Request table with an Approval value of 1
    cursor.execute("SELECT Approval FROM Enrollment_Request WHERE Staff_ID = ? AND Approval IN (0, 1)", (staff_id,))
    result = cursor.fetchone()
    if result is None:
        EnrollTree.insert("", "end", values=row)

def Enrollreject_button_clicked():
    # Get the selected item(s) from the Treeview
    selected_items = EnrollTree.selection()

    # Iterate over the selected items
    for item in selected_items:
        values = EnrollTree.item(item, 'values')
        staff_id = values[2]  # Assuming Staff ID is the third column

        # Insert the data into Enrollment_Request table
        cursor.execute("INSERT INTO Enrollment_Request (Approval, Staff_ID) VALUES (?, ?)", (0, staff_id))
        conn.commit()

        # Delete the selected item from the Treeview
        EnrollTree.delete(item)


def Enrollapprove_button_clicked():
    # Get the selected item(s) from the Treeview
    selected_items = EnrollTree.selection()

    # Extract the email addresses of the selected person(s)
    recipient_emails = []
    staff_ids = []
    names = []
    for item in selected_items:
        values = EnrollTree.item(item, 'values')
        recipient_emails.append(values[4]) # Assuming email is the fifth column
        staff_ids.append(values[2])
        names.append(values[0])  # Assuming name is the first column

    # SMTP server settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'seproject5001@gmail.com'
    smtp_password = 'whvvwdspoqfqtdso'

    # Sender information
    sender_email = 'seproject5001@gmail.com'

    # Email content
    subject = 'Enrollment Approval'
    message = f'Dear {", ".join(names)},Staff ID: {", ".join(staff_ids)} your enrollment has been approved.'

    # Compose the email
    email = f'Subject: {subject}\n\n{message}'

    try:
        # Establish a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Login to the SMTP server
        server.login(smtp_username, smtp_password)

        # Send the email to each recipient
        for recipient_email in recipient_emails:
            server.sendmail(sender_email, recipient_email, email)
            print(f'Email sent to {recipient_email} successfully!')

        for staff_id in staff_ids:
            cursor.execute("INSERT INTO Enrollment_Request (Approval, Staff_ID) VALUES (?, ?)", (1, staff_id))
            conn.commit()
        for item in selected_items:
            EnrollTree.delete(item)

    except Exception as e:
        print(f'An error occurred while sending the email: {e}')

    finally:
        # Close the connection to the SMTP server
        server.quit()

Enrollreject_button_frame = Frame(EnrollFrame, bg='#F5C8D0')
Enrollreject_button_frame.place(x=800, y=85, width=80, height=30)

Enrollapprove_button_frame = Frame(EnrollFrame, bg='#F5C8D0')
Enrollapprove_button_frame.place(x=900, y=85, width=80, height=30)
# Add the search button
Enrollsearch_button = Button(Enrollsearch_button_frame, text="Search", bg='#E84966', fg='white', font=('Arial', 12),
                             relief='flat')
Enrollsearch_button.pack(fill=BOTH, expand=True)

Enrollreject_button = Button(Enrollreject_button_frame, text="Reject", bg='#E84966', fg='white', font=('Arial', 12),
                             relief='flat', command=Enrollreject_button_clicked)

Enrollreject_button.pack(fill=BOTH, expand=True)

Enrollapprove_button = Button(Enrollapprove_button_frame, text="Approve", bg='#E84966', fg='white', font=('Arial', 12),
                              relief='flat', command=Enrollapprove_button_clicked)
Enrollapprove_button.pack(fill=BOTH, expand=True)

#===============================================hr homepage========================================================
hrhome = Frame(hrhomepage, bg='white', highlightthickness=1)
hrhome.place(x=150, y=20, height=715, width=1200)

# Create the label
hplabel = Label(hrhome, text='Hello, Person', font=('Arial', 40), fg='#E84966', bg='white')
hplabel.place(x=400, y=15, width=400)

twlabel = Label(hrhome, text='This Week', font=('Arial', 15, 'bold'), fg='#E84966', bg='white')
twlabel.place(x=50, y=60)

hrbackframe = Frame(hrhome, bg='white')
hrbackframe.place(x=40, y=85, height=600, width=1115)

# Table

# Add some style
hrstyle = ttk.Style()

hrstyle.theme_use("clam")
hrstyle.configure("Treeview.Heading", background="#E84966", foreground='white', rowheight=100)

hrhometree = ttk.Treeview(
    hrbackframe,
    selectmode="extended",
    show='headings',
    columns=('Training Name', 'Venue', 'Date', 'Time', 'No. Participants'),
    style="style1.Treeview"
)
hrhometree.place(x=20, y=60, relwidth=0.97, relheight=0.82)

# Configure horizontal and vertical scrollbar for treeview
hrx_scroller = Scrollbar(hrhometree, orient=HORIZONTAL, command=hrhometree.xview)
hry_scroller = Scrollbar(hrhometree, orient=VERTICAL, command=hrhometree.yview)
hrx_scroller.pack(side=BOTTOM, fill=X)
hry_scroller.pack(side=RIGHT, fill=Y)
hrhometree.config(yscrollcommand=hry_scroller.set, xscrollcommand=hrx_scroller.set)

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
conn = sqlite3.connect("C:\Program Files\SQLiteStudio\SE Project")
cursor = conn.cursor()
cursor.execute("SELECT Training_Name,Training_Venue, Date, Time, No_Of_Participant FROM Add_Training")
training_data = cursor.fetchall()  # Fetches all the rows of data

# Insert data into the treeview
for row in training_data:
    hrhometree.insert('', 'end', values=row)

menuFrame = Frame(hrhomepage, bg='#E84966', width=170, height=715, highlightthickness=1)
menuFrame.place(x=0, y=20)

# Defining the buttons for menu bar in Home page left
hrhome_icon = PhotoImage(file="images/home_icon.png")
hradd_train_icon = PhotoImage(file="images/at_icon.png")
hrtrain_sch_icon = PhotoImage(file="images/ts_icon.png")
hrlist_staff_icon = PhotoImage(file="images/ls_icon.png")
hrenrol_req_icon = PhotoImage(file="images/er_icon.png")
hrlogout_icon = PhotoImage(file="images/logout_icon.png")

hrhome_b = Button(
    menuFrame,
    text="Home",
    image=hrhome_icon,
    compound=TOP,
    bg='#E84966',
    relief='flat',
    fg='white',
    font=('yu gothic ui', 13),
    activebackground='#74bc94',
    command=lambda: show_frame(hrhome)
)
hradd_training_b = Button(
    menuFrame,
    text="Add Training",
    image=hradd_train_icon,
    compound=TOP,
    bg='#E84966',
    relief='flat',
    fg='white',
    font=('yu gothic ui', 13),
    activebackground='#74bc94'
)
hrTraining_Sch_b = Button(
    menuFrame,
    text="Training \nSchedule",
    image=hrtrain_sch_icon,
    compound=TOP,
    bg='#E84966',
    relief='flat',
    fg='white',
    font=('yu gothic ui', 13),
    activebackground='#74bc94',
    command=lambda: show_frame(hrtransFrame)
)
hrlist_staff_b = Button(
    menuFrame,
    text="List of Staff",
    image=hrlist_staff_icon,
    compound=TOP,
    bg='#E84966',
    relief='flat',
    fg='white',
    font=('yu gothic ui', 13),
    activebackground='#74bc94',
    command=lambda: show_frame(lstaff)
)
hrEnrollment_req_b = Button(
    menuFrame,
    text="Enrollment \nRequest",
    image=hrenrol_req_icon,
    compound=TOP,
    bg='#E84966',
    relief='flat',
    fg='white',
    font=('yu gothic ui', 13),
    activebackground='#74bc94',
    command=lambda: show_frame(EnrollFrame)
)
hrlogout_b = Button(
    menuFrame,
    text="Log Out",
    image=hrlogout_icon,
    compound=TOP,
    bg='#E84966',
    relief='flat',
    fg='white',
    font=('yu gothic ui', 13),
    activebackground='#74bc94',
    command=lambda: logout_system()
)

# Placing buttons in menu bar Home Page
hrhome_b.place(x=11, y=20, width=150)
hradd_training_b.place(x=11, y=110, width=150)
hrTraining_Sch_b.place(x=11, y=220, width=150)
hrlist_staff_b.place(x=11, y=350, width=150)
hrEnrollment_req_b.place(x=11, y=440, width=150)
hrlogout_b.place(x=11, y=570, width=150)

#=================================================function for staff===================================================
def staffhome():
    show_frame(staffhomepage)
def staff_training_enrolment():
    show_frame(st_transFrame)
def staff_training_list():
    show_frame(stafftraininglist)
def schdulerpage():
    show_frame(scheduler)

def list_of_staff():
    show_frame(sftrainlist)


#=================================================Staff home page=======================================================
staffhomepage.configure(bg='white')

transFrame = Frame(staffhomepage, bg='white', highlightthickness=1)
transFrame.place(x=150, y=0, height=715, width=1200)

# Create the label
TransTopLabel = Label(transFrame, text='Home', font=('Arial', 30), fg='#2181aa', bg='white')
TransTopLabel.place(x=15, y=15, width=400)
TransBottomFrame = Frame(transFrame, bg='white')
TransBottomFrame.place(x=40, y=65, height=700, width=1115)
Calendar = Frame(TransBottomFrame)
Calendar.place(x = 10, y = 0, relwidth=0.97, relheight=5)

month = date.today().month
year = date.today().year

# Create function to output the month and year
def printMonthYear(month, year):
    # Create table for the written month
    if month == 1:
        writtenMonth = "January"
    elif month == 2:
        writtenMonth = "February"
    elif month == 3:
        writtenMonth = "March"
    elif month == 4:
        writtenMonth = "April"
    elif month == 5:
        writtenMonth = "May"
    elif month == 6:
        writtenMonth = "June"
    elif month == 7:
        writtenMonth = "July"
    elif month == 8:
        writtenMonth = "August"
    elif month == 9:
        writtenMonth = "September"
    elif month == 10:
        writtenMonth = "October"
    elif month == 11:
        writtenMonth = "November"
    else:
        writtenMonth = "December"

    # Output month and year at top of calendar
    monthYear = Label(Calendar, text=writtenMonth + " " + str(year), font=("Arial", 20))
    monthYear.grid(column=2, row=0, columnspan=3)

# Function to switch month calendar (1 for forwards and -1 for backwards)
def switchMonths(direction):
    global Calendar
    global month
    global year
    # check if we are goint to a new year
    if month == 12 and direction == 1:
        month = 0
        year += 1
    if month == 1 and direction == -1:
        month = 13
        year -= 1

    # Clears the old dictionarys so they can be used in the next month
    textObjectDict.clear()
    saveDict.clear()

    # Reprint the calendar with the new values
    Calendar.destroy()
    Calendar = Frame(staffhomepage)
    Calendar.place(x=200, y=75, relwidth=0.70, relheight=0.8)

    printMonthYear(month + direction, year)  # pylint: disable=E0601
    makeButtons()
    monthGenerator(dayMonthStarts(month + direction, year), daysInMonth(month + direction, year))
    month += direction

# Change month buttons at top of the page
def makeButtons():
    goBack = Button(Calendar, text="<", command=lambda: switchMonths(-1))
    goBack.grid(column=0, row=0)
    goForward = Button(Calendar, text=">", command=lambda: switchMonths(1))
    goForward.grid(column=6, row=0)

# Creates most of the calendar
def monthGenerator(startDate, numberOfDays):
    # Holds the names for each day of the week
    dayNames = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Places the days of the week on the top of the calender
    for nameNumber in range(len(dayNames)):
        names = Label(Calendar, text=dayNames[nameNumber], fg="black")
        names.grid(column=nameNumber, row=1, sticky='nsew')

    index = 0
    day = 1
    for row in range(6):
        for column in range(7):
            if index >= startDate and index <= startDate + numberOfDays - 1:
                # Creates a frame that will hold each day and text box
                dayFrame = Frame(Calendar)

                # Creates a textbox inside the dayframe
                t = Text(dayFrame, width=15, height=4)
                t.grid(row=1)

                # Adds the text object to the save dict
                textObjectDict[day] = t

                # Changes changes dayframe to be formated correctly
                dayFrame.grid(row=row + 2, column=column, sticky='nsew')
                dayFrame.columnconfigure(0, weight=1)
                dayNumber = Label(dayFrame, text=day)
                dayNumber.grid(row=0)
                day += 1
            index += 1
    # Creates the buttons to load and save JSON's
    loadFrom =Button(Calendar, text="load month from...", command=loadFromJSON)
    saveToButton = Button(Calendar, text="save month to...", command=saveToJSON)

    # Places them below the calendar
    loadFrom.grid(row=8, column=4)
    saveToButton.grid(row=8, column=2)

def saveToJSON():
    # Saves the raw text data from the text objects
    for day in range(len(textObjectDict)):
        saveDict[day] = textObjectDict[day + 1].get("1.0", "end - 1 chars")

    # Asks the user for a file location and saves a JSON containg the text for each day.
    fileLocation = filedialog.asksaveasfilename(initialdir="/", title="Save JSON to..")
    if fileLocation != '':
        with open(fileLocation, 'w') as jFile:
            json.dump(saveDict, jFile)

def loadFromJSON():
    # Asks the user for a JSON file to open
    fileLocation = filedialog.askopenfilename(initialdir="/", title="Select a JSON to open")
    if fileLocation != '':
        f = open(fileLocation)
        global saveDict
        saveDict = json.load(f)

        # Copies the saved text data to the current text objects
        for day in range(len(textObjectDict)):
            textObjectDict[day + 1].insert("1.0", saveDict[str(day)])

# Create function for calculating if it is a leap year
def isLeapYear(year):
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False

# Create function for calculating what day month starts
def dayMonthStarts(month, year):
    # Get last two digits (default 21 for 2021)
    lastTwoYear = year - 2000
    # Integer division by 4
    calculation = lastTwoYear // 4
    # Add day of month (always 1)
    calculation += 1
    # Table for adding proper month key
    if month == 1 or month == 10:
        calculation += 1
    elif month == 2 or month == 3 or month == 11:
        calculation += 4
    elif month == 5:
        calculation += 2
    elif month == 6:
        calculation += 5
    elif month == 8:
        calculation += 3
    elif month == 9 or month == 12:
        calculation += 6
    else:
        calculation += 0
    # Check if the year is a leap year
    leapYear = isLeapYear(year)
    # Subtract 1 if it is January or February of a leap year
    if leapYear and (month == 1 or month == 2):
        calculation -= 1
    # Add century code (assume we are in 2000's)
    calculation += 6
    # Add last two digits to the caluclation
    calculation += lastTwoYear
    # Get number output based on calculation (Sunday = 1, Monday =2..... Saturday =0)
    dayOfWeek = calculation % 7
    return dayOfWeek

# Create function to figure out how many days are in a month
def daysInMonth(month, year):
    # All months that have 31 days
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 12 or month == 10:
        numberDays = 31
    # All months that have 30 days
    elif month == 4 or month == 6 or month == 9 or month == 11:
        numberDays = 30
    else:
        # Check to see if leap year to determine how many days in Feb
        leapYear = isLeapYear(year)
        if leapYear:
            numberDays = 29
        else:
            numberDays = 28
    return numberDays

# Holds the raw text input for each day
saveDict = {}

# Holds the text objects on each day
textObjectDict = {}

# This makes the grid object appear
today = date.today()

printMonthYear(month, year)
makeButtons()
monthGenerator(dayMonthStarts(month, year), daysInMonth(month, year))

#============================================menu for staff============================================================
staffmenuFrame = Frame(staffhomepage, bg='#2181aa', width=170, height=715, highlightthickness=1)
staffmenuFrame.place(x=0, y=20)

# Defining the buttons for menu bar in Home page left
staffhome_icon2 = PhotoImage(file="images/home_icon.png")
stafftrainingenrolment_icon2 = PhotoImage(file="images/at_icon.png")
stafflist_training_icon2 = PhotoImage(file="images/ls_icon.png")
stafftrain_sch_icon2 = PhotoImage(file="images/ts_icon.png")
stafflogout_icon2 = PhotoImage(file="images/logout_icon.png")


staffhome_b = Button(staffmenuFrame, text="Home", image=staffhome_icon2, compound=TOP, bg='#2181aa', relief='flat',
                     fg='white', font=('yu gothic ui', 13), activebackground='#74bc94',command=staffhome)

stafftraining_enrolment_b = Button(staffmenuFrame, text="Training \nEnrolment", image=stafftrainingenrolment_icon2,
                                   compound=TOP, bg='#2181aa', relief='flat', fg='white', font=('yu gothic ui', 13),
                                   activebackground='#74bc94',command=staff_training_enrolment)

staffTraining_Sch_b = Button(staffmenuFrame, text="Training \nSchedule", image=stafftrain_sch_icon2, compound=TOP,
                             bg='#2181aa', relief='flat', fg='white', font=('yu gothic ui', 13),
                             activebackground='#74bc94',command=schdulerpage)

stafflist_training_b = Button(staffmenuFrame, text="Training List", image=stafflist_training_icon2, compound=TOP,
                              bg='#2181aa', relief='flat', fg='white', font=('yu gothic ui', 13),
                              activebackground='#74bc94',command=staff_training_list)

stafflogout_b = Button(staffmenuFrame, text="Log Out", image=stafflogout_icon2, compound=TOP, bg='#2181aa',
                       relief='flat',fg='white', font=('yu gothic ui', 13), activebackground='#74bc94',
                       command=logout_system)

# Placing buttons in menu bar Home Page
staffhome_b.place(x=15, y=40, width=150)
stafftraining_enrolment_b.place(x=15, y=130, width=150)
stafflist_training_b.place(x=15, y=250, width=150)
staffTraining_Sch_b.place(x=15, y=350, width=150)
stafflogout_b.place(x=15, y=460, width=150)

window.mainloop()

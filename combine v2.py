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
#==============================================global===================================================================
username = ""
password = ""
#===========================================clear search================================================================
def handle_backspace(event):
    clear_table(event)
    Enrollclear_table(event)
    listofstaffclear_table(event)



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
    global username, password
    username = usernameEntry.get()
    password = passwordEntry.get()

    conn = sqlite3.connect("C:\Program Files\SQLiteStudio\SE Project")
    cursor = conn.cursor()

    # Retrieve data from the database
    cursor.execute("SELECT Role FROM Staff_Information WHERE User_name=? AND Password=?",
                   (username, password))
    role = cursor.fetchone()
    if role:
        if role[0] == "staff":
            messagebox.showinfo('Success', 'Login Successful')
            usernameEntry.delete(0, END)
            passwordEntry.delete(0, END)
            show_frame(staffhomepage)
        elif role[0] == "HR":
            messagebox.showinfo('Success', 'Login Successful')
            usernameEntry.delete(0, END)
            passwordEntry.delete(0, END)
            show_frame(hrhomepage)

    elif username == "" or password == "":
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

usernameHeading = Label(login, text='Username', font=('Regular', 20, 'bold'), bg='white', fg='Black')
usernameHeading.place(x=116, y=268)
usernameEntry = Entry(login, width=30, font=('Microsoft Yahei UI light', 14, 'normal'), highlightbackground="black",
                      highlightthickness=2, bd=0, bg='Grey', fg='black')
usernameEntry.place(x=116, y=341)

passwordHeading = Label(login, text='Password', font=('Regular', 20, 'bold'), bg='white', fg='Black')
passwordHeading.place(x=116, y=469)
passwordEntry = Entry(login, width=30, font=('Microsoft Yahei UI light', 14, 'normal'), highlightbackground="black",
                      highlightthickness=2, bd=0, bg='Grey', fg='black')
passwordEntry.place(x=116, y=533)

loginButton = Button(login, text='Sign in', font=('Regular', 20, 'bold'),
                     fg='white', bg='#E84966', highlightbackground="black",
                     highlightthickness=2, cursor='hand2', width=19, command=on_enter)
loginButton.place(x=116, y=664)
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
search_button_ls = Button(lssearch_button_frame, text="Search", bg='#E84966', fg='white', font=('Arial', 12),
                          relief='flat')
search_button_ls.pack(fill=BOTH, expand=True)

def search_button_ls_clicked():
    lssearch_text_value = lssearch_text.get().lower()  # Get the search text from the entry and convert to lowercase

    if not lssearch_text_value:
        messagebox.showinfo("Validation", "Please enter a search keyword.")
        return

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

    if not filtered_data:
        messagebox.showinfo("Validation", "No matching records found.")
        lssearch_text.delete(0, 'end')  # Clear the search text
        return

    # Clear the Treeview
    lsttree.delete(*lsttree.get_children())

    # Insert the filtered data into the Treeview
    for row in filtered_data:
        lsttree.insert("", "end", values=row)

def listofstaffclear_table(event):
    # Retrieve data from the database
    cursor.execute("SELECT Staff_Name, Gender, Staff_ID, Department, Phone_Number, Email FROM Staff_Information")
    filtered_data = cursor.fetchall()  # Fetches all the rows of data

    # Clear the Treeview
    lsttree.delete(*lsttree.get_children())

    # Insert data into the Treeview
    for row in filtered_data:
        lsttree.insert("", "end", values=row)

# Bind the backspace key to the clear_table function
window.bind("<BackSpace>", handle_backspace)

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


def Enrollsearch_button_clicked():
    Enrollsearch_text_value = Enrollsearch_text.get().lower()  # Get the search text from the entry

    if not Enrollsearch_text_value:
        messagebox.showinfo("Validation", "Please enter a search keyword.")
        return
    # Implement your search functionality here
    # Update the Treeview based on the search results
    cursor.execute("SELECT Staff_Name, Gender, Staff_ID, Department, Email FROM Staff_Information")
    staffenroll_data = cursor.fetchall()  # Fetch all the rows of data
    enrollfiltered_data = []
    for row in staffenroll_data:
        if (
                Enrollsearch_text_value in str(row[0]).lower()  # Convert row[0] to string and then apply lower()
                or Enrollsearch_text_value in str(row[1]).lower()
                or Enrollsearch_text_value in str(row[2]).lower()
                or Enrollsearch_text_value in str(row[3]).lower()
                or Enrollsearch_text_value in str(row[4]).lower()
        ):
            enrollfiltered_data.append(row)

    if not enrollfiltered_data:
        messagebox.showinfo("Validation", "No matching records found.")
        Enrollsearch_text.delete(0, 'end')  # Clear the search text
        return
        # Clear the Treeview
    EnrollTree.delete(*EnrollTree.get_children())

        # Insert the filtered data into the Treeview
    for row in enrollfiltered_data:
        EnrollTree.insert("", "end", values=row)

def Enrollclear_table(event):
    # Retrieve data from the database
    cursor.execute("SELECT Staff_Name, Gender, Staff_ID, Department, Email FROM Staff_Information")
    staffenroll_data = cursor.fetchall()  # Fetches all the rows of data

    # Clear the Treeview
    EnrollTree.delete(*EnrollTree.get_children())

    # Insert data into the Treeview
    for row in staffenroll_data:
        EnrollTree.insert("", "end", values=row)

# Bind the backspace key to the clear_table function
window.bind("<BackSpace>", handle_backspace)

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
    EnrollTree.insert("", "end", values=row)

def Enrollreject_button_clicked():
    # Get the selected item(s) from the Treeview
    selected_items = EnrollTree.selection()

    if not selected_items:
        messagebox.showerror("Error", "No item selected.")
        return

    # Extract the email addresses of the selected person(s)
    recipient_emails = []
    staff_ids = []
    names = []
    for item in selected_items:
        values = EnrollTree.item(item, 'values')
        recipient_emails.append(values[4])  # Assuming email is the fifth column
        staff_ids.append(values[2])
        names.append(values[0])  # Assuming name is the first column

    # Get the selected Training_ID from the Combobox
    selected_training_id = training_id_combobox.get()

    if not selected_training_id:
        messagebox.showerror("Error", "No Training ID selected.")
        return

    # Confirm sending the email
    confirm_message = f"Are you sure you want to send the Rejection email to the selected recipients for Training ID {selected_training_id}?"
    confirmed = messagebox.askyesno("Confirm", confirm_message)

    if not confirmed:
        return

    # SMTP server settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'seproject5001@gmail.com'
    smtp_password = 'whvvwdspoqfqtdso'

    # Sender information
    sender_email = 'seproject5001@gmail.com'

    # Email content
    subject = 'Enrollment Rejection'
    message = f'Dear {", ".join(names)}, Staff ID: {", ".join(staff_ids)}, your enrollment for Training ID {selected_training_id} has been Rejected.'

    # Compose the email
    email = f'Subject: {subject}\n\n{message}'

    try:
        # Establish a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Login to the SMTP server
        server.login(smtp_username, smtp_password)

        # Send the email to each recipient
        for recipient_email,staff_id in zip(recipient_emails, staff_ids):
            # Check if the selected Staff_ID and Training_ID combination already exists in Enrollment_Request table with Approval value of 1
            cursor.execute(
                "SELECT Approval FROM Enrollment_Request WHERE Staff_ID = ? AND Training_ID = ? AND Approval = 0",
                (staff_id, selected_training_id))
            result = cursor.fetchone()
            if result:
                messagebox.showwarning("Already Rejected",
                                       f"The enrollment for Staff ID: {staff_id} and Training ID: {selected_training_id} has already been rejected.")
                continue

            server.sendmail(sender_email, recipient_email, email)
            messagebox.showinfo("Success", f'Email sent to {recipient_email} successfully!')

            # Insert the Approval record in the Enrollment_Request table
            cursor.execute(
                "INSERT INTO Enrollment_Request (Approval_ID, Approval, Staff_ID, Training_ID) VALUES (NULL, ?, ?, ?)",
                (0, staff_id, selected_training_id))
            conn.commit()

        # Clear the selected Training ID in the Combobox
        training_id_combobox.set('')

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while sending the email: {str(e)}")

    finally:
        # Close the connection to the SMTP server
        server.quit()


def Enrollapprove_button_clicked():
    # Get the selected item(s) from the Treeview
    selected_items = EnrollTree.selection()

    if not selected_items:
        messagebox.showerror("Error", "No item selected.")
        return

    # Extract the email addresses of the selected person(s)
    recipient_emails = []
    staff_ids = []
    names = []
    for item in selected_items:
        values = EnrollTree.item(item, 'values')
        recipient_emails.append(values[4])  # Assuming email is the fifth column
        staff_ids.append(values[2])
        names.append(values[0])  # Assuming name is the first column

    # Get the selected Training_ID from the Combobox
    selected_training_id = training_id_combobox.get()

    if not selected_training_id:
        messagebox.showerror("Error", "No Training ID selected.")
        return

    # Confirm sending the email
    confirm_message = f"Are you sure you want to send the approval email to the selected recipients for Training ID {selected_training_id}?"
    confirmed = messagebox.askyesno("Confirm", confirm_message)

    if not confirmed:
        return
    # SMTP server settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'seproject5001@gmail.com'
    smtp_password = 'nspuhlxduhtsapjr'

    # Sender information
    sender_email = 'seproject5001@gmail.com'
    # Email content
    subject = 'Enrollment Approval'
    message = f'Dear {", ".join(names)}, Staff ID: {", ".join(staff_ids)}, your enrollment for Training ID {selected_training_id} has been approved.'

    # Compose the email
    email = f'Subject: {subject}\n\n{message}'

    try:
        # Establish a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Login to the SMTP server
        server.login(smtp_username, smtp_password)



        # Send the email to each recipient
        for recipient_email, staff_id in zip(recipient_emails, staff_ids):
            # Check if the selected Staff_ID and Training_ID combination already exists in Enrollment_Request table with Approval value of 1
            cursor.execute(
                "SELECT Approval FROM Enrollment_Request WHERE Staff_ID = ? AND Training_ID = ? AND Approval = 1",
                (staff_id, selected_training_id))
            result = cursor.fetchone()
            if result:
                messagebox.showwarning("Already Approved",
                                       f"The enrollment for Staff ID: {staff_id} and Training ID: {selected_training_id} has already been approved.")
                continue

            server.sendmail(sender_email, recipient_email, email)
            messagebox.showinfo("Success", f'Email sent to {recipient_email} successfully!')

            # Insert the Approval record in the Enrollment_Request table
            cursor.execute(
                "INSERT INTO Enrollment_Request (Approval_ID, Approval, Staff_ID, Training_ID) VALUES (NULL, ?, ?, ?)",
                (1, staff_id, selected_training_id))
            cursor.execute(
                "INSERT INTO Participants (Training_ID, Staff_ID) VALUES (?, ?)",
                (selected_training_id, staff_id))
            conn.commit()

        # Clear the selected Training ID in the Combobox
        training_id_combobox.set('')


    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while sending the email: {str(e)}")

    finally:
        # Close the connection to the SMTP server
        server.quit()


# Retrieve Training IDs from Add_Training table
cursor.execute("SELECT Training_ID FROM Add_Training")
training_ids = cursor.fetchall()
training_id_values = [training[0] for training in training_ids]

# Create the Combobox for selecting Training ID
training_id_combobox = ttk.Combobox(EnrollFrame, values=training_id_values)
training_id_combobox.place(x=1000, y=85, width=80, height=30)

Enrollreject_button_frame = Frame(EnrollFrame, bg='#F5C8D0')
Enrollreject_button_frame.place(x=800, y=85, width=80, height=30)

Enrollapprove_button_frame = Frame(EnrollFrame, bg='#F5C8D0')
Enrollapprove_button_frame.place(x=900, y=85, width=80, height=30)
# Add the search button
Enrollsearch_button = Button(Enrollsearch_button_frame, text="Search", bg='#E84966', fg='white', font=('Arial', 12),
                             relief='flat',command=Enrollsearch_button_clicked)
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
hrstyle.configure("Treeview.Heading2", background="#E84966", foreground='white', rowheight=100)

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
#==============================================Staff Training list======================================================
st_transFrame = Frame(staffhomepage, bg='white', highlightthickness=1)
st_transFrame.place(x=150, y=20, height=715, width=1200)

# Create the label
trainlabel = Label(st_transFrame, text='TRAINING', font=('Arial', 35), fg='#2181AA', bg='white')
trainlabel.place(x=0, y=15, width=400)

venue_static_label = Label(st_transFrame, text='Venue:', font=('Arial', 20), fg='#2181AA', bg='white')
venue_static_label.place(x=50, y=100)

venue_value_label = Label(st_transFrame, fg='black', bg='white')
venue_value_label.place(x=150, y=103)

date_static_label = Label(st_transFrame, text='Date:', font=('Arial', 20), fg='#2181AA', bg='white')
date_static_label.place(x=50, y=150)

date_value_label = Label(st_transFrame, fg='black', bg='white')
date_value_label.place(x=130, y=152)

time_static_label = Label(st_transFrame, text='Time:', font=('Arial', 20), fg='#2181AA', bg='white')
time_static_label.place(x=50, y=200)

time_value_label = Label(st_transFrame, fg='black', bg='white')
time_value_label.place(x=125, y=203)

department_static_label = Label(st_transFrame, text='Department:', font=('Arial', 20), fg='#2181AA', bg='white')
department_static_label.place(x=50, y=250)

department_value_label = Label(st_transFrame, fg='black', bg='white')
department_value_label.place(x=210, y=253)

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
    conn = sqlite3.connect("C:\Program Files\SQLiteStudio\SE Project")
    cursor = conn.cursor()

    # ログインしているユーザーのEmailを取得
    cursor.execute("SELECT Email, Staff_ID, Staff_Name FROM Staff_Information WHERE User_name=? AND Password=? ",
                   (username, password))
    result = cursor.fetchone()
    sender_email = result[0] if result else "noreply@example.com"
    staff_id = result[1] if result else ""
    staff_name = result[2] if result else ""

    # 送信先のメールアドレスとメッセージ内容を設定
    recipient_email = 'seproject5001@gmail.com'
    subject = "Subject of the email"

    # メッセージの内容を作成
    venue = venue_value_label.cget("text")  # venue_value_labelから値を取得
    date = date_value_label.cget("text")  # date_value_labelから値を取得
    time = time_value_label.cget("text")  # time_value_labelから値を取得
    department = department_value_label.cget("text")  # department_value_labelから値を取得

    # ツリービューから選択されたトレーニングの名前を取得
    selected_item = sttranstree.selection()
    training_name = sttranstree.item(selected_item)['values'][0]

    # Training_IDを取得
    cursor.execute("SELECT Training_ID FROM Add_Training WHERE Training_Name=?", (training_name,))
    result = cursor.fetchone()
    training_id = result[0] if result else ""

    message = f"Could you please enroll in the {training_name} training program?\n"
    message += 'Details:\n'
    message += f"Staff ID: {staff_id}\n"
    message += f"Staff Name: {staff_name}\n"
    message += f"Training Name: {training_name}\n"
    message += f"Training ID: {training_id}\n"
    message += f"Venue: {venue}\n"
    message += f"Date: {date}\n"
    message += f"Time: {time}\n"
    message += f"Department: {department}\n"
    message += f"Email: {sender_email}"  # 取得した Email を表記

    # 以下は元のコードと同じです
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = 'seproject5001@gmail.com'
    smtp_password = 'nspuhlxduhtsapjr'

    # Confirmation popup message before sending the email
    confirm_message = f"Do you want to send the following message?\n\n{message}"
    confirmed = messagebox.askyesno("Email Confirmation", confirm_message)

    if confirmed:
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)

            # Construct the email message
            email_message = f"Subject: {subject}\n\n{message}"

            # Send the email
            server.sendmail(sender_email, recipient_email, email_message)
            server.quit()

            # Popup message for successful sending
            messagebox.showinfo("Success", "The email has been sent successfully.")
            show_frame(sftrainlist)

        except smtplib.SMTPException as e:
            # Popup message for sending failure
            messagebox.showerror("Error", f"There was an error sending the email:\n{str(e)}")

    else:
        # Popup message for cancellation
        messagebox.showinfo("Cancelled", "The email sending has been cancelled.")

    cursor.close()
    conn.close()


    "message = ""You have been registered to this training"
    "messagebox.showinfo(""Registration Successful"", message)"


# Add the register button
register_button_ep = Button(register_button_frame_ep, text="Register", bg='#2181AA', fg='white', font=('Arial', 12), relief='flat', command=register_button_ep_clicked)
register_button_ep.pack(fill=BOTH, expand=True)

sftrainlist = Frame(staffhomepage, bg='white', highlightthickness=1)
sftrainlist.place(x=150, y=20, height=715, width=1200)

# Create the label
tl_label = Label(sftrainlist, text='TRAINING LIST', font=('Arial', 35), fg='#2181AA', bg='white')
tl_label.place(x=30, y=15, width=400)

# Search area
search_area_framesft = Frame(sftrainlist, bg='#7AB8F0')
search_area_framesft.place(x=60, y=80, width=300, height=40)

search_icon_sft = PhotoImage(file="images/search_icon.png")
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
window.bind("<BackSpace>", handle_backspace)

search_button_lps = Button(
    search_button_framesft, text="Search", bg='#2181AA', fg='white', font=('Arial', 12), relief='flat',
    command=search_button_lps_clicked)
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
backframsfp.place(x=40, y=130, height=555, width=1115)

#Table

#Add some style:
stylesfp = ttk.Style()
stylesfp.configure("Search.TEntry", borderwidth=0, relief="flat", background="#7AB8F0")
stylesfp.theme_use("clam")
stylesfp.configure("custom.Treeview.Heading", background="#2181AA", foreground='white', rowheight=100)

sttranstree = ttk.Treeview(
    backframsfp,
    selectmode="extended",
    show='headings',
    columns=('Training Name', 'Venue','Department','Date', 'Time', 'No. Participants'),
    style="custom.Treeview"
)
sttranstree.place(x=5, y=0, relwidth=0.99, relheight=1)

#configure horizontal and vertical scrollbar for treeview
x_scrollersfp = Scrollbar(sttranstree, orient=HORIZONTAL, command=sttranstree.xview)
y_scrollersfp = Scrollbar(sttranstree, orient=VERTICAL, command=sttranstree.yview)
x_scrollersfp.pack(side=BOTTOM, fill=X)
y_scrollersfp.pack(side=RIGHT, fill=Y)
sttranstree.config(yscrollcommand=y_scrollersfp.set, xscrollcommand=x_scrollersfp.set)

#set heading name for treeview column
sttranstree.heading('Training Name', text='Training Name', anchor=CENTER)
sttranstree.heading('Venue', text='Venue', anchor=CENTER)
sttranstree.heading('Department', text='Department', anchor=CENTER)
sttranstree.heading('Date', text='Date', anchor=CENTER)
sttranstree.heading('Time', text='Time', anchor=CENTER)
sttranstree.heading('No. Participants', text='No. Participants', anchor=CENTER)

sttranstree.column("Training Name", anchor=CENTER, width=100)
sttranstree.column("Venue", anchor=CENTER, width=100)
sttranstree.column("Department", anchor=CENTER, width=100)
sttranstree.column("Date", anchor=CENTER, width=100)
sttranstree.column("Time", anchor=CENTER, width=100)
sttranstree.column("No. Participants", anchor=CENTER, width=50)

# Retrieve data from the database
cursor.execute("SELECT Training_Name,Training_Venue, Department,Date, Time, No_Of_Participant FROM Add_Training")
training_datast = cursor.fetchall()  # Fetches all the rows of data

# Insert data into the treeview
for row in training_datast:
    sttranstree.insert('', 'end', values=row)

# ============================================staff scheduler===========================================================


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
Calendar.place(x=10, y=0, relwidth=0.97, relheight=5)



#============================================menu for staff============================================================
staffmenuFrame = Frame(staffhomepage, bg='#2181aa', width=170, height=715, highlightthickness=1)
staffmenuFrame.place(x=0, y=20)

# Defining the buttons for menu bar in Home page left
staffhome_icon2 = PhotoImage(file="images/home_icon.png")
stafflist_training_icon2 = PhotoImage(file="images/ls_icon.png")
stafftrain_sch_icon2 = PhotoImage(file="images/ts_icon.png")
stafflogout_icon2 = PhotoImage(file="images/logout_icon.png")


staffhome_b = Button(staffmenuFrame, text="Home", image=staffhome_icon2, compound=TOP, bg='#2181aa', relief='flat',
                     fg='white', font=('yu gothic ui', 13), activebackground='#74bc94',
                     command=lambda: show_frame(transFrame))


staffTraining_Sch_b = Button(staffmenuFrame, text="Training \nSchedule", image=stafftrain_sch_icon2, compound=TOP,
                             bg='#2181aa', relief='flat', fg='white', font=('yu gothic ui', 13),
                             activebackground='#74bc94',command=lambda: show_frame(stschedule))

stafflist_training_b = Button(staffmenuFrame, text="Training List", image=stafflist_training_icon2, compound=TOP,
                              bg='#2181aa', relief='flat', fg='white', font=('yu gothic ui', 13),
                              activebackground='#74bc94',command=lambda: show_frame(sftrainlist))

stafflogout_b = Button(staffmenuFrame, text="Log Out", image=stafflogout_icon2, compound=TOP, bg='#2181aa',
                       relief='flat',fg='white', font=('yu gothic ui', 13), activebackground='#74bc94',
                       command=logout_system)

# Placing buttons in menu bar Home Page
staffhome_b.place(x=15, y=40, width=150)
stafflist_training_b.place(x=15, y=130, width=150)
staffTraining_Sch_b.place(x=15, y=220, width=150)
stafflogout_b.place(x=15, y=330, width=150)

window.mainloop()

import random
import time
from datetime import date
import datetime
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
conn = sqlite3.connect("SE Project.db")  # Replace "your_database.db" with your actual database file name
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
home_icon = PhotoImage(file="house_icon.png")
add_train_icon = PhotoImage(file="at_icon.png")
train_sch_icon = PhotoImage(file="ts_icon.png")
list_staff_icon = PhotoImage(file="ls_icon.png") 
enrol_req_icon = PhotoImage(file="er_icon.png")
logout_icon = PhotoImage(file="logout_icon.png")

Calendar = Frame(hrbackframe)
Calendar.place(x = 20, y = 60, relwidth=0.97, relheight=5)


month = date.today().month
year = date.today().year

# Create function to output the month and year
def hr_printMonthYear(month, year):
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
def hr_switchMonths(direction):
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


    # Reprint the calendar with the new values
    Calendar.destroy()
    Calendar = Frame(hrhomepage)
    Calendar.place(x=200, y=75, relwidth=0.70, relheight=0.8)

    hr_printMonthYear(month + direction, year)  # pylint: disable=E0601
    hr_makeButtons()
    month += direction
    hr_monthGenerator(hr_dayMonthStarts(month, year), hr_daysInMonth(month, year),month, year)
    
  
# Change month buttons at top of the page
def hr_makeButtons():
    goBack = Button(Calendar, text="<", command=lambda: hr_switchMonths(-1))
    goBack.grid(column=0, row=0)
    goForward = Button(Calendar, text=">", command=lambda: hr_switchMonths(1))
    goForward.grid(column=6, row=0)

# Creates most of the calendar
def hr_monthGenerator(startDate, numberOfDays,month,year):
    
    #staff details
    

    hr_scheduler_training= cursor.execute("""SELECT Add_Training.Date, Add_Training.Traning_Name FROM Add_Training
                                        """)
    hr_scheduler_date = cursor.fetchall()


        

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
                t = Text(dayFrame, width=15, height=4, fg= 'black')
                t.grid(row=1)

                if len(str(month)) ==1:
                    month = str('0')+ str(month)


                for i in hr_scheduler_date:
                    if i[0][3:5]  == str(month) and str(i[0][0:2]) == str(day) and str(i[0][6:10]) == str(year):
                        t.insert(END,str(i[1]))

                    else:
                        pass


                # Changes changes dayframe to be formated correctly
                dayFrame.grid(row=row + 2, column=column, sticky='nsew')
                dayFrame.columnconfigure(0, weight=1)
                dayNumber = Label(dayFrame, text=day)
                dayNumber.grid(row=0)
                day += 1
            index += 1

def hr_isLeapYear(year):
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False

# Create function for calculating what day month starts
def hr_dayMonthStarts(month, year):
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
    leapYear = hr_isLeapYear(year)
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
def hr_daysInMonth(month, year):
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


# This makes the grid object appear
today = date.today()

hr_printMonthYear(month, year)
hr_makeButtons()
hr_monthGenerator(hr_dayMonthStarts(month, year), hr_daysInMonth(month, year),month,year)







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
Training_Sch_b = Button(menuFrame,text="Training \nSchedule",image=train_sch_icon,compound=TOP,bg='#E84966',relief='flat',fg='white',font=('yu gothic ui', 13),activebackground='#74bc94', command = lambda: show_frame(Calendar))

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

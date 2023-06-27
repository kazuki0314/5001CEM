#from tkinter import ttk
from tkinter import messagebox
#import datetime
#import sqlite3
from tkinter import *
from tkcalendar import Calendar
from datetime import date
from tkinter import filedialog
from tkinter import PhotoImage
import json

window = Tk()
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.state('zoomed')  # window full screen
window.title('Staff Training Tracking System')  # set name for window title
login = Frame(window)  # login page
staffhomepage = Frame(window)  # page for staff
staffenrolpage=Frame(window) #page for staff enrolment page
stafftraininglist=Frame(window) #page for staff training list
scheduler = Frame(window) # page for staff scheduler
HRhomepage = Frame(window)  # page for HR
listofstaff = Frame(window)  # page for HR
for frame in (login, staffhomepage, staffenrolpage, stafftraininglist, scheduler, HRhomepage,listofstaff):
    frame.grid(row=0, column=0, sticky='nsew')

# function to show frame in window
def show_frame(frame):
    frame.tkraise()

show_frame(staffhomepage)
def logout_system():
    answer = messagebox.askyesno(title='Confirmation',
                                 message='Are you sure that you want to logout?')
    if answer:
        show_frame(login)
        messagebox.showinfo('Logout', 'You have successfully Logged Out!')
def staffhome():
    show_frame(staffhomepage)
def staff_training_enrolment():
    show_frame(staffenrolpage)
def staff_training_list():
    show_frame(stafftraininglist)

def HRhome():
    show_frame(HRhomepage)
def schdulerpage():
    show_frame(scheduler)

def list_of_staff():
    show_frame(listofstaff)

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


#placing frame for menu bar left
menuFrame = Frame(staffhomepage, bg='#2181aa', width=170, height=715, highlightthickness=1)
menuFrame.place(x=0, y=20)

# Defining the buttons for menu bar in Home page left
staffshome_icon2 = PhotoImage(file="home_icon.png")
staffstrainingenrolment_icon2 = PhotoImage(file="at_icon.png")
stafflist_training_icon2 = PhotoImage(file="ls_icon.png")
stafftrain_sch_icon2 = PhotoImage(file="ts_icon.png")
stafflogout_icon2 = PhotoImage(file="logout_icon.png")


home_b = Button(menuFrame, text="Home", image=staffshome_icon2, compound=TOP, bg='#2181aa', relief='flat', fg='white',
                font=('yu gothic ui', 13), activebackground='#74bc94',command=staffhome)
training_enrolment_b = Button(menuFrame, text="Training \nEnrolment", image=staffstrainingenrolment_icon2, compound=TOP, bg='#2181aa', relief='flat', fg='white',
                font=('yu gothic ui', 13), activebackground='#74bc94',command=staff_training_enrolment)
Training_Sch_b = Button(menuFrame, text="Training \nSchedule", image=stafftrain_sch_icon2, compound=TOP, bg='#2181aa', relief='flat',
                   fg='white', font=('yu gothic ui', 13), activebackground='#74bc94',command=schdulerpage)
list_training_b = Button(menuFrame, text="Training List", image=stafflist_training_icon2, compound=TOP, bg='#2181aa',
                          relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94',command=staff_training_list)
logout_b = Button(menuFrame, text="Log Out", image=stafflogout_icon2, compound=TOP, bg='#2181aa', relief='flat', fg='white',
                  font=('yu gothic ui', 13), activebackground='#74bc94', command=logout_system)

# Placing buttons in menu bar Home Page
home_b.place(x=15, y=40, width=150)
training_enrolment_b.place(x=15, y=130, width=150)
list_training_b.place(x=15, y=250, width=150)
Training_Sch_b.place(x=15, y=350, width=150)
logout_b.place(x=15, y=460, width=150)
window.mainloop()
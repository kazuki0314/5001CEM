#from tkinter import ttk
from tkinter import messagebox
#import datetime
import sqlite3
from tkinter import *
#from tkcalendar import Calendar
#from datetime import date
#from tkinter import filedialog
#from tkinter import PhotoImage
#import json

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

show_frame(login)
def on_enter():
    conn = sqlite3.connect('SE Project (1)')

    cursor = conn.cursor()

    # Retrieve data from the database
    cursor.execute("SELECT * FROM Staff_Information")
    rows = cursor.fetchall()
    if rows:
        messagebox.showinfo('Success', 'Login Successful')
        usernameEntry.delete(0, END)
        passwordEntry.delete(0, END)
        #show_frame(staffhomepage)

    elif usernameEntry.get()=="" or passwordEntry.get()=="":
        messagebox.showinfo('No blank spaces', 'Please fill up the details.')

    else:
        messagebox.showinfo('Failed', 'Try Again')
        usernameEntry.delete(0, END)
        passwordEntry.delete(0, END)

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
window.mainloop()

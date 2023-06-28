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
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sqlite3


window = Tk()
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)


# ===================== Window Setting ==================================

window.resizable(0,0)   # Delete the restore button
window_height = 800
window_width = 1550


screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


# ==============================Database==============================================================
def connect_database():
    try:
        global conn
        global cursor
        conn = sqlite3.connect("SE Project.unknown")  # Replace "your_database.db" with your actual database file name
        print("Created database successfully");
        cursor = conn.cursor()
    except:
        messagebox.showerror('Error', 'Cannot connect to database!')

connect_database()



# ===================== Set Frame ======================================

page1 = Frame(window)
page2 = Frame(window)
page3 = Frame(window)
page4 = Frame(window)

for frame in (page1, page2, page3, page4):
    frame.grid(row=0, column=0, sticky='nsew')

def show_frame(frame):
    frame.tkraise()

show_frame(page1)



# ==================== Training List Page(Page 1) =====================

page1.config()


# ==================== Training List Page =====================

#===================== Define Function ========================================================

def display_training_list():
    training_tree.delete(*training_tree.get_children())
    connect_database()
    cursor.execute(
        "SELECT Training_Name, Department, Training_Budget, Budget_Per_Person, Training_Venue, Time FROM Add_Training"
    )
    data = cursor.fetchall()
    count = 0
    for records in data:
        if count % 2 == 0:
            training_tree.insert('', END, values=records, tags=('evenrow',))
        else:
            training_tree.insert('', END, values=records, tags=('oddrow',))
        count += 1

    conn.commit()


def add_training_reset():
    for i in ['add_training_name_star', 'add_department_star', 'add_training_budget_star', 'add_budget_per_person_star',
              'add_venue_star', 'add_time_star', 'add_date_star']:
        exec(f"{i}.set('')")


def add_training_open():
    show_frame(add_training_frame)


def add_training():
    training_name = add_training_name_star.get()
    department = add_department_star.get()
    training_budget = add_training_budget_star.get()
    budget_per_person = add_budget_per_person_star.get()
    venue = add_venue_star.get()
    time = add_time_star.get()
    date = add_date_star.get()
    training_id = str(uuid4())

    day_format = '%m/%d/%y'
    reset_training = True

    if not training_name or not department or not training_budget or not budget_per_person or not venue or not time or not date:
        messagebox.showerror('Error', 'Please complete all the necessary requirement!')
    else:
        try:
            reset_training = bool(datetime.strptime(date, day_format))

        except ValueError:
            messagebox.showerror('Error', 'Please choose the date in the calendar or enter in Month/Day/Year!')

        else:
            connect_database()
            conn.execute("""INSERT INTO Add_Training (Training_Name, Department, Training_Budget, Budget_Per_Person, 
                        Training_Venue, Time, Date) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                                     (training_name, department, training_budget, budget_per_person, venue,
                                      time, date))



def close_add():
    add_training_reset()
    show_frame(training_frame)


add_training_name_star = tk.StringVar()
add_department_star = tk.StringVar()
add_training_budget_star = tk.StringVar()
add_budget_per_person_star = tk.StringVar()
add_venue_star = tk.StringVar()
add_time_star = tk.StringVar()
add_date_star = tk.StringVar()







edit_training_name_star = tk.StringVar()
edit_department_star = tk.StringVar()
edit_training_budget_star = tk.StringVar()
edit_budget_per_person_star = tk.StringVar()
edit_venue_star = tk.StringVar()
edit_time_star = tk.StringVar()
edit_date_star = tk.StringVar()



#=========================== Add Training List Page ================================

add_training_frame = Frame(page1, bg='white', highlightbackground='white', highlightthickness=1)
add_training_frame.place(x=0, y=0, height=841, width=1535)

add_training_left_side_frame = Frame(add_training_frame, bg='#E84966')
add_training_left_side_frame.place(x=0, y=0, height=841, width=204)

add_training_top_label = Label(add_training_frame, text='Add Training', bg='white', fg='#E84966',
                               font=('yu gothic ui', 70, 'italic'))
add_training_top_label.place(x=220, y=13)

add_training_back_button = Button(add_training_frame, text="Back", bg='#2a2e31', fg='white',
                                     font=('yu gothic ui', 13, 'italic'), padx=10, command=close_add)
add_training_back_button.place(x=1010, y=40)


add_training_name_label = Label(add_training_frame, bg='white', fg='#E84966',
                                        text='Training Name:', font=('yu gothic ui', 20, 'italic'))
add_training_name_label.place(x=230, y=170)
add_training_name_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_training_name_star)
add_training_name_entry.place(x=225, y=210)


add_department_label = Label(add_training_frame, bg='white', fg='#E84966', text='Department:',
                                          font=('yu gothic ui', 20, 'italic'))
add_department_label.place(x=230, y=260)
add_department_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_department_star)
add_department_entry.place(x=225, y=300)


add_training_budget_label = Label(add_training_frame, bg='white', fg='#E84966', text='Training Budget:',
                                          font=('yu gothic ui', 20, 'italic'))
add_training_budget_label.place(x=230, y=350)
add_training_budget_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_training_budget_star)
add_training_budget_entry.place(x=225, y=390)


add_budget_per_person_label = Label(add_training_frame, bg='white', fg='#E84966', text='Budget Per Person:',
                                          font=('yu gothic ui', 20, 'italic'))
add_budget_per_person_label.place(x=230, y=440)
add_budget_per_person_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_budget_per_person_star)
add_budget_per_person_entry.place(x=225, y=480)


add_venue_label = Label(add_training_frame, bg='white', fg='#E84966', text='Venue:',
                                          font=('yu gothic ui', 20, 'italic'))
add_venue_label.place(x=230, y=530)
add_venue_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_venue_star)
add_venue_entry.place(x=225, y=570)


add_time_label = Label(add_training_frame, bg='white', fg='#E84966', text='Time:',
                                          font=('yu gothic ui', 20, 'italic'))
add_time_label.place(x=230, y=620)
add_time_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_time_star)
add_time_entry.place(x=225, y=660)


add_date_label = Label(add_training_frame, bg='white', fg='#E84966',
                                        text='Date:', font=('yu gothic ui', 20, 'italic'))
add_date_label.place(x=850, y=170)



# =================================== Next Button ======================================
a_next_icon = Image.open("next_icon.png")
a_next = ImageTk.PhotoImage(a_next_icon)

a_next_button = Button(add_training_frame, image=a_next, compound=TOP, bg='white',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

a_next_button.place(x=1400, y=780, width=150)



# ================================= Programme Flow =============================================

add_programme_flow_label = Label(add_training_frame, bg='white', fg='#E84966', text='Programme Flow:',
                                          font=('yu gothic ui', 20, 'italic'))
add_programme_flow_label.place(x=850, y=530)

add_programme_flow_frame = Frame(add_training_frame, bg='white', highlightbackground='black', highlightthickness=1)
add_programme_flow_frame.place(x=845, y=580, height=70, width=500)

add_programme_flow_button = Button(add_programme_flow_frame, text="Choose File", bg='#E84966', fg='white',
                                     font=('yu gothic ui', 18, 'italic'))
add_programme_flow_button.place(x=12, y=5)

add_no_file_chosen_label = Label(add_programme_flow_frame, bg='white', fg='black', text='No file chosen',
                                          font=('yu gothic ui', 18, 'italic'))
add_no_file_chosen_label.place(x=310, y=14)




# Defining the buttons for menu bar
a_home_icon = Image.open("home_icon.png")
a_home = ImageTk.PhotoImage(a_home_icon)

a_training_list_icon = Image.open("at_icon.png")
a_add_training = ImageTk.PhotoImage(a_training_list_icon)

a_training_sche_icon = Image.open("training_sche_icon.png")
a_training_sche = ImageTk.PhotoImage(a_training_sche_icon)

a_list_staff_icon = Image.open("list_staff_icon.png")
a_list_staff = ImageTk.PhotoImage(a_list_staff_icon)

a_enrollment_icon = Image.open("enrollment_icon.png")
a_enrollment = ImageTk.PhotoImage(a_enrollment_icon)

a_logout_icon = Image.open("logout_icon.png")
a_logout = ImageTk.PhotoImage(a_logout_icon)



a_home_button = Button(add_training_left_side_frame, text="Home", image=a_home, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

a_training_list_button = Button(add_training_left_side_frame, text="Training List", image=a_add_training, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

a_training_sche_button = Button(add_training_left_side_frame, text="Training Schedule", image=a_training_sche, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

a_list_staff_button = Button(add_training_left_side_frame, text="List of Staff", image=a_list_staff, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

a_enrollment_button = Button(add_training_left_side_frame, text="Enrollment Request", image=a_enrollment, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

a_logout_button = Button(add_training_left_side_frame, text="Log Out", image=a_logout, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')



# Placing buttons in menu bar
a_home_button.place(x=27, y=25, width=150)
a_training_list_button.place(x=27, y=125, width=150)
a_training_sche_button.place(x=27, y=230, width=150)
a_list_staff_button.place(x=27, y=330, width=150)
a_enrollment_button.place(x=27, y=420, width=150)
a_logout_button.place(x=27, y=535, width=150)





# ================================ Edit Training List Page ===================================================

#Add Calendar in Add Training Page(Find Date)
def add_find_date():
    add_date_entry.delete(0, END)
    add_date_entry.insert(0, add_training_calendar.get_date())

# Create the calendar widget
add_training_calendar = Calendar(add_training_frame, selectmode='day', year=2023, month=10, day=30,
                                 background='#E84966', fieldbackground='#F5C8D0', foreground='white', selectbackground='#FC95A6',
                                 selectforeground='#E84966')
add_training_calendar.place(x=950, y=265)

add_training_calendar_button = Button(add_training_frame, bg='#E84966', fg='white', text='Find Date',
                                      font=('yu gothic ui', 13, 'italic'), padx=10,
                                      command=add_find_date)
add_training_calendar_button.place(x=1025, y=460)

add_date_entry = Entry(add_training_frame, font=16, width=40, highlightbackground='black', highlightthickness=1, textvariable=add_date_star)
add_date_entry.place(x=845, y=210)





#==================================================================================
# ==================== Training Details View Page ================================
#===================================================================================

hrl_transFrame = Frame(page1, bg='white', highlightthickness=1)
hrl_transFrame.place(x=0, y=0, height=841, width=1535)


# Create the label
mainhrl_frame = tk.Frame(hrl_transFrame)
mainhrl_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

myhrl_canvas = tk.Canvas(mainhrl_frame)
myhrl_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

myhrl_scrollbar = ttk.Scrollbar(mainhrl_frame, orient=tk.VERTICAL, command=myhrl_canvas.yview)
myhrl_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

myhrl_canvas.configure(yscrollcommand=myhrl_scrollbar.set)
myhrl_canvas.bind('<Configure>', lambda e: myhrl_canvas.configure(scrollregion=myhrl_canvas.bbox("all")))

secondhrl_frame = tk.Frame(myhrl_canvas, background='white')
secondhrl_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
myhrl_canvas.create_window((0, 0), window=secondhrl_frame, anchor="nw", width=window.winfo_screenwidth(), height=window.winfo_screenheight())

#menu frame
training_details_left_side_frame = Frame(secondhrl_frame, bg='#E84966')
training_details_left_side_frame.place(x=0, y=0, height=1100, width=204)

# Create the label
trainlabelhrl = tk.Label(secondhrl_frame, text='TRAINING', font=('Arial', 35), fg='#E84966', bg='white')
trainlabelhrl.place(x=230, y=20)

venue_static_labelhrl = tk.Label(secondhrl_frame, text='Venue:', font=('Arial', 20), fg='#E84966', bg='white')
venue_static_labelhrl.place(x=230, y=100)

venue_value_labelhrl = tk.Label(secondhrl_frame, fg='black', bg='white')
venue_value_labelhrl.place(x=320, y=103)

date_static_labelhrl = tk.Label(secondhrl_frame, text='Date:', font=('Arial', 20), fg='#E84966', bg='white')
date_static_labelhrl.place(x=230, y=150)

date_value_labelhrl = tk.Label(secondhrl_frame, fg='black', bg='white')
date_value_labelhrl.place(x=300, y=153)

time_static_labelhrl = tk.Label(secondhrl_frame, text='Time:', font=('Arial', 20), fg='#E84966', bg='white')
time_static_labelhrl.place(x=230, y=200)

time_value_labelhrl = tk.Label(secondhrl_frame, fg='black', bg='white')
time_value_labelhrl.place(x=300, y=203)

department_static_labelhrl = tk.Label(secondhrl_frame, text='Department:', font=('Arial', 20), fg='#E84966', bg='white')
department_static_labelhrl.place(x=230, y=250)

department_value_labelhrl = tk.Label(secondhrl_frame, fg='black', bg='white')
department_value_labelhrl.place(x=390, y=253)

program_flow_labelhrl = tk.Label(secondhrl_frame, text='Program Flow:', font=('Arial', 20), fg='#E84966', bg='white')
program_flow_labelhrl.place(x=230, y=300)


#Create a box under the program flow label
box_canvas_hrl = Canvas(secondhrl_frame, width=1150, height=650, bg='white', highlightthickness=1, highlightbackground='black')
box_canvas_hrl.place(x=230, y=350)


#Add some style:
styleshrl = ttk.Style()
styleshrl.theme_use("classic")
styleshrl.configure("Treeview", background="#D6EAF8", fieldbackground="#D6EAF8", foreground="black", font=('times', 13))
styleshrl.configure("Treeview.Heading", font=('times', 15, 'bold'), background='#2181AA', foreground='white')
styleshrl.map("Treeview", foreground=[('selected', 'white')])

hrl_tree = ttk.Treeview(
    secondhrl_frame,
    selectmode="extended",
    show='headings',
    columns=('Anything'),
    style="Treeview"
)


#configure horizontal and vertical scrollbar for treeview
x_scrollershrl = Scrollbar(hrl_tree, orient=HORIZONTAL, command=hrl_tree.xview)
y_scrollershrl = Scrollbar(hrl_tree, orient=VERTICAL, command=hrl_tree.yview)
x_scrollershrl.pack(side=BOTTOM, fill=X)
x_scrollershrl.pack(side=RIGHT, fill=Y)


# Defining the buttons for menu bar
home_icon_dp = Image.open("home_icon.png")
home_dp = ImageTk.PhotoImage(home_icon_dp)

training_list_icon_dp = Image.open("at_icon.png")
training_list_dp = ImageTk.PhotoImage(training_list_icon_dp)

training_sche_icon_dp = Image.open("training_sche_icon.png")
training_sche_dp = ImageTk.PhotoImage(training_sche_icon_dp)

list_staff_icon_dp = Image.open("list_staff_icon.png")
list_staff_dp = ImageTk.PhotoImage(list_staff_icon_dp)

enrollment_icon_dp = Image.open("enrollment_icon.png")
enrollment_dp = ImageTk.PhotoImage(enrollment_icon_dp)

logout_icon_dp = Image.open("logout_icon.png")
logout_dp = ImageTk.PhotoImage(logout_icon_dp)



home_button_dp = Button(training_details_left_side_frame, text="Home", image=home_dp, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

training_list_button_dp = Button(training_details_left_side_frame, text="Training List", image=training_list_dp, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

training_sche_button_dp = Button(training_details_left_side_frame, text="Training Schedule", image=training_sche_dp, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

list_staff_button_dp = Button(training_details_left_side_frame, text="List of Staff", image=list_staff_dp, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

enrollment_button_dp = Button(training_details_left_side_frame, text="Enrollment Request", image=enrollment_dp, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

logout_button_dp = Button(training_details_left_side_frame, text="Log Out", image=logout_dp, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')



# Placing buttons in menu bar
home_button_dp.place(x=27, y=25, width=150)
training_list_button_dp.place(x=27, y=125, width=150)
training_sche_button_dp.place(x=27, y=230, width=150)
list_staff_button_dp.place(x=27, y=330, width=150)
enrollment_button_dp.place(x=27, y=420, width=150)
logout_button_dp.place(x=27, y=535, width=150)



#==================================================================
# ==================== Training List UI Page =====================
#=================================================================

training_frame = Frame(page1, bg='white', highlightbackground='white', highlightthickness=1)
training_frame.place(x=0, y=0, height=841, width=1535)

training_left_side_frame = Frame(training_frame, bg='#E84966')
training_left_side_frame.place(x=0, y=0, height=841, width=204)

training_top_label = Label(training_frame, text='Training List', bg='white', fg='#E84966',
                               font=('yu gothic ui', 70, 'italic'))
training_top_label.place(x=220, y=13)


#add_training_tree_frame = Frame(add_training_frame, bg='white', highlightbackground='#E84966', highlightthickness=1)
#add_training_tree_frame.place(x=218, y=248, height=841, width=1000)


training_frame_search_entry = Entry(training_frame, bg='#F5C8D0', font=20,
                                        highlightcolor='#E84966', highlightbackground='#E84966',
                                        highlightthickness=3)
                                          # textvariable=add_type_trans_star)
training_frame_search_entry.place(x=235, y=160, height=45, width=320)



#=============================Search Icon===================================
search_icon = Image.open("search_icon.png")
photo = ImageTk.PhotoImage(search_icon)
search_icon_label = Label(page1, image=photo, bg='#F5C8D0')
search_icon_label.image = photo
search_icon_label.place(x=517, y=167)



#======================== Button ==================================


#========================Search Button===========================
search_button = Button(training_frame, text='Search', font=('yu gothic ui', 13, 'bold'), width=15, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0')    #, command=login)
search_button.place(x=590, y=166)

#========================Add Button===========================
add_training_button = Button(training_frame, text='Add', font=('yu gothic ui', 13, 'bold'), width=10, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0', command=add_training_open)
add_training_button.place(x=1182, y=166)

#========================Edit Button===========================
edit_training_button = Button(training_frame, text='Edit', font=('yu gothic ui', 13, 'bold'), width=10, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0')    #, command=login)
edit_training_button.place(x=1292, y=166)

#========================Delete Button===========================
delete_training_button = Button(training_frame, text='Delete', font=('yu gothic ui', 13, 'bold'), width=10, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0')    #, command=login)
delete_training_button.place(x=1402, y=166)



def view_button_clicked():
    # Get the selected item from the Treeview
    selected_item = training_tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "No item selected.")
        return

    # Get the values of the selected item
    values_sep = training_tree.item(selected_item, 'values')

    # Get the necessary information from the values (assuming Staff ID is the second column and Training ID is the third column)

    venue_value_labelhrl.config(text=values_sep[1], font=('Arial', 19))
    date_value_labelhrl.config(text=values_sep[3], font=('Arial', 19))
    time_value_labelhrl.config(text=values_sep[4], font=('Arial', 19))
    department_value_labelhrl.config(text=values_sep[2], font=('Arial', 19))

    # Show the desired frame using the show_frame method
    show_frame(hrl_transFrame)


view_training_button = Button(training_frame, text='View', font=('yu gothic ui', 13, 'bold'), width=10, height=1,
                              bd=0, bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0',
                              command=view_button_clicked)
view_training_button.place(x=1182, y=120)



#Add style
style = ttk.Style()
style.theme_use('clam')
style.configure("style1.Treeview", background='#6C6C6C', foreground='white', rowheight=25, fieldbackground='white',
                bordercolor='#E84966', focuscolor='#E84966')
style.configure("Treeview.Heading", background='#E84966', foreground='white', rowheight=25)
style.configure("page1.Treeview", background='#6C6C6C', foreground='white', rowheight=80, fieldbackground='#2A2E31',
                font=('None', 19))


training_tree = ttk.Treeview(training_frame, selectmode='extended', show='headings', columns=('Training Name', 'Venue','Department','Date', 'Time', 'No. Participants'),
                                style='style1.Treeview')
training_tree.place(x=235, y=250, relheight=0.60, relwidth=0.83)


#Striped row
training_tree.tag_configure('oddrow', background='#FFFFFF')
training_tree.tag_configure('evenrow', background='#E84966')


#Scrollbar for treeview
x_scroll = Scrollbar(training_tree, orient=HORIZONTAL, command=training_tree.xview)
y_scroll = Scrollbar(training_tree, orient=VERTICAL, command=training_tree.yview)
x_scroll.pack(side=BOTTOM, fill=X)
y_scroll.pack(side=RIGHT, fill=Y)
training_tree.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)


#Heading Name

training_tree.heading('Training Name', text='Training', anchor=CENTER)
training_tree.heading('Venue', text='Venue', anchor=CENTER)
training_tree.heading('Department', text='Department', anchor=CENTER)
training_tree.heading('Date', text='Date', anchor=CENTER)
training_tree.heading('Time', text='Time', anchor=CENTER)
training_tree.heading('No. Participants', text='No. Participants', anchor=CENTER)

training_tree.column('Training Name', anchor=CENTER, width=90)
training_tree.column('Venue', anchor=CENTER, width=90)
training_tree.column('Department', anchor=CENTER, width=90)
training_tree.column('Date', anchor=CENTER, width=90)
training_tree.column('Time', anchor=CENTER, width=90)
training_tree.column('No. Participants', anchor=CENTER, width=90)



# Retrieve data from the database
cursor.execute("SELECT Training_Name,Training_Venue, Department,Date, Time, No_Of_Participant FROM Add_Training")
training_datast = cursor.fetchall()  # Fetches all the rows of data

# Insert data into the treeview
for row in training_datast:
    training_tree.insert('', 'end', values=row)




# Defining the buttons for menu bar
home_icon = Image.open("home_icon.png")
home = ImageTk.PhotoImage(home_icon)

training_list_icon = Image.open("at_icon.png")
training_list = ImageTk.PhotoImage(training_list_icon)

training_sche_icon = Image.open("training_sche_icon.png")
training_sche = ImageTk.PhotoImage(training_sche_icon)

list_staff_icon = Image.open("list_staff_icon.png")
list_staff = ImageTk.PhotoImage(list_staff_icon)

enrollment_icon = Image.open("enrollment_icon.png")
enrollment = ImageTk.PhotoImage(enrollment_icon)

logout_icon = Image.open("logout_icon.png")
logout = ImageTk.PhotoImage(logout_icon)



home_button = Button(training_left_side_frame, text="Home", image=home, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

training_list_button = Button(training_left_side_frame, text="Training List", image=training_list, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

training_sche_button = Button(training_left_side_frame, text="Training Schedule", image=training_sche, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

list_staff_button = Button(training_left_side_frame, text="List of Staff", image=list_staff, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

enrollment_button = Button(training_left_side_frame, text="Enrollment Request", image=enrollment, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')

logout_button = Button(training_left_side_frame, text="Log Out", image=logout, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94')



# Placing buttons in menu bar
home_button.place(x=27, y=25, width=150)
training_list_button.place(x=27, y=125, width=150)
training_sche_button.place(x=27, y=230, width=150)
list_staff_button.place(x=27, y=330, width=150)
enrollment_button.place(x=27, y=420, width=150)
logout_button.place(x=27, y=535, width=150)


window.mainloop()

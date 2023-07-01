import random
import time
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from PIL import ImageTk, Image  # pip install pillow
from tkinter import StringVar
from tkinter import END
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
import pymysql

window = Tk()
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)


# ===================== Window Setting ==================================

window.resizable(0,0)   # Delete the restore button
window_height = 750
window_width = 1440
window.state('zoomed')

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

def close_database():
    global conn, cursor
    cursor.close()
    conn.close()

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
    # Connect to the database
    connect_database()

    # Clear the existing items in the treeview
    training_tree.delete(*training_tree.get_children())

    cursor.execute(
        "SELECT Training_ID, Training_Name, Training_Venue, Date, Time, No_Of_Participant FROM Add_Training"
    )
    data = cursor.fetchall()
    count = 0
    for records in data:
        if count % 2 == 0:
            training_tree.insert('', END, values=records, tags=('evenrow',))
        else:
            training_tree.insert('', END, values=records, tags=('oddrow',))
        count += 1

    # Close the database connection
    close_database()





def add_training_reset():
    for i in ['add_training_name_star', 'add_department_star', 'add_training_budget_star', 'add_budget_per_person_star',
              'add_venue_star', 'add_time_star', 'add_date_star']:
        exec(f"{i}.set('')")


def add_training_open():
    show_frame(add_training_frame)



def add_training():
    available_slot = add_available_slot_star.get()
    available_slot_var.set("")
    training_id = str(uuid4())
    training_name = add_training_name_star.get()
    department = add_department_star.get()
    training_budget = add_training_budget_star.get()
    budget_per_person = add_budget_per_person_star.get()
    venue = add_venue_star.get()
    time = add_time_star.get()
    date = add_date_star.get()
    gender = add_gender_star.get()



    selected_staff = add_training_two_tree.selection()

    if not selected_staff:
        messagebox.showerror("Error", "Please select staff to add!")
    else:
        display = messagebox.askyesno("Add", "The selected staff will be added to the database.")

        if display == 1:
            try:
                connect_database()

                # Calculate the number of participants
                no_participants = len(selected_staff)

                # Determine the register_status based on the available slots
                if no_participants < available_slot:
                    register_status = "Open"
                else:
                    register_status = "Closed"

                # Insert the training details into Add_Training table
                add_training_values = [
                    (training_id, training_name, training_budget, budget_per_person, department, venue, time, date,
                     no_participants, 0, register_status, gender)  # Set Available_Slot to 0 as the default value
                ]
                cursor.executemany(
                    """INSERT INTO Add_Training (Training_ID, Training_Name, Training_Budget, Budget_Per_Person, Department,
                    Training_Venue, Time, Date, No_Of_Participant, Available_Slot, Register_Status, Gender) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    add_training_values
                )

                training_id = add_training_values[0][0]  # Get the generated training_id

                # Insert the participants into Participants table
                participant_values = [(training_id, record) for record in selected_staff]
                cursor.executemany(
                    """INSERT INTO Participants (Training_ID, Staff_ID) VALUES (?, ?)""",
                    participant_values
                )

                # Update the No_Of_Participant in Add_Training table
                cursor.execute(
                    """UPDATE Add_Training SET No_Of_Participant = (
                        SELECT COUNT(*) FROM Participants WHERE Training_ID = ?
                    ) WHERE Training_ID = ?""",
                    (training_id, training_id)
                )

                # Check if the Max_Participants column exists in the Add_Training table
                cursor.execute("PRAGMA table_info(Add_Training)")
                columns = cursor.fetchall()
                column_names = [column[1] for column in columns]

                if "Max_Participants" not in column_names:
                    # Add the Max_Participants column to the Add_Training table
                    cursor.execute("ALTER TABLE Add_Training ADD COLUMN Max_Participants INTEGER")

                # Calculate the Available_Slot for each row in Add_Training
                cursor.execute(
                    """UPDATE Add_Training SET Available_Slot = Training_Budget / Budget_Per_Person - No_Of_Participant"""
                )

                # Update the available_slot_var with the current values from Add_Training
                cursor.execute(
                    """SELECT Available_Slot FROM Add_Training WHERE Training_ID = ?""",
                    (training_id,)
                )
                row = cursor.fetchone()
                if row is not None:
                    available_slot = row[0]
                    if available_slot < 0:
                        available_slot = 0  # Set the available_slot to 0 if it's negative
                else:
                    # Handle the case when no row is found
                    available_slot = 0

                # Update the Available_Slot in Add_Training table
                cursor.execute(
                    """UPDATE Add_Training SET Available_Slot = ? WHERE Training_ID = ?""",
                    (available_slot, training_id)
                )

                # Update the available_slot_var with the current value of available_slot
                available_slot_var.set(available_slot)

                conn.commit()
                conn.close()

                add_training_two_open()

                # Create a label widget to display the available_slot value
                available_slot_label = Label(add_training_two_frame, bg='white', fg='#E84966', width=10,
                                             highlightbackground='black',
                                             highlightthickness=1, text=f"{available_slot}")
                available_slot_label.pack()
                available_slot_label.place(x=1200, y=77)

                # Resize the font size
                available_slot_label.config(font=("Arial", 40))

                messagebox.showinfo('Success', f'{len(selected_staff)} staff(s) have been added.')
            except sqlite3.Error as e:
                messagebox.showerror('Database Error', str(e))
            except Exception as e:
                messagebox.showerror('Error', str(e))




def add_two_training_search():
    search = add_two_training_frame_search_entry.get()
    if search:
        cursor.execute("""SELECT Staff_Name, Staff_ID, Department, Gender FROM Staff_Information
                          WHERE Staff_Name LIKE ?""", ('%' + search + '%',))
        rows = cursor.fetchall()
        add_training_two_tree.delete(*add_training_two_tree.get_children())
        for row in rows:
            add_training_two_tree.insert("", "end", values=row)
    else:
        messagebox.showerror("Error", "Please fill the search box!")
    pass



def close_add():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to return to Training List page?  The entries made will be cleared.')
    if answer:
        display_training_list()
        show_frame(training_frame)
    pass

# Initialize variables
add_training_two_frame_search_entry = None
add_training_two_tree = None
add_staff_search_star = tk.StringVar()
add_training_id_invar = tk.IntVar()
add_training_name_star = tk.StringVar()
add_department_star = tk.StringVar()
add_training_budget_star = tk.StringVar()
add_budget_per_person_star = tk.StringVar()
add_venue_star = tk.StringVar()
add_time_star = tk.StringVar()
add_date_star = tk.StringVar()
add_no_participant_invar = tk.IntVar()
add_available_slot_invar = tk.IntVar()
add_register_status_star = tk.StringVar()
add_available_slot_star = tk.IntVar()
add_gender_star = tk.StringVar()
staff_star = tk.StringVar()
add_staff_search_star = StringVar()
available_slot_var = StringVar()





def display_add_training():
    add_training_two_tree.delete(*add_training_two_tree.get_children())
    connect_database()
    cursor.execute(
        "SELECT Staff_Name, Staff_ID, Department, Gender FROM Staff_Information"
    )
    data = cursor.fetchall()
    count = 0
    for records in data:
        if count % 2 == 0:
            add_training_two_tree.insert('', END, values=records, tags=('evenrow',))
        else:
            add_training_two_tree.insert('', END, values=records, tags=('oddrow',))
        count += 1

    conn.commit()



def add_training_two_open():
    training_id = str(uuid4())
    training_name = add_training_name_star.get()
    department = add_department_star.get()
    training_budget = add_training_budget_star.get()
    budget_per_person = add_budget_per_person_star.get()
    venue = add_venue_star.get()
    time = add_time_star.get()
    date = add_date_star.get()

    format = '%m/%d/%y'

    res = True

    if not training_id or not training_name or not department or not training_budget or not budget_per_person or not venue or not time or not date:
        messagebox.showerror('Error', "Please fill in all the necessary information!")
    else:
        try:
            float(training_budget)
        except ValueError:
            messagebox.showerror('Error', "Please insert the Training Budget in number form")
        else:
            try:
                float(budget_per_person)
            except ValueError:
                messagebox.showerror('Error', "Please insert the Budget Per Person in number form")
            else:
                try:

                    res = bool(datetime.strptime(date, format))
                except ValueError:
                    messagebox.showerror('Error',
                                         "Please insert date in MM/DD/YY format or choose the date from the calendar")

                else:
                    display_add_training()
                    show_frame(add_training_two_frame)
    pass



def back_add_training():
    show_frame(add_training_frame)
    pass










def back_to_training_list():
    display_training_list()
    show_frame(training_frame)


def edit_training():
    global e_home, e_add_training, e_training_sche, e_list_staff, e_enrollment, e_logout

    # Get the selected item from the training_tree
    selected_item = training_tree.selection()

    if selected_item:
        # Extract the training ID from the selected item
        training_id = training_tree.item(selected_item)['values'][0]

        # Connect to the database
        connect_database()

        # Retrieve the data for the selected training from the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Add_Training WHERE Training_ID=?", (training_id,))
        training_data = cursor.fetchone()  # Assuming one row is retrieved

        if training_data:

            # Create the edit training frame
            edit_training_frame = Frame(page1, bg='white', highlightbackground='white', highlightthickness=1)
            edit_training_frame.place(x=0, y=0, height=841, width=1535)

            # Remove previous entries from the frame
            for widget in edit_training_frame.winfo_children():
                widget.destroy()

            # Initialize the entry fields
            training_name_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1)
            department_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1)
            training_budget_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1)
            budget_per_person_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1)
            training_venue_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1)
            time_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1)
            date_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1)

            # Set the initial values for the entry fields
            training_name_entry.insert(0, training_data[1])  # Training Name
            department_entry.insert(0, training_data[2])  # Department
            training_budget_entry.insert(0, training_data[3])  # Training Budget
            budget_per_person_entry.insert(0, training_data[4])  # Budget per Person
            training_venue_entry.insert(0, training_data[5])  # Training Venue
            time_entry.insert(0, training_data[6])  # Time
            date_entry.insert(0, training_data[7])  # Date



            edit_training_label = Label(edit_training_frame, text='Edit Training', bg='white', fg='#E84966',
                                        font=('arial', 70, 'italic'))
            edit_training_label.place(x=220, y=13)



            edit_training_left_side_frame = Frame(edit_training_frame, bg='#E84966')
            edit_training_left_side_frame.place(x=0, y=0, height=841, width=204)

            # Defining the buttons for menu bar
            e_home_icon = Image.open("home_icon.png")
            e_home = ImageTk.PhotoImage(e_home_icon)

            e_training_list_icon = Image.open("at_icon.png")
            e_add_training = ImageTk.PhotoImage(e_training_list_icon)

            e_training_sche_icon = Image.open("training_sche_icon.png")
            e_training_sche = ImageTk.PhotoImage(e_training_sche_icon)

            e_list_staff_icon = Image.open("list_staff_icon.png")
            e_list_staff = ImageTk.PhotoImage(e_list_staff_icon)

            e_enrollment_icon = Image.open("enrollment_icon.png")
            e_enrollment = ImageTk.PhotoImage(e_enrollment_icon)

            e_logout_icon = Image.open("logout_icon.png")
            e_logout = ImageTk.PhotoImage(e_logout_icon)

            e_home_button = Button(edit_training_left_side_frame, text="Home", image=e_home, compound=TOP, bg='#E84966',
                                   relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

            e_training_list_button = Button(edit_training_left_side_frame, text="Training List", image=e_add_training,
                                            compound=TOP, bg='#E84966',
                                            relief='flat', fg='white', font=('arial', 13),
                                            activebackground='#74bc94')

            e_training_sche_button = Button(edit_training_left_side_frame, text="Training Schedule",
                                            image=e_training_sche, compound=TOP, bg='#E84966',
                                            relief='flat', fg='white', font=('arial', 13),
                                            activebackground='#74bc94')

            e_list_staff_button = Button(edit_training_left_side_frame, text="List of Staff", image=e_list_staff,
                                         compound=TOP, bg='#E84966',
                                         relief='flat', fg='white', font=('arial', 13),
                                         activebackground='#74bc94', command=back_to_training_list)

            e_enrollment_button = Button(edit_training_left_side_frame, text="Enrollment Request", image=e_enrollment,
                                         compound=TOP, bg='#E84966',
                                         relief='flat', fg='white', font=('arial', 13),
                                         activebackground='#74bc94')

            e_logout_button = Button(edit_training_left_side_frame, text="Log Out", image=e_logout, compound=TOP,
                                     bg='#E84966',
                                     relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

            # Placing buttons in menu bar
            e_home_button.place(x=27, y=25, width=150)
            e_training_list_button.place(x=27, y=125, width=150)
            e_training_sche_button.place(x=27, y=230, width=150)
            e_list_staff_button.place(x=27, y=330, width=150)
            e_enrollment_button.place(x=27, y=420, width=150)
            e_logout_button.place(x=27, y=535, width=150)




            edit_training_back_button = Button(edit_training_frame, text="Back", bg='#E84966', fg='white',
                                               font=('arial', 13, 'italic'), padx=10, command=close_edit)
            edit_training_back_button.place(x=230, y=780)

            # Training ID label and entry field
            training_id_label = Label(edit_training_frame, bg='white', fg='#E84966', text='Training ID:', font=('arial', 20))
            training_id_label.place(x=850, y=170)

            training_id_entry = Entry(edit_training_frame, font=20, width=50, highlightbackground='black', highlightthickness=1)
            training_id_entry.place(x=845, y=210)
            training_id_entry.insert(0, training_id)

            # Training ID label and entry field
            training_id_label = Label(edit_training_frame, bg='white', fg='#E84966', text='Training ID:',
                                      font=('arial', 20))
            training_id_label.place(x=850, y=170)

            training_id_entry = Entry(edit_training_frame, font=20, width=50, highlightbackground='black',
                                      highlightthickness=1)
            training_id_entry.place(x=845, y=210)
            training_id_entry.insert(0, training_data[0])  # Update with the correct variable holding training ID

            # Training Name label and entry field
            training_name_label = Label(edit_training_frame, text='Training Name:', bg='white', fg='#E84966',
                                        font=('arial', 20))
            training_name_label.place(x=230, y=170)

            training_name_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black',
                                        highlightthickness=1)
            training_name_entry.place(x=225, y=210)
            training_name_entry.insert(0, training_data[1])  # Update with the correct variable holding training name

            # Department label and entry field
            department_label = Label(edit_training_frame, text='Department:', bg='white', fg='#E84966',
                                     font=('arial', 20))
            department_label.place(x=230, y=260)

            department_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black',
                                     highlightthickness=1)
            department_entry.place(x=225, y=300)
            department_entry.insert(0, training_data[2])  # Update with the correct variable holding department

            # Training Budget label and entry field
            training_budget_label = Label(edit_training_frame, text='Training Budget:', bg='white', fg='#E84966',
                                          font=('arial', 20))
            training_budget_label.place(x=230, y=350)

            training_budget_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black',
                                          highlightthickness=1)
            training_budget_entry.place(x=225, y=390)
            training_budget_entry.insert(0,
                                         training_data[3])  # Update with the correct variable holding training budget

            # Budget Per Person label and entry field
            budget_per_person_label = Label(edit_training_frame, text='Budget Per Person:', bg='white', fg='#E84966',
                                            font=('arial', 20))
            budget_per_person_label.place(x=230, y=440)

            budget_per_person_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black',
                                            highlightthickness=1)
            budget_per_person_entry.place(x=225, y=480)
            budget_per_person_entry.insert(0, training_data[4])  # Update with the correct variable holding budget per person

            # Training Venue label and entry field
            training_venue_label = Label(edit_training_frame, text='Training Venue:', bg='white', fg='#E84966',
                                         font=('arial', 20))
            training_venue_label.place(x=230, y=530)

            training_venue_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black',
                                         highlightthickness=1)
            training_venue_entry.place(x=225, y=570)
            training_venue_entry.insert(0, training_data[5])  # Update with the correct variable holding training venue

            # Time label and entry field
            time_label = Label(edit_training_frame, text='Time:', bg='white', fg='#E84966', font=('arial', 20))
            time_label.place(x=230, y=620)

            time_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black',
                               highlightthickness=1)
            time_entry.place(x=225, y=660)
            time_entry.insert(0, training_data[6])  # Update with the correct variable holding time

            date_label = Label(edit_training_frame, text='Date:', bg='white', fg='#E84966', font=('arial', 20))
            date_label.place(x=850, y=260)

            # Add Calendar in Add Training Page(Find Date)
            def edit_find_date():
                date_entry.delete(0, END)
                date_entry.insert(0, edit_training_calendar.get_date())

            # Create the calendar widget
            edit_training_calendar = Calendar(edit_training_frame, selectmode='day', year=2023, month=10, day=30,
                                             background='#E84966', fieldbackground='#F5C8D0', foreground='white',
                                             selectbackground='#FC95A6',
                                             selectforeground='#E84966')
            edit_training_calendar.place(x=950, y=355)

            edit_training_calendar_button = Button(edit_training_frame, bg='#E84966', fg='white', text='Find Date',
                                                  font=('arial', 13, 'italic'), padx=10,
                                                  command=edit_find_date)
            edit_training_calendar_button.place(x=1025, y=560)

            date_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black',
                                        highlightthickness=1)
            date_entry.place(x=845, y=300, width=320)
            date_entry.insert(0, training_data[7])

            # ================================= Programme Flow =============================================

            programme_flow_label = Label(edit_training_frame, bg='white', fg='#E84966', text='Programme Flow:',
                                         font=('arial', 20, 'italic'))
            programme_flow_label.place(x=850, y=620)

            programme_flow_frame = Frame(edit_training_frame, bg='white', highlightbackground='black',
                                         highlightthickness=1)
            programme_flow_frame.place(x=845, y=670, height=70, width=500)

            programme_flow_button = Button(programme_flow_frame, text="Choose File", bg='#E84966', fg='white',
                                           font=('arial', 18, 'italic'))
            programme_flow_button.place(x=12, y=5)

            no_file_chosen_label = Label(programme_flow_frame, bg='white', fg='black', text='No file chosen',
                                         font=('arial', 18, 'italic'))
            no_file_chosen_label.place(x=310, y=14)


            # Update button
            def update_training():

                # Get the selected item from the training_tree
                selected_item = training_tree.selection()

                # Get the updated values from the entry fields
                updated_training_id = training_id_entry.get()
                updated_training_name = training_name_entry.get()
                updated_department = department_entry.get()
                updated_training_budget = training_budget_entry.get()
                updated_budget_per_person = budget_per_person_entry.get()
                updated_training_venue = training_venue_entry.get()
                updated_time = time_entry.get()
                updated_date = date_entry.get()

                # Check if any of the fields are empty
                if not updated_training_id or not updated_training_name or not updated_department or not updated_training_budget or not updated_budget_per_person or not updated_training_venue or not updated_time or not updated_date:
                    messagebox.showerror('Error', "Please fill in all the necessary information!")
                    return  # Return without proceeding further

                # Display a Yes/No messagebox to confirm the update
                confirmation = messagebox.askyesno('Confirmation', 'Are you sure you want to update the training?')


                if confirmation:
                    # Update the data in the training_tree
                    training_tree.item(selected_item, text='', values=(updated_training_id, updated_training_name,
                                                                        updated_department, updated_training_budget,
                                                                        updated_budget_per_person,
                                                                        updated_training_venue,
                                                                        updated_time, updated_date))

                    # Update the data in the database
                    cursor.execute(
                        "UPDATE Add_Training SET Training_ID=?, Training_Name=?, Department=?, Training_Budget=?, Budget_Per_Person=?, Training_Venue=?, Time=?, Date=? WHERE Training_ID=?",
                        (updated_training_id, updated_training_name, updated_department, updated_training_budget,
                        updated_budget_per_person, updated_training_venue, updated_time, updated_date, training_id))
                    conn.commit()



                    # Close the edit training frame
                    edit_training_frame.destroy()

                    # Display a messagebox to indicate successful update
                    messagebox.showinfo('Success', 'Training updated successfully!')

                    display_training_list()

                else:
                    messagebox.showinfo("Error", "No training selected!")

            update_button = Button(edit_training_frame, text='Edit', bg='#E84966', fg='white',
                                   font=('arial', 16),
                                   relief='flat', command=update_training)
            update_button.place(x=750, y=765, width=150)

        else:
            messagebox.showinfo("Error", "No training selected!")


    else:
        messagebox.showinfo("Error", "No training selected!")



def close_edit():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to return to Training List page?  The entries made will be cleared.')
    if answer:
        display_training_list()
        show_frame(training_frame)
    pass




# Define StringVar variables before using them
edit_training_name_star = StringVar()
edit_department_star = StringVar()
edit_training_budget_star = StringVar()
edit_budget_per_person_star = StringVar()
edit_venue_star = StringVar()
edit_time_star = StringVar()
edit_date_star = StringVar()
edit_no_participant_invar = tk.IntVar
edit_register_status_star = tk.StringVar
edit_gender_star = tk.StringVar
#edit_budget_per_person_star = tk.StringVar
edit_two_training_search_star = tk.StringVar
edit_staff_search_star = tk.StringVar



def delete_training():
    if not training_tree.selection():
        messagebox.showerror("Error", "Please choose a training to delete.")
    else:
        display = messagebox.askyesno("Delete", "The selected training(s) will be deleted from the database.")

        if display:
            selected_items = training_tree.selection()

            # Connect to the database
            connect_database()

            item_delete = []
            for record in selected_items:
                training_id = training_tree.item(record, 'values')[0]
                item_delete.append(training_id)

            # Delete the training from the Add_Training table
            delete_query = "DELETE FROM Add_Training WHERE Training_ID IN ({})".format(", ".join("?" * len(item_delete)))
            cursor.execute(delete_query, tuple(item_delete))
            conn.commit()

            # Delete the training from the Participants table
            delete_query = "DELETE FROM Participants WHERE Training_ID IN ({})".format(", ".join("?" * len(item_delete)))
            cursor.execute(delete_query, tuple(item_delete))
            conn.commit()

            # Close the database connection
            close_database()

            display_training_list()

            messagebox.showinfo('Success', f'{len(item_delete)} training(s) have been deleted.')


#=========================== Add Training List Page ================================

add_training_frame = Frame(page1, bg='white', highlightbackground='white', highlightthickness=1)
add_training_frame.place(x=0, y=0, height=841, width=1535)

add_training_left_side_frame = Frame(add_training_frame, bg='#E84966')
add_training_left_side_frame.place(x=0, y=0, height=841, width=204)

add_training_top_label = Label(add_training_frame, text='Add Training', bg='white', fg='#E84966',
                               font=('arial', 70, 'italic'))
add_training_top_label.place(x=220, y=13)

add_training_back_button = Button(add_training_frame, text="Back", bg='#2a2e31', fg='white',
                                     font=('arial', 13, 'italic'), padx=10, command=close_add)
add_training_back_button.place(x=230, y=780)


add_training_name_label = Label(add_training_frame, bg='white', fg='#E84966',
                                        text='Training Name:', font=('arial', 20, 'italic'))
add_training_name_label.place(x=230, y=170)
add_training_name_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_training_name_star)
add_training_name_entry.place(x=225, y=210)


add_department_label = Label(add_training_frame, bg='white', fg='#E84966', text='Department:',
                                          font=('arial', 20, 'italic'))
add_department_label.place(x=230, y=260)
add_department_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_department_star)
add_department_entry.place(x=225, y=300)


add_training_budget_label = Label(add_training_frame, bg='white', fg='#E84966', text='Training Budget:',
                                          font=('arial', 20, 'italic'))
add_training_budget_label.place(x=230, y=350)
add_training_budget_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_training_budget_star)
add_training_budget_entry.place(x=225, y=390)


add_budget_per_person_label = Label(add_training_frame, bg='white', fg='#E84966', text='Budget Per Person:',
                                          font=('arial', 20, 'italic'))
add_budget_per_person_label.place(x=230, y=440)
add_budget_per_person_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_budget_per_person_star)
add_budget_per_person_entry.place(x=225, y=480)


add_venue_label = Label(add_training_frame, bg='white', fg='#E84966', text='Venue:',
                                          font=('arial', 20, 'italic'))
add_venue_label.place(x=230, y=530)
add_venue_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_venue_star)
add_venue_entry.place(x=225, y=570)


add_time_label = Label(add_training_frame, bg='white', fg='#E84966', text='Time:',
                                          font=('arial', 20, 'italic'))
add_time_label.place(x=230, y=620)
add_time_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_time_star)
add_time_entry.place(x=225, y=660)


add_date_label = Label(add_training_frame, bg='white', fg='#E84966',
                                        text='Date:', font=('arial', 20, 'italic'))
add_date_label.place(x=850, y=170)



# =================================== Next Button ======================================
a_next_icon = Image.open("next_icon.png")
a_next = ImageTk.PhotoImage(a_next_icon)

a_next_button = Button(add_training_frame, image=a_next, compound=TOP, bg='white',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94', command=add_training_two_open)

a_next_button.place(x=1400, y=780, width=150)



# ================================= Programme Flow =============================================

add_programme_flow_label = Label(add_training_frame, bg='white', fg='#E84966', text='Programme Flow:',
                                          font=('arial', 20, 'italic'))
add_programme_flow_label.place(x=850, y=530)

add_programme_flow_frame = Frame(add_training_frame, bg='white', highlightbackground='black', highlightthickness=1)
add_programme_flow_frame.place(x=845, y=580, height=70, width=500)

add_programme_flow_button = Button(add_programme_flow_frame, text="Choose File", bg='#E84966', fg='white',
                                     font=('arial', 18, 'italic'))
add_programme_flow_button.place(x=12, y=5)

add_no_file_chosen_label = Label(add_programme_flow_frame, bg='white', fg='black', text='No file chosen',
                                          font=('arial', 18, 'italic'))
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
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

a_training_list_button = Button(add_training_left_side_frame, text="Training List", image=a_add_training, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

a_training_sche_button = Button(add_training_left_side_frame, text="Training Schedule", image=a_training_sche, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

a_list_staff_button = Button(add_training_left_side_frame, text="List of Staff", image=a_list_staff, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94', command=back_to_training_list)

a_enrollment_button = Button(add_training_left_side_frame, text="Enrollment Request", image=a_enrollment, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

a_logout_button = Button(add_training_left_side_frame, text="Log Out", image=a_logout, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')



# Placing buttons in menu bar
a_home_button.place(x=27, y=25, width=150)
a_training_list_button.place(x=27, y=125, width=150)
a_training_sche_button.place(x=27, y=230, width=150)
a_list_staff_button.place(x=27, y=330, width=150)
a_enrollment_button.place(x=27, y=420, width=150)
a_logout_button.place(x=27, y=535, width=150)



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
                                      font=('arial', 13, 'italic'), padx=10,
                                      command=add_find_date)
add_training_calendar_button.place(x=1025, y=460)

add_date_entry = Entry(add_training_frame, font=16, width=40, highlightbackground='black', highlightthickness=1, textvariable=add_date_star)
add_date_entry.place(x=845, y=210)



#==================================================================
# ==================== Add Training List 2 UI Page =====================
#=================================================================

add_training_two_frame = Frame(page1, bg='white', highlightbackground='white', highlightthickness=1)
add_training_two_frame.place(x=0, y=0, height=841, width=1535)

add_training_two_left_side_frame = Frame(add_training_two_frame, bg='#E84966')
add_training_two_left_side_frame.place(x=0, y=0, height=841, width=204)

add_training_two_top_label = Label(add_training_two_frame, text='Training List', bg='white', fg='#E84966',
                               font=('arial', 70, 'italic'))
add_training_two_top_label.place(x=220, y=13)


#=========================Available Text============================
add_two_available_label = Label(add_training_two_frame, text='Available', bg='white', fg='#E84966',
                               font=('arial', 35, 'italic'))
add_two_available_label.place(x=940, y=50)


#=========================Slot Text============================
add_two_slot_label = Label(add_training_two_frame, text='Slot ', bg='white', fg='#E84966',
                               font=('arial', 35, 'italic'))
add_two_slot_label.place(x=940, y=104)



#=======================Add Button=============================
add_icon = Image.open("add_icon.png")
photo5 = ImageTk.PhotoImage(add_icon)
add_button = Button(add_training_two_frame, image=photo5, bd=0, background='white', activebackground='white', command=add_training)
add_button.place(x=750, y=765)


##=======================Back Button=============================
add_two_back_icon = Image.open("back_icon.png")
photo6 = ImageTk.PhotoImage(add_two_back_icon)
add_two_back_button = Button(add_training_two_frame, image=photo6, bd=0, background='white', activebackground='white', command=back_add_training)
add_two_back_button.place(x=235, y=780)



#=============================Search Entry===================================
add_two_training_frame_search_entry = Entry(add_training_two_frame, bg='#F5C8D0', font=20,
                                            highlightcolor='#E84966', highlightbackground='#E84966',
                                            highlightthickness=3,
                                            textvariable=add_staff_search_star)
add_two_training_frame_search_entry.place(x=235, y=160, height=45, width=320)

#=============================Search Icon===================================
search_icon = Image.open("search_icon.png")
photo7 = ImageTk.PhotoImage(search_icon)
search_icon_label = Label(add_training_two_frame, image=photo7, bg='#F5C8D0')
search_icon_label.image = photo7
search_icon_label.place(x=517, y=167)


#======================== Button ==================================


#========================Search Button===========================
add_two_search_button = Button(add_training_two_frame, text='Search', font=('arial', 13, 'bold'), width=15, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0', command=add_two_training_search)
add_two_search_button.place(x=590, y=166)




#Add style
style = ttk.Style()
style.theme_use('clam')
style.configure("style1.Treeview", background='#6C6C6C', foreground='white', rowheight=25, fieldbackground='white',
                bordercolor='#E84966', focuscolor='#E84966')
style.configure("Treeview.Heading", background='#E84966', foreground='white', rowheight=25)
style.configure("page1.Treeview", background='#6C6C6C', foreground='white', rowheight=80, fieldbackground='#2A2E31',
                font=('None', 19))


add_training_two_tree = ttk.Treeview(add_training_two_frame, selectmode='extended', show='headings', columns=('Name',
                                'Staff ID', 'Department', 'Gender'),
                                style='style1.Treeview')
add_training_two_tree.place(x=235, y=250, relheight=0.60, relwidth=0.83)


#Striped row
add_training_two_tree.tag_configure('oddrow', background='#E43D5B')
add_training_two_tree.tag_configure('evenrow', background='#FF9DAF')


#Scrollbar for treeview
x_scroll = Scrollbar(add_training_two_tree, orient=HORIZONTAL, command=add_training_two_tree.xview)
y_scroll = Scrollbar(add_training_two_tree, orient=VERTICAL, command=add_training_two_tree.yview)
x_scroll.pack(side=BOTTOM, fill=X)
y_scroll.pack(side=RIGHT, fill=Y)
add_training_two_tree.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)


#Heading Name
add_training_two_tree.heading('Name', text='Name', anchor=CENTER)
add_training_two_tree.heading('Staff ID', text='Staff ID', anchor=CENTER)
add_training_two_tree.heading('Department', text='Department', anchor=CENTER)
add_training_two_tree.heading('Gender', text='Gender', anchor=CENTER)

add_training_two_tree.column('Name', anchor=CENTER, width=90)
add_training_two_tree.column('Staff ID', anchor=CENTER, width=90)
add_training_two_tree.column('Department', anchor=CENTER, width=90)
add_training_two_tree.column('Gender', anchor=CENTER, width=90)



# Defining the buttons for menu bar
add_two_home_icon = Image.open("home_icon.png")
add_two_home = ImageTk.PhotoImage(add_two_home_icon)

add_two_training_list_icon = Image.open("at_icon.png")
add_two_training_list = ImageTk.PhotoImage(add_two_training_list_icon)

add_two_training_sche_icon = Image.open("training_sche_icon.png")
add_two_training_sche = ImageTk.PhotoImage(add_two_training_sche_icon)

add_two_list_staff_icon = Image.open("list_staff_icon.png")
add_two_list_staff = ImageTk.PhotoImage(add_two_list_staff_icon)

add_two_enrollment_icon = Image.open("enrollment_icon.png")
add_two_enrollment = ImageTk.PhotoImage(add_two_enrollment_icon)

add_two_logout_icon = Image.open("logout_icon.png")
add_two_logout = ImageTk.PhotoImage(add_two_logout_icon)



add_two_home_button = Button(add_training_two_left_side_frame, text="Home", image=add_two_home, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

add_two_training_list_button = Button(add_training_two_left_side_frame, text="Training List", image=add_two_training_list, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

add_two_training_sche_button = Button(add_training_two_left_side_frame, text="Training Schedule", image=add_two_training_sche, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

add_two_list_staff_button = Button(add_training_two_left_side_frame, text="List of Staff", image=add_two_list_staff, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94', command=back_to_training_list)

add_two_enrollment_button = Button(add_training_two_left_side_frame, text="Enrollment Request", image=add_two_enrollment, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

add_two_logout_button = Button(add_training_two_left_side_frame, text="Log Out", image=add_two_logout, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')



# Placing buttons in menu bar
add_two_home_button.place(x=27, y=25, width=150)
add_two_training_list_button.place(x=27, y=125, width=150)
add_two_training_sche_button.place(x=27, y=230, width=150)
add_two_list_staff_button.place(x=27, y=330, width=150)
add_two_enrollment_button.place(x=27, y=420, width=150)
add_two_logout_button.place(x=27, y=535, width=150)









# =============================================================================
def training_list_search():
    connect_database()
    #training_name = add_training_name_star.get()
    search = training_list_search_star.get()
    if not search:
        messagebox.showerror('Error', 'Please fill the search box!')

    else:
        cursor.execute("""SELECT Training_ID, Training_Name, Training_Venue, Date, Time, No_Of_Participant FROM Add_Training 
        WHERE Training_Name LIKE ? ORDER BY date DESC""", ('%'+search+'%',))

        data = cursor.fetchall()
        if len(data) != 0:
            training_tree.delete(*training_tree.get_children())
            count = 0
            for records in data:
                if count % 2 ==0:
                    training_tree.insert('', END, values=records, tags=('evenrow',))

                else:
                    training_tree.insert('', END, values=records, tags=('oddrow',))
                count = count + 1
                conn.commit()

        else:
            messagebox.showerror('Error', 'There is no record in the database!')


def training_list_reset():
    display_training_list()
    training_list_search_star.set('')


training_list_search_star = tk.StringVar()

#==================================================================
# ==================== Training List UI Page =====================
#=================================================================


training_frame = Frame(page1, bg='white', highlightbackground='white', highlightthickness=1)
training_frame.place(x=0, y=0, height=841, width=1535)

training_left_side_frame = Frame(training_frame, bg='#E84966')
training_left_side_frame.place(x=0, y=0, height=841, width=204)

training_top_label = Label(training_frame, text='Training List', bg='white', fg='#E84966',
                               font=('arial', 70, 'italic'))
training_top_label.place(x=220, y=13)




training_frame_search_entry = Entry(training_frame, bg='#F5C8D0', font=20,
                                        highlightcolor='#E84966', highlightbackground='#E84966',
                                        highlightthickness=3,
                                        textvariable=training_list_search_star)
training_frame_search_entry.place(x=235, y=160, height=45, width=320)



#=============================Search Icon===================================
search_icon = Image.open("search_icon.png")
photo = ImageTk.PhotoImage(search_icon)
search_icon_label = Label(page1, image=photo, bg='#F5C8D0')
search_icon_label.image = photo
search_icon_label.place(x=517, y=167)





#======================== Button ==================================


#========================Search Button===========================
search_button = Button(training_frame, text='Search', font=('arial', 13, 'bold'), width=15, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0', command=training_list_search)
search_button.place(x=590, y=166)




#========================Add Button===========================
add_training_button = Button(training_frame, text='Add', font=('arial', 13, 'bold'), width=10, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0', command=add_training_open)
add_training_button.place(x=1182, y=166)

#========================Edit Button===========================
edit_training_button = Button(training_frame, text='Edit', font=('arial', 13, 'bold'), width=10, height=1, bd=0,
                              bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0', command=edit_training)
edit_training_button.place(x=1292, y=166)

#========================Delete Button===========================
delete_training_button = Button(training_frame, text='Delete', font=('arial', 13, 'bold'), width=10, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0', command=delete_training)
delete_training_button.place(x=1402, y=166)





#Add style
style = ttk.Style()
style.theme_use('clam')
style.configure("style1.Treeview", background='#6C6C6C', foreground='white', rowheight=25, fieldbackground='white',
                bordercolor='#E84966', focuscolor='#E84966')
style.configure("Treeview.Heading", background='#E84966', foreground='white', rowheight=25)
style.configure("page1.Treeview", background='#6C6C6C', foreground='white', rowheight=80, fieldbackground='#2A2E31',
                font=('None', 19))


# Create the training_tree widget
training_tree = ttk.Treeview(training_frame, selectmode='extended', show='headings', columns=('Training ID', 'Training Name', 'Training Venue', 'Date', 'Time', 'No. Participants'), style='style1.Treeview')
training_tree.place(x=235, y=250, relheight=0.60, relwidth=0.83)


#Striped row
training_tree.tag_configure('oddrow', background='#E43D5B')
training_tree.tag_configure('evenrow', background='#FF9DAF')


#Scrollbar for treeview
x_scroll = Scrollbar(training_frame, orient=HORIZONTAL, command=training_tree.xview)
y_scroll = Scrollbar(training_frame, orient=VERTICAL, command=training_tree.yview)
x_scroll.pack(side=BOTTOM, fill=X)
y_scroll.pack(side=RIGHT, fill=Y)
training_tree.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)


#columns=('Training ID', 'Training Name', 'Training Venue', 'Date', 'Time', 'No. Participants')

#Heading Name
training_tree.heading('Training ID', text='Training ID', anchor=CENTER)
training_tree.heading('Training Name', text='Training Name', anchor=CENTER)
training_tree.heading('Training Venue', text='Training Venue', anchor=CENTER)
training_tree.heading('Date', text='Date', anchor=CENTER)
training_tree.heading('Time', text='Time', anchor=CENTER)
training_tree.heading('No. Participants', text='No. Participants', anchor=CENTER)

training_tree.column('Training ID', anchor=CENTER, width=90)
training_tree.column('Training Name', anchor=CENTER, width=120)
training_tree.column('Training Venue', anchor=CENTER, width=90)
training_tree.column('Date', anchor=CENTER, width=90)
training_tree.column('Time', anchor=CENTER, width=90)
training_tree.column('No. Participants', anchor=CENTER, width=90)


display_training_list()

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
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

training_list_button = Button(training_left_side_frame, text="Training List", image=training_list, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

training_sche_button = Button(training_left_side_frame, text="Training Schedule", image=training_sche, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

list_staff_button = Button(training_left_side_frame, text="List of Staff", image=list_staff, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94', command=back_to_training_list)

enrollment_button = Button(training_left_side_frame, text="Enrollment Request", image=enrollment, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')

logout_button = Button(training_left_side_frame, text="Log Out", image=logout, compound=TOP, bg='#E84966',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94')



# Placing buttons in menu bar
home_button.place(x=27, y=25, width=150)
training_list_button.place(x=27, y=125, width=150)
training_sche_button.place(x=27, y=230, width=150)
list_staff_button.place(x=27, y=330, width=150)
enrollment_button.place(x=27, y=420, width=150)
logout_button.place(x=27, y=535, width=150)


window.mainloop()

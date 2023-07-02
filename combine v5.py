import random
import time
from datetime import datetime
from datetime import date
from dateutil import parser
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
import pymysql
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
conn = sqlite3.connect("C:/Users/Ohta K/Desktop/SE/SE Project")
cursor = conn.cursor()

def connect_database():
    try:
        global conn
        global cursor
        conn = sqlite3.connect("C:/Users/Ohta K/Desktop/SE/SE Project") # Replace "your_database.db" with your actual database file name
        print("Created database successfully");
        cursor = conn.cursor()
    except:
        messagebox.showerror('Error', 'Cannot connect to database!')

connect_database()

def close_database():
    global conn, cursor
    cursor.close()
    conn.close()
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


for frame in(login, hrhomepage,staffhomepage):
    frame.grid(row=0,column=0,sticky='nsew')

def show_frame(frame):
    frame.tkraise()


show_frame(login)


def on_enter():
    global username, password
    username = usernameEntry.get()
    password = passwordEntry.get()

    conn = sqlite3.connect("C:/Users/Ohta K/Desktop/SE/SE Project")
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
            show_canban()
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
#================================Add Training===========================================================================
def go_back_trd():
    show_frame(hrtraining_frame)
    
def display_hrtraining_list():
    # Connect to the database
    
    connect_database()

    # Clear the existing items in the treeview
    hrtraining_tree.delete(*hrtraining_tree.get_children())

    cursor.execute(
        "SELECT Training_ID, Training_Name, Training_Venue, Date, Time, Department, No_Of_Participant FROM Add_Training"
    )
    data = cursor.fetchall()
    count = 0
    for records in data:
        if count % 2 == 0:
            hrtraining_tree.insert('', END, values=records, tags=('evenrow',))
        else:
            hrtraining_tree.insert('', END, values=records, tags=('oddrow',))
        count += 1

    # Close the database connection
    close_database()

def add_training_reset():
    for i in ['add_training_name_star', 'add_department_star', 'add_training_budget_star', 'add_budget_per_person_star',
              'add_venue_star', 'add_time_star', 'add_date_star']:
        exec(f"{i}.set('')")


def add_training_open():
    show_frame(add_training_frame)

def send_email(recipients, training_name):
    # SMTPサーバーの設定
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'seproject5001@gmail.com'
    smtp_password = 'nspuhlxduhtsapjr'

    # Sender information
    sender_email = 'seproject5001@gmail.com'

    # メールの作成
    message = MIMEMultipart()
    message['From'] = sender_email
    message['Subject'] = 'Training Invitation'

    # メール本文の作成
    body = f"Dear recipient,\n\nYou have been invited to participate in the training '{training_name}'.\nPlease make sure to attend the training on the scheduled date and time.\n You may check the details from Staff Home page\n\nBest regards,\nYour Training Team"

    # 各受信者に対してメールを送信
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        
        for recipient_email in recipients:
            message['To'] = recipient_email
            message.attach(MIMEText(body, 'plain'))
            server.send_message(message)



# send_email_to_financial関数の実装
def send_email_to_financial(recipients, training_name, training_id, training_budget, budget_per_person):
    # 送信元のメールアドレスとパスワードを設定
    sender_email = 'seproject5001@gmail.com'
    sender_password = 'nspuhlxduhtsapjr'

    # SMTPサーバーの設定
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # メールの内容を構築
    subject = f"Training Registration - {training_name}"
    message = f"Dear Finance Team,\n\nA new training has been registered: {training_name}.\n\nPlease review the training details below:\n\n- Training ID: {training_id}\n- Training Budget: {training_budget}\n- Budget Per Person: {budget_per_person}\n\nThank you for your attention.\n\nBest regards,\nThe Training Team"

    # 確認のポップアップメッセージを表示
    confirm_message = f"The following email will be sent to the Finance Team:\n\n{message}\n\nDo you want to proceed?"
    confirmed = messagebox.askyesno("Confirm Email", confirm_message)

    if confirmed:
        try:
            # SMTPサーバーへの接続
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            for recipient in recipients:
                # メールのヘッダーと内容を構築
                email_message = f"Subject: {subject}\n\n{message}"

                # メールの送信
                server.sendmail(sender_email, recipient, email_message)

            # SMTPサーバーとの接続を終了
            server.quit()

            messagebox.showinfo("Email Sent", "The email has been sent to the Finance Team.")
        except Exception as e:
            messagebox.showerror('Error', f"Failed to send email: {str(e)}")
    else:
        messagebox.showinfo("Email Canceled", "The email sending has been canceled.")




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
        print(selected_staff)
        display = messagebox.askyesno("Add", "The selected staff will be added to the database.")

        if display == 1:
            try:
                connect_database()

                # Calculate the number of participants
                no_participants = len(selected_staff)

                # Insert the training details into Add_Training table
                add_training_values = [
                    (training_id, training_name, training_budget, budget_per_person, department, venue, time, date,
                     no_participants, 0)  # Set Available_Slot to 0 as the default value
                ]
                cursor.executemany(
                    """INSERT INTO Add_Training (Training_ID, Training_Name, Training_Budget, Budget_Per_Person, Department,
                    Training_Venue, Time, Date, No_Of_Participant, Available_Slot) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    add_training_values
                )

                training_id = add_training_values[0][0]  # Get the generated training_id

                # Insert the participants into Participants table
                participant_values = [(training_id, record) for record in selected_staff]  # Remove 'I' from Staff_ID
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
                        available_slot = 0
                else:
                    # Handle the case when no row is found
                    available_slot = 0

                # Update the Available_Slot in Add_Training table
                cursor.execute(
                    """UPDATE Add_Training SET Available_Slot = ? WHERE Training_ID = ?""",
                    (available_slot, training_id)
                )

                # Determine the register_status based on the available slots
                if no_participants <= available_slot:
                    register_status = "Open"
                else:
                    register_status = "Closed"

                # Update the Register_Status in Add_Training table
                cursor.execute(
                    """UPDATE Add_Training SET Register_Status = ? WHERE Training_ID = ?""",
                    (register_status, training_id)
                )

                # Insert participants into Enrollment_Request table with Approval flag
                enrollment_values = [(record, training_id, 1) for record in selected_staff]
                cursor.executemany(
                    """INSERT INTO Enrollment_Request (Staff_ID, Training_ID, Approval) VALUES (?, ?, ?)""",
                    enrollment_values
                )

                # Retrieve the emails of selected staff
                recipients = []
                fcrecipients = []

                for staff_id in selected_staff:
                    cursor.execute(
                        """SELECT Email, Role FROM Staff_Information WHERE Staff_ID = ?""",
                        (staff_id,)
                    )
                    row = cursor.fetchone()
                    if row is not None:
                        email, role = row
                        recipients.append(email)
                        if role == 'Financial':
                            fcrecipients.append(email)

                # Add the emails of Financial staff who were not selected in the treeview
                cursor.execute(
                    """SELECT Email FROM Staff_Information WHERE Role = 'Financial' AND Staff_ID NOT IN ({})""".format(
                        ','.join(['?'] * len(selected_staff))),
                    selected_staff
                )
                rows = cursor.fetchall()
                for row in rows:
                    email = row[0]
                    fcrecipients.append(email)

                # RoleがFinancialの人が存在する場合、Financialの人にメールを送信する
                if fcrecipients:
                    send_email_to_financial(fcrecipients, training_name, training_id, training_budget, budget_per_person)

                conn.commit()
                conn.close()
                add_training_two_open()

                messagebox.showinfo('Success', f'{len(selected_staff)} staff(s) have been added.')

                # Clear the entry fields
                add_training_name_star.delete(0, END)
                add_department_star.delete(0, END)
                add_training_budget_star.delete(0, END)
                add_budget_per_person_star.delete(0, END)
                add_venue_star.delete(0, END)
                add_time_star.delete(0, END)
                add_date_star.delete(0, END)
                add_gender_star.delete(0, END)

            except sqlite3.Error as e:
                messagebox.showerror('Database Error', str(e))
            except Exception as e:
                messagebox.showerror('Error', str(e))



def add_two_training_search():
    search = add_two_training_frame_search_entry.get()
    if search:
        cursor.execute("""SELECT Staff_ID, Staff_Name, Department, Gender FROM Staff_Information
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
        "SELECT Staff_ID, Staff_Name, Department, Gender FROM Staff_Information"
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

    format = '%d/%m/%Y'  # 年を4桁で表記するためにフォーマットを'%m/%d/%Y'に変更する

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
                    selected_date = datetime.strptime(date, format).date()  # フォーマットを'%m/%d/%Y'に修正する
                    date = selected_date.strftime("%d/%m/%Y")  # 年を4桁で表記するように変更する
                    res = True
                except ValueError:
                    messagebox.showerror('Error',
                                         "Please insert date in DD/MM/YYYY format or choose the date from the calendar")
                    res = False

                if res:
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
    selected_item = hrtraining_tree.selection()

    if selected_item:
        # Extract the training ID from the selected item
        training_id = hrtraining_tree.item(selected_item)['values'][0]

        # Connect to the database
        connect_database()

        # Retrieve the data for the selected training from the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Add_Training WHERE Training_ID=?", (training_id,))
        training_data = cursor.fetchone()  # Assuming one row is retrieved

        if training_data:

            # Create the edit training frame
            edit_training_frame = Frame(hrhomepage, bg='white', highlightbackground='white', highlightthickness=1)
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
                                        font=('arial', 70))
            edit_training_label.place(x=220, y=13)



            edit_training_back_button = Button(edit_training_frame, text="Back", bg='#E84966', fg='white',
                                               font=('arial', 13, 'italic'), padx=10, command=close_edit)
            edit_training_back_button.place(x=750, y=650)

          
            # Training ID label and entry field
            training_id_label = Label(edit_training_frame, bg='white', fg='#E84966', text='Training ID:',
                                      font=('arial', 20))
            training_id_label.place(x=650, y=170)

            training_id_entry = Entry(edit_training_frame, font=20, width=50, highlightbackground='black',
                                      highlightthickness=1)
            training_id_entry.place(x=650, y=210)
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
            date_label.place(x=650, y=260)

            # Add Calendar in Add Training Page(Find Date)
            

            date_entry = Entry(edit_training_frame, font=20, width=40, highlightbackground='black',
                                        highlightthickness=1)
            date_entry.place(x=650, y=300, width=320)
            date_entry.insert(0, training_data[7])

            # ================================= Programme Flow =============================================

            programme_flow_label = Label(edit_training_frame, bg='white', fg='#E84966', text='Programme Flow:',
                                         font=('arial', 20, 'italic'))
            programme_flow_label.place(x=650, y=500)

            programme_flow_frame = Frame(edit_training_frame, bg='white', highlightbackground='black',
                                         highlightthickness=1)
            programme_flow_frame.place(x=650, y=550, height=70, width=500)

            programme_flow_button = Button(programme_flow_frame, text="Choose File", bg='#E84966', fg='white',
                                           font=('arial', 18, 'italic'))
            programme_flow_button.place(x=12, y=5)

            no_file_chosen_label = Label(programme_flow_frame, bg='white', fg='black', text='No file chosen',
                                         font=('arial', 18, 'italic'))
            no_file_chosen_label.place(x=310, y=14)


            # Update button
            def update_training():

                # Get the selected item from the training_tree
                selected_item = hrtraining_tree.selection()

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
                    hrtraining_tree.item(selected_item, text='', values=(updated_training_id, updated_training_name,
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

                    display_hrtraining_list()

                else:
                    messagebox.showinfo("Error", "No training selected!")

            update_button = Button(edit_training_frame, text='Update', bg='#E84966', fg='white',
                                   font=('arial', 13),padx=10,
                                   command=update_training)
            update_button.place(x=850, y=650)

        else:
            messagebox.showinfo("Error", "No training selected!")


    else:
        messagebox.showinfo("Error", "No training selected!")



def close_edit():
    answer = messagebox.askyesno(title='Confirmation',
                          message='Are you sure that you want to return to Training List page?  The entries made will be cleared.')
    if answer:
        show_frame(hrtraining_frame)
        show_frame(menuFrame)
        display_hrtraining_list()

        
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
    if not hrtraining_tree.selection():
        messagebox.showerror("Error", "Please choose a training to delete.")
    else:
        display = messagebox.askyesno("Delete", "The selected training(s) will be deleted from the database.")

        if display:
            selected_items = hrtraining_tree.selection()

            # Connect to the database
            connect_database()

            item_delete = []
            for record in selected_items:
                training_id = hrtraining_tree.item(record, 'values')[0]
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

            display_hrtraining_list()

            messagebox.showinfo('Success', f'{len(item_delete)} training(s) have been deleted.')

def open_button_clicked():
    # Get the selected item from the Treeview
    selected_item = hrtraining_tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "No item selected.")
        return

    # Get the values of the selected item
    values_trd = hrtraining_tree.item(selected_item, 'values')

    # Get the necessary information from the values 

    venue_value_labelhrl.config(text=values_trd[2], font=('Arial', 19))
    date_value_labelhrl.config(text=values_trd[3], font=('Arial', 19))
    time_value_labelhrl.config(text=values_trd[4], font=('Arial', 19))
    department_value_labelhrl.config(text=values_trd[5], font=('Arial', 19))

    # Show the desired page using the show_frame method
    show_frame(hrl_transFrame)

#=========================== Add Training List Page ================================

add_training_frame = Frame(hrhomepage, bg='white', highlightbackground='white', highlightthickness=1)
add_training_frame.place(x=150, y=20, height=715, width=1200)


add_training_top_label = Label(add_training_frame, text='Add Training', bg='white', fg='#E84966',
                               font=('arial', 30))
add_training_top_label.place(x=15, y=15, width=400)

add_training_back_button = Button(add_training_frame, text="Back", bg='#2a2e31', fg='white',
                                     font=('arial', 13), padx=10, command=close_add)
add_training_back_button.place(x=230, y=780)


add_training_name_label = Label(add_training_frame, bg='white', fg='#E84966',
                                        text='Training Name:', font=('arial', 20))
add_training_name_label.place(x=150, y=140)
add_training_name_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_training_name_star)
add_training_name_entry.place(x=150, y=180)


add_department_label = Label(add_training_frame, bg='white', fg='#E84966', text='Department:',
                                          font=('arial', 20))
add_department_label.place(x=150, y=230)
add_department_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_department_star)
add_department_entry.place(x=150, y=270)


add_training_budget_label = Label(add_training_frame, bg='white', fg='#E84966', text='Training Budget:',
                                          font=('arial', 20))
add_training_budget_label.place(x=150, y=320)
add_training_budget_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_training_budget_star)
add_training_budget_entry.place(x=150, y=360)


add_budget_per_person_label = Label(add_training_frame, bg='white', fg='#E84966', text='Budget Per Person:',
                                          font=('arial', 20))
add_budget_per_person_label.place(x=150, y=410)
add_budget_per_person_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_budget_per_person_star)
add_budget_per_person_entry.place(x=150, y=450)


add_venue_label = Label(add_training_frame, bg='white', fg='#E84966', text='Venue:',
                                          font=('arial', 20))
add_venue_label.place(x=150, y=500)
add_venue_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_venue_star)
add_venue_entry.place(x=150, y=540)


add_time_label = Label(add_training_frame, bg='white', fg='#E84966', text='Time:',
                                          font=('arial', 20))
add_time_label.place(x=150, y=590)
add_time_entry = Entry(add_training_frame, font=20, width=40, highlightbackground='black', highlightthickness=1,
                                          textvariable=add_time_star)
add_time_entry.place(x=150, y=630)


add_date_label = Label(add_training_frame, bg='white', fg='#E84966',
                                        text='Date:', font=('arial', 20))
add_date_label.place(x=650, y=140)



# =================================== Next Button ======================================
a_next_icon = Image.open("next_icon.png")
a_next = ImageTk.PhotoImage(a_next_icon)

a_next_button = Button(add_training_frame, image=a_next, compound=TOP, bg='white',
            relief='flat', fg='white', font=('arial', 13), activebackground='#74bc94', command=add_training_two_open)

a_next_button.place(x=1000, y=645, width=130)



# ================================= Programme Flow =============================================

add_programme_flow_label = Label(add_training_frame, bg='white', fg='#E84966', text='Programme Flow:',
                                          font=('arial', 20, 'italic'))
add_programme_flow_label.place(x=650, y=500)

add_programme_flow_frame = Frame(add_training_frame, bg='white', highlightbackground='black', highlightthickness=1)
add_programme_flow_frame.place(x=650, y=550, height=70, width=500)

add_programme_flow_button = Button(add_programme_flow_frame, text="Choose File", bg='#E84966', fg='white',
                                     font=('arial', 18, 'italic'))
add_programme_flow_button.place(x=12, y=5)

add_no_file_chosen_label = Label(add_programme_flow_frame, bg='white', fg='black', text='No file chosen',
                                          font=('arial', 18, 'italic'))
add_no_file_chosen_label.place(x=310, y=14)








#Add Calendar in Add Training Page(Find Date)


def add_find_date():
    selected_date = add_training_calendar.get_date()
    if isinstance(selected_date, str):
        selected_date = datetime.strptime(selected_date, "%m/%d/%y").date()  # フォーマットを"%m/%d/%y"に修正する
    formatted_date = selected_date.strftime("%d/%m/%Y")  # 年を4桁で表示するようにフォーマットを"%d/%m/%Y"に変更する
    add_date_entry.delete(0, END)
    add_date_entry.insert(0, formatted_date)

# Create the calendar widget
add_training_calendar = Calendar(add_training_frame, selectmode='day', year=2023, month=10, day=30,
                                 background='#E84966', fieldbackground='#F5C8D0', foreground='white', selectbackground='#FC95A6',
                                 selectforeground='#E84966')
add_training_calendar.place(x=700, y=235)

add_training_calendar_button = Button(add_training_frame, bg='#E84966', fg='white', text='Find Date',
                                      font=('arial', 13, 'italic'), padx=10,
                                      command=add_find_date)
add_training_calendar_button.place(x=760, y=430)

add_date_entry = Entry(add_training_frame, font=16, width=40, highlightbackground='black', highlightthickness=1, textvariable=add_date_star)
add_date_entry.place(x=650, y=180)



#==================================================================
# ==================== Add Training List 2 UI Page =====================
#=================================================================

add_training_two_frame = Frame(hrhomepage, bg='white', highlightbackground='white', highlightthickness=1)
add_training_two_frame.place(x=150, y=20, height=715, width=1200)

add_training_two_top_label = Label(add_training_two_frame, text='Training List', bg='white', fg='#E84966',
                               font=('arial', 30))
add_training_two_top_label.place(x=15, y=15, width=400)


#=========================Available Text============================
add_two_available_label = Label(add_training_two_frame, text='Available', bg='white', fg='#E84966',
                               font=('arial', 20))
add_two_available_label.place(x=550, y=55, height=45, width=320)


#=========================Slot Text============================
add_two_slot_label = Label(add_training_two_frame, text='Slot ', bg='white', fg='#E84966',
                               font=('arial', 20))
add_two_slot_label.place(x=550, y=90, height=45, width=320)



#=======================Add Button=============================
add_icon = Image.open("next_icon.png")
photo5 = ImageTk.PhotoImage(add_icon)
add_button = Button(add_training_two_frame, image=photo5, bd=0, background='white', activebackground='white', command=add_training)
add_button.place(x=1100, y=70, width=80, height=30)


##=======================Back Button=============================
add_two_back_icon = Image.open("back_icon.png")
photo6 = ImageTk.PhotoImage(add_two_back_icon)
add_two_back_button = Button(add_training_two_frame, image=photo6, bd=0, background='white', activebackground='white', command=back_add_training)
add_two_back_button.place(x=1000, y=70, width=80, height=30)



#=============================Search Entry===================================
add_two_training_frame_search_entry = Entry(add_training_two_frame, bg='#F5C8D0', font=20,
                                            highlightcolor='#E84966', highlightbackground='#E84966',
                                            highlightthickness=3,
                                            textvariable=add_staff_search_star)
add_two_training_frame_search_entry.place(x=70, y=80, height=45, width=320)

#=============================Search Icon===================================
search_icon = Image.open("search_icon.png")
photo7 = ImageTk.PhotoImage(search_icon)
search_icon_label = Label(add_training_two_frame, image=photo7, bg='#F5C8D0')
search_icon_label.image = photo7
search_icon_label.place(x=350, y=85)



#========================Search Button===========================
add_two_search_button = Button(add_training_two_frame, text='Search', font=('arial', 13, 'bold'), width=15, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0', command=add_two_training_search)
add_two_search_button.place(x=400, y=85, width=80, height=30)


backhrtraining2frame =Frame(add_training_two_frame, bg='white')
backhrtraining2frame.place(x=40, y=130, height=555, width=1115)

#Add style
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview.Heading", background='#E84966', foreground='white', rowheight=100)


add_training_two_tree = ttk.Treeview(backhrtraining2frame, selectmode='extended', show='headings', columns=('Staff ID',
                                'Name', 'Department', 'Gender'),
                                style='style1.Treeview')
add_training_two_tree.place(x=20, y=0, relheight=0.97, relwidth=1)


#Striped row
add_training_two_tree.tag_configure('oddrow', background='#E43D5B')
add_training_two_tree.tag_configure('evenrow', background='#FF9DAF')


#Scrollbar for treeview
hrtraining2x_scroll = Scrollbar(add_training_two_tree, orient=HORIZONTAL, command=add_training_two_tree.xview)
hrtraining2y_scroll = Scrollbar(add_training_two_tree, orient=VERTICAL, command=add_training_two_tree.yview)
hrtraining2x_scroll.pack(side=BOTTOM, fill=X)
hrtraining2y_scroll.pack(side=RIGHT, fill=Y)
add_training_two_tree.config(xscrollcommand=hrtraining2x_scroll.set, yscrollcommand=hrtraining2y_scroll.set)


#Heading Name
add_training_two_tree.heading('Staff ID', text='Staff ID', anchor=CENTER)
add_training_two_tree.heading('Name', text='Name', anchor=CENTER)
add_training_two_tree.heading('Department', text='Department', anchor=CENTER)
add_training_two_tree.heading('Gender', text='Gender', anchor=CENTER)

add_training_two_tree.column('Staff ID', anchor=CENTER, width=90)
add_training_two_tree.column('Name', anchor=CENTER, width=90)
add_training_two_tree.column('Department', anchor=CENTER, width=90)
add_training_two_tree.column('Gender', anchor=CENTER, width=90)














# =============================================================================
def training_list_search():
    connect_database()
    #training_name = add_training_name_star.get()
    search = hrtraining_list_search_star.get()
    if not search:
        messagebox.showerror('Error', 'Please fill the search box!')

    else:
        cursor.execute("""SELECT Training_ID, Training_Name, Training_Venue, Date, Time, Department, No_Of_Participant FROM Add_Training 
        WHERE Training_Name LIKE ? ORDER BY date DESC""", ('%'+search+'%',))

        data = cursor.fetchall()
        if len(data) != 0:
            hrtraining_tree.delete(*hrtraining_tree.get_children())
            count = 0
            for records in data:
                if count % 2 ==0:
                    hrtraining_tree.insert('', END, values=records, tags=('evenrow',))

                else:
                    hrtraining_tree.insert('', END, values=records, tags=('oddrow',))
                count = count + 1
                conn.commit()

        else:
            messagebox.showerror('Error', 'There is no record in the database!')


def training_list_reset():
    display_training_list()
    hrtraining_list_search_star.set('')


hrtraining_list_search_star = tk.StringVar()
#=================================Training Detail ======================================================================
hrl_transFrame = Frame(hrhomepage, bg='white', highlightthickness=1)
hrl_transFrame.place(x=150, y=20, height=715, width=1200)


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


# Create the label
trainlabelhrl = tk.Label(secondhrl_frame, text='TRAINING', font=('Arial', 35), fg='#E84966', bg='white')
trainlabelhrl.place(x=10, y=20)

venue_static_labelhrl = tk.Label(secondhrl_frame, text='Venue:', font=('Arial', 20), fg='#E84966', bg='white')
venue_static_labelhrl.place(x=10, y=100)

venue_value_labelhrl = tk.Label(secondhrl_frame, fg='black', bg='white')
venue_value_labelhrl.place(x=100, y=103)

date_static_labelhrl = tk.Label(secondhrl_frame, text='Date:', font=('Arial', 20), fg='#E84966', bg='white')
date_static_labelhrl.place(x=10, y=150)

date_value_labelhrl = tk.Label(secondhrl_frame, fg='black', bg='white')
date_value_labelhrl.place(x=80, y=153)

time_static_labelhrl = tk.Label(secondhrl_frame, text='Time:', font=('Arial', 20), fg='#E84966', bg='white')
time_static_labelhrl.place(x=10, y=200)

time_value_labelhrl = tk.Label(secondhrl_frame, fg='black', bg='white')
time_value_labelhrl.place(x=80, y=203)

department_static_labelhrl = tk.Label(secondhrl_frame, text='Department:', font=('Arial', 20), fg='#E84966', bg='white')
department_static_labelhrl.place(x=10, y=250)

department_value_labelhrl = tk.Label(secondhrl_frame, fg='black', bg='white')
department_value_labelhrl.place(x=170, y=253)

program_flow_labelhrl = tk.Label(secondhrl_frame, text='Program Flow:', font=('Arial', 20), fg='#E84966', bg='white')
program_flow_labelhrl.place(x=10, y=300)


#Create a box under the program flow label
box_canvas_hrl = Canvas(secondhrl_frame, width=1150, height=450, bg='white', highlightthickness=1, highlightbackground='black')
box_canvas_hrl.place(x=10, y=350)



go_back_button_trd = tk.Button(hrl_transFrame, text="Go Back", command=go_back_trd)
go_back_button_trd.pack()


#==================================================================
# ==================== Training List UI Page =====================
#=================================================================


hrtraining_frame = Frame(hrhomepage, bg='white', highlightbackground='white', highlightthickness=1)
hrtraining_frame.place(x=150, y=20, height=715, width=1200)

hrtraining_top_label = Label(hrtraining_frame, text='Training List', bg='white', fg='#E84966',
                               font=('arial', 30))
hrtraining_top_label.place(x=15, y=15, width=400)




hrtraining_frame_search_entry = Entry(hrtraining_frame, bg='#F5C8D0', font=20,
                                        highlightcolor='#E84966', highlightbackground='#E84966',
                                        highlightthickness=3,
                                        textvariable=hrtraining_list_search_star)
hrtraining_frame_search_entry.place(x=70, y=80, height=45, width=320)


#=============================Search Icon===================================
search_icon = Image.open("search_icon.png")
photo = ImageTk.PhotoImage(search_icon)
search_icon_label = Label(hrtraining_frame, image=photo, bg='#F5C8D0')
search_icon_label.image = photo
search_icon_label.place(x=350, y=85)





#======================== Button ==================================


#========================Search Button===========================
hrtrainingsearch_button = Button(hrtraining_frame, text='Search', font=('arial', 13, 'bold'), width=15, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0', command=training_list_search)
hrtrainingsearch_button.place(x=400, y=85, width=80, height=30)
#-----------------------Open Buton=------------------------------------------------------------------------------------
open_training_button = Button(hrtraining_frame, text='Open', font=('arial', 13, 'bold'), width=10, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0',command=open_button_clicked)
open_training_button.place(x=700, y=85, width=80, height=30)


#========================Add Button===========================
add_training_button = Button(hrtraining_frame, text='Add', font=('arial', 13, 'bold'), width=10, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0', command=add_training_open)
add_training_button.place(x=800, y=85, width=80, height=30)

#========================Edit Button===========================
edit_training_button = Button(hrtraining_frame, text='Edit', font=('arial', 13, 'bold'), width=10, height=1, bd=0,
                              bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0', command=edit_training)
edit_training_button.place(x=900, y=85, width=80, height=30)

#========================Delete Button===========================
delete_training_button = Button(hrtraining_frame, text='Delete', font=('arial', 13, 'bold'), width=10, height=1, bd=0,
                      bg='#E84966', fg='white', cursor='hand2', activebackground='#F5C8D0', command=delete_training)
delete_training_button.place(x=1000, y=85, width=80, height=30)


backhrtrainingframe =Frame(hrtraining_frame, bg='white')
backhrtrainingframe.place(x=40, y=130, height=555, width=1115)


#Add style
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview.Heading", background='#E84966', foreground='white', rowheight=100)



# Create the training_tree widget
hrtraining_tree = ttk.Treeview(backhrtrainingframe, selectmode='extended', show='headings', columns=('Training ID', 'Training Name', 'Training Venue', 'Date', 'Time','Department', 'No. Participants'), style='style1.Treeview')
hrtraining_tree.place(x=20, y=0, relheight=0.97, relwidth=1)


#Striped row
hrtraining_tree.tag_configure('oddrow', background='#E43D5B')
hrtraining_tree.tag_configure('evenrow', background='#FF9DAF')


#Scrollbar for treeview
hrtrainingx_scroll = Scrollbar(hrtraining_tree, orient=HORIZONTAL, command=hrtraining_tree.xview)
hrtrainingy_scroll = Scrollbar(hrtraining_tree, orient=VERTICAL, command=hrtraining_tree.yview)
hrtrainingx_scroll.pack(side=BOTTOM, fill=X)
hrtrainingy_scroll.pack(side=RIGHT, fill=Y)
hrtraining_tree.config(xscrollcommand=hrtrainingx_scroll.set, yscrollcommand=hrtrainingy_scroll.set)


#columns=('Training ID', 'Training Name', 'Training Venue', 'Date', 'Time', 'No. Participants')

#Heading Name
hrtraining_tree.heading('Training ID', text='Training ID', anchor=CENTER)
hrtraining_tree.heading('Training Name', text='Training Name', anchor=CENTER)
hrtraining_tree.heading('Training Venue', text='Training Venue', anchor=CENTER)
hrtraining_tree.heading('Date', text='Date', anchor=CENTER)
hrtraining_tree.heading('Time', text='Time', anchor=CENTER)
hrtraining_tree.heading('Department', text='Department', anchor=CENTER)
hrtraining_tree.heading('No. Participants', text='No. Participants', anchor=CENTER)

hrtraining_tree.column('Training ID', anchor=CENTER, width=90)
hrtraining_tree.column('Training Name', anchor=CENTER, width=120)
hrtraining_tree.column('Training Venue', anchor=CENTER, width=90)
hrtraining_tree.column('Date', anchor=CENTER, width=90)
hrtraining_tree.column('Time', anchor=CENTER, width=90)
hrtraining_tree.column('Department', anchor=CENTER, width=90)
hrtraining_tree.column('No. Participants', anchor=CENTER, width=90)


display_hrtraining_list()



#====================================HR Scheduler=======================================================================
hrschedulerFrame = Frame(hrhomepage, bg='white', highlightthickness=1)
hrschedulerFrame.place(x=150, y=20, height=715, width=1200)
hrscedulerLabel = Label(hrschedulerFrame, text='Scheduler', font=('Arial', 30), fg='#E84966', bg='white')
hrscedulerLabel.place(x=15, y=15, width=400)
hrscedulerbottomFrame = Frame(hrschedulerFrame, bg='#f0f0f0')
hrscedulerbottomFrame.place(x=40, y=65, height=700, width=1115)


hr_Calendar = Frame(hrscedulerbottomFrame)
hr_Calendar.place(x = 160, y = 0, relwidth=0.97, relheight=5)


hr_month = date.today().month
hr_year = date.today().year

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
    monthYear = Label(hr_Calendar, text=writtenMonth + " " + str(year), font=("Arial", 20))
    monthYear.grid(column=2, row=0, columnspan=3)

# Function to switch month calendar (1 for forwards and -1 for backwards)
def hr_switchMonths(direction):
    global hr_Calendar
    global hr_month
    global hr_year
    # check if we are goint to a new year
    if hr_month == 12 and direction == 1:
        hr_month = 0
        hr_year += 1
    if hr_month == 1 and direction == -1:
        hr_month = 13
        hr_year -= 1


    # Reprint the calendar with the new values
    hr_Calendar.destroy()
    hr_Calendar = Frame(hrscedulerbottomFrame)
    hr_Calendar.place(x = 160, y = 0, relwidth=0.97, relheight=5)

    hr_printMonthYear(hr_month + direction, hr_year)  # pylint: disable=E0601
    hr_makeButtons()
    hr_month += direction
    hr_monthGenerator(hr_dayMonthStarts(hr_month, hr_year), hr_daysInMonth(hr_month, hr_year),hr_month, hr_year)
    
  
# Change month buttons at top of the page
def hr_makeButtons():
    goBack = Button(hr_Calendar, text="<", command=lambda: hr_switchMonths(-1))
    goBack.grid(column=0, row=0)
    goForward = Button(hr_Calendar, text=">", command=lambda: hr_switchMonths(1))
    goForward.grid(column=6, row=0)

# Creates most of the calendar
def hr_monthGenerator(startDate, numberOfDays,month,year):
    
    #staff details
    conn = sqlite3.connect("C:/Users/Ohta K/Desktop/SE/SE Project")
    cursor = conn.cursor()

    hr_scheduler_training= cursor.execute("""SELECT Add_Training.Date, Add_Training.Training_Name FROM Add_Training
                                        """)
    hr_scheduler_date = cursor.fetchall()


        

    # Holds the names for each day of the week
    dayNames = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Places the days of the week on the top of the calender
    for nameNumber in range(len(dayNames)):
        names = Label(hr_Calendar, text=dayNames[nameNumber], fg="black")
        names.grid(column=nameNumber, row=1, sticky='nsew')

    index = 0
    day = 1
    for row in range(6):
        for column in range(7):
            if index >= startDate and index <= startDate + numberOfDays - 1:
                # Creates a frame that will hold each day and text box
                dayFrame = Frame(hr_Calendar)

                # Creates a textbox inside the dayframe
                t = Text(dayFrame, width=15, height=4, fg= 'black')
                t.grid(row=1)

                if len(str(month)) ==1:
                    month = str('0')+ str(month)
                    
                if len(str(day)) ==1:
                    day = str('0')+ str(day)
                    

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
                day= int(day)
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
hr_today = date.today()

hr_printMonthYear(hr_month, hr_year)
hr_makeButtons()
hr_monthGenerator(hr_dayMonthStarts(hr_month, hr_year), hr_daysInMonth(hr_month, hr_year),hr_month,hr_year)

def show_hr_Calendar():
    show_frame(hrschedulerFrame)
    hr_monthGenerator(hr_dayMonthStarts(hr_month, hr_year), hr_daysInMonth(hr_month, hr_year),hr_month,hr_year)

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
conn = sqlite3.connect("C:/Users/Ohta K/Desktop/SE/SE Project")
cursor = conn.cursor()
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

conn = sqlite3.connect("C:/Users/Ohta K/Desktop/SE/SE Project")
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
    smtp_password = 'nspuhlxduhtsapjr'

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

    try:
        connect_database()

        cursor.execute(
            """SELECT Available_Slot FROM Add_Training WHERE Training_ID = ?""",
            (selected_training_id,)
        )
        available_slot = cursor.fetchone()[0]

        if available_slot == 0:
            messagebox.showwarning("Training Full", "The training is already full. Enrollment cannot be added.")
            return

        # Update No_Of_Participant in Add_Training table
        cursor.execute(
            """UPDATE Add_Training SET No_Of_Participant = No_Of_Participant + 1 WHERE Training_ID = ?""",
            (selected_training_id,)
        )

        # Update Available_Slot in Add_Training table
        cursor.execute(
            """UPDATE Add_Training SET Available_Slot = Training_Budget / Budget_Per_Person - No_Of_Participant
               WHERE Training_ID = ?""",
            (selected_training_id,)
        )

        # Commit the changes
        conn.commit()

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
                (1, staff_id, selected_training_id))
            cursor.execute(
                "INSERT INTO Participants (Training_ID, Staff_ID) VALUES (?, ?)",
                (selected_training_id, staff_id))

        # Commit the changes
        conn.commit()

        # Clear the selected Training ID in the Combobox
        training_id_combobox.set('')

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        # Close the connection to the SMTP server
        server.quit()
        conn.close()



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

twlabel = Label(hrhome, text='This Month', font=('Arial', 15, 'bold'), fg='#E84966', bg='white')
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
conn = sqlite3.connect("C:/Users/Ohta K/Desktop/SE/SE Project")
cursor = conn.cursor()
cursor.execute("SELECT Training_Name,Training_Venue, Date, Time, No_Of_Participant FROM Add_Training")
hrhometraining_data = cursor.fetchall()  # Fetches all the rows of data

current_month = datetime.now().month
current_year = datetime.now().year

# Filter the data for the current month and year
hrhome_filtered_data = []
for row in hrhometraining_data:
    date_str = row[2]  # Assuming 'Date' is the third column in the result
    date_obj = parser.parse(date_str)  # Parse the date string using dateutil.parser.parse()
    if date_obj.month == current_month and date_obj.year == current_year:
        hrhome_filtered_data.append(row)
# Insert data into the treeview
for row in hrhome_filtered_data:
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
    activebackground='#74bc94',
    command=lambda: show_frame(hrtraining_frame)
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
    command= show_hr_Calendar
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
trainlabel = Label(second_frame, text='TRAINING', font=('Arial', 35), fg='#2181AA', bg='white')
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

# Create a box under the program flow label
box_canvas_ep = Canvas(second_frame, width=1150, height=450, bg='white', highlightthickness=1, highlightbackground='black')
box_canvas_ep.place(x=10, y=350)


# Create a new frame for the Register button
register_button_frame_ep = Frame(second_frame, bg='#7AB8F0')
register_button_frame_ep.place(x=500, y=820, width=120, height=30)

# Function to handle the register button click
def register_button_ep_clicked():
    conn = sqlite3.connect("C:/Users/Ohta K/Desktop/SE/SE Project")
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

    cursor.execute(
        "SELECT Approval FROM Enrollment_Request WHERE Staff_ID = ? AND Training_ID = ? AND Approval = 1",
        (staff_id, training_id))
    result = cursor.fetchone()
    if result:
        messagebox.showwarning("Already Approved",
                               f"The enrollment for Staff ID: {staff_id} and Training ID: {training_id} has already been approved. Please check your email or Staff Homepage")
        return

# Check if the selected Staff_ID and Training_ID combination already exists in Enrollment_Request table with Approval value of 0
    cursor.execute(
        "SELECT Approval FROM Enrollment_Request WHERE Staff_ID = ? AND Training_ID = ? AND Approval = 0",
        (staff_id, training_id))
    result = cursor.fetchone()
    if result:
        messagebox.showwarning("Already Rejected",
                               f"Sorry to inform you,The enrollment for Staff ID: {staff_id} and Training ID: {training_id} has already been rejected.")
        return

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
stschedulerFrame = Frame(staffhomepage, bg='white', highlightthickness=1)
stschedulerFrame.place(x=150, y=20, height=715, width=1200)
stscedulerLabel = Label(stschedulerFrame, text='Scheduler', font=('Arial', 30), fg='#2181aa', bg='white')
stscedulerLabel.place(x=15, y=15, width=400)
stscedulerbottomFrame = Frame(stschedulerFrame, bg='#f0f0f0')
stscedulerbottomFrame.place(x=40, y=65, height=700, width=1115)

Calendar = Frame(stscedulerbottomFrame)
Calendar.place(x = 160, y = 0, relwidth=0.97, relheight=5)



month = date.today().month
year = date.today().year

def get_staff_id_scheduler(username, password):
    # データベースに接続
    conn = sqlite3.connect("C:/Users/Ohta K/Desktop/SE/SE Project")
    cursor = conn.cursor()

    # ログインしているユーザーからStaff_IDを取得
    cursor.execute("SELECT Staff_ID FROM Staff_Information WHERE User_name=? AND Password=?", (username, password))
    result = cursor.fetchone()
    staff_id_scheduler = result[0] if result else None

    if staff_id_scheduler is None:
        print("User not found")
    
    # データベース接続を閉じる
    conn.close()

    return staff_id_scheduler

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


    # Reprint the calendar with the new values
    Calendar.destroy()
    Calendar = Frame(stscedulerbottomFrame)
    Calendar.place(x = 15, y = 0, relwidth=0.97, relheight=5)

    printMonthYear(month + direction, year)  # pylint: disable=E0601
    makeButtons()
    month += direction
    monthGenerator(dayMonthStarts(month, year), daysInMonth(month, year),month, year)
    
  
# Change month buttons at top of the page
def makeButtons():
    goBack = Button(Calendar, text="<", command=lambda: switchMonths(-1))
    goBack.grid(column=0, row=0)
    goForward = Button(Calendar, text=">", command=lambda: switchMonths(1))
    goForward.grid(column=6, row=0)

# Creates most of the calendar
def monthGenerator(startDate, numberOfDays, month, year):
    
    staff_id_scheduler = get_staff_id_scheduler(username, password)
    staff_id_scheduler_training= cursor.execute("""SELECT Add_Training.Date, Add_Training.Training_Name FROM Add_Training
                                                            JOIN Participants ON Add_Training.Training_ID = Participants.Training_ID
                                                            WHERE Participants.Staff_ID = ? """,(staff_id_scheduler,))
    scheduler_date = cursor.fetchall()
    

        

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

                if len(str(day)) ==1:
                    day = str('0')+ str(day)


                for i in scheduler_date:
                    if i[0][3:5]  == str(month) and str(i[0][0:2]) == str(day) and str(i[0][6:10]) == str(year) :
                        t.insert(END,str(i[1]))
                        print("1")
                        

                    else:
                        pass


                # Changes changes dayframe to be formated correctly
                dayFrame.grid(row=row + 2, column=column, sticky='nsew')
                dayFrame.columnconfigure(0, weight=1)
                dayNumber = Label(dayFrame, text=day)
                dayNumber.grid(row=0)
                day= int(day)
                day += 1
            index += 1
##    # Creates the buttons to load and save JSON's
##    loadFrom =Button(Calendar, text="load month from...", command=loadFromJSON)
##    saveToButton = Button(Calendar, text="save month to...", command=saveToJSON)
##
##    # Places them below the calendar
##    loadFrom.grid(row=8, column=4)
##    saveToButton.grid(row=8, column=2)

##def saveToJSON():
##    # Saves the raw text data from the text objects
##    for day in range(len(textObjectDict)):
##        saveDict[day] = textObjectDict[day + 1].get("1.0", "end - 1 chars")
##
##    # Asks the user for a file location and saves a JSON containg the text for each day.
##    fileLocation = filedialog.asksaveasfilename(initialdir="/", title="Save JSON to..")
##    if fileLocation != '':
##        with open(fileLocation, 'w') as jFile:
##            json.dump(saveDict, jFile)
##
##def loadFromJSON():
##    # Asks the user for a JSON file to open
##    fileLocation = filedialog.askopenfilename(initialdir="/", title="Select a JSON to open")
##    if fileLocation != '':
##        f = open(fileLocation)
##        global saveDict
##        saveDict = json.load(f)
##
##        # Copies the saved text data to the current text objects
##        for day in range(len(textObjectDict)):
##            textObjectDict[day + 1].insert("1.0", saveDict[str(day)])

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



# This makes the grid object appear
today = date.today()

printMonthYear(month, year)
makeButtons()
monthGenerator(dayMonthStarts(month, year), daysInMonth(month, year), month, year)

def show_Calendar():
    show_frame(stschedulerFrame)
    monthGenerator(dayMonthStarts(month, year), daysInMonth(month, year), month, year)
    


#=================================================Staff home page=======================================================
staffhomepage.configure(bg='white')

transFrame = Frame(staffhomepage, bg='white', highlightthickness=1)
transFrame.place(x=150, y=20, height=715, width=1200)

# Create the label
TransTopLabel = Label(transFrame, text='Home', font=('Arial', 30), fg='#2181aa', bg='white')
TransTopLabel.place(x=15, y=15, width=400)
TransBottomFrame = Frame(transFrame, bg='white')
TransBottomFrame.place(x=40, y=65, height=700, width=1115)
column1 = Frame(TransBottomFrame, bg='white')
column1.grid(sticky='nw', row=0, column=0, padx=45)

column2 = Frame(TransBottomFrame, bg='white')
column2.grid(sticky='nw', row=0, column=1, padx=45)

column3 = Frame(TransBottomFrame, bg='white')
column3.grid(sticky='nw', row=0, column=2, padx=45)

conn = sqlite3.connect("C:/Users/Ohta K/Desktop/SE/SE Project")
cursor = conn.cursor()

def display_page(username, password, rows):
    st_transFrame = Frame(staffhomepage, bg='white', highlightthickness=1)
    st_transFrame.place(x=150, y=20, height=715, width=1200)

    # Create the label
    main_frame = Frame(st_transFrame)
    main_frame.pack(side=TOP, fill=BOTH, expand=True)
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=True)
    second_frame = Frame(my_canvas, background='white')
    second_frame.pack(side=TOP, fill=BOTH, expand=True)
    trainlabel = Label(second_frame, text='TRAINING', font=('Arial', 35), fg='#2181AA', bg='white')
    trainlabel.place(x=0, y=15, width=400)

    my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    my_canvas.create_window((0, 0), window=second_frame, anchor="nw", width=window.winfo_screenwidth(),
                            height=window.winfo_screenheight())

    venue_static_label = Label(second_frame, text=f'Venue: {rows[3]}', font=('Arial', 20), fg='#2181AA', bg='white')
    venue_static_label.place(x=50, y=100)

    date_static_label = Label(second_frame, text=f'Date: {rows[4]}', font=('Arial', 20), fg='#2181AA', bg='white')
    date_static_label.place(x=50, y=150)

    time_static_label = Label(second_frame, text=f'Time: {rows[5]}', font=('Arial', 20), fg='#2181AA', bg='white')
    time_static_label.place(x=50, y=200)

    department_static_label = Label(second_frame, text=f'Department: {rows[6]}', font=('Arial', 20), fg='#2181AA', bg='white')
    department_static_label.place(x=50, y=250)

    program_flow_label = Label(second_frame, text='Program Flow: ', font=('Arial', 20), fg='#2181AA', bg='white')
    program_flow_label.place(x=50, y=300)

    # Create a box under the program flow label
    box_canvas_ep = Canvas(second_frame, width=800, height=250, bg='white', highlightthickness=1,
                           highlightbackground='black')
    box_canvas_ep.place(x=250, y=350)
    stylesfp = ttk.Style()
    
    stylesfp.theme_use("clam")
    stylesfp.configure("Search.TEntry", background="#7AB8F0", foreground='white', rowheight=100)

    open_tree = ttk.Treeview(
        second_frame,
        selectmode="extended",
        show='headings',
        columns=('Anything'),
        style="Treeview"
    )
    x_scrollersfp = Scrollbar(open_tree, orient=HORIZONTAL, command=open_tree.xview)
    y_scrollersfp = Scrollbar(open_tree, orient=VERTICAL, command=open_tree.yview)
    x_scrollersfp.pack(side=BOTTOM, fill=X)
    y_scrollersfp.pack(side=RIGHT, fill=Y)

    # Create a new frame for the Go back button
    goback_frame_ep = Button(st_transFrame, bg='#7AB8F0', text='Go back', command=show_canban)
    goback_frame_ep.place(x=500, y=650, width=120, height=30)


def show_canban():
    show_frame(transFrame)

    cursor.execute("SELECT Staff_ID FROM Staff_Information WHERE User_name=? AND Password=?", (username, password))
    result = cursor.fetchone()

    if result is not None:
        staff_id_canvan = result[0]  # Staff_IDを取得

        # Execute the query to retrieve specific data based on the staff ID
        cursor.execute(
            "SELECT Enrollment_Request.Approval, Enrollment_Request.Training_ID, Add_Training.Training_Name, "
            "Add_Training.Training_Venue, Add_Training.Date, Add_Training.Time, Add_Training.Department, "
            "Add_Training.Program_Flow,Staff_Information.Role "
            "FROM Enrollment_Request "
            "INNER JOIN Add_Training ON Enrollment_Request.Training_ID = Add_Training.Training_ID "
            "INNER JOIN Staff_Information ON Staff_Information.Staff_ID = Enrollment_Request.Staff_ID "
            "WHERE Enrollment_Request.Approval='1' AND Staff_Information.Staff_ID=?", (staff_id_canvan,))
        rows = cursor.fetchall()

        for frame in column1.winfo_children() + column2.winfo_children() + column3.winfo_children():
            frame.destroy()

        # Display the retrieved data in the columns
        for i, row in enumerate(rows):
            if i % 3 == 0:
                frame = Frame(column1, highlightthickness=2, highlightbackground="black", bg='#2181aa')
                label1 = Label(frame, font=('Arial', 20, 'bold'), text=row[2], bg='#2181aa', width=15,
                               anchor='nw')  # Collect training name
                label1.pack()
                label1.bind("<Button-1>", lambda event, row=row: display_page(username, password, row))
                label2 = Label(frame, font=('Arial', 15), text=f"{row[3]}.{row[4]}", bg='#2181aa',
                               anchor='nw')  # Collect venue and date
                label2.pack(anchor='nw')
                label2.bind("<Button-1>", lambda event, row=row: display_page(username, password, row))
                frame.grid(sticky='nw', pady=20, ipady=20)
                frame.bind("<Button-1>", lambda event, row=row: display_page(username, password, row))
            elif i % 3 == 1:
                frame = Frame(column2, highlightthickness=2, highlightbackground="black", bg='#2181aa')
                label1 = Label(frame, font=('Arial', 20, 'bold'), text=row[2], bg='#2181aa', width=15,
                               anchor='nw')  # Collect training name
                label1.pack()
                label1.bind("<Button-1>", lambda event, row=row: display_page(username, password, row))
                label2 = Label(frame, font=('Arial', 15), text=f"{row[3]}.{row[4]}", bg='#2181aa',
                               anchor='nw')  # Collect venue and date
                label2.pack(anchor='nw')
                label2.bind("<Button-1>", lambda event, row=row: display_page(username, password, row))
                frame.grid(sticky='nw', pady=20, ipady=20)
                frame.bind("<Button-1>", lambda event, row=row: display_page(username, password, row))
            else:
                frame = Frame(column3, highlightthickness=2, highlightbackground="black", bg='#2181aa')
                label1 = Label(frame, font=('Arial', 20, 'bold'), text=row[2], bg='#2181aa', width=15,
                               anchor='nw')  # Collect training name
                label1.pack()
                label1.bind("<Button-1>", lambda event, row=row: display_page(username, password, row))
                label2 = Label(frame, font=('Arial', 15), text=f"{row[3]}.{row[4]}", bg='#2181aa',
                               anchor='nw')  # Collect venue and date
                label2.pack(anchor='nw')
                label2.bind("<Button-1>", lambda event, row=row: display_page(username, password, row))
                frame.grid(sticky='nw', pady=20, ipady=20)
                frame.bind("<Button-1>", lambda event, row=row: display_page(username, password, row))

    else:
        print("Invalid username or password")


# Call the initial function to display the training information
show_canban()






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
                     command=show_canban)


staffTraining_Sch_b = Button(staffmenuFrame, text="Training \nSchedule", image=stafftrain_sch_icon2, compound=TOP,
                             bg='#2181aa', relief='flat', fg='white', font=('yu gothic ui', 13),
                             activebackground='#74bc94',command= show_Calendar)

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

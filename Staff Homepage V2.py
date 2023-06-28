from tkinter import messagebox
import sqlite3
from tkinter import *

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
transFrame = Frame(staffhomepage, bg='white')
transFrame.place(x=150, y=20, height=715, width=1250)

# Create the label
TransTopLabel = Label(transFrame, text='Home', font=('Arial', 55),  fg='#2181aa',bg='white')
TransTopLabel.place(x=0, y=0, width=400)

TransBottomFrame = Frame(transFrame, bg='white')
TransBottomFrame.place(x=40, y=85, height=600, width=1250)

column1 = Frame(TransBottomFrame,bg='white')
column1.grid(sticky='nw',row=0,column=0,padx=45)

column2 = Frame(TransBottomFrame,bg='white')
column2.grid(sticky='nw',row=0,column=1,padx=45)

column3 = Frame(TransBottomFrame,bg='white')
column3.grid(sticky='nw',row=0,column=2,padx=45)

#Connect to database to retreive data into the card frames
conn = sqlite3.connect(r'C:\Users\User\OneDrive\Desktop\SE Project.unknown')

cursor = conn.cursor()
# Retrieve the data of the staff for the homepage only
cursor.execute("SELECT Enrollment_Request.Approval, Enrollment_Request.Training_ID, Add_Training.Training_Name, Add_Training.Training_Venue, Add_Training.Date, "
"Staff_Information.Role FROM Enrollment_Request INNER JOIN Add_Training ON Enrollment_Request.Training_ID = Add_Training.Training_ID "
"INNER JOIN Staff_Information ON Staff_Information.Staff_ID = Enrollment_Request.Staff_ID WHERE Enrollment_Request.Approval='1' and Staff_Information.Role='staff'")
rows = cursor.fetchall()
for frame in column1.winfo_children() + column2.winfo_children() + column3.winfo_children():
    frame.destroy()

    # Retrieve data from sqlite database into card frames
for i, row in enumerate(rows):
    if row[0] == '1': # If training has approved
       if i % 3 == 0:
          frame = Frame(column1, highlightthickness=2, highlightbackground="black", bg='#2181aa')
       elif i % 3 == 1:
          frame = Frame(column2, highlightthickness=2, highlightbackground="black", bg='#2181aa')
       else:
          frame = Frame(column3, highlightthickness=2, highlightbackground="black", bg='#2181aa')
       label1 = Label(frame, font=('Arial', 20, 'bold'), text=row[2], bg='#2181aa',width=15,anchor='nw')  # Collect training name
       label1.pack()
       label2 = Label(frame, font=('Arial', 15), text=f"{row[3]}.{row[4]}", bg='#2181aa',anchor='nw')  # Collect venue and date
       label2.pack(anchor='nw')
       frame.grid(sticky='nw',pady=20,ipady=20)
       conn.close()

#Destroy the card frames by refreshing from refresh button
def refresh_data():
    conn = sqlite3.connect(r'C:\Users\User\OneDrive\Desktop\SE Project.unknown')

    cursor = conn.cursor()
    # Retrieve the data of the staff for the homepage only
    cursor.execute("SELECT Enrollment_Request.Approval, Enrollment_Request.Training_ID, Add_Training.Training_Name, Add_Training.Training_Venue, Add_Training.Date, "
        "Staff_Information.Role FROM Enrollment_Request INNER JOIN Add_Training ON Enrollment_Request.Training_ID = Add_Training.Training_ID "
        "INNER JOIN Staff_Information ON Staff_Information.Staff_ID = Enrollment_Request.Staff_ID WHERE Enrollment_Request.Approval='1' and Staff_Information.Role='staff'")
    rows = cursor.fetchall()
    for frame in column1.winfo_children() + column2.winfo_children() + column3.winfo_children():
        frame.destroy()

    # Retrieve data from sqlite database into card frames
    for i, row in enumerate(rows):
        if row[0] == '1': # If training has approved
            if i % 3 == 0:
                frame = Frame(column1, highlightthickness=2, highlightbackground="black", bg='#2181aa')
            elif i % 3 == 1:
                frame = Frame(column2, highlightthickness=2, highlightbackground="black", bg='#2181aa')
            else:
                frame = Frame(column3, highlightthickness=2, highlightbackground="black", bg='#2181aa')
            label1 = Label(frame, font=('Arial', 20, 'bold'), text=row[2], bg='#2181aa',width=15,anchor='nw')  # Collect training name
            label1.pack()
            label2 = Label(frame, font=('Arial', 15), text=f"{row[3]}.{row[4]}", bg='#2181aa',anchor='nw')  # Collect venue and date
            label2.pack(anchor='nw')
            frame.grid(sticky='nw',pady=20,ipady=20)
            conn.close()

display1 = Button(transFrame, text='Refresh', font=(35),fg='white',bg='#2181aa', width=10,command=refresh_data) #Refresh the whole card frames if there is new data inside the sqlite database
display1.place(x=800, y=20)
menuFrame = Frame(staffhomepage, bg='#2181aa', width=170, height=715, highlightthickness=1)
menuFrame.place(x=0, y=20)

# Defining the buttons for menu bar in Home page left
staffshome1_icon = PhotoImage(file="house_icon.png")
stafflist1_training_icon = PhotoImage(file="ls_icon.png")
stafftrain1_sch_icon = PhotoImage(file="ts_icon.png")
stafflogout1_icon = PhotoImage(file="logout_icon.png")

home_b = Button(menuFrame, text="Home", image=staffshome1_icon, compound=TOP, bg='#2181aa', relief='flat', fg='white',
                font=('yu gothic ui', 13), activebackground='#74bc94',command=staffhome)
Training_Sch_b = Button(menuFrame, text="Training \nSchedule", image=stafftrain1_sch_icon, compound=TOP, bg='#2181aa', relief='flat',
                   fg='white', font=('yu gothic ui', 13), activebackground='#74bc94',command=schdulerpage)
list_training_b = Button(menuFrame, text="Training List", image=stafflist1_training_icon, compound=TOP, bg='#2181aa',
                          relief='flat', fg='white', font=('yu gothic ui', 13), activebackground='#74bc94',command=staff_training_list)
logout_b = Button(menuFrame, text="Log Out", image=stafflogout1_icon, compound=TOP, bg='#2181aa', relief='flat', fg='white',
                  font=('yu gothic ui', 13), activebackground='#74bc94', command=logout_system)

# Placing buttons in menu bar Home Page
home_b.place(x=15, y=40, width=150)
list_training_b.place(x=15, y=130, width=150)
Training_Sch_b.place(x=15, y=240, width=150)
logout_b.place(x=15, y=350, width=150)

window.mainloop()
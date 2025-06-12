import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import csv
from datetime import datetime, timedelta
import time
import os
import functools


# Define global variables for day and time
current_day = "Monday"
current_time = "08:00"
week = 6

# Function to manually set the day and time using global variables
def set_day_and_time(day, time, time_label):
    # Update the time label
    time_label.config(text=f'{day} {time}')


# Function to resize the logo
def resize_image(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(image)

# Function to read data from a file
def read_data_from_file(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            lines = file.readlines()  # Skip the first row (heading)
            data = [line.strip().split(",") for line in lines]
        return data
    else:
        print(f"Error: {filename} not found.")
        return []

# Function to read initial data from text files
def read_initial_data():
    student_info_data = read_data_from_file("student_info.txt")
    faculty_info_data = read_data_from_file("faculty_info.txt")
    subject_info_data = read_data_from_file("subject_info.txt")
    attendance_data = read_data_from_file("attendance_StudentID.txt")
    timetable_data = read_data_from_file("timetables_StudentID.txt")
    assignment_data = read_data_from_file("assignments_StudentID.txt")
    return student_info_data, faculty_info_data, subject_info_data, attendance_data, timetable_data, assignment_data

# Function to write data to a text file
def write_data_to_file(filename, data):
    with open(filename, "w") as file:
        if data:
            file.write(",".join(data[0]) + "\n")
            for line in data[1:]:
                file.write(",".join(line) + "\n")

# Function to write updated data to text files
def write_data_to_files(student_info_data, faculty_info_data, subject_info_data, attendance_data, timetable_data, assignment_data):
    write_data_to_file("student_info.txt", student_info_data)
    write_data_to_file("faculty_info.txt", faculty_info_data)
    write_data_to_file("subject_info.txt", subject_info_data)
    write_data_to_file("attendance_StudentID.txt", attendance_data)
    write_data_to_file("timetables_StudentID.txt", timetable_data)
    write_data_to_file("assignments_StudentID.txt", assignment_data)


def exit_application(root):
    # Destroy the main Tkinter window
    root.destroy()
    # Write all data to files
    write_data_to_files(student_info, faculty_info, subject_info, attendance_data, timetable_data, assignment_data)


# Function to read initial data from text files
student_info, faculty_info, subject_info, attendance_data, timetable_data, assignment_data = read_initial_data()


# Function to validate login credentials
def login(student_info, faculty_info):
    try:
        username = entry_username.get()
        password = entry_password.get()

        # Check if the username exists in student_info
        for student in student_info:
            if student[0] == username:
                if student[1] == password:
                    full_name = student[2]
                    messagebox.showinfo("Login Successful", f"Welcome, {full_name}!")
                    window.destroy()  # Close login window
                    student_homepage(username)  # Call function to open student home page
                    return

        # Check if the username exists in faculty_info
        for faculty in faculty_info:
            if faculty[0] == username:
                if faculty[1] == password:
                    full_name = faculty[2]
                    messagebox.showinfo("Login Successful", f"Welcome, {full_name}!")
                    window.destroy()  # Close login window
                    faculty_homepage(username)  # Call function to open faculty dashboard
                    return

        # If username or password is incorrect
        messagebox.showerror("Login Failed", "Invalid username or password.")
    except IndexError:
        messagebox.showerror("Error", "Index error occurred. Please check the data format.")
    except ValueError:
        messagebox.showerror("Error", "Value error occurred. Please check the data format.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


def display_student_profile(username, student_info, profile_frame):
    for student in student_info:
        if username == student[0]:
            # Display Name
            name_label = tk.Label(profile_frame, text=f"Name:", font=("Montserrat", 20), anchor="w")
            name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            name_data_label = tk.Label(profile_frame, text=student[2], font=("Montserrat", 20, "bold"), anchor="e",
                                       borderwidth=1, relief="solid", fg="green")
            name_data_label.grid(row=0, column=1, padx=10, pady=5, sticky="e")

            # Display Student ID
            student_id_label = tk.Label(profile_frame, text=f"Student ID:", font=("Montserrat", 20), anchor="w")
            student_id_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            student_id_data_label = tk.Label(profile_frame, text=student[0], font=("Montserrat", 20, "bold"),
                                             anchor="e", borderwidth=1, relief="solid", fg="green")
            student_id_data_label.grid(row=1, column=1, padx=10, pady=5, sticky="e")

            # Display Passport/IC Number
            passport_label = tk.Label(profile_frame, text=f"Passport/IC Number:", font=("Montserrat", 20), anchor="w")
            passport_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
            passport_data_label = tk.Label(profile_frame, text=student[3], font=("Montserrat", 20, "bold"), anchor="e",
                                           borderwidth=1, relief="solid", fg="green")
            passport_data_label.grid(row=2, column=1, padx=10, pady=5, sticky="e")

            # Display Nationality
            nationality_label = tk.Label(profile_frame, text=f"Nationality:", font=("Montserrat", 20), anchor="w")
            nationality_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
            nationality_data_label = tk.Label(profile_frame, text=student[4], font=("Montserrat", 20, "bold"),
                                              anchor="e", borderwidth=1, relief="solid", fg="green")
            nationality_data_label.grid(row=3, column=1, padx=10, pady=5, sticky="e")

            # Display Gender
            gender_label = tk.Label(profile_frame, text=f"Gender:", font=("Montserrat", 20), anchor="w")
            gender_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
            gender_data_label = tk.Label(profile_frame, text=student[5], font=("Montserrat", 20, "bold"), anchor="e",
                                         borderwidth=1, relief="solid", fg="green")
            gender_data_label.grid(row=4, column=1, padx=10, pady=5, sticky="e")

            # Display Programme
            programme_label = tk.Label(profile_frame, text=f"Programme:", font=("Montserrat", 20), anchor="w")
            programme_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
            programme_data_label = tk.Label(profile_frame, text=student[6], font=("Montserrat", 20, "bold"), anchor="e",
                                            borderwidth=1, relief="solid", fg="green")
            programme_data_label.grid(row=5, column=1, padx=10, pady=5, sticky="e")

            # Display Date of Birth
            dob_label = tk.Label(profile_frame, text=f"Date of Birth:", font=("Montserrat", 20), anchor="w")
            dob_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
            dob_data_label = tk.Label(profile_frame, text=student[7], font=("Montserrat", 20, "bold"), anchor="e",
                                      borderwidth=1, relief="solid", fg="green")
            dob_data_label.grid(row=6, column=1, padx=10, pady=5, sticky="e")

            break  # Exit loop once student is found


def populate_timetable(username, parent_frame):
    # Find the timetable entry for the given username
    student_timetable_entry = None
    for index, entry in enumerate(timetable_data):
        if entry[0] == username:
            student_timetable_entry = entry
            timetable_entry_index = index  # Save the index of the entry
            break

    if student_timetable_entry:
        # Create the timetable grid headers
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        times = ['8:00 to 10:00 AM', '10:00 AM to 12:00 PM', '1:00 to 3:00 PM', '3:00 to 5:00 PM']

        # Create empty boxes for days and time slots in the first row and first column
        # Create empty boxes for days and time slots in the first row and first column
        for i, day in enumerate(days):
            label = tk.Label(parent_frame, text=day, height=4, width=20, font=("Helvetica", 14), relief="ridge")
            label.grid(row=i + 1, column=0, padx=5, pady=5)

        for j, time_slot in enumerate(times):
            label = tk.Label(parent_frame, text=time_slot, height=4, width=20, font=("Helvetica", 14), relief="ridge")
            label.grid(row=0, column=j + 1, padx=5, pady=5)

        # Populate timetable based on student timetable entry
        for i in range(len(student_timetable_entry[1:]) + 1):
            subject_code = student_timetable_entry[i]
            if subject_code == 'CSC1024':
                label_subject = tk.Label(parent_frame, text=f"{subject_info[0][0]}:\n{subject_info[0][1]}", height=4,
                                         width=20, font=("Helvetica", 14), relief="solid")
                label_subject.grid(row=1, column=1, padx=5, pady=5)
                label_instructor = tk.Label(parent_frame, text=f"{subject_info[0][2]}",
                                            font=("Helvetica", 8))
                label_instructor.grid(row=1, column=1, sticky="s", padx=5)
                label_room = tk.Label(parent_frame, text=f"{subject_info[0][3]}", font=("Helvetica", 8))
                label_room.grid(row=1, column=1, sticky="n", padx=5)
                label_subject = tk.Label(parent_frame, text=f"{subject_info[0][0]}:\n{subject_info[0][1]}", height=4,
                                         width=20, font=("Helvetica", 14), relief="solid")
                label_subject.grid(row=3, column=2, padx=5, pady=5)
                label_instructor = tk.Label(parent_frame, text=f"{subject_info[0][2]}",
                                            font=("Helvetica", 8))
                label_instructor.grid(row=3, column=2, sticky="s", padx=5)
                label_room = tk.Label(parent_frame, text=f"{subject_info[0][3]}", font=("Helvetica", 8))
                label_room.grid(row=3, column=2, sticky="n", padx=5)
            elif subject_code == 'MTH1114':
                label_subject = tk.Label(parent_frame, text=f"{subject_info[1][0]}:\n{subject_info[1][1]}", height=4,
                                         width=20, font=("Helvetica", 14), relief="solid")
                label_subject.grid(row=2, column=1, padx=5, pady=5)

                label_instructor = tk.Label(parent_frame, text=f"{subject_info[1][2]}",
                                            font=("Helvetica", 8))
                label_instructor.grid(row=2, column=1, sticky="s", padx=5)
                label_room = tk.Label(parent_frame, text=f"{subject_info[1][3]}", font=("Helvetica", 8))
                label_room.grid(row=2, column=1, sticky="n", padx=5)

                label_subject = tk.Label(parent_frame, text=f"{subject_info[1][0]}:\n{subject_info[1][1]}", height=4,
                                         width=20, font=("Helvetica", 14), relief="solid")
                label_subject.grid(row=4, column=2, padx=5, pady=5)
                label_instructor = tk.Label(parent_frame, text=f"{subject_info[1][2]}",
                                            font=("Helvetica", 8))
                label_instructor.grid(row=4, column=2, sticky="s", padx=5)
                label_room = tk.Label(parent_frame, text=f"{subject_info[1][3]}", font=("Helvetica", 8))
                label_room.grid(row=4, column=2, sticky="n", padx=5)
            elif subject_code == 'MPU3112':
                label_subject = tk.Label(parent_frame, text=f"{subject_info[2][0]}:\n{subject_info[2][1]}", height=4,
                                         width=20, font=("Helvetica", 14), relief="solid")
                label_subject.grid(row=3, column=3, padx=5, pady=5)
                label_instructor = tk.Label(parent_frame, text=f"{subject_info[2][2]}",
                                            font=("Helvetica", 8))
                label_instructor.grid(row=3, column=3, sticky="s", padx=5)
                label_room = tk.Label(parent_frame, text=f"{subject_info[2][3]}", font=("Helvetica", 8))
                label_room.grid(row=3, column=3, sticky="n", padx=5)

                label_subject = tk.Label(parent_frame, text=f"{subject_info[2][0]}:\n{subject_info[2][1]}", height=4,
                                         width=20, font=("Helvetica", 14), relief="solid")
                label_subject.grid(row=5, column=4, padx=5, pady=5)
                label_instructor = tk.Label(parent_frame, text=f"{subject_info[2][2]}",
                                            font=("Helvetica", 8))
                label_instructor.grid(row=5, column=4, sticky="s", padx=5)
                label_room = tk.Label(parent_frame, text=f"{subject_info[2][3]}", font=("Helvetica", 8))
                label_room.grid(row=5, column=4, sticky="n", padx=5)
            elif subject_code == 'MPU3122':
                label_subject = tk.Label(parent_frame, text=f"{subject_info[3][0]}:\n{subject_info[3][1]}", height=4,
                                         width=20, font=("Helvetica", 14), relief="solid")
                label_subject.grid(row=1, column=4, padx=5, pady=5)
                label_instructor = tk.Label(parent_frame, text=f"{subject_info[3][2]}",
                                            font=("Helvetica", 8))
                label_instructor.grid(row=1, column=4, sticky="s", padx=5)
                label_room = tk.Label(parent_frame, text=f"{subject_info[3][3]}", font=("Helvetica", 8))
                label_room.grid(row=1, column=4, sticky="n", padx=5)

                label_subject = tk.Label(parent_frame, text=f"{subject_info[3][0]}:\n{subject_info[3][1]}", height=4,
                                         width=20, font=("Helvetica", 14), relief="solid")
                label_subject.grid(row=4, column=3, padx=5, pady=5)
                label_instructor = tk.Label(parent_frame, text=f"{subject_info[3][2]}",
                                            font=("Helvetica", 8))
                label_instructor.grid(row=4, column=3, sticky="s", padx=5)
                label_room = tk.Label(parent_frame, text=f"{subject_info[3][3]}", font=("Helvetica", 8))
                label_room.grid(row=4, column=3, sticky="n", padx=5)
            elif subject_code == 'MPU3142':
                label_subject = tk.Label(parent_frame, text=f"{subject_info[4][0]}:\n{subject_info[4][1]}", height=4,
                                         width=20, font=("Helvetica", 14), relief="solid")
                label_subject.grid(row=3, column=4, padx=5, pady=5)
                label_instructor = tk.Label(parent_frame, text=f"{subject_info[4][2]}",
                                            font=("Helvetica", 8))
                label_instructor.grid(row=3, column=4, sticky="s", padx=5)
                label_room = tk.Label(parent_frame, text=f"{subject_info[4][3]}", font=("Helvetica", 8))
                label_room.grid(row=3, column=4, sticky="n", padx=5)

                label_subject = tk.Label(parent_frame, text=f"{subject_info[4][0]}:\n{subject_info[4][1]}", height=4,
                                         width=20, font=("Helvetica", 14), relief="solid")
                label_subject.grid(row=5, column=1, padx=5, pady=5)
                label_instructor = tk.Label(parent_frame, text=f"{subject_info[4][2]}",
                                            font=("Helvetica", 8))
                label_instructor.grid(row=5, column=1, sticky="s", padx=5)
                label_room = tk.Label(parent_frame, text=f"{subject_info[4][3]}", font=("Helvetica", 8))
                label_room.grid(row=5, column=1, sticky="n", padx=5)
    else:
        messagebox.showerror("Timetable Not Found", "Timetable data not found for the given username.")
    return timetable_entry_index, [subject_code for subject_code in student_timetable_entry[1:]]


def submit_assignment(username, subject_code, parent_frame, assignment_tab):
    # Find the index of the subject in subject_info
    subject_info_entry = next((info for info in subject_info if info[0] == subject_code), None)
    if subject_info_entry is None:
        # Display an error message if subject info is not found
        messagebox.showerror("Error", f"Subject info not found for subject code: {subject_code}")
        return

    subject_name = subject_info_entry[1]

    # Ask the user to select the file to submit
    file_path = filedialog.askopenfilename(title=f"Select Assignment for {subject_name}")

    # Check if the file exists
    if os.path.exists(file_path):
        # Update the status of the assignment to completed
        for i, entry in enumerate(assignment_data):
            if entry[0] == username:
                assignment_data[i][1 + subject_info.index(subject_info_entry)] = "completed"
                for data in assignment_data:
                    print(data)
                break
        else:
            # Display an error message if the username is not found in the assignments
            messagebox.showerror("Error", "StudentID not found in assignment_student.txt")
            return

        # Display a success message
        messagebox.showinfo("Success", f"Assignment for {subject_name} submitted successfully!")

        # Refresh the assignment tab
        display_assignment_frame(username, parent_frame, assignment_tab)
    else:
        # Display an error message if the file does not exist
        messagebox.showerror("Error", "File not found. Please select a valid file.")


def display_assignment_frame(username, parent_frame, assignment_tab):
    # Clear the previous contents of the assignment tab
    for widget in assignment_tab.winfo_children():
        widget.destroy()

    # Find the assignment entry for the given username
    for entry in assignment_data:
        if entry[0] == username:
            subject_status = entry[1:]
            break
    else:
        # Display an error message if the username is not found in the assignments
        messagebox.showerror("Error", "StudentID not found in assignment_student.txt")
        return

    # Create a frame for the assignment data
    assignment_frame = ttk.Frame(assignment_tab, borderwidth=2, relief="solid")
    assignment_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Iterate through the subject codes and their statuses
    for subject_code, status in zip(subject_info, subject_status):
        # Create a frame for each subject's assignment
        subject_frame = ttk.Frame(assignment_frame, borderwidth=1, relief="solid")
        subject_frame.pack(pady=10, padx=10, fill="x")

        # Add labels for subject code, name, status, and submit button
        subject_code_label = ttk.Label(subject_frame, text=f"{subject_code[0]}: {subject_code[1]}",
                                       font=("Montserrat", 16, "bold"))
        subject_code_label.pack(side='left')

        # Define the color based on status
        status_color = "green" if status == "completed" else "red"
        status_label = ttk.Label(subject_frame, text=f"{status}", font=("Montserrat", 18, "bold"),
                                 foreground=status_color)
        status_label.pack(side='right')

        # Add label for "Final Assignment"
        final_assignment_label = ttk.Label(subject_frame, text="Final Assignment", font=("Montserrat", 12))
        final_assignment_label.pack(side='right', padx=(0, 10))

        # Display submit button only if status is incomplete
        if status == "incomplete":
            submit_button = ttk.Button(subject_frame, text="Submit",
                                       command=lambda u=username, sc=subject_code[0], pf=parent_frame, at=assignment_tab:
                                       submit_assignment(u, sc, pf, at))
            submit_button.pack(side='right')


def attendance_list(subject, record):
    # Create a new window
    list_of_attendance = tk.Toplevel()
    list_of_attendance.title(f"Attendance for {subject}")

    # Create a frame for the attendance data
    frame = ttk.Frame(list_of_attendance)
    frame.pack(anchor='w')

    # Create a label for the subject name
    subject_label = ttk.Label(frame, text=subject, font=("Helvetica", 14, "bold"))
    subject_label.grid(row=1, column=0, sticky="w")

    num_classes = len(record)

    # Create labels for each class
    for i in range(num_classes):
        class_label = ttk.Label(frame, text=f"Class {i + 1}", font=("Helvetica", 12, "bold"))
        class_label.grid(row=0, column=i + 1, sticky="w")
        class_record = ttk.Label(frame, text=f"{record[i]}", font=("Times New Roman", 14))
        class_record.grid(row=1, column=i + 1, sticky="w")


def attendance_percentage(subject, record):
    # Create a new window
    percentage_of_attendance = tk.Toplevel()
    percentage_of_attendance.title(f"Attendance for {subject}")

    # Create a frame for the attendance data
    frame = ttk.Frame(percentage_of_attendance)
    frame.pack()

    present = absent = total = 0
    for i in range(len(record)):
        if record[i] == 'present':
            present += 1
        elif record[i] == 'absent':
            absent += 1
        else:
            messagebox.showerror('data in attendance_studentID.txt is no understood')
        total += 1

    # Create a label for the subject name
    subject_label = ttk.Label(frame, text='Attendance Percentage:\n'
                                          f'Total Class so far: {total}\n'
                                          f'Number of times present: {present}\n'
                                          f'Number of times absent: {absent}\n'
                                          f'Percentage: {(present/total*100)}%', font=("Helvetica", 14, "bold"))
    subject_label.grid(row=1, column=0, sticky="w")


def mark_attendance(i, j, display):
    global attendance_data
    if i < len(attendance_data) and j < len(attendance_data[i]):
        if attendance_data[i][j] is None:
            attendance_data[i][j] = 'present'
            messagebox.showwarning(message="Attendance has been marked")
        else:
            messagebox.showinfo(message="You are already marked present")
    else:
        attendance_data[i].append('present')
        messagebox.showinfo(message=f"Attendance was already marked")
    for data in attendance_data:
        print(data)


def mark_current_subject_attendance(index, subject, display, record, parent_frame):
    global current_time, current_day

    # Assuming current_time is a string in the format 'HH:MM'
    if isinstance(current_time, str):
        current_time = datetime.strptime(current_time, '%H:%M')

    for data in subject_info:
        if data[0] == subject:
            if current_day == data[4]:
                data5_datetime = datetime.strptime(data[5], '%H:%M')
                data7_datetime = datetime.strptime(data[7], '%H:%M')
                if isinstance(data[5], str) and isinstance(data[7], str):
                    if data5_datetime <= current_time <= (data5_datetime + timedelta(minutes=15)):
                        # Create a frame in parent_frame
                        frame = ttk.Frame(parent_frame)
                        frame.pack()  # Adjust as needed

                        # Create a label with the subject name
                        subject_label = ttk.Label(frame, text=f"Mark attendance for {display}",
                                                  font=("Helvetica", 14))
                        subject_label.pack(side='left')

                        # Create a button to mark attendance
                        mark_button = ttk.Button(frame, text="Mark Attendance",
                                                 command=lambda: mark_attendance(index, len(record) + 2, subject))
                        mark_button.pack(side='right')
                    elif data7_datetime <= current_time <= (data7_datetime + timedelta(minutes=15)):
                        # Create a frame in parent_frame
                        frame = ttk.Frame(parent_frame)
                        frame.pack()  # Adjust as needed

                        # Create a label with the subject name
                        subject_label = ttk.Label(frame, text=f"Mark attendance for {display}",
                                                  font=("Helvetica", 14))
                        subject_label.pack()

                        # Create a button to mark attendance
                        mark_button = ttk.Button(frame, text="Mark Attendance",
                                                 command=lambda: mark_attendance(index, len(record) + 3, display))
                        mark_button.pack()


# Student home page
def student_homepage(username):
    root = tk.Tk()  # Create a new instance of Tk
    root.title("EduHub University")
    root.geometry("1300x900")  # Set window size

    # Function to handle tab selection
    def on_tab_selected(event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == "Exit":
            exit_application(root)

    # Create a frame for the main content
    content_frame = ttk.Frame(root)
    content_frame.pack(fill='both', expand=True)

    # Create a label with the university name and additional information
    university_label = ttk.Label(content_frame, text="Welcome to EduHub University", font=("Helvetica", 20))
    university_label.pack(pady=20)

    time_label = ttk.Label(root, text="Time:", font=("Helvetica", 24))
    time_label.place(x=1000, y=90)

    # To manually set the day and time
    set_day_and_time(current_day, current_time, time_label)

    # Create a custom style for the tabs
    style = ttk.Style()
    style.configure("Custom.TNotebook.Tab", padding=[40, 10], font=('Helvetica', 12))

    # Create notebook for main tabs
    notebook = ttk.Notebook(content_frame, style="Custom.TNotebook")
    notebook.pack(fill='both', expand=True, padx=20, pady=10)

    # My Profile tab
    my_profile_tab = ttk.Frame(notebook)
    notebook.add(my_profile_tab, text="My Profile")

    # Create a frame for the student profile table
    profile_frame = ttk.Frame(my_profile_tab)
    profile_frame.pack(pady=20, padx=20, anchor="w")  # Align to the left

    # Display student profile
    display_student_profile(username, student_info, profile_frame)

    # Timetable tab
    timetable_tab = ttk.Frame(notebook)
    notebook.add(timetable_tab, text="Timetable")

    # Create a frame for the timetable tab
    timetable_frame = ttk.Frame(timetable_tab)
    timetable_frame.pack(pady=20, padx=20, anchor="w")  # Align to the left

    populate_timetable(username, timetable_frame)

    # Attendance tab
    attendance_tab = ttk.Frame(notebook)
    notebook.add(attendance_tab, text="Attendance")

    # Create a frame for the attendance tab
    attendance_frame = ttk.Frame(attendance_tab)
    attendance_frame.pack(pady=20, padx=20, anchor="w")  # Align to the left

    for i, data in enumerate(attendance_data):
        if data[0] == username:
            row = i
            subject = data[1]
            attendance_record = data[2:]

            # Create a frame for the attendance data
            attendance_frame = ttk.Frame(attendance_tab, borderwidth=2, relief="solid")
            attendance_frame.pack(anchor='w')

            # Display subject name label
            subject_label = ttk.Label(attendance_frame, text=subject, font=("Helvetica", 14, "bold"))
            subject_label.grid(row=0, column=0, sticky="w")

            # Create buttons to call attendance_list and attendance_percentage
            list_button = ttk.Button(attendance_frame, text="Attendance List",
                                     command=lambda subj=subject, rec=attendance_record: attendance_list(subj, rec))
            list_button.grid(row=0, column=1)

            percentage_button = ttk.Button(attendance_frame, text="Attendance Percentage",
                                           command=lambda subj=subject, rec=attendance_record:
                                           attendance_percentage(subj, rec))
            percentage_button.grid(row=0, column=2)

    for i, data in enumerate(attendance_data):
        if data[0] == username:
            row = i
            subject = data[1]
            attendance_record = data[2:]
            mark_current_subject_attendance(row, subject, subject, attendance_record, attendance_tab)

    # Assignments tab
    assignments_tab = ttk.Frame(notebook)
    notebook.add(assignments_tab, text="Assignments")

    # Create a frame for the attendance tab
    assignment_frame = ttk.Frame(assignments_tab)
    assignment_frame.pack(pady=20, padx=20, anchor="w")  # Align to the left

    # Display assignment frames for each subject
    display_assignment_frame(username, assignment_frame, assignments_tab)

    exit_tab = ttk.Frame(notebook)
    notebook.add(exit_tab, text="Exit")

    exit_frame = ttk.Frame(exit_tab)
    exit_frame.pack(pady=20, padx=20, anchor="w")

    # Bind the tab selection event to the notebook widget
    notebook.bind("<<NotebookTabChanged>>", on_tab_selected)

    root.mainloop()


def display_faculty_profile(username, faculty_info, profile_frame):
    for faculty in faculty_info:
        if username == faculty[0]:
            # Display Faculty ID
            faculty_id_label = tk.Label(profile_frame, text=f"Faculty ID:", font=("Montserrat", 20), anchor="w")
            faculty_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            faculty_id_data_label = tk.Label(profile_frame, text=faculty[0], font=("Montserrat", 20, "bold"),
                                             anchor="e", borderwidth=1, relief="solid", fg="green")
            faculty_id_data_label.grid(row=0, column=1, padx=10, pady=5, sticky="e")

            # Display Faculty Name
            faculty_name_label = tk.Label(profile_frame, text=f"Faculty Name:", font=("Montserrat", 20), anchor="w")
            faculty_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            faculty_name_data_label = tk.Label(profile_frame, text=faculty[2], font=("Montserrat", 20, "bold"),
                                               anchor="e", borderwidth=1, relief="solid", fg="green")
            faculty_name_data_label.grid(row=1, column=1, padx=10, pady=5, sticky="e")

            # Display Faculty Courses
            faculty_courses_label = tk.Label(profile_frame, text=f"Faculty Courses:", font=("Montserrat", 20),
                                             anchor="w")
            faculty_courses_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
            faculty_courses_data_label = tk.Label(profile_frame, text=faculty[3], font=("Montserrat", 20, "bold"),
                                                  anchor="e", borderwidth=1, relief="solid", fg="green")
            faculty_courses_data_label.grid(row=2, column=1, padx=10, pady=5, sticky="e")
            break  # Exit loop once faculty member is found


def add_subject_to_timetable(student_id, subject_code, timetable_entry_index, timetable_window):
    # Ensure timetable_entry_index is valid
    if 0 <= timetable_entry_index < len(timetable_data):
        # Check if subject_code is not empty
        if subject_code[0] != "No subjects available to add":
            # Add the subject_code to the timetable entry at the specified index
            timetable_data[timetable_entry_index].append(subject_code)
            # Add assignment for the new subject
            assignment_data[timetable_entry_index].append('incomplete')
            # Add Timetable record for the new subject
            attendance_data.append([f'{student_id}',f'{subject_code}'])
            absent_to_add = week * 2
            for i in range(absent_to_add):
                attendance_data[len(attendance_data)].append('absent')
            # Refresh the timetable window
            timetable_window.destroy()
            display_student_timetable(student_id, timetable_window.master)
    else:
        # Display an error message if the timetable_entry_index is out of range
        messagebox.showerror("Error", "Invalid timetable entry index")


def delete_subject_from_timetable(student_id, subject_code, timetable_entry_index, timetable_window):
    # Ensure timetable_entry_index is valid
    if 0 <= timetable_entry_index < len(timetable_data):
        # Check if the subject code exists in the timetable entry
        if 0 <= timetable_entry_index < len(timetable_data):
            # Check if the subject code exists in the timetable entry
            if subject_code in timetable_data[timetable_entry_index]:
                # Get the subject index in the timetable entry
                subject_index = timetable_data[timetable_entry_index].index(subject_code)
                # Remove the subject code from the timetable entry
                removed_subject = timetable_data[timetable_entry_index].pop(subject_index)
                # Remove the corresponding assignment data from assignment_data
                removed_assignment = assignment_data[timetable_entry_index].pop(subject_index)
                # Remove attendance data for the student that got his subject removed
    for i in range(attendance_data):
        if attendance_data[i][0] == student_id and attendance_data[i][1] == subject_code:
            del attendance_data[i]
            # Refresh the timetable window
            timetable_window.destroy()
            display_student_timetable(student_id, timetable_window)
    else:
        # Display an error message if the timetable_entry_index is out of range
        messagebox.showerror("Error", "Invalid timetable entry index")


def display_student_timetable(student_id_entry, root):
    student_id = student_id_entry.get()

    programme = False
    for data in timetable_data:
        if data[0] == student_id:
            programme = True
            break

    if programme:
        # Create a new window for displaying student timetable
        timetable_window = tk.Toplevel(root)
        timetable_window.title(f"Timetable - Student {student_id}")
        timetable_window.geometry("1300x900+{}+{}".format(50, 10))

        # Create a frame for displaying student timetable
        timetable_frame = ttk.Frame(timetable_window)
        timetable_frame.pack(pady=20, padx=20)

        # Populate the timetable for the new student ID
        timetable_entry_index, subject_codes = populate_timetable(student_id, timetable_frame)

        # Add a back button to close the window
        back_button = ttk.Button(timetable_frame, text="Close Window", command=timetable_window.destroy)
        back_button.grid(row=6, column=0)

        add_subject = [subject_info[j][0] for j in range(5) if subject_info[j][0] not in subject_codes]
        if not add_subject:
            add_subject.append("No subjects available to add")

        # Create a dropdown menu and button for adding subjects
        add_subject_var = tk.StringVar()
        add_subject_var.set(f"{add_subject[0]}")

        add_subject_menu = tk.OptionMenu(timetable_frame, add_subject_var, *add_subject)
        add_subject_menu.grid(row=7, column=0, padx=10, pady=10)

        # Create a button for adding subjects only if subjects are available to add
        if add_subject[0] != "No subjects available to add":
            add_subject_button = ttk.Button(timetable_frame, text="Add Subject",
                                            command=lambda: add_subject_to_timetable(student_id_entry,
                                                                                     add_subject_var.get(),
                                                                                     timetable_entry_index,
                                                                                     timetable_window))
            add_subject_button.grid(row=7, column=1, padx=10, pady=10)

        delete_subject = [subject_info[j][0] for j in range(5) if subject_info[j][0] in subject_codes]
        if not delete_subject:
            delete_subject.append("No subjects available to delete")

        # Create a dropdown menu and button for deleting subjects
        delete_subject_var = tk.StringVar()
        delete_subject_var.set(f"{delete_subject[0]}")

        delete_subject_menu = tk.OptionMenu(timetable_frame, delete_subject_var, *delete_subject)
        delete_subject_menu.grid(row=8, column=0, padx=10, pady=10)

        # Create a button for deleting subjects only if subjects are available to delete
        if delete_subject[0] != "No subjects available to delete":
            delete_subject_button = ttk.Button(timetable_frame, text="Delete Subject",
                                               command=lambda: delete_subject_from_timetable(student_id_entry,
                                                                                             delete_subject_var.get(),
                                                                                             timetable_entry_index,
                                                                                             timetable_window))
            delete_subject_button.grid(row=8, column=1, padx=10, pady=10)
    else:
        messagebox.showerror(message=f"{student_id} does not exist")


def change_status(index, j, faculty_code, parent_frame):
    current_status = assignment_data[j][index]

    if current_status == 'completed':
        assignment_data[j][index] = 'incomplete'
    else:
        assignment_data[j][index] = 'completed'

    # Refresh the display of assignments
    display_students_assignments(faculty_code, parent_frame)


# Define function to display students' assignments
def display_students_assignments(faculty_code, parent_frame):
    # Destroy any existing widgets to clear the display
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Find the subject code for the given faculty code
    for faculty_entry in faculty_info:
        if faculty_entry[0] == faculty_code:
            subject_code = faculty_entry[3]
            break
    else:
        # Display an error message if the faculty code is not found
        messagebox.showerror("Error", f"Faculty code not found: {faculty_code}")
        return

    # Initialize an empty list to store student information
    students_with_assignments = []

    # Flag to check if any students have been found
    students_found = False

    # Find all students enrolled in the subject code
    for j in range(len(student_info)):
        current_student = timetable_data[j][0]
        current_student_codes = timetable_data[j][1:]
        if subject_code in current_student_codes:
            # Get the index of the subject code
            index = current_student_codes.index(subject_code) + 1

            student_id = current_student
            student_name = student_info[j][2]
            assignment_status = assignment_data[j][index]

            # Set flag to indicate at least one student has been found
            students_found = True

            # Create a frame for each student
            student_frame = ttk.Frame(parent_frame, borderwidth=1, relief="solid", width=600)
            student_frame.pack(pady=6, padx=6 , fill='x')

            # Add labels for student ID and name
            student_id_label = ttk.Label(student_frame, text=f"{student_id}", font=("Montserrat", 16, "bold"))
            student_id_label.pack(side='left')

            student_name_label = ttk.Label(student_frame, text=f"{student_name}",
                                           font=("Montserrat", 16, "bold"))
            student_name_label.pack(side='left', padx=10)

            # Define the color based on status
            status_color = "green" if assignment_status == "completed" else "red"

            # Create a label to display assignment status
            status_label = ttk.Label(student_frame, text=f"{assignment_status}",
                                     font=("Montserrat", 14, "bold"), foreground=status_color)
            status_label.pack(side='right', padx=10)

            # Create a button to change assignment status
            change_status_button = ttk.Button(student_frame, text="Change Status",
                                              command=functools.partial(change_status, index, j, faculty_code,
                                                                        parent_frame))
            change_status_button.pack(side='right', padx=5)

    # Check if no students have been found
    if not students_found:
        messagebox.showinfo("Information", "No students found for the given subject code.")


# Lecturer home page
def faculty_homepage(username):
    root = tk.Tk()  # Create a new instance of Tk
    root.title("EduHub University - Lecturer Dashboard")
    root.geometry("1300x900")  # Set window size

    # Function to handle tab selection
    def on_tab_selected(event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == "Exit":
            exit_application(root)

    # Create a frame for the main content
    content_frame = ttk.Frame(root)
    content_frame.pack(fill='both', expand=True)

    # Create a label with the university name and additional information
    university_label = ttk.Label(content_frame, text="Welcome to EduHub University", font=("Helvetica", 20))
    university_label.pack(pady=20)

    # Create labels for day and time
    time_label = ttk.Label(root, text="Time:", font=("Helvetica", 24))
    time_label.place(x=1000, y=50)

    # To manually set the day and time
    set_day_and_time(current_day, current_time, time_label)

    # Create a custom style for the tabs
    style = ttk.Style()
    style.configure("Custom.TNotebook.Tab", padding=[40, 10], font=('Helvetica', 12))

    # Create notebook for main tabs
    notebook = ttk.Notebook(content_frame, style="Custom.TNotebook")
    notebook.pack(fill='both', expand=True, padx=20, pady=10)

    # My Profile tab
    my_profile_tab = ttk.Frame(notebook)
    notebook.add(my_profile_tab, text="My Profile")

    # Create a frame for the lecturer profile table
    profile_frame = ttk.Frame(my_profile_tab)
    profile_frame.pack(pady=20, padx=20, anchor="w")  # Align to the left

    # Display faculty profile
    display_faculty_profile(username, faculty_info, profile_frame)

    # Attendance tab
    attendance_tab = ttk.Frame(notebook)
    notebook.add(attendance_tab, text="View Attendance")

    # Create a frame for the attendance tab
    attendance_frame = ttk.Frame(attendance_tab)
    attendance_frame.pack(pady=20, padx=20, anchor="w")  # Align to the left

    # Loop to populate the "View Attendance" tab
    for faculty in faculty_info:
        if faculty[0] == username:
            subject = faculty[3]
            for i, data in enumerate(attendance_data):
                if data[1] == subject:
                    student_id = data[0]
                    attendance_record = data[2:]

                    # Create a frame for each student's attendance data
                    student_attendance_frame = ttk.Frame(attendance_frame, borderwidth=2, relief="solid")
                    student_attendance_frame.pack(anchor='w')

                    # Display student ID label
                    student_id_label = ttk.Label(student_attendance_frame, text=student_id,
                                                 font=("Helvetica", 14, "bold"))
                    student_id_label.grid(row=0, column=0, sticky="w")

                    # Create buttons to call attendance_list and attendance_percentage
                    list_button = ttk.Button(student_attendance_frame, text="Attendance List",
                                             command=lambda subj=subject, rec=attendance_record: attendance_list(subj,
                                                                                                                 rec))
                    list_button.grid(row=0, column=1)

                    percentage_button = ttk.Button(student_attendance_frame, text="Attendance Percentage",
                                                   command=lambda subj=subject, rec=attendance_record:
                                                   attendance_percentage(subj, rec))
                    percentage_button.grid(row=0, column=2)

    # Mark Attendance tab
    mark_attendance_tab = ttk.Frame(notebook)
    notebook.add(mark_attendance_tab, text="Mark Attendance")

    # Create a frame for the mark attendance tab
    mark_attendance_frame = ttk.Frame(mark_attendance_tab)
    mark_attendance_frame.pack(pady=20, padx=20, anchor="w")  # Align to the left

    # Loop to populate the "Mark Attendance" tab
    for faculty in faculty_info:
        if faculty[0] == username:
            subject = faculty[3]
            for i, data in enumerate(attendance_data):
                if data[1] == subject:
                    display = data[0]
                    row = i
                    attendance_record = data[2:]
                    mark_current_subject_attendance(row, subject, display, attendance_record, mark_attendance_tab)

    # Timetable tab
    timetable_tab = ttk.Frame(notebook)
    notebook.add(timetable_tab, text="Timetable")

    # Create a frame for entering student ID and displaying timetable
    timetable_frame = ttk.Frame(timetable_tab)
    timetable_frame.pack(pady=20, padx=20, anchor="w")  # Align to the left

    # Label and Entry for entering student ID
    student_id_label = ttk.Label(timetable_frame, text="Enter Student ID:", font=("Helvetica", 14))
    student_id_label.grid(row=0, column=0, padx=5, pady=5)

    student_id_entry = ttk.Entry(timetable_frame, font=("Helvetica", 14))
    student_id_entry.grid(row=0, column=1, padx=5, pady=5)

    # Button to display student timetable
    display_button = ttk.Button(timetable_frame, text="Display Timetable",
                                command=lambda: display_student_timetable(student_id_entry, root))
    display_button.grid(row=0, column=2, padx=5, pady=5)

    # Assignments tab
    assignments_tab = ttk.Frame(notebook)
    notebook.add(assignments_tab, text="Assignments")

    # Create a frame for displaying students and assignments
    display_students_assignments(username, assignments_tab)

    # Exit tab
    exit_tab = ttk.Frame(notebook)
    notebook.add(exit_tab, text="Exit")

    # Create a frame for the attendance tab
    exit_frame = ttk.Frame(exit_tab)
    exit_frame.pack(pady=20, padx=20, anchor="w")  # Align to the left

    # Bind the tab selection event to the notebook widget
    notebook.bind("<<NotebookTabChanged>>", on_tab_selected)

    root.mainloop()


# Main login window
window = tk.Tk()
window.title("Login Page")

# Set window size and position
window_width = 1000
window_height = 550
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Resized login page image
login_image = resize_image("login.png", 676, 548)
login_label = tk.Label(window, image=login_image)
login_label.pack(side='left')

# Create a frame for login components
login_frame = tk.Frame(window, bg="light gray", width=1028, height=1094, relief="ridge")
login_frame.place(x=750, y=200)

label_login = tk.Label(login_frame, text="Login", fg="blue", bg='light gray')
label_login.grid(row=0, column=0)

label_username = tk.Label(login_frame, text="Username:")
label_username.grid(row=1, column=0)
entry_username = tk.Entry(login_frame)
entry_username.grid(row=1, column=1)

label_password = tk.Label(login_frame, text="Password:")
label_password.grid(row=2, column=0)
entry_password = tk.Entry(login_frame, show="*")
entry_password.grid(row=2, column=1)

login_button = tk.Button(login_frame, text="Login", command=lambda: login(student_info, faculty_info))
login_button.grid(row=3, column=0)

window.mainloop()

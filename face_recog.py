import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring
from tkinter import messagebox

# Function to capture a limited number of photos of the new person and save them
def capture_limited_photos(new_person_folder_path, num_photos_to_capture=15):
    # Initialize video capture
    video_capture = cv2.VideoCapture(0)
    photos_captured = 0

    if not os.path.exists(new_person_folder_path):
        os.makedirs(new_person_folder_path)

    while photos_captured < num_photos_to_capture:
        _, frame = video_capture.read()
        photo_path = os.path.join(new_person_folder_path, f"{photos_captured}.jpg")
        cv2.imwrite(photo_path, frame)
        photos_captured += 1

    video_capture.release()

# Function to load and encode faces from multiple folders
def load_faces_from_folders(data_folder):
    face_encodings = []
    face_names = []

    for person_folder in os.listdir(data_folder):
        person_name = person_folder  # Use folder name as the person's name
        person_folder_path = os.path.join(data_folder, person_folder)

        if os.path.isdir(person_folder_path):
            for image_file in os.listdir(person_folder_path):
                image_path = os.path.join(person_folder_path, image_file)

                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)

                if encoding:
                    for enc in encoding:
                        face_encodings.append(enc)
                        face_names.append(person_name)

    return face_encodings, face_names

# Function to add a new person
def add_new_person():
    # Ask for the new person's name
    new_person_name = askstring("Add New Person", "Enter the name of the new person:")

    if new_person_name:
        new_person_folder_path = os.path.join(data_folder, new_person_name)

        # Create a new folder for the person
        os.makedirs(new_person_folder_path)

        # Capture and save a limited number of photos of the new person (15 in this case)
        capture_limited_photos(new_person_folder_path, num_photos_to_capture=15)

        # Reload known face encodings and names
        known_face_encodings, known_face_names = load_faces_from_folders(data_folder)

        # Add the new person to the GUI
        if new_person_name not in known_face_names:
            known_face_names.extend([new_person_name])
            present_students_listbox.insert("end", new_person_name)
            messagebox.showinfo("Success", f"{new_person_name} has been added to the system.")
        else:
            messagebox.showerror("Error", f"{new_person_name} is already in the system.")

# Function to remove a person
def remove_person():
    global known_face_names

    selected_student = selected_student_combobox.get().strip()
    selected_student = selected_student.title()  # Capitalize the name

    if selected_student:
        response = messagebox.askquestion("Remove Student", f"Are you sure you want to remove {selected_student} from the system?")

        if response == "yes":
            folder_to_remove = os.path.join(data_folder, selected_student)

            if os.path.exists(folder_to_remove):
                for file in os.listdir(folder_to_remove):
                    file_path = os.path.join(folder_to_remove, file)
                    os.remove(file_path)

                os.rmdir(folder_to_remove)

            if selected_student in known_face_names:
                known_face_names.remove(selected_student)

            selected_student_combobox.set("")  # Clear the selected student

            # Reload known face encodings and names
            known_face_encodings, known_face_names = load_faces_from_folders(data_folder)

            # Update the listbox to remove the person
            present_students_listbox.delete(0, "end")
            for name in known_face_names:
                present_students_listbox.insert("end", name)

            # Show a removal message
            removal_message_label.config(text=f"{selected_student} is removed", fg="white", bg="black")
            removal_message_label.after(3000, clear_removal_message)

     # Start updating attendance status
    update_attendance_status()

# Function to clear the removal message
def clear_removal_message():
    removal_message_label.config(text="", bg="black")

# Function to start tracking attendance
def record_attendance():
    global tracking, video_capture  # Add 'video_capture' to the global scope if it's outside
    tracking = True
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    attendance_label.config(text="Recording attendance...")
    
    # Initialize video capture here
    video_capture = cv2.VideoCapture(0)


# Function to stop tracking attendance
def stop_attendance():
    global tracking, video_capture  # Add 'video_capture' to the global scope if it's outside
    tracking = False
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    attendance_label.config(text="Press 'Start Tracking' to begin attendance recording")

    # Release video capture
    video_capture.release()


# Initialize video capture
video_capture = cv2.VideoCapture(0)

# Load face encodings and names from folders
data_folder = "DataBase"  # Change this to the path of your data folder
known_face_encodings, known_face_names = load_faces_from_folders(data_folder)

# Function to load folder names from the data folder as known names
def load_folder_names(data_folder):
    known_names = []

    for person_folder in os.listdir(data_folder):
        person_folder_path = os.path.join(data_folder, person_folder)

        if os.path.isdir(person_folder_path):
            known_names.append(person_folder)

    return known_names

# Initialize known face names by loading folder names
known_face_names = load_folder_names(data_folder)

# Initialize other variables
attendance_recorded = set()
tracking = False
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

# Open CSV file for writing
csv_file_path = current_date + '.csv'
f = open(csv_file_path, 'w+', newline='')
lnwriter = csv.writer(f)

# Create a Tkinter GUI window
root = tk.Tk()
root.title("Attendance Ease")
root.attributes('-fullscreen', True)  # Make the GUI full-screen

# Create a black background
root.configure(bg="black")

# Create a label for the project name
project_name_label = tk.Label(root, text="Attendance Ease", font=("Helvetica", 32, "bold"), foreground="white", background="black")
project_name_label.pack(pady=20)

# Create a frame for student attendance list
attendance_frame = tk.LabelFrame(root, text="Present Students", foreground="white", bg="black")
attendance_frame.place(x=20, y=80, width=1600, height=100)

# Create a listbox to display present students
present_students_listbox = tk.Listbox(attendance_frame, bg="black", fg="white")
present_students_listbox.pack(fill="both", expand=True)

# Create a label for displaying attendance status
attendance_label = tk.Label(root, text="Press 'Start Tracking' to begin attendance recording", font=("Helvetica", 18), foreground="white", background="black")
attendance_label.pack(pady=20)

# Create buttons frame
buttons_frame = tk.Frame(root, bg="black")
buttons_frame.pack(pady=10)

# Create buttons for starting and stopping attendance tracking
start_button = tk.Button(buttons_frame, text="Start Tracking", command=record_attendance, state="normal", bg="green", fg="white", padx=20)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(buttons_frame, text="Stop Tracking", command=stop_attendance, state="disabled", bg="red", fg="white", padx=20)
stop_button.pack(side=tk.LEFT, padx=10)

# Create an exit button to close the GUI
exit_button = tk.Button(root, text="Exit", command=root.destroy, bg="gray", fg="white", padx=20)
exit_button.pack(pady=20)

# Create a button for adding a new person
add_person_button = tk.Button(root, text="Add New Person", command=add_new_person, bg="blue", fg="white", padx=20)
add_person_button.pack(pady=10)

# Create a combobox for removing a person
available_students = known_face_names.copy()
selected_student_combobox = ttk.Combobox(root, values=available_students)
selected_student_combobox.set("")  # Set initial value to nothing
selected_student_combobox.pack(pady=10)

# Create a button for removing a person
remove_person_button = tk.Button(root, text="Remove Person", command=remove_person, bg="red", fg="white", padx=20)
remove_person_button.pack(pady=10)

# Create a label for removal message
removal_message_label = tk.Label(root, text="", font=("Helvetica", 18), bg="black")
removal_message_label.pack(pady=10)

def update_attendance_status():
    if tracking:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Debug point 1: Check if faces are detected
        print(f"Number of faces detected: {len(face_locations)}")

        face_names = []

        for face_encoding in face_encodings:
            # Debug point 2: Check if face encodings are generated
            print(f"Face encoding: {face_encoding}")

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                if first_match_index < len(known_face_names):
                    name = known_face_names[first_match_index]

            face_names.append(name)

        for name in face_names:
            if name != "Unknown" and name not in attendance_recorded:
                attendance_recorded.add(name)
                present_students_listbox.insert("end", name)
                current_time = now.strftime("%H-%M-[%S]")
                lnwriter.writerow([name, current_time])

        attendance_label.config(text=', '.join(face_names) + ' Present')

    root.after(100, update_attendance_status)


root.mainloop()

# Release video capture and close CSV file
video_capture.release()
f.close()

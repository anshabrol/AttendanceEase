# AttendanceEase

Attendance Ease is a facial recognition-based attendance tracking system, which captures real-time attendance of individuals using a camera and stores the data in a CSV file. The system allows adding and removing individuals from the database and tracking their attendance with a user-friendly graphical interface built with Tkinter.

## Features
- **Real-time Face Recognition**: Uses facial recognition to detect and record attendance.
- **Database Management**: Easily add or remove people from the attendance system.
- **CSV Export**: Attendance records, including timestamps, are saved as CSV files for easy access.
- **Full-Screen GUI**: A full-screen Tkinter-based GUI for a seamless experience.
- **User-Friendly Controls**: Start, stop, add, and remove persons with ease.

## Prerequisites
To run this project, ensure you have the following packages installed:
- **OpenCV**: For camera access and image handling
- **face_recognition**: To handle face encoding and recognition
- **Tkinter**: For GUI components
- **Numpy**: For numerical operations

To install these packages, run:
```bash
pip install opencv-python face-recognition numpy
```

## Project Structure
- **`AttendanceEase.py`**: Main Python file that contains the attendance tracking code.
- **`DataBase/`**: Folder where images of each person are stored for facial recognition.
- **`[DATE].csv`**: CSV files generated daily, containing attendance records with timestamps.

## How It Works
1. **Face Encoding**: Loads and encodes faces from the `DataBase` folder, where each person has a dedicated folder with their photos.
2. **Attendance Recording**: Recognizes faces in real-time and logs attendance with a timestamp when someone is present.
3. **Adding New People**: Allows adding new individuals by capturing their photos and storing them for recognition.
4. **Removing People**: Easily remove a person from the database, if needed.
5. **User Interface**: Start/stop attendance tracking and manage individuals through an intuitive interface.

## Usage
1. **Run the Application**:
   ```bash
   python face_recog.py
   ```
2. **Start Attendance Tracking**: Click **Start Tracking** in the GUI to begin recording attendance.
3. **Add a New Person**: Click **Add New Person**, enter the name, and the system will capture photos for future recognition.
4. **Remove a Person**: Select a person from the dropdown list and click **Remove Person**.
5. **Stop Attendance Tracking**: Click **Stop Tracking** to end attendance recording for the day.

## GUI Overview
The GUI includes:
- **Start/Stop Buttons**: Control the attendance tracking.
- **Add/Remove Person**: Easily manage the individuals in the system.
- **Present Students List**: Displays currently recognized and recorded attendees.
- **Exit Button**: Closes the application.

## Example
1. To add a new person:
   - Click **Add New Person** and follow prompts.
2. To remove a person:
   - Select from the dropdown and click **Remove Person**.

## CSV Output
- Daily CSV files are generated in the format `[DATE].csv`, where each row records the name and timestamp of each recognized person.

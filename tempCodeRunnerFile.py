import cv2
import face_recognition
import os
import serial
import requests

url = 'https://tzzywstbjsjmuylgmtdh.supabase.co/rest/v1/project'
headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR6enl3c3RianNqbXV5bGdtdGRoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDgwOTY0MTQsImV4cCI6MjAyMzY3MjQxNH0.V_8dZhCMW8gAGKUi7XZ62W4Wv8xlVvZnCUcr3koEbFA',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR6enl3c3RianNqbXV5bGdtdGRoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDgwOTY0MTQsImV4cCI6MjAyMzY3MjQxNH0.V_8dZhCMW8gAGKUi7XZ62W4Wv8xlVvZnCUcr3koEbFA',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'
}

# Define the serial port where your Arduino is connected
serial_port = 'COM5'  # Change this to your specific port
baud_rate = 9600

# Open serial connection
ser = serial.Serial(serial_port, baud_rate)



# Load images from the 'photos' directory
photo_dir = 'photos'
known_face_encodings = []
known_face_names = []

for file_name in os.listdir(photo_dir):
    if file_name.endswith('.jpg') or file_name.endswith('.png'):
        image_path = os.path.join(photo_dir, file_name)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(file_name)[0])

# Open the webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture each frame from the webcam
    ret, frame = video_capture.read()

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # If a match is found, use the name from the known faces
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Display the name on the console
        print(f"Detected face: {name}")
        if name != "Unknown":
            dt = "b"
            ser.write(dt.encode())
            data = {
                'name': name
            }

            response = requests.post(url, headers=headers, json=data)

            print(response.status_code)
            print(response.text)
        else:
            dt = "a"
            ser.write(dt.encode())

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
video_capture.release()
cv2.destroyAllWindows()
ser.close()
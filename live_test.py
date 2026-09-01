import cv2
import os
import csv
import numpy as np
from datetime import datetime


print("===================================")
print(" FACE RECOGNITION ATTENDANCE SYSTEM")
print("===================================")


# -----------------------------------
# 1. PATHS
# -----------------------------------

detector_model = "models/face_detection_yunet_2026may.onnx"
recognizer_model = "models/face_recognition_sface_2021dec.onnx"
known_faces_folder = "known_faces"

attendance_file = "attendance.csv"


# -----------------------------------
# 2. CHECK FILES
# -----------------------------------

if not os.path.exists(detector_model):
    print("YuNet model not found!")
    exit()

if not os.path.exists(recognizer_model):
    print("SFace model not found!")
    exit()

if not os.path.exists(known_faces_folder):
    print("known_faces folder not found!")
    exit()


# -----------------------------------
# 3. CREATE DETECTOR
# -----------------------------------

detector = cv2.FaceDetectorYN.create(
    detector_model,
    "",
    (320, 320),
    0.9,
    0.3,
    5000
)

print("Face detector ready!")


# -----------------------------------
# 4. CREATE RECOGNIZER
# -----------------------------------

recognizer = cv2.FaceRecognizerSF.create(
    recognizer_model,
    ""
)

print("Face recognizer ready!")


# -----------------------------------
# 5. LOAD KNOWN FACES
# -----------------------------------

known_features = {}

for file_name in os.listdir(known_faces_folder):

    if not file_name.lower().endswith(
        (".jpg", ".jpeg", ".png")
    ):
        continue

    image_path = os.path.join(
        known_faces_folder,
        file_name
    )

    image = cv2.imread(image_path)

    if image is None:
        print("Image load failed:", file_name)
        continue

    h, w = image.shape[:2]

    detector.setInputSize((w, h))

    _, faces = detector.detect(image)

    if faces is None:
        print("No face found:", file_name)
        continue

    face = faces[0]

    aligned_face = recognizer.alignCrop(
        image,
        face
    )

    feature = recognizer.feature(
        aligned_face
    )

    name = os.path.splitext(file_name)[0]

    known_features[name] = feature

    print("Loaded:", name)


# -----------------------------------
# 6. CHECK KNOWN FACES
# -----------------------------------

if len(known_features) == 0:
    print("No known faces found!")
    exit()

print()
print("Known people:")

for name in known_features:
    print("-", name)

print()
print("Total known people:", len(known_features))


# -----------------------------------
# 7. CREATE ATTENDANCE FILE
# -----------------------------------

if not os.path.exists(attendance_file):

    with open(
        attendance_file,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Name",
            "Date",
            "Time",
            "Status"
        ])

    print("attendance.csv created!")


# -----------------------------------
# 8. READ TODAY'S ATTENDANCE
# -----------------------------------

today = datetime.now().strftime("%Y-%m-%d")

marked_today = set()


with open(
    attendance_file,
    "r",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        if row["Date"] == today:

            marked_today.add(
                row["Name"]
            )


print()
print("Already marked today:")

for name in marked_today:
    print("-", name)


# -----------------------------------
# 9. FUNCTION TO MARK ATTENDANCE
# -----------------------------------

def mark_attendance(name):

    # Already marked
    if name in marked_today:
        return False

    now = datetime.now()

    date = now.strftime(
        "%Y-%m-%d"
    )

    time = now.strftime(
        "%H:%M:%S"
    )

    # Save attendance
    with open(
        attendance_file,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            name,
            date,
            time,
            "Present"
        ])

    # Remember today's attendance
    marked_today.add(name)

    print()
    print("Attendance marked!")
    print("Name:", name)
    print("Date:", date)
    print("Time:", time)

    return True


# -----------------------------------
# 10. OPEN CAMERA
# -----------------------------------

cap = cv2.VideoCapture(
    0,
    cv2.CAP_DSHOW
)

if not cap.isOpened():
    print("Could not open camera!")
    exit()

print()
print("Camera successfully opened!")
print("Face recognition started!")
print("Press Q to exit.")


# -----------------------------------
# 11. THRESHOLD
# -----------------------------------

threshold = 0.30


# -----------------------------------
# 12. UI HELPER FUNCTIONS
# -----------------------------------

# Colors (BGR format)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_YELLOW = (0, 255, 255)
COLOR_BLUE = (255, 165, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_DARK_GRAY = (40, 40, 40)
COLOR_PANEL_BG = (20, 25, 35)

def draw_rounded_rect(img, top_left, bottom_right, color, thickness=-1, radius=10):
    """Draw a rounded rectangle"""
    x1, y1 = top_left
    x2, y2 = bottom_right
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)
    cv2.circle(img, (x1 + radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x1 + radius, y2 - radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y2 - radius), radius, color, thickness)


def draw_text_with_bg(img, text, pos, font, font_scale, text_color, bg_color, padding=5, thickness=2):
    """Draw text with background rectangle"""
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = pos
    cv2.rectangle(img, (x - padding, y - text_h - padding), (x + text_w + padding, y + baseline + padding), bg_color, -1)
    cv2.putText(img, text, (x, y), font, font_scale, text_color, thickness, cv2.LINE_AA)


def draw_status_panel(panel_width, panel_height, status_text, name_text, attendance_text, date_text, time_text, status_color):
    """Create a separate status panel image"""
    # Colors (BGR format)
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLUE = (255, 165, 0)
    COLOR_DARK_GRAY = (40, 40, 40)
    COLOR_PANEL_BG = (20, 25, 35)
    
    # Create panel
    panel = np.full((panel_height, panel_width, 3), COLOR_PANEL_BG, dtype=np.uint8)
    
    # Title
    cv2.putText(panel, "RECOGNITION STATUS", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_WHITE, 2, cv2.LINE_AA)
    
    # Divider
    cv2.line(panel, (20, 55), (panel_width - 20, 55), COLOR_BLUE, 1)
    
    # Status
    cv2.putText(panel, "Status:", (20, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, 1, cv2.LINE_AA)
    draw_text_with_bg(panel, status_text, (20, 130), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_WHITE, status_color, 10)
    
    # Name
    cv2.putText(panel, "Name:", (20, 180), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, 1, cv2.LINE_AA)
    draw_text_with_bg(panel, name_text, (20, 210), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_WHITE, COLOR_DARK_GRAY, 10)
    
    # Attendance
    cv2.putText(panel, "Attendance:", (20, 260), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, 1, cv2.LINE_AA)
    draw_text_with_bg(panel, attendance_text, (20, 290), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, COLOR_DARK_GRAY, 10)
    
    # Divider
    cv2.line(panel, (20, 330), (panel_width - 20, 330), COLOR_BLUE, 1)
    
    # Date & Time
    cv2.putText(panel, "Date:", (20, 360), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, 1, cv2.LINE_AA)
    draw_text_with_bg(panel, date_text, (20, 390), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, COLOR_DARK_GRAY, 10)
    
    cv2.putText(panel, "Time:", (20, 430), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, 1, cv2.LINE_AA)
    draw_text_with_bg(panel, time_text, (20, 460), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, COLOR_DARK_GRAY, 10)
    
    # Exit instruction
    cv2.line(panel, (20, 500), (panel_width - 20, 500), COLOR_BLUE, 1)
    cv2.putText(panel, "Press 'Q' to Exit", (20, 530), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_BLUE, 1, cv2.LINE_AA)
    
    return panel


def draw_header_bar(frame):
    """Draw top header bar on frame"""
    h, w = frame.shape[:2]
    bar_height = 60
    
    # Colors
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLUE = (255, 165, 0)
    COLOR_PANEL_BG = (20, 25, 35)
    
    # Header background
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, bar_height), COLOR_PANEL_BG, -1)
    cv2.addWeighted(overlay, 0.95, frame, 0.05, 0, frame)
    
    # Title
    cv2.putText(frame, "FACE RECOGNITION ATTENDANCE SYSTEM", (30, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, COLOR_WHITE, 2, cv2.LINE_AA)
    
    # Bottom border
    cv2.line(frame, (0, bar_height), (w, bar_height), COLOR_BLUE, 2)


def draw_face_box(frame, x, y, fw, fh, name, score, is_recognized, attendance_marked=False, already_marked=False):
    """Draw professional face bounding box with label"""
    
    if is_recognized:
        box_color = COLOR_GREEN
        label_bg = COLOR_GREEN
        if already_marked:
            label_text = f"{name} (Already Marked)"
        elif attendance_marked:
            label_text = f"{name} - Attendance Marked"
        else:
            label_text = f"{name} ({score:.2f})"
    else:
        box_color = COLOR_RED
        label_bg = COLOR_RED
        label_text = f"Unknown ({score:.2f})"
    
    # Draw face rectangle with rounded corners effect
    thickness = 3
    cv2.rectangle(frame, (x, y), (x + fw, y + fh), box_color, thickness)
    
    # Corner accents
    corner_len = 20
    cv2.line(frame, (x, y), (x + corner_len, y), box_color, 4)
    cv2.line(frame, (x, y), (x, y + corner_len), box_color, 4)
    cv2.line(frame, (x + fw, y), (x + fw - corner_len, y), box_color, 4)
    cv2.line(frame, (x + fw, y), (x + fw, y + corner_len), box_color, 4)
    cv2.line(frame, (x, y + fh), (x + corner_len, y + fh), box_color, 4)
    cv2.line(frame, (x, y + fh), (x, y + fh - corner_len), box_color, 4)
    cv2.line(frame, (x + fw, y + fh), (x + fw - corner_len, y + fh), box_color, 4)
    cv2.line(frame, (x + fw, y + fh), (x + fw, y + fh - corner_len), box_color, 4)
    
    # Label background
    (text_w, text_h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
    label_x = x
    label_y = max(y - 15, 25)
    
    cv2.rectangle(frame, (label_x - 5, label_y - text_h - 5), 
                  (label_x + text_w + 5, label_y + 5), label_bg, -1)
    
    # Label text
    cv2.putText(frame, label_text, (label_x, label_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_WHITE, 2, cv2.LINE_AA)


# -----------------------------------
# 13. CAMERA LOOP
# -----------------------------------

PANEL_WIDTH = 340

frame_counter = 0
last_recognized_name = None
attendance_just_marked = False
already_marked_flag = False

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame not captured!")
        break

    frame_counter += 1

    # Frame size
    h, w = frame.shape[:2]

    detector.setInputSize((w, h))

    # -----------------------------------
    # DETECT FACES
    # -----------------------------------

    _, faces = detector.detect(frame)

    face_detected = False
    recognized_this_frame = False
    current_name = "---"
    current_attendance = "---"
    current_status = "Scanning..."
    status_color = COLOR_BLUE
    best_score = -1
    best_name = "Unknown"

    if faces is not None:

        for face in faces:

            face_detected = True

            # Face coordinates
            x, y, fw, fh = face[:4].astype(int)

            # -----------------------------------
            # ALIGN FACE
            # -----------------------------------

            aligned_face = recognizer.alignCrop(frame, face)

            # -----------------------------------
            # EXTRACT FEATURE
            # -----------------------------------

            feature = recognizer.feature(aligned_face)

            # -----------------------------------
            # COMPARE WITH ALL PEOPLE
            # -----------------------------------

            best_name = "Unknown"
            best_score = -1

            for name, known_feature in known_features.items():

                score = recognizer.match(
                    known_feature,
                    feature,
                    cv2.FaceRecognizerSF_FR_COSINE
                )

                if score > best_score:
                    best_score = score
                    best_name = name

            # -----------------------------------
            # RECOGNITION LOGIC
            # -----------------------------------

            if best_score >= threshold:
                current_name = best_name
                recognized_this_frame = True
                
                # Mark attendance
                if best_name in marked_today:
                    already_marked_flag = True
                    current_status = "Already Marked"
                    current_attendance = "Already Marked Today"
                    status_color = COLOR_YELLOW
                else:
                    attendance_marked = mark_attendance(best_name)
                    if attendance_marked:
                        attendance_just_marked = True
                        last_recognized_name = best_name
                        current_status = "Attendance Marked"
                        current_attendance = "Marked Successfully"
                        status_color = COLOR_GREEN
                    else:
                        current_status = "Recognized"
                        current_attendance = "Pending"
                        status_color = COLOR_GREEN
            else:
                current_status = "Face Detected - Unknown"
                current_attendance = "Not Registered"
                status_color = COLOR_RED

            # Draw face box on frame (no panel overlap)
            draw_face_box(frame, x, y, fw, fh, best_name, best_score, 
                         best_score >= threshold, attendance_just_marked, already_marked_flag)

    # Update status if no face detected
    if not face_detected:
        current_status = "Waiting for face..."
        current_name = "---"
        current_attendance = "---"
        status_color = COLOR_BLUE
        attendance_just_marked = False
        already_marked_flag = False

    # Get current date and time
    now = datetime.now()
    date_str = now.strftime("%d %B %Y")
    time_str = now.strftime("%H:%M:%S")

    # -----------------------------------
    # DRAW UI ELEMENTS ON FRAME
    # -----------------------------------

    # Header bar on camera frame
    draw_header_bar(frame)

    # -----------------------------------
    # CREATE COMBINED DISPLAY
    # -----------------------------------
    # Create canvas: camera frame on left, status panel on right
    canvas_height = h
    canvas_width = w + PANEL_WIDTH
    canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
    
    # Place camera frame on left
    canvas[0:h, 0:w] = frame
    
    # Create and place status panel on right
    status_panel = draw_status_panel(PANEL_WIDTH, h, current_status, current_name, 
                                      current_attendance, date_str, time_str, status_color)
    canvas[0:h, w:w+PANEL_WIDTH] = status_panel

    # -----------------------------------
    # DISPLAY CAMERA
    # -----------------------------------

    cv2.imshow(
        "Face Recognition Attendance",
        canvas
    )

    # -----------------------------------
    # PRESS Q TO EXIT
    # -----------------------------------

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        print("Q pressed.")
        break


# -----------------------------------
# 14. CLOSE CAMERA
# -----------------------------------

cap.release()
cv2.destroyAllWindows()

print()
print("===================================")
print("Attendance System Closed.")
print("===================================")
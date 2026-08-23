import cv2
import os
import csv
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
    print("YuNet model nahi mila!")
    exit()

if not os.path.exists(recognizer_model):
    print("SFace model nahi mila!")
    exit()

if not os.path.exists(known_faces_folder):
    print("known_faces folder nahi mila!")
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
        print("Image load nahi hui:", file_name)
        continue

    h, w = image.shape[:2]

    detector.setInputSize((w, h))

    _, faces = detector.detect(image)

    if faces is None:
        print("Face nahi mila:", file_name)
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
    print("Koi known face nahi mila!")
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

    print("Camera open nahi hua!")
    exit()


print()
print("Camera successfully opened!")
print("Face recognition started!")
print("Q dabakar exit karo.")


# -----------------------------------
# 11. THRESHOLD
# -----------------------------------

threshold = 0.30


# -----------------------------------
# 12. CAMERA LOOP
# -----------------------------------

while True:

    ret, frame = cap.read()

    if not ret:

        print("Frame nahi mila!")

        break


    # Frame size
    h, w = frame.shape[:2]

    detector.setInputSize(
        (w, h)
    )


    # --------------------------------
    # 13. DETECT FACES
    # --------------------------------

    _, faces = detector.detect(
        frame
    )


    if faces is not None:

        for face in faces:

            # Face coordinates
            x, y, fw, fh = face[:4].astype(int)


            # --------------------------------
            # 14. ALIGN FACE
            # --------------------------------

            aligned_face = recognizer.alignCrop(
                frame,
                face
            )


            # --------------------------------
            # 15. EXTRACT FEATURE
            # --------------------------------

            feature = recognizer.feature(
                aligned_face
            )


            # --------------------------------
            # 16. COMPARE WITH ALL PEOPLE
            # --------------------------------

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


            # --------------------------------
            # 17. RECOGNITION
            # --------------------------------

            if best_score >= threshold:

                name = best_name

                box_color = (0, 255, 0)

                # Mark attendance
                mark_attendance(name)

            else:

                name = "Unknown"

                box_color = (0, 0, 255)


            # --------------------------------
            # 18. LABEL
            # --------------------------------

            label = f"{name} | Score: {best_score:.2f}"


            # --------------------------------
            # 19. DRAW BOX
            # --------------------------------

            cv2.rectangle(
                frame,
                (x, y),
                (x + fw, y + fh),
                box_color,
                2
            )


            # --------------------------------
            # 20. DISPLAY NAME
            # --------------------------------

            cv2.putText(
                frame,
                label,
                (x, max(y - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                box_color,
                2
            )


    # --------------------------------
    # 21. DISPLAY CAMERA
    # --------------------------------

    cv2.imshow(
        "Face Recognition Attendance",
        frame
    )


    # --------------------------------
    # 22. PRESS Q
    # --------------------------------

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        print("Q pressed.")

        break


# -----------------------------------
# 23. CLOSE CAMERA
# -----------------------------------

cap.release()

cv2.destroyAllWindows()

print()
print("===================================")
print("Attendance System Closed.")
print("===================================")
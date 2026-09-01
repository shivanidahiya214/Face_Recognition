import cv2
import os
import numpy as np


# -----------------------------------
# PATHS
# -----------------------------------

detector_model = "models/face_detection_yunet_2026may.onnx"
recognizer_model = "models/face_recognition_sface_2021dec.onnx"
known_faces_folder = "known_faces"

threshold = 0.30


# -----------------------------------
# CHECK FILES
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
# CREATE DETECTOR
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
# CREATE RECOGNIZER
# -----------------------------------

recognizer = cv2.FaceRecognizerSF.create(
    recognizer_model,
    ""
)

print("Face recognizer ready!")


# -----------------------------------
# LOAD KNOWN FACES
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
# CHECK KNOWN FACES
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
# OPEN CAMERA
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
# CAMERA LOOP
# -----------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame not captured!")
        break

    # Frame size
    h, w = frame.shape[:2]

    detector.setInputSize((w, h))

    # DETECT FACES
    _, faces = detector.detect(frame)

    if faces is not None:

        for face in faces:

            # Face coordinates
            x, y, fw, fh = face[:4].astype(int)

            # ALIGN FACE
            aligned_face = recognizer.alignCrop(frame, face)

            # EXTRACT FEATURE
            feature = recognizer.feature(aligned_face)

            # COMPARE WITH ALL PEOPLE
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

            # RECOGNITION
            if best_score >= threshold:
                name = best_name
                box_color = (0, 255, 0)  # Green
            else:
                name = "Unknown"
                box_color = (0, 0, 255)  # Red

            # DRAW FACE BOX
            cv2.rectangle(
                frame,
                (x, y),
                (x + fw, y + fh),
                box_color,
                2
            )

            # DISPLAY NAME AND SCORE
            label = f"{name} ({best_score:.2f})"

            cv2.putText(
                frame,
                label,
                (x, max(y - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                box_color,
                2
            )

    # DISPLAY CAMERA (FULL FRAME)
    cv2.imshow(
        "Face Recognition",
        frame
    )

    # PRESS Q TO EXIT
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        print("Q pressed.")
        break


# -----------------------------------
# CLOSE CAMERA
# -----------------------------------

cap.release()
cv2.destroyAllWindows()

print()
print("Face Recognition Closed.")
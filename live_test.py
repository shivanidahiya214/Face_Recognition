import cv2
import os
import numpy as np

print("Face Recognition starting...")

# -----------------------------
# MODEL PATHS
# -----------------------------
detector_model = "models/face_detection_yunet_2026may.onnx"
recognizer_model = "models/face_recognition_sface_2021dec.onnx"
known_face_path = "known_faces/Shivani.jpg"

# -----------------------------
# CHECK FILES
# -----------------------------
if not os.path.exists(detector_model):
    print("YuNet model nahi mila!")
    exit()

if not os.path.exists(recognizer_model):
    print("SFace model nahi mila!")
    exit()

if not os.path.exists(known_face_path):
    print("Known face nahi mila:", known_face_path)
    exit()

# -----------------------------
# CREATE FACE DETECTOR
# -----------------------------
detector = cv2.FaceDetectorYN.create(
    detector_model,
    "",
    (320, 320),
    0.9,
    0.3,
    5000
)

# -----------------------------
# CREATE FACE RECOGNIZER
# -----------------------------
recognizer = cv2.FaceRecognizerSF.create(
    recognizer_model,
    ""
)

# -----------------------------
# LOAD KNOWN FACE
# -----------------------------
known_image = cv2.imread(known_face_path)

if known_image is None:
    print("Shivani.jpg load nahi hui!")
    exit()

h, w = known_image.shape[:2]

detector.setInputSize((w, h))

_, known_faces = detector.detect(known_image)

if known_faces is None:
    print("Known image mein face nahi mila!")
    exit()

print("Known face detected!")

# First detected face
known_face = known_faces[0]

# -----------------------------
# ALIGN KNOWN FACE
# -----------------------------
known_aligned = recognizer.alignCrop(
    known_image,
    known_face
)

# -----------------------------
# EXTRACT KNOWN FACE FEATURE
# -----------------------------
known_feature = recognizer.feature(
    known_aligned
)

print("Known face successfully loaded!")

# -----------------------------
# OPEN CAMERA
# -----------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera open nahi hua!")
    exit()

print("Camera successfully opened!")
print("Face recognition starting...")
print("Q dabakar exit karo.")

# -----------------------------
# RECOGNITION THRESHOLD
# -----------------------------
threshold = 0.363

# -----------------------------
# LIVE CAMERA
# -----------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame nahi mila!")
        break

    h, w = frame.shape[:2]

    # Detector input size
    detector.setInputSize((w, h))

    # Detect faces
    _, faces = detector.detect(frame)

    # -----------------------------
    # IF FACE FOUND
    # -----------------------------
    if faces is not None:

        for face in faces:

            # Face coordinates
            x, y, fw, fh = face[:4].astype(int)

            # -----------------------------
            # ALIGN DETECTED FACE
            # -----------------------------
            aligned_face = recognizer.alignCrop(
                frame,
                face
            )

            # -----------------------------
            # EXTRACT FACE FEATURE
            # -----------------------------
            feature = recognizer.feature(
                aligned_face
            )

            # -----------------------------
            # COMPARE WITH KNOWN FACE
            # -----------------------------
            score = recognizer.match(
                known_feature,
                feature,
                cv2.FaceRecognizerSF_FR_COSINE
            )

            # -----------------------------
            # KNOWN / UNKNOWN
            # -----------------------------
            if score >= threshold:

                name = "Shivani"
                label = f"{name} ({score:.2f})"

                # GREEN = KNOWN
                box_color = (0, 255, 0)

            else:

                name = "Unknown"
                label = f"{name} ({score:.2f})"

                # RED = UNKNOWN
                box_color = (0, 0, 255)

            # -----------------------------
            # DRAW FACE BOX
            # -----------------------------
            cv2.rectangle(
                frame,
                (x, y),
                (x + fw, y + fh),
                box_color,
                2
            )

            # -----------------------------
            # DRAW NAME
            # -----------------------------
            cv2.putText(
                frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                box_color,
                2
            )

    # -----------------------------
    # SHOW CAMERA
    # -----------------------------
    cv2.imshow(
        "Face Recognition",
        frame
    )

    # -----------------------------
    # PRESS Q TO EXIT
    # -----------------------------
    if cv2.waitKey(1) & 0xFF == ord("q"):

        print("Q pressed. Camera closing...")
        break

# -----------------------------
# CLOSE CAMERA
# -----------------------------
cap.release()

cv2.destroyAllWindows()

print("Face Recognition closed.")
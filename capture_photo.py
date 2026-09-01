import cv2
import os
import sys

print("===================================")
print("       FACE PHOTO CAPTURE")
print("===================================")

# Get name from GUI argument
if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = input("Enter person's name: ")

name = name.strip()

if not name:
    print("No name provided!")
    exit()

# Create folder
folder = "known_faces"

if not os.path.exists(folder):
    os.makedirs(folder)

# Open camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Could not open camera!")
    exit()

print()
print("Camera started!")
print("Position your face in front of the camera.")
print("Press SPACE = Capture photo")
print("Press Q = Exit")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame not captured!")
        break

    # Draw instructions on frame
    cv2.putText(
        frame,
        "SPACE = Capture Photo  |  Q = Exit",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    # Draw center guide
    h, w = frame.shape[:2]
    center_x, center_y = w // 2, h // 2
    cv2.circle(frame, (center_x, center_y), 100, (0, 255, 0), 2)
    cv2.line(frame, (center_x - 120, center_y), (center_x - 80, center_y), (0, 255, 0), 2)
    cv2.line(frame, (center_x + 80, center_y), (center_x + 120, center_y), (0, 255, 0), 2)
    cv2.line(frame, (center_x, center_y - 120), (center_x, center_y - 80), (0, 255, 0), 2)
    cv2.line(frame, (center_x, center_y + 80), (center_x, center_y + 120), (0, 255, 0), 2)

    cv2.imshow("Photo Capture", frame)

    key = cv2.waitKey(1) & 0xFF

    # SPACE = Capture photo
    if key == 32:

        file_path = os.path.join(
            folder,
            name + ".jpg"
        )

        success = cv2.imwrite(
            file_path,
            frame
        )

        if success:
            print()
            print("Photo successfully saved!")
            print("File:", file_path)
        else:
            print("Failed to save photo!")

        break

    # Q = Exit
    if key == ord("q"):
        print("Capture cancelled.")
        break

cap.release()
cv2.destroyAllWindows()

print("Done!")
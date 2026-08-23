import cv2
import os
import sys

print("===================================")
print("       FACE PHOTO CAPTURE")
print("===================================")

# GUI se name receive karo
if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = input("Person ka naam enter karo: ")

name = name.strip()

if not name:
    print("Name nahi diya gaya!")
    exit()

# Folder create karo
folder = "known_faces"

if not os.path.exists(folder):
    os.makedirs(folder)

# Camera open
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera open nahi hua!")
    exit()

print()
print("Camera started!")
print("Face camera ke saamne rakho.")
print("SPACE dabao = Photo capture")
print("Q dabao = Exit")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame nahi mila!")
        break

    cv2.putText(
        frame,
        "SPACE = Capture | Q = Exit",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.imshow("Photo Capture", frame)

    key = cv2.waitKey(1) & 0xFF

    # SPACE = Photo capture
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
            print("Photo save nahi hui!")

        break

    # Q = Exit
    if key == ord("q"):
        print("Capture cancelled.")
        break

cap.release()
cv2.destroyAllWindows()

print("Done!")
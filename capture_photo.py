import cv2

cap = cv2.VideoCapture(0)

print("Camera start ho raha hai...")
print("Photo lene ke liye SPACE dabao")
print("Band karne ke liye Q dabao")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera nahi chal raha.")
        break

    cv2.imshow("Take Photo", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):
        cv2.imwrite("known_faces/new_person.jpg", frame)
        print("Photo save ho gayi: known_faces/new_person.jpg")
        break

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
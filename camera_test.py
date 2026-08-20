import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera open nahi hua!")
    exit()

print("Camera open hai.")
print("ESC dabakar band karo.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Frame nahi mila!")
        break

    cv2.imshow("Camera Test", frame)

    # ESC = 27
    key = cv2.waitKey(30)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

print("Camera closed.")
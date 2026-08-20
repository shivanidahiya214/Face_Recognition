# import cv2

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# if not cap.isOpened():
#     print("Camera open nahi hua!")
#     exit()

# print("Live camera starting...")
# print("Q dabakar exit karo.")

# while True:
#     ret, frame = cap.read()

#     if not ret:
#         print("Frame nahi mila!")
#         break

#     cv2.imshow("LIVE CAMERA", frame)

#     key = cv2.waitKey(30) & 0xFF

#     if key == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()
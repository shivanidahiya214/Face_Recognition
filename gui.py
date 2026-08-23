import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import os
import sys
import cv2
from PIL import Image, ImageTk


# ==========================================
# CAMERA VARIABLE
# ==========================================

cap = None


# ==========================================
# START GUI CAMERA
# ==========================================

def start_gui_camera():

    global cap

    if cap is not None and cap.isOpened():
        return

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        messagebox.showerror(
            "Camera Error",
            "Camera open nahi hua!"
        )
        return

    update_camera()


# ==========================================
# STOP GUI CAMERA
# ==========================================

def stop_gui_camera():

    global cap

    if cap is not None:
        cap.release()
        cap = None


# ==========================================
# UPDATE CAMERA
# ==========================================

def update_camera():

    global cap

    if cap is None or not cap.isOpened():
        return

    ret, frame = cap.read()

    if ret:

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(frame)

        image = image.resize(
            (496, 216)
        )

        photo = ImageTk.PhotoImage(image)

        camera_label.config(
            image=photo,
            text=""
        )

        camera_label.image = photo

    root.after(
        20,
        update_camera
    )


# ==========================================
# REGISTER FACE
# ==========================================

def register_face():

    if not os.path.exists("capture_photo.py"):

        messagebox.showerror(
            "Error",
            "capture_photo.py nahi mila!"
        )

        return

    name = simpledialog.askstring(
        "Register Face",
        "Enter your name:"
    )

    if not name:
        return

    try:

        stop_gui_camera()

        subprocess.Popen(
            [
                sys.executable,
                "capture_photo.py",
                name
            ]
        )

        messagebox.showinfo(
            "Register Face",
            "Camera open ho raha hai.\n\n"
            "Face camera ke saamne rakho."
        )

        start_gui_camera()

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

        start_gui_camera()


# ==========================================
# LIVE RECOGNITION
# ==========================================

def start_recognition():

    if not os.path.exists("live_test.py"):

        messagebox.showerror(
            "Error",
            "live_test.py nahi mila!"
        )

        return

    try:

        stop_gui_camera()

        subprocess.Popen(
            [
                sys.executable,
                "live_test.py"
            ]
        )

        messagebox.showinfo(
            "Live Recognition",
            "Live Recognition camera open ho raha hai."
        )

        start_gui_camera()

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

        start_gui_camera()


# ==========================================
# VIEW ATTENDANCE
# ==========================================

def view_attendance():

    if not os.path.exists("attendance.csv"):

        messagebox.showinfo(
            "Attendance",
            "Abhi attendance record available nahi hai."
        )

        return

    try:

        os.startfile(
            "attendance.csv"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ==========================================
# EXIT
# ==========================================

def exit_app():

    stop_gui_camera()

    root.destroy()


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title(
    "Face Recognition Attendance System"
)

root.geometry(
    "600x750"
)

root.resizable(
    False,
    False
)

root.configure(
    bg="#0f172a"
)


# ==========================================
# HEADER
# ==========================================

title = tk.Label(
    root,
    text="FACE RECOGNITION",
    font=("Arial", 26, "bold"),
    bg="#0f172a",
    fg="white"
)

title.pack(
    pady=(25, 0)
)


subtitle = tk.Label(
    root,
    text="ATTENDANCE SYSTEM",
    font=("Arial", 18, "bold"),
    bg="#0f172a",
    fg="#60a5fa"
)

subtitle.pack(
    pady=(2, 20)
)


# ==========================================
# REGISTER BUTTON
# ==========================================

register_button = tk.Button(
    root,
    text="REGISTER FACE",
    command=register_face,
    font=("Arial", 14, "bold"),
    width=25,
    height=2,
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)

register_button.pack(
    pady=8
)


# ==========================================
# CAMERA AREA
# ==========================================

camera_frame = tk.Frame(
    root,
    width=500,
    height=220,
    bg="#020617",
    highlightbackground="#334155",
    highlightthickness=2
)

camera_frame.pack(
    pady=15
)

camera_frame.pack_propagate(
    False
)


camera_label = tk.Label(
    camera_frame,
    text="CAMERA AREA",
    font=("Arial", 20, "bold"),
    bg="#020617",
    fg="#94a3b8"
)

camera_label.pack(
    expand=True
)


# ==========================================
# LIVE RECOGNITION
# ==========================================

live_button = tk.Button(
    root,
    text="LIVE RECOGNITION",
    command=start_recognition,
    font=("Arial", 14, "bold"),
    width=25,
    height=2,
    bg="#16a34a",
    fg="white",
    activebackground="#15803d",
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)

live_button.pack(
    pady=7
)


# ==========================================
# VIEW ATTENDANCE
# ==========================================

attendance_button = tk.Button(
    root,
    text="VIEW ATTENDANCE",
    command=view_attendance,
    font=("Arial", 14, "bold"),
    width=25,
    height=2,
    bg="#f59e0b",
    fg="white",
    activebackground="#d97706",
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)

attendance_button.pack(
    pady=7
)


# ==========================================
# EXIT
# ==========================================

exit_button = tk.Button(
    root,
    text="EXIT",
    command=exit_app,
    font=("Arial", 14, "bold"),
    width=25,
    height=2,
    bg="#dc2626",
    fg="white",
    activebackground="#b91c1c",
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)

exit_button.pack(
    pady=7
)


# ==========================================
# FOOTER
# ==========================================

footer = tk.Label(
    root,
    text="Face Recognition • Automated Attendance",
    font=("Arial", 10),
    bg="#0f172a",
    fg="#64748b"
)

footer.pack(
    pady=18
)


# ==========================================
# START CAMERA
# ==========================================

start_gui_camera()


# ==========================================
# START APPLICATION
# ==========================================

root.mainloop()
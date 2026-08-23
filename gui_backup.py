import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import os
import sys


# -----------------------------------
# COLORS
# -----------------------------------

BG_COLOR = "#0B1F3A"          # Dark Navy
TITLE_COLOR = "#FFFFFF"       # White
SUBTITLE_COLOR = "#7DD3FC"    # Light Blue
BUTTON_COLOR = "#2563EB"      # Blue
BUTTON_HOVER = "#3B82F6"      # Light Blue
ATTENDANCE_COLOR = "#0891B2"  # Cyan Blue
EXIT_COLOR = "#DC2626"        # Red
EXIT_HOVER = "#EF4444"
FOOTER_COLOR = "#94A3B8"


# -----------------------------------
# START RECOGNITION
# -----------------------------------

def start_recognition():

    if not os.path.exists("live_test.py"):
        messagebox.showerror(
            "Error",
            "live_test.py nahi mila!"
        )
        return

    try:
        subprocess.Popen(
            [sys.executable, "live_test.py"]
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


# -----------------------------------
# REGISTER FACE
# -----------------------------------

def register_face():

    if not os.path.exists("capture_photo.py"):
        messagebox.showerror(
            "Error",
            "capture_photo.py nahi mila!"
        )
        return

    name = simpledialog.askstring(
        "Register Face",
        "Person ka naam enter karo:"
    )

    if name is None:
        return

    name = name.strip()

    if not name:
        messagebox.showwarning(
            "Warning",
            "Please naam enter karo!"
        )
        return

    try:
        subprocess.Popen(
            [sys.executable, "capture_photo.py", name]
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


# -----------------------------------
# VIEW ATTENDANCE
# -----------------------------------

def view_attendance():

    if not os.path.exists("attendance.csv"):

        messagebox.showinfo(
            "Attendance",
            "Abhi attendance.csv available nahi hai."
        )

        return

    try:
        os.startfile(
            os.path.abspath("attendance.csv")
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


# -----------------------------------
# EXIT
# -----------------------------------

def exit_app():
    root.destroy()


# -----------------------------------
# BUTTON HOVER EFFECT
# -----------------------------------

def button_hover(button, normal_color, hover_color):

    button.bind(
        "<Enter>",
        lambda event: button.config(
            bg=hover_color
        )
    )

    button.bind(
        "<Leave>",
        lambda event: button.config(
            bg=normal_color
        )
    )


# -----------------------------------
# CREATE WINDOW
# -----------------------------------

root = tk.Tk()

root.title(
    "Face Recognition Attendance System"
)

root.geometry(
    "600x500"
)

root.resizable(
    False,
    False
)

root.configure(
    bg=BG_COLOR
)


# -----------------------------------
# TITLE
# -----------------------------------

title = tk.Label(
    root,
    text="FACE RECOGNITION",
    font=("Arial", 24, "bold"),
    fg=TITLE_COLOR,
    bg=BG_COLOR
)

title.pack(
    pady=(40, 5)
)


# -----------------------------------
# SUBTITLE
# -----------------------------------

subtitle = tk.Label(
    root,
    text="ATTENDANCE SYSTEM",
    font=("Arial", 18, "bold"),
    fg=SUBTITLE_COLOR,
    bg=BG_COLOR
)

subtitle.pack(
    pady=(0, 30)
)


# -----------------------------------
# REGISTER BUTTON
# -----------------------------------

register_button = tk.Button(
    root,
    text="REGISTER FACE",
    font=("Arial", 14, "bold"),
    width=25,
    height=2,
    bg=BUTTON_COLOR,
    fg="white",
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=register_face
)

register_button.pack(
    pady=8
)

button_hover(
    register_button,
    BUTTON_COLOR,
    BUTTON_HOVER
)


# -----------------------------------
# RECOGNITION BUTTON
# -----------------------------------

recognition_button = tk.Button(
    root,
    text="LIVE RECOGNITION",
    font=("Arial", 14, "bold"),
    width=25,
    height=2,
    bg=BUTTON_COLOR,
    fg="white",
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=start_recognition
)

recognition_button.pack(
    pady=8
)

button_hover(
    recognition_button,
    BUTTON_COLOR,
    BUTTON_HOVER
)


# -----------------------------------
# ATTENDANCE BUTTON
# -----------------------------------

attendance_button = tk.Button(
    root,
    text="VIEW ATTENDANCE",
    font=("Arial", 14, "bold"),
    width=25,
    height=2,
    bg=ATTENDANCE_COLOR,
    fg="white",
    activebackground="#06B6D4",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=view_attendance
)

attendance_button.pack(
    pady=8
)

button_hover(
    attendance_button,
    ATTENDANCE_COLOR,
    "#06B6D4"
)


# -----------------------------------
# EXIT BUTTON
# -----------------------------------

exit_button = tk.Button(
    root,
    text="EXIT",
    font=("Arial", 14, "bold"),
    width=25,
    height=2,
    bg=EXIT_COLOR,
    fg="white",
    activebackground=EXIT_HOVER,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=exit_app
)

exit_button.pack(
    pady=8
)

button_hover(
    exit_button,
    EXIT_COLOR,
    EXIT_HOVER
)


# -----------------------------------
# FOOTER
# -----------------------------------

footer = tk.Label(
    root,
    text="AI Based Face Recognition System",
    font=("Arial", 10),
    fg=FOOTER_COLOR,
    bg=BG_COLOR
)

footer.pack(
    pady=22
)


# -----------------------------------
# START GUI
# -----------------------------------

root.mainloop()

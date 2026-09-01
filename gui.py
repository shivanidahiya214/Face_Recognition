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
            "Could not open camera!"
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
            (496, 180)
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
            "capture_photo.py not found!"
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
            "Opening camera...\n\n"
            "Position your face in front of the camera."
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
            "live_test.py not found!"
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
            "Live Recognition camera is opening."
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
            "No attendance records available yet."
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

# Start maximized (fullscreen on Windows)
root.state('zoomed')

root.configure(
    bg="#0d1117"
)

# Set minimum size to prevent squishing
root.minsize(800, 600)


# ==========================================
# STYLES
# ==========================================

BG_DARK = "#0d1117"
BG_CARD = "#161b22"
BG_CARD_HOVER = "#1f2428"
BORDER = "#30363d"
TEXT_PRIMARY = "#e6edf3"
TEXT_SECONDARY = "#8b949e"
TEXT_MUTED = "#6e7681"
ACCENT_BLUE = "#58a6ff"
ACCENT_GREEN = "#3fb950"
ACCENT_ORANGE = "#d29922"
ACCENT_RED = "#f85149"


def create_modern_button(parent, text, command, bg_color, hover_color, width=28, height=2, font_size=13):
    """Create a modern flat button with hover effect"""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", font_size, "bold"),
        width=width,
        height=height,
        bg=bg_color,
        fg="white",
        activebackground=hover_color,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        bd=0,
        highlightthickness=0
    )
    
    def on_enter(e):
        btn.config(bg=hover_color)
    def on_leave(e):
        btn.config(bg=bg_color)
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def create_card_frame(parent):
    """Create a card-style frame"""
    frame = tk.Frame(
        parent,
        bg=BG_CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    return frame


# ==========================================
# HEADER SECTION
# ==========================================

header_frame = tk.Frame(root, bg=BG_DARK)
header_frame.pack(fill="x", pady=(15, 5))

title = tk.Label(
    header_frame,
    text="FACE RECOGNITION",
    font=("Segoe UI", 24, "bold"),
    bg=BG_DARK,
    fg=TEXT_PRIMARY
)
title.pack()

subtitle = tk.Label(
    header_frame,
    text="ATTENDANCE SYSTEM",
    font=("Segoe UI", 14, "bold"),
    bg=BG_DARK,
    fg=ACCENT_BLUE
)
subtitle.pack(pady=(3, 0))

# Divider line
divider = tk.Frame(root, height=1, bg=BORDER)
divider.pack(fill="x", padx=30, pady=10)


# ==========================================
# CAMERA PREVIEW CARD
# ==========================================

camera_card = create_card_frame(root)
camera_card.pack(fill="x", padx=20, pady=5)

camera_header = tk.Frame(camera_card, bg=BG_CARD)
camera_header.pack(fill="x", padx=15, pady=(10, 3))

camera_title = tk.Label(
    camera_header,
    text="CAMERA PREVIEW",
    font=("Segoe UI", 11, "bold"),
    bg=BG_CARD,
    fg=TEXT_SECONDARY
)
camera_title.pack(side="left")

status_indicator = tk.Label(
    camera_header,
    text="● LIVE",
    font=("Segoe UI", 9, "bold"),
    bg=BG_CARD,
    fg=ACCENT_GREEN
)
status_indicator.pack(side="right")

camera_frame = tk.Frame(
    camera_card,
    width=520,
    height=180,
    bg="#000000",
    highlightbackground=BORDER,
    highlightthickness=1
)
camera_frame.pack(padx=15, pady=(0, 12))
camera_frame.pack_propagate(False)

camera_label = tk.Label(
    camera_frame,
    text="Initializing camera...",
    font=("Segoe UI", 12),
    bg="#000000",
    fg=TEXT_MUTED
)
camera_label.pack(expand=True)


# ==========================================
# CONTROL BUTTONS CARD
# ==========================================

controls_card = create_card_frame(root)
controls_card.pack(fill="x", padx=20, pady=5)

controls_title = tk.Label(
    controls_card,
    text="CONTROLS",
    font=("Segoe UI", 11, "bold"),
    bg=BG_CARD,
    fg=TEXT_SECONDARY
)
controls_title.pack(anchor="w", padx=15, pady=(10, 5))

buttons_frame = tk.Frame(controls_card, bg=BG_CARD)
buttons_frame.pack(padx=15, pady=(0, 10))

# Register Face Button
register_button = create_modern_button(
    buttons_frame,
    "REGISTER FACE",
    register_face,
    ACCENT_BLUE,
    "#3b82f6",
    width=28,
    height=1,
    font_size=12
)
register_button.pack(pady=4)

# Start Recognition Button
live_button = create_modern_button(
    buttons_frame,
    "START RECOGNITION",
    start_recognition,
    ACCENT_GREEN,
    "#3fb950",
    width=28,
    height=1,
    font_size=12
)
live_button.pack(pady=4)

# View Attendance Button
attendance_button = create_modern_button(
    buttons_frame,
    "VIEW ATTENDANCE",
    view_attendance,
    ACCENT_ORANGE,
    "#d29922",
    width=28,
    height=1,
    font_size=12
)
attendance_button.pack(pady=4)

# Exit Button
exit_button = create_modern_button(
    buttons_frame,
    "EXIT",
    exit_app,
    ACCENT_RED,
    "#f85149",
    width=28,
    height=1,
    font_size=12
)
exit_button.pack(pady=4)


# ==========================================
# INFO CARD
# ==========================================

info_card = create_card_frame(root)
info_card.pack(fill="x", padx=20, pady=5)

info_title = tk.Label(
    info_card,
    text="SYSTEM INFO",
    font=("Segoe UI", 11, "bold"),
    bg=BG_CARD,
    fg=TEXT_SECONDARY
)
info_title.pack(anchor="w", padx=15, pady=(8, 5))

info_items = [
    ("Model", "YuNet + SFace"),
    ("Format", "ONNX (CPU Optimized)"),
    ("Storage", "CSV (attendance.csv)"),
    ("Threshold", "0.30 Cosine Similarity"),
]

for label, value in info_items:
    item_frame = tk.Frame(info_card, bg=BG_CARD)
    item_frame.pack(fill="x", padx=15, pady=1)
    
    tk.Label(
        item_frame,
        text=label + ":",
        font=("Segoe UI", 9),
        bg=BG_CARD,
        fg=TEXT_MUTED,
        width=10,
        anchor="w"
    ).pack(side="left")
    
    tk.Label(
        item_frame,
        text=value,
        font=("Segoe UI", 9, "bold"),
        bg=BG_CARD,
        fg=TEXT_PRIMARY,
        anchor="w"
    ).pack(side="left")

tk.Frame(info_card, height=5, bg=BG_CARD).pack()


# ==========================================
# FOOTER
# ==========================================

footer = tk.Label(
    root,
    text="Face Recognition • Automated Attendance System",
    font=("Segoe UI", 8),
    bg=BG_DARK,
    fg=TEXT_MUTED
)
footer.pack(pady=8)


# ==========================================
# START CAMERA
# ==========================================

start_gui_camera()


# ==========================================
# START APPLICATION
# ==========================================

root.mainloop()
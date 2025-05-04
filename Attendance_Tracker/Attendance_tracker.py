import tkinter as tk
from tkinter import ttk, messagebox

# Initialize the main app window
root = tk.Tk()
root.title("Smart Attendance Tracker")
root.geometry("650x600")
root.configure(bg="white")

# Dictionary to store attendance data
# Format: {'Subject': {'Student': {'attended': x, 'total': y}}}
attendance_data = {}

# ----- UI FRAMES -----
frame_top = tk.Frame(root, bg="white")
frame_top.pack(pady=10)

frame_input = tk.LabelFrame(root, text="Add Student", padx=10, pady=10, bg="white")
frame_input.pack(padx=10, pady=10, fill="x")

frame_mark = tk.LabelFrame(root, text="Mark Attendance", padx=10, pady=10, bg="white")
frame_mark.pack(padx=10, pady=10, fill="x")

frame_display = tk.LabelFrame(root, text="Attendance Display", padx=10, pady=10, bg="white")
frame_display.pack(padx=10, pady=10, fill="both", expand=True)

# ----- TOP TITLE -----
tk.Label(frame_top, text="Smart Attendance Tracker", font=("Arial", 18, "bold"), bg="white").pack()

# ----- INPUT SECTION -----
tk.Label(frame_input, text="Student Name:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_student = ttk.Entry(frame_input, width=30)
entry_student.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Subject Name:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_subject = ttk.Entry(frame_input, width=30)
entry_subject.grid(row=1, column=1, padx=5, pady=5)

def add_student():
    student = entry_student.get().strip()
    subject = entry_subject.get().strip()

    if student == "" or subject == "":
        messagebox.showerror("Error", "Both fields are required.")
        return

    if subject not in attendance_data:
        attendance_data[subject] = {}

    if student not in attendance_data[subject]:
        attendance_data[subject][student] = {"attended": 0, "total": 0}
        messagebox.showinfo("Success", f"{student} added to {subject}")
        update_student_menu()
    else:
        messagebox.showwarning("Exists", f"{student} already exists in {subject}")

    entry_student.delete(0, tk.END)
    entry_subject.delete(0, tk.END)

ttk.Button(frame_input, text="Add Student", command=add_student).grid(row=2, columnspan=2, pady=10)

# ----- MARK ATTENDANCE SECTION -----
tk.Label(frame_mark, text="Student:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
student_menu = ttk.Combobox(frame_mark, state="readonly", width=27)
student_menu.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_mark, text="Subject:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
subject_entry = ttk.Entry(frame_mark, width=30)
subject_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_mark, text="Status:", bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="e")
action_menu = ttk.Combobox(frame_mark, values=["Present", "Absent"], state="readonly", width=27)
action_menu.grid(row=2, column=1, padx=5, pady=5)

def mark_attendance():
    student = student_menu.get().strip()
    subject = subject_entry.get().strip()
    action = action_menu.get().strip()

    if student == "" or subject == "" or action == "":
        messagebox.showerror("Error", "All fields must be filled.")
        return

    if subject not in attendance_data or student not in attendance_data[subject]:
        messagebox.showerror("Error", "Student or subject not found.")
        return

    if action == "Present":
        attendance_data[subject][student]["attended"] += 1
    attendance_data[subject][student]["total"] += 1

    update_attendance_display()
    messagebox.showinfo("Success", f"{action} marked for {student} in {subject}")

ttk.Button(frame_mark, text="Mark Attendance", command=mark_attendance).grid(row=3, columnspan=2, pady=10)

# ----- ATTENDANCE DISPLAY -----
text_display = tk.Text(frame_display, height=15, wrap=tk.WORD, state=tk.DISABLED, font=("Courier", 10))
text_display.pack(fill="both", expand=True)

def update_student_menu():
    students = set()
    for subject in attendance_data:
        students.update(attendance_data[subject].keys())
    student_menu['values'] = sorted(students)

def update_attendance_display():
    text_display.config(state=tk.NORMAL)
    text_display.delete(1.0, tk.END)

    for subject, students in attendance_data.items():
        text_display.insert(tk.END, f"Subject: {subject}\n", "bold")

        for student, record in students.items():
            attended = record["attended"]
            total = record["total"]
            percentage = (attended / total * 100) if total > 0 else 0

            line = f"  {student}: {attended}/{total} ({percentage:.2f}%)\n"

            if percentage < 75:
                text_display.insert(tk.END, line, "low")
            else:
                text_display.insert(tk.END, line)

        text_display.insert(tk.END, "\n")

    text_display.tag_config("low", foreground="red")
    text_display.tag_config("bold", font=("Courier", 10, "bold"))
    text_display.config(state=tk.DISABLED)

# Run the main event loop
root.mainloop()

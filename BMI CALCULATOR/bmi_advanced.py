import tkinter as tk
from tkinter import messagebox
from datetime import datetime


FILE_NAME = "bmi_history.txt"


def calculate_bmi():
    name = name_entry.get().strip()

    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter numeric values.")
        return

    if weight <= 0 or height <= 0:
        messagebox.showerror("Invalid Input", "Weight and height must be positive.")
        return

    bmi = weight / (height ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    result_label.config(
        text=f"BMI: {bmi:.2f}\nCategory: {category}"
    )

    save_data(name, weight, height, bmi, category)
    load_history()


def save_data(name, weight, height, bmi, category):
    with open(FILE_NAME, "a") as file:
        file.write(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
            f"{name or 'Unknown'} | {weight}kg | {height}m | "
            f"BMI: {bmi:.2f} | {category}\n"
        )


def load_history():
    history_box.delete(0, tk.END)
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                history_box.insert(tk.END, line.strip())
    except FileNotFoundError:
        pass


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("520x520")
root.resizable(False, False)

tk.Label(root, text="Advanced BMI Calculator",
         font=("Arial", 18, "bold")).pack(pady=10)

# Input Frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
name_entry = tk.Entry(frame, width=25)
name_entry.grid(row=0, column=1)

tk.Label(frame, text="Weight (kg):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
weight_entry = tk.Entry(frame, width=25)
weight_entry.grid(row=1, column=1)

tk.Label(frame, text="Height (m):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
height_entry = tk.Entry(frame, width=25)
height_entry.grid(row=2, column=1)

tk.Button(root, text="Calculate BMI", width=20,
          command=calculate_bmi).pack(pady=10)

result_label = tk.Label(root, text="BMI: --\nCategory: --",
                        font=("Arial", 12))
result_label.pack(pady=10)

tk.Label(root, text="BMI History",
         font=("Arial", 12, "bold")).pack(pady=5)

history_box = tk.Listbox(root, width=75, height=10)
history_box.pack(pady=5)

load_history()

root.mainloop()

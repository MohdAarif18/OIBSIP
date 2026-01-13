import tkinter as tk
from tkinter import messagebox
import random
import string


def generate_password():
    length = length_var.get()

    use_lower = lower_var.get()
    use_upper = upper_var.get()
    use_digits = digits_var.get()
    use_symbols = symbols_var.get()
    exclude = exclude_var.get()

    if length < 8:
        messagebox.showwarning("Weak Password", "Password length should be at least 8.")
        return

    if not any([use_lower, use_upper, use_digits, use_symbols]):
        messagebox.showerror("Error", "Select at least one character type.")
        return

    password_chars = []
    pool = ""

    if use_lower:
        chars = [c for c in string.ascii_lowercase if c not in exclude]
        password_chars.append(random.choice(chars))
        pool += "".join(chars)

    if use_upper:
        chars = [c for c in string.ascii_uppercase if c not in exclude]
        password_chars.append(random.choice(chars))
        pool += "".join(chars)

    if use_digits:
        chars = [c for c in string.digits if c not in exclude]
        password_chars.append(random.choice(chars))
        pool += "".join(chars)

    if use_symbols:
        chars = [c for c in string.punctuation if c not in exclude]
        password_chars.append(random.choice(chars))
        pool += "".join(chars)

    if not pool:
        messagebox.showerror("Error", "All characters excluded!")
        return

    while len(password_chars) < length:
        password_chars.append(random.choice(pool))

    random.shuffle(password_chars)
    password = "".join(password_chars)

    password_var.set(password)
    update_strength(password)


def update_strength(password):
    length = len(password)
    categories = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(not c.isalnum() for c in password)
    ])

    if length >= 14 and categories >= 3:
        strength = "Strong"
    elif length >= 10 and categories >= 2:
        strength = "Medium"
    else:
        strength = "Weak"

    strength_label.config(text=f"Strength: {strength}")


def copy_password():
    pwd = password_var.get()
    if not pwd:
        messagebox.showinfo("Info", "Generate a password first.")
        return
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copied", "Password copied to clipboard.")


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("460x420")
root.resizable(False, False)

tk.Label(root, text="🔐 Password Generator",
         font=("Arial", 18, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame, text="Password Length:").grid(row=0, column=0, sticky="w")
length_var = tk.IntVar(value=12)
tk.Spinbox(frame, from_=8, to=64, textvariable=length_var, width=5)\
    .grid(row=0, column=1, sticky="w")

lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)

tk.Checkbutton(frame, text="Lowercase (a-z)", variable=lower_var)\
    .grid(row=1, column=0, columnspan=2, sticky="w")
tk.Checkbutton(frame, text="Uppercase (A-Z)", variable=upper_var)\
    .grid(row=2, column=0, columnspan=2, sticky="w")
tk.Checkbutton(frame, text="Digits (0-9)", variable=digits_var)\
    .grid(row=3, column=0, columnspan=2, sticky="w")
tk.Checkbutton(frame, text="Symbols (!@#$)", variable=symbols_var)\
    .grid(row=4, column=0, columnspan=2, sticky="w")

tk.Label(frame, text="Exclude characters:").grid(row=5, column=0, sticky="w")
exclude_var = tk.StringVar()
tk.Entry(frame, textvariable=exclude_var, width=25)\
    .grid(row=5, column=1, pady=5)

tk.Button(root, text="Generate Password", width=22,
          command=generate_password).pack(pady=10)

password_var = tk.StringVar()
tk.Entry(root, textvariable=password_var, font=("Arial", 12),
         width=40, justify="center").pack(pady=5)

tk.Button(root, text="Copy to Clipboard", width=20,
          command=copy_password).pack(pady=5)

strength_label = tk.Label(root, text="Strength: --",
                          font=("Arial", 11, "bold"))
strength_label.pack(pady=10)

root.mainloop()

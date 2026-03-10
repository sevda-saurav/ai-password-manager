import customtkinter as ctk
from encryption import encrypt_password, decrypt_password
from db import add_password, get_passwords, delete_password
from generator import generate_password
from ai_strength import password_strength
import pyperclip

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("AI Password Manager")
app.geometry("600x720")


# ---------------- INPUT FIELDS ---------------- #

account_entry = ctk.CTkEntry(app, placeholder_text="Account")
account_entry.pack(pady=10)

password_entry = ctk.CTkEntry(app, placeholder_text="Password")
password_entry.pack(pady=10)

strength_label = ctk.CTkLabel(app, text="")
strength_label.pack()

message_label = ctk.CTkLabel(app, text="", text_color="red")
message_label.pack(pady=5)


# ---------------- PASSWORD VAULT FRAME ---------------- #

accounts_frame = ctk.CTkScrollableFrame(app, height=180)
accounts_frame.pack(pady=20, padx=10, fill="x")

# ---------------- TEXTBOX DISPLAY ---------------- #

display_box = ctk.CTkTextbox(app, width=500, height=80)
display_box.pack(pady=10)


# ---------------- FUNCTIONS ---------------- #

def check_strength():

    pwd = password_entry.get().strip()

    if pwd == "":
        message_label.configure(text="Enter a password to check strength")
        return

    result = password_strength(pwd)
    strength_label.configure(text=f"Strength: {result}")


def generate():

    pwd = generate_password()

    password_entry.delete(0, "end")
    password_entry.insert(0, pwd)


def save():

    acc = account_entry.get().strip()
    pwd = password_entry.get().strip()

    if acc == "" or pwd == "":
        message_label.configure(text="Account and Password required", text_color="red")
        return

    enc = encrypt_password(pwd)
    add_password(acc, enc)

    message_label.configure(text="Password saved", text_color="green")

    account_entry.delete(0, "end")
    password_entry.delete(0, "end")

    load_accounts()


def view():

    display_box.delete("1.0", "end")

    data = get_passwords()

    if len(data) == 0:
        display_box.insert("end", "No saved passwords\n")
        return

    for row in data:

        acc = row[1]
        pwd = decrypt_password(row[2])

        display_box.insert("end", f"{acc} : {pwd}\n")


def load_accounts():

    # Clear existing widgets
    for widget in accounts_frame.winfo_children():
        widget.destroy()

    data = get_passwords()

    if len(data) == 0:

        empty_label = ctk.CTkLabel(
            accounts_frame,
            text="No saved passwords yet",
            text_color="gray"
        )

        empty_label.pack(pady=20)
        return

    for row in data:

        account = row[1]
        password = decrypt_password(row[2])

        row_frame = ctk.CTkFrame(accounts_frame)
        row_frame.pack(fill="x", pady=5, padx=10)

        masked = "*" * len(password)

        account_label = ctk.CTkLabel(
            row_frame,
            text=f"{account} : {masked}",
            width=300,
            anchor="w"
        )

        account_label.pack(side="left", padx=10)

        delete_btn = ctk.CTkButton(
            row_frame,
            text="Delete",
            width=80,
            fg_color="red",
            command=lambda acc=account: delete_account(acc)
        )

        delete_btn.pack(side="right", padx=10)


def delete_account(account):

    result = delete_password(account)

    if result:
        message_label.configure(text=f"{account} deleted", text_color="green")
    else:
        message_label.configure(text="Account not found", text_color="red")

    load_accounts()


def copy():

    pwd = password_entry.get()

    if pwd == "":
        message_label.configure(text="No password to copy", text_color="red")
        return

    pyperclip.copy(pwd)

    message_label.configure(text="Password copied to clipboard", text_color="green")


# ---------------- BUTTONS ---------------- #

ctk.CTkButton(app, text="Check Strength", command=check_strength).pack(pady=5)

ctk.CTkButton(app, text="Generate Password", command=generate).pack(pady=5)

ctk.CTkButton(app, text="Save Password", command=save).pack(pady=5)

ctk.CTkButton(app, text="View Passwords", command=view).pack(pady=5)

ctk.CTkButton(app, text="Copy Password", command=copy).pack(pady=5)


# ---------------- START APP ---------------- #

load_accounts()

app.mainloop()
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_contacts():
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

def add_contact():
    name = simpledialog.askstring("Add Contact", "Enter Name:")
    if not name:
        return
    if name in contacts:
        messagebox.showwarning("Error", "Contact already exists!")
        return
    phone = simpledialog.askstring("Phone Number", f"Enter phone for {name}:")
    email = simpledialog.askstring("Email Address", f"Enter email for {name}:")
    contacts[name] = {"phone": phone, "email": email}
    save_contacts()
    refresh_list()

def edit_contact():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Error", "Select a contact to edit")
        return
    name = listbox.get(selection[0])
    phone = simpledialog.askstring("Edit Phone", f"Enter new phone for {name}:", initialvalue=contacts[name]["phone"])
    email = simpledialog.askstring("Edit Email", f"Enter new email for {name}:", initialvalue=contacts[name]["email"])
    contacts[name] = {"phone": phone, "email": email}
    save_contacts()
    refresh_list()

def delete_contact():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Error", "Select a contact to delete")
        return
    name = listbox.get(selection[0])
    if messagebox.askyesno("Delete", f"Are you sure you want to delete {name}?"):
        del contacts[name]
        save_contacts()
        refresh_list()

def show_details(event):
    selection = listbox.curselection()
    if selection:
        name = listbox.get(selection[0])
        contact = contacts[name]
        details.set(f"Name: {name}\nPhone: {contact['phone']}\nEmail: {contact['email']}")

def refresh_list():
    listbox.delete(0, tk.END)
    for name in sorted(contacts.keys()):
        listbox.insert(tk.END, name)
    details.set("")

# Initialize GUI
root = tk.Tk()
root.title("Contact Manager")

contacts = load_contacts()

# Layout
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

listbox = tk.Listbox(frame, height=10, width=30)
listbox.grid(row=0, column=0, rowspan=6, padx=5, pady=5)
listbox.bind("<<ListboxSelect>>", show_details)

details = tk.StringVar()
label = tk.Label(frame, textvariable=details, justify="left", anchor="w")
label.grid(row=0, column=1, sticky="nw", padx=10)

tk.Button(frame, text="Add", width=12, command=add_contact).grid(row=1, column=1, sticky="w")
tk.Button(frame, text="Edit", width=12, command=edit_contact).grid(row=2, column=1, sticky="w")
tk.Button(frame, text="Delete", width=12, command=delete_contact).grid(row=3, column=1, sticky="w")
tk.Button(frame, text="Exit", width=12, command=root.quit).grid(row=4, column=1, sticky="w")

refresh_list()
root.mainloop()
import tkinter as tk
import sqlite3


#Importib messageboxide andmed
from tkinter import messagebox

#Funktsioonid
def insert_data():
    if validate_data():
        connection = sqlite3.connect("kkold.db")
        cursor = connection.cursor()
        
        cursor.execute("""
            INSERT into users(first_name, last_name, email, phone, image)
            VALUES (?, ?, ?, ?, ?)
        """, (
            entries["Eesnimi"].get(),
            entries["Perekonnanimi"].get(),
            entries["Email"].get(),
            entries["Telefon"].get(),
            entries["Pilt"].get(),
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo("Edu", "Andmed sisestati edukalt!")
# validate_data funktsioon, mis kontrollib kas sisestatud andmed on korrektsed
def validate_data():
    enimi = entries["Eesnimi"].get()
    pnimi = entries["Perekonnanimi"].get()
    email = entries["Email"].get()
    telefon = entries["Telefon"].get()
    pilt = entries["Pilt"].get()
    if not enimi:
        tk.messagebox.showerror("Viga", "Eesnimi on kohustuslik!")
        return False
    if not pnimi:
        tk.messagebox.showerror("Viga", "Perekonnanimi on kohustuslik!")
        return False
    if not email:
        tk.messagebox.showerror("Viga", "Email on kohustuslik!")
        return False 
    if not telefon:
        tk.messagebox.showerror("Viga", "Telefon on kohustuslik!")
        return False
    if not pilt:
        tk.messagebox.showerror("Viga", "Pilt on kohustuslik!")
        return False
    # tk.messagebox.showinfo("Tehtud", "Andmed on salvestatud!")
    return True



# Loo Tkinteri aken
root = tk.Tk()
root.title("Kasutaja lisamine")

# Loo sildid ja sisestusväljad
labels = ["Eesnimi", "Perekonnanimi", "Email", "Telefon", "Pilt"]
entries = {}

for i, label in enumerate(labels):
    tk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5)
    entry = tk.Entry(root, width=40)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[label] = entry

# Loo nupp andmete sisestamiseks
submit_button = tk.Button(root, text="Sisesta kasutaja", command=insert_data)
submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

# Näita Tkinteri akent
root.mainloop()
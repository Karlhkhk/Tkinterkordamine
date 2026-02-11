import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess


#Funktsioon, mis laadib andmed SQLite andmebaasist ja sisestab need Treeview tabelisse
def load_data_from_db(tree):
    # Loo ühendus SQLite andmebaasiga
    conn = sqlite3.connect('kkold.db')
    cursor = conn.cursor()

    # Tee päring andmebaasist andmete toomiseks
    cursor.execute("SELECT first_name, last_name, email, phone, image FROM users")
    rows = cursor.fetchall()

    # Lisa andmed tabelisse
    for row in rows:
        tree.insert("", "end", values=row)

    # Sulge ühendus andmebaasiga
    conn.close()

root = tk.Tk()
root.title("Kasutajad")


# Loo raam kerimisribaga
frame = tk.Frame(root)
frame.pack(pady=20, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# Loo tabel (Treeview) andmete kuvamiseks
tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, columns=("Eesnimi", "Perekonnanimi", "Email", "Telefon", "Pilt"), show="headings")
tree.pack(fill=tk.BOTH, expand=True)
#Otsingufunktsioon
def on_search():
    search_query = search_entry.get()
    load_data_from_db(tree, search_query)

# Loo otsinguväli ja nupp
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Otsi kasutajat:")
search_label.pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=10)

search_button = tk.Button(search_frame, text="Otsi", command=on_search)
search_button.pack(side=tk.LEFT)
# Avab lisamise faili
def add_data():
    subprocess.run(["python", "lisa_kasutaja.py"])


    
#Funktsioon, mis laadib andmed SQLite andmebaasist ja sisestab need Treeview tabelisse
def load_data_from_db(tree, search_query=""):
    # Puhasta Treeview tabel enne uute andmete lisamist
    for item in tree.get_children():
        tree.delete(item)

    # Loo ühendus SQLite andmebaasiga
    conn = sqlite3.connect('kkold.db')
    cursor = conn.cursor()

    # Tee päring andmebaasist andmete toomiseks
    if search_query:
        cursor.execute("SELECT id, first_name, last_name, email, phone, image FROM users WHERE first_name LIKE ?", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT id, first_name, last_name, email, phone, image FROM users")

    rows = cursor.fetchall()

    # Lisa andmed tabelisse
    for row in rows:
        tree.insert("", "end", values=row[1:], iid=row[0])  # iid määratakse ID-ks

    # Sulge ühendus andmebaasiga
    conn.close()

# Seosta kerimisriba tabeliga
scrollbar.config(command=tree.yview)


# 2. Määra veergude pealkirjad (mis on kasutajale näha)
tree.heading("Eesnimi", text="Eesnimi")
tree.heading("Perekonnanimi", text="Perekonnanimi")
tree.heading("Email", text="Email")
tree.heading("Telefon", text="Telefon")
tree.heading("Pilt", text="Pildid")

# 3. Määra veergude laius
tree.column("Eesnimi", width=100)
tree.column("Perekonnanimi", width=120)
tree.column("Email", width=150)
tree.column("Telefon", width=100)
tree.column("Pilt", width=150)

tree.pack(pady=20)

# Lisa andmed tabelisse
load_data_from_db(tree)


# Käivita Tkinteri tsükkel
root.mainloop()
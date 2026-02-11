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
# Loo nupp, mis avab teise akna
open_button = tk.Button(root, text="Lisa andmeid", command=add_data)
open_button.pack(pady=20)

# Funktsioon, mis näitab valitud rea ID-d
def on_update():
    selected_item = tree.selection()  # Võta valitud rida
    if selected_item:
        record_id = selected_item[0]  # iid (ID)
        print(f"Valitud ID: {record_id}")
    else:
        print("Vali kõigepealt rida!")
    # Funktsioon, mis avab uue akna andmete muutmiseks
def open_update_window(record_id):
    # Loo uus aken
    update_window = tk.Toplevel(root)
    update_window.title("Muuda kasutaja andmeid")

    # Loo andmebaasi ühendus ja toomine olemasolevad andmed
    conn = sqlite3.connect('kkold.db')
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, email, phone, image FROM users WHERE id=?", (record_id,))
    record = cursor.fetchone()
    conn.close()

    # Veergude nimed ja vastavad sisestusväljad
    labels = ["Eesnimi", "Perekonnanimi", "Email", "Telefon", "Pilt"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(update_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        entry = tk.Entry(update_window, width=50)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, record[i])
        entries[label] = entry

    # Salvestamise nupp
    save_button = tk.Button(update_window, text="Salvesta", command=lambda: update_record(record_id, entries, update_window))
    save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)
    # Funktsioon, mis näitab valitud rea ID-d ja avab muutmise vormi
def on_update():
    selected_item = tree.selection()  # Võta valitud rida
    if selected_item:
        record_id = selected_item[0]  # iid (ID)
        open_update_window(record_id)
    else:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")
        # Funktsioon, mis avab uue akna andmete muutmiseks
def open_update_window(record_id):
    # Loo uus aken
    update_window = tk.Toplevel(root)
    update_window.title("Muuda kasutaja andmeid")
    # Funktsioon, mis uuendab andmed andmebaasis
def update_record(record_id, entries, window):
   # Koguge andmed sisestusväljadest
    first_name = entries["Eesnimi"].get()
    last_name = entries["Perekonnanimi"].get()
    email = entries["Email"].get()
    phone = entries["Telefon"].get()
    image = entries["Pilt"].get()

    # Andmete uuendamine andmebaasis
    conn = sqlite3.connect('kkold.db')
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users
    SET first_name=?, last_name=?, email=?, phone=?, image=?
    WHERE id=?
    """, (first_name, last_name, email, phone, image, record_id))
    conn.commit()
    conn.close()

    # Värskenda Treeview tabelit
    load_data_from_db(tree)

    # Sulge muutmise aken
    window.destroy()

    messagebox.showinfo("Salvestamine", "Andmed on edukalt uuendatud!")

# Lisa Uuenda nupp, mis näitab selekteeritud rea ID-d
update_button = tk.Button(root, text="Uuenda", command=on_update)
update_button.pack(pady=10)



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
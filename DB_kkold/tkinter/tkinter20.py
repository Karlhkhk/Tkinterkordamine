import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess

# --- FUNKTSIOONID ---

def load_data_from_db(tree, search_query=""):
    for item in tree.get_children():
        tree.delete(item)
    conn = sqlite3.connect('kkold.db')
    cursor = conn.cursor()
    if search_query:
        cursor.execute("SELECT id, first_name, last_name, email, phone, image FROM users WHERE first_name LIKE ?", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT id, first_name, last_name, email, phone, image FROM users")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row[1:], iid=row[0])
    conn.close()

def on_search():
    search_query = search_entry.get()
    load_data_from_db(tree, search_query)

def add_data():
    subprocess.run(["python", "lisa_kasutaja.py"])

def update_record(record_id, entries, window):
    new_values = (
        entries["Eesnimi"].get(),
        entries["Perekonnanimi"].get(),
        entries["Email"].get(),
        entries["Telefon"].get(),
        entries["Pilt"].get(),
        record_id
    )

    conn = sqlite3.connect('kkold.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users 
        SET first_name=?, last_name=?, email=?, phone=?, image=? 
        WHERE id=?
    """, new_values)
    conn.commit()
    conn.close()

    load_data_from_db(tree) 
    window.destroy()        
    messagebox.showinfo("Edu", "Andmed on edukalt uuendatud!")

def open_update_window(record_id):
    update_window = tk.Toplevel(root)
    update_window.title("Muuda andmeid")

    conn = sqlite3.connect('kkold.db')
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, email, phone, image FROM users WHERE id=?", (record_id,))
    record = cursor.fetchone()
    conn.close()

    labels = ["Eesnimi", "Perekonnanimi", "Email", "Telefon", "Pilt"]
    entries = {}

    for i, label_text in enumerate(labels):
        tk.Label(update_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(update_window, width=40)
        entry.grid(row=i, column=1, padx=10, pady=5)
        if record[i] is not None:
            entry.insert(0, record[i])
        entries[label_text] = entry

    save_button = tk.Button(update_window, text="Salvesta", 
                            command=lambda: update_record(record_id, entries, update_window))
    save_button.grid(row=len(labels), columnspan=2, pady=10)

def on_update():
    selected_item = tree.selection()
    if selected_item:
        record_id = selected_item[0]
        open_update_window(record_id)
    else:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")

def on_delete():
    selected_item = tree.selection()
    if selected_item:
        record_id = selected_item[0]
        confirm = messagebox.askyesno("Kinnita kustutamine", "Kas oled kindel, et soovid selle rea kustutada?")
        if confirm:
            try:
                conn = sqlite3.connect('kkold.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id=?", (record_id,))
                conn.commit()
                conn.close()
                load_data_from_db(tree)
                messagebox.showinfo("Edukalt kustutatud", "Rida on edukalt kustutatud!")
            except sqlite3.Error as e:
                messagebox.showerror("Viga", f"Andmebaasi viga: {e}")
    else:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")


root = tk.Tk()
root.title("Kasutajad")

frame = tk.Frame(root)
frame.pack(pady=20, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, columns=("Eesnimi", "Perekonnanimi", "Email", "Telefon", "Pilt"), show="headings")
tree.pack(fill=tk.BOTH, expand=True)

scrollbar.config(command=tree.yview)

# Otsingu osa
search_frame = tk.Frame(root)
search_frame.pack(pady=10)
tk.Label(search_frame, text="Otsi kasutajat:").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=10)
tk.Button(search_frame, text="Otsi", command=on_search).pack(side=tk.LEFT)

# Nuppude osa 
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Lisa andmeid", command=add_data)
add_button.pack(side=tk.LEFT, padx=5)

update_button = tk.Button(button_frame, text="Uuenda valitut", command=on_update)
update_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="Kustuta", command=on_delete)
delete_button.pack(side=tk.LEFT, padx=5)


tree.heading("Eesnimi", text="Eesnimi")
tree.heading("Perekonnanimi", text="Perekonnanimi")
tree.heading("Email", text="Email")
tree.heading("Telefon", text="Telefon")
tree.heading("Pilt", text="Pildid")

tree.column("Eesnimi", width=100)
tree.column("Perekonnanimi", width=120)
tree.column("Email", width=150)
tree.column("Telefon", width=100)
tree.column("Pilt", width=150)

load_data_from_db(tree)

root.mainloop()
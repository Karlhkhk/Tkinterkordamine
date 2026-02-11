import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title("Filmid")


# Loo raam kerimisribaga
frame = tk.Frame(root)
frame.pack(pady=20, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# Loo tabel (Treeview) andmete kuvamiseks
tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, columns=("title", "director", "year", "genre", "duration", "rating", "language", "country", "description"), show="headings")
tree.pack(fill=tk.BOTH, expand=True)


# Seosta kerimisriba tabeliga
scrollbar.config(command=tree.yview)


# Määra veergude pealkirjad ja laius
tree.heading("title", text="Pealkiri")
tree.heading("director", text="Režissöör")
tree.heading("year", text="Aasta")
tree.heading("genre", text="Žanr")
tree.heading("duration", text="Kestus")
tree.heading("rating", text="Reiting")
tree.heading("language", text="Keel")
tree.heading("country", text="Riik")
tree.heading("description", text="Kirjeldus")

tree.column("title", width=150)
tree.column("director", width=100)
tree.column("year", width=60)
tree.column("genre", width=100)
tree.column("duration", width=60)
tree.column("rating", width=60)
tree.column("language", width=80)
tree.column("country", width=80)
tree.column("description", width=200)

# Lisa andmed tabelisse
tree.insert("", "end", values=("The Shawshank Redemption", "Frank Darabont", 1994, "Drama", 142, 9.3, "English", "USA", "Two imprisoned men bond over a number of years."))
tree.insert("", "end", values=("The Godfather", "Francis Ford Coppola", 1972, "Crime, Drama", 175, 9.2, "English", "USA", "The aging patriarch of an organized crime dynasty transfers control of his empire to his reluctant son."))
tree.insert("", "end", values=("The Dark Knight", "Christopher Nolan", 2008, "Action, Crime, Drama", 152, 9.0, "English", "USA", "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham."))


# Käivita Tkinteri tsükkel
root.mainloop()
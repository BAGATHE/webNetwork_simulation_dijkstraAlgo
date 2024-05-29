import tkinter as tk
from tkinter import ttk

# Création de la fenêtre principale
root = tk.Tk()
root.title("Tableau avec Tkinter")

# Création du tableau
tree = ttk.Treeview(root, columns=("col1", "col2", "col3"), show="headings")
tree.heading("col1", text="Colonne 1")
tree.heading("col2", text="Colonne 2")
tree.heading("col3", text="Colonne 3")

# Ajout de données au tableau
data = [
    ("Donnée 1", "Donnée 2", "Donnée 3"),
    ("Donnée 4", "Donnée 5", "Donnée 6"),
    ("Donnée 7", "Donnée 8", "Donnée 9")
]

for item in data:
    tree.insert("", "end", values=item)

# Affichage du tableau
tree.pack(expand=True, fill="both")

# Lancement de la boucle principale
root.mainloop()

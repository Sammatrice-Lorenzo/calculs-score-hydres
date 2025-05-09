import os
import tkinter as tk
from score_builder import ScoreBuilder
from tkinter import filedialog, messagebox


FONT = 'Arial'
BACKGROUND_COLOR = '#f4f4f4'


def choose_file():
    file: str = filedialog.askopenfilename(
        filetypes=[("Fichiers Excel", "*.xlsx *.xls")]
    )

    if file:
        entry_file.insert(0, file)
        entry_file_var.set(file)


def start():
    file: str = entry_file.get()
    rows: str = entry_rows.get()

    if not os.path.exists(file):
        messagebox.showerror("Erreur", "Fichier non trouvé.")
        return

    try:
        rows = int(rows)
    except ValueError:
        messagebox.showerror("Erreur", "Nombre de lignes invalide.")
        return

    try:
        score_builder = ScoreBuilder()
        score_builder.calculate(file, rows)
        messagebox.showinfo(
            "Succès",
            """Traitement terminé avec succès.
            Le fichier a été placé au même endroit que le fichier inséré"""
        )
    except Exception as e:
        messagebox.showerror("Erreur", str(e))


app = tk.Tk()
app.title("Calculateur de score")
app.geometry("500x250")
app.configure(bg=BACKGROUND_COLOR)

label_style = {
    "bg": BACKGROUND_COLOR,
    "fg": "#333",
    "font": (FONT, 10, "bold")
}
entry_style = {"font": (FONT, 10)}
button_style = {"font": (FONT, 10, "bold"), "padx": 10, "pady": 5}

tk.Label(app, text="Fichier Excel :", **label_style).pack(pady=(10, 0))
frame_file = tk.Frame(app, bg=BACKGROUND_COLOR)
frame_file.pack(pady=5)

entry_file_var = tk.StringVar()
entry_file = tk.Entry(
    frame_file,
    textvariable=entry_file_var,
    width=50,
    state="readonly",
    **entry_style
)
entry_file.pack(side=tk.LEFT, padx=(0, 10))

tk.Button(
    frame_file,
    text="Parcourir",
    command=choose_file,
    bg='#48c78e',
    fg='white',
    **button_style
).pack(side=tk.LEFT)

tk.Label(
    app,
    text="Nombre total des lignes du tableau :",
    **label_style
).pack(pady=(15, 0))
entry_rows = tk.Entry(app, **entry_style)
entry_rows.pack(pady=5)

tk.Button(
    app,
    text="Lancer le traitement",
    command=start,
    bg="#3273dc",
    fg="white",
    **button_style
).pack(pady=20)

app.mainloop()

import tkinter as tk
from tkinter import filedialog
import os


def seleccionar_imagen():

    try:

        root = tk.Tk()
        root.withdraw()

        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imagenes", "*.png *.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("JPG", "*.jpg"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not ruta:
            raise Exception("No se seleccionó ningún archivo")

        if not os.path.exists(ruta):
            raise FileNotFoundError("El archivo no existe")

        return ruta

    except Exception as e:

        print("❌ Error al seleccionar imagen:", e)
        return None
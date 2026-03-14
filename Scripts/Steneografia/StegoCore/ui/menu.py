from .extractor import ejecutar_extraccion
import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image

from core.encoder import ocultar_mensaje, texto_a_binario
from core.decoder import extraer_mensaje
from core.file_encoder import ocultar_archivo_en_imagen
from core.file_decoder import extraer_archivo

# UI CENTRAL
from .ui_central import (
    pausa,
    limpiar,
    banner,
    boot_stegocore,
    mostrar_banner,
    menu_visual,
)


# ==========================================
# SELECTOR DE IMAGEN
# ==========================================

def seleccionar_imagen():

    ventana = tk.Tk()
    ventana.withdraw()

    ruta = filedialog.askopenfilename(
        title="Selecciona una imagen PNG",
        filetypes=[
            ("Imagen PNG", "*.png"),
            ("Todos los archivos", "*.*")
        ]
    )

    return ruta


# ==========================================
# SELECTOR DE ARCHIVO
# ==========================================

def seleccionar_archivo():

    ventana = tk.Tk()
    ventana.withdraw()

    ruta = filedialog.askopenfilename(
        title="Selecciona archivo para ocultar",
        filetypes=[("Todos los archivos", "*.*")]
    )

    return ruta


# ==========================================
# SELECTOR DE CARPETA DESTINO
# ==========================================

def seleccionar_guardado():

    ventana = tk.Tk()
    ventana.withdraw()

    ruta = filedialog.askdirectory(
        title="Selecciona carpeta donde guardar archivo extraído"
    )

    return ruta


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

def menu():

    imagen_cargada = None
    texto_secreto = None

    limpiar()
    banner()
    boot_stegocore()
    mostrar_banner()    

    while True:

        menu_visual(imagen_cargada, texto_secreto)

        opcion = input("\nSelecciona opción → ")

        # ============================
        # CARGAR IMAGEN
        # ============================

        if opcion == "1":

            ruta = seleccionar_imagen()

            try:

                if not ruta:
                    raise Exception("Operación cancelada")

                if not os.path.exists(ruta):
                    raise FileNotFoundError("La ruta no existe")

                if not ruta.lower().endswith(".png"):
                    raise ValueError("Solo se permiten imágenes PNG")

                imagen_cargada = ruta

                img = Image.open(ruta)
                ancho, alto = img.size

                capacidad_bits = ancho * alto * 3
                capacidad_bytes = capacidad_bits // 8

                print("\n✅ Imagen cargada correctamente")
                print(f"Archivo: {os.path.basename(ruta)}")
                print(f"Resolución: {ancho} x {alto}")
                print(f"Capacidad máxima: {capacidad_bytes/1024/1024:.2f} MB\n")

                pausa()

            except Exception as e:

                print("❌ Error al cargar imagen:", e)
                pausa()

        # ============================
        # ESCRIBIR MENSAJE
        # ============================

        elif opcion == "2":

            try:

                texto = input("Escribe el mensaje secreto: ").strip()

                if len(texto) == 0:
                    raise ValueError("El mensaje está vacío")

                texto_secreto = texto

                print("✅ Mensaje almacenado correctamente")
                pausa()

            except Exception as e:

                print("❌ Error:", e)
                pausa()

        # ============================
        # OCULTAR MENSAJE
        # ============================

        elif opcion == "3":

            try:

                if imagen_cargada is None:
                    raise Exception("Primero debes cargar una imagen")

                if texto_secreto is None:
                    raise Exception("Primero debes escribir un mensaje")

                confirmacion = input("¿Seguro que deseas ocultar el mensaje? (s/n): ")

                if confirmacion.strip().lower() != "s":
                    print("Operación cancelada")
                    pausa()
                    continue

                binario = texto_a_binario(texto_secreto)

                resultado = ocultar_mensaje(imagen_cargada, binario)

                if resultado:
                    print("✅ Mensaje ocultado correctamente")
                else:
                    print("❌ No se pudo ocultar el mensaje")

                pausa()

            except Exception as e:

                print("❌ Error durante el proceso:", e)
                pausa()

        # ============================
        # EXTRAER MENSAJE
        # ============================

        elif opcion == "4":

            ejecutar_extraccion()
            pausa()

        # ============================
        # OCULTAR ARCHIVO
        # ============================

        elif opcion == "5":

            try:

                if imagen_cargada is None:
                    raise Exception("Primero debes cargar una imagen PNG")

                archivo = seleccionar_archivo()

                if not archivo:
                    raise Exception("Operación cancelada")

                confirmacion = input("¿Ocultar este archivo en la imagen? (s/n): ")

                if confirmacion.lower() != "s":
                    print("Operación cancelada")
                    pausa()
                    continue

                resultado = ocultar_archivo_en_imagen(imagen_cargada, archivo)

                if resultado:
                    print("✅ Archivo ocultado correctamente")
                else:
                    print("❌ No se pudo ocultar el archivo")

                pausa()

            except Exception as e:

                print("❌ Error al ocultar archivo:", e)
                pausa()

        # ============================
        # EXTRAER ARCHIVO
        # ============================

        elif opcion == "6":

            try:

                imagen = seleccionar_imagen()

                if not imagen:
                    raise Exception("Operación cancelada")

                carpeta = seleccionar_guardado()

                if not carpeta:
                    raise Exception("No se seleccionó carpeta destino")

                extraer_archivo(imagen, carpeta)
                pausa()

            except Exception as e:

                print("❌ Error al extraer archivo:", e)
                pausa()

        # ============================
        # SALIR
        # ============================

        elif opcion == "7":

            print("Saliendo del sistema...")
            break

        else:

            print("❌ Opción inválida")
            pausa()
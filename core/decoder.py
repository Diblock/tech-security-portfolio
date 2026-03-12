from PIL import Image
import numpy as np
import sys


# ==========================================
# BARRA DE PROGRESO
# ==========================================

from .progress import barra_progreso   



# ==========================================
# EXTRAER MENSAJE
# ==========================================

def extraer_mensaje(ruta_imagen):

    try:

        img = Image.open(ruta_imagen).convert("RGB")
        pixeles = np.array(img)

        alto = pixeles.shape[0]
        ancho = pixeles.shape[1]

        total_pixeles = alto * ancho

        print("\nImagen cargada correctamente")
        print(f"Resolución: {ancho} x {alto}")
        print(f"Total de píxeles: {total_pixeles}\n")

        print("Iniciando análisis de bits ocultos...\n")

        bits = ""
        contador = 0
        mensaje = ""

        for y in range(alto):

            for x in range(ancho):

                pixel = pixeles[y][x]

                for color in pixel:

                    bits += str(color & 1)

                    if len(bits) == 8:

                        byte = bits
                        bits = ""

                        caracter = chr(int(byte, 2))
                        mensaje += caracter

                        # DETECCIÓN DE FINAL DE MENSAJE
                        if mensaje.endswith("#####END#####"):

                            mensaje = mensaje.replace("#####END#####", "")

                            barra_progreso(total_pixeles, total_pixeles)

                            print("\n\nMensaje encontrado antes de analizar toda la imagen.")
                            return mensaje

                contador += 1
                barra_progreso(contador, total_pixeles)

        print("\n")

        return mensaje

    except Exception as e:

        print("Error al extraer mensaje:", e)
        return None
import sys
import time
from PIL import Image
import numpy as np


# ==========================================
# BARRA DE PROGRESO VISUAL
# ==========================================

from .progress import barra_progreso

# ==========================================
# TEXTO A BINARIO
# ==========================================
def texto_a_binario(texto):

    texto += "#####END#####"

    mensaje_binario = ''.join(format(ord(letra), '08b') for letra in texto)

    return mensaje_binario


# ==========================================
# OCULTAR MENSAJE EN IMAGEN
# ==========================================
def ocultar_mensaje(ruta_imagen_original, mensaje_binario):

    try:

        mostrar_banner()

        img = Image.open(ruta_imagen_original).convert('RGB')
        pixeles = np.array(img)

        capacidad_maxima = pixeles.shape[0] * pixeles.shape[1] * 3
        capacidad_texto = capacidad_maxima // 8

        print(f"Imagen cargada: {ruta_imagen_original}")
        print(f"Capacidad máxima aproximada: {capacidad_texto} caracteres\n")

        if len(mensaje_binario) > capacidad_maxima:

            print("❌ Imagen demasiado pequeña para el mensaje")
            return False

        indice_bit = 0
        longitud_mensaje = len(mensaje_binario)

        print("Iniciando proceso de esteganografía...\n")

        for y in range(pixeles.shape[0]):

            for x in range(pixeles.shape[1]):

                r, g, b = pixeles[y, x]

                if indice_bit < longitud_mensaje:

                    r_bin = f"{r:08b}"[:-1] + mensaje_binario[indice_bit]
                    pixeles[y, x][0] = int(r_bin, 2)
                    indice_bit += 1

                if indice_bit < longitud_mensaje:

                    g_bin = f"{g:08b}"[:-1] + mensaje_binario[indice_bit]
                    pixeles[y, x][1] = int(g_bin, 2)
                    indice_bit += 1

                if indice_bit < longitud_mensaje:

                    b_bin = f"{b:08b}"[:-1] + mensaje_binario[indice_bit]
                    pixeles[y, x][2] = int(b_bin, 2)
                    indice_bit += 1

                if indice_bit <= longitud_mensaje:

                    barra_progreso(indice_bit, longitud_mensaje)
                    time.sleep(0.0002)

                if indice_bit >= longitud_mensaje:
                    break

            if indice_bit >= longitud_mensaje:
                break

        print("\n\n✔ Payload inyectado correctamente")
        print("✔ Imagen esteganográfica generada")

        nueva_img = Image.fromarray(pixeles)
        nueva_img.save("output/imagen_secreta.png")

        print("\n📁 Archivo generado:")
        print("output/imagen_secreta.png\n")

        return True

    except FileNotFoundError:

        print("❌ No se encontró la imagen especificada")
        return False

    except Exception as e:

        print("❌ Error inesperado:", e)
        return False
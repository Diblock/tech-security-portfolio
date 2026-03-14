from PIL import Image
import numpy as np
from ui.ui_central import mostrar_banner
from .progress import barra_progreso


def texto_a_binario(texto):
    texto += "#####END#####"
    return ''.join(format(ord(letra), '08b') for letra in texto)


def ocultar_mensaje(ruta_imagen_original, mensaje_binario):

    try:
        img = Image.open(ruta_imagen_original).convert('RGB')
        pixeles = np.array(img)

        capacidad_maxima = pixeles.shape[0] * pixeles.shape[1] * 3

        if len(mensaje_binario) > capacidad_maxima:
            print("❌ Imagen demasiado pequeña para el mensaje")
            return False

        indice_bit = 0
        longitud_mensaje = len(mensaje_binario)

        print("\nIniciando proceso de esteganografía...\n")

        for y in range(pixeles.shape[0]):
            for x in range(pixeles.shape[1]):
                for canal in range(3):
                    if indice_bit < longitud_mensaje:
                        pixeles[y, x, canal] = (
                            int(pixeles[y, x, canal]) & 0xFE
                        ) | int(mensaje_binario[indice_bit])

                        indice_bit += 1
                        barra_progreso(indice_bit, longitud_mensaje)

                if indice_bit >= longitud_mensaje:
                    break

            if indice_bit >= longitud_mensaje:
                break

        nueva_img = Image.fromarray(pixeles)
        nueva_img.save("output/imagen_secreta.png")

        print("\n\n✔ Payload inyectado correctamente")
        print("✔ Imagen guardada en output/imagen_secreta.png")

        return True

    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
from PIL import Image
import numpy as np
import os

from .progress import barra_progreso


def ocultar_archivo_en_imagen(imagen, archivo, salida="output/imagen_payload.png"):

    try:

        if not imagen.lower().endswith(".png"):
            raise Exception("Solo se permiten imágenes PNG")

        img = Image.open(imagen).convert("RGB")
        pixeles = np.array(img)

        alto = pixeles.shape[0]
        ancho = pixeles.shape[1]
        total_pixeles = alto * ancho

        print("\nImagen cargada correctamente")
        print(f"Resolución: {ancho} x {alto}")
        print(f"Total de píxeles: {total_pixeles}\n")

        with open(archivo, "rb") as f:
            datos = f.read()

        extension = os.path.splitext(archivo)[1].replace(".", "")
        ext_bytes = extension.encode()

        tamaño = len(datos)

        header = (
            b"STEG"
            + len(ext_bytes).to_bytes(1, "big")
            + ext_bytes
            + tamaño.to_bytes(4, "big")
        )

        payload = header + datos
        bits = "".join(format(b, "08b") for b in payload)

        capacidad_bits = alto * ancho * 3
        capacidad_bytes = capacidad_bits // 8

        print(f"Capacidad imagen: {capacidad_bytes / 1024:.2f} KB")
        print(f"Tamaño archivo: {len(payload) / 1024:.2f} KB\n")

        if len(bits) > capacidad_bits:
            raise Exception("La imagen no tiene capacidad suficiente")

        print("Inyectando archivo en la imagen...\n")

        indice = 0
        total_bits = len(bits)

        for y in range(alto):
            for x in range(ancho):
                for canal in range(3):
                    if indice < total_bits:
                        pixeles[y][x][canal] = (
                            int(pixeles[y][x][canal]) & 0xFE
                        ) | int(bits[indice])

                        indice += 1
                        barra_progreso(indice, total_bits)

                if indice >= total_bits:
                    break

            if indice >= total_bits:
                break

        nueva = Image.fromarray(pixeles)
        nueva.save(salida)

        print("\n\n✔ Archivo ocultado correctamente")
        print("Imagen generada:", salida)

        return True

    except Exception as e:
        print("\n❌ Error:", e)
        return False
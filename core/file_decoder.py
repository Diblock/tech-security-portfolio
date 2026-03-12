from PIL import Image
import numpy as np
import os
from .progress import barra_progreso


def extraer_archivo(imagen, salida="output"):

    try:

        img = Image.open(imagen).convert("RGB")
        pixeles = np.array(img)

        alto = pixeles.shape[0]
        ancho = pixeles.shape[1]

        total_pixeles = alto * ancho
        procesados = 0

        print("\nIniciando extracción del archivo oculto...\n")

        bits = ""

        for y in range(alto):
            for x in range(ancho):

                pixel = pixeles[y][x]

                for color in pixel:
                    bits += str(color & 1)

                procesados += 1
                barra_progreso(procesados, total_pixeles)

        print("\n")

        datos = bytearray()

        for i in range(0, len(bits), 8):

            byte = bits[i:i+8]

            if len(byte) == 8:
                datos.append(int(byte, 2))

        if datos[0:4] != b"STEG":
            raise Exception("No se encontró archivo oculto")

        ext_len = datos[4]
        extension = datos[5:5+ext_len].decode()

        pos = 5 + ext_len

        tamaño = int.from_bytes(datos[pos:pos+4], "big")

        pos += 4

        contenido = datos[pos:pos+tamaño]

        nombre = os.path.join(salida, f"archivo_extraido.{extension}")

        with open(nombre, "wb") as f:
            f.write(contenido)

        print("\n✔ Archivo extraído:", nombre)

        return nombre

    except Exception as e:

        print("\n❌ Error al extraer archivo:", e)
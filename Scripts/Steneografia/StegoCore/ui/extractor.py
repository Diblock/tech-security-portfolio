from core.decoder import extraer_mensaje
from .image_selector import seleccionar_imagen


def ejecutar_extraccion():

    try:

        print("\nSelecciona la imagen para extraer el mensaje...\n")

        ruta = seleccionar_imagen()

        if ruta is None:
            return

        print("Imagen seleccionada:", ruta)

        mensaje = extraer_mensaje(ruta)

        if mensaje.strip() == "":
            print("\n⚠ No se encontró mensaje oculto\n")
        else:
            print("\n📩 MENSAJE ENCONTRADO\n")
            print("----------------------------")
            print(mensaje)
            print("----------------------------\n")

    except Exception as e:

        print("❌ Error durante la extracción:", e)
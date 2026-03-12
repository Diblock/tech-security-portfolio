import os
from colorama import Fore, Style, init

# ==============================================
# INICIALIZAR COLORAMA (permite colores consola)
# ==============================================

init(autoreset=True)


# ==============================================
# PAUSAR EJECUCIÓN (mejora UX)
# Permite al usuario leer resultados antes
# de que el menú vuelva a mostrarse.
# ==============================================

def pausa():

    input("\nPulsa ENTER para continuar...")


# ==============================================
# LIMPIAR PANTALLA
# Limpia la consola dependiendo del sistema
# operativo (Windows / Linux / Mac)
# ==============================================

def limpiar():

    os.system("cls" if os.name == "nt" else "clear")


# ==============================================
# BANNER PRINCIPAL
# Encabezado visual de la herramienta
# ==============================================

def banner():

    print(Fore.GREEN + """
╔══════════════════════════════════════════════════════╗
║      DIBLOCK STEGANOGRAPHY FRAMEWORK v1.0            ║
║      LSB PAYLOAD INJECTOR / EXTRACTOR                ║
╚══════════════════════════════════════════════════════╝
""")


def mostrar_banner():

    print("""
██████╗ ██╗██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
██╔══██╗██║██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝
██║  ██║██║██████╔╝██║     ██║   ██║██║     █████╔╝
██║  ██║██║██╔══██╗██║     ██║   ██║██║     ██╔═██╗
██████╔╝██║██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗
╚═════╝ ╚═╝╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
""")

    print("⚠ IMPORTANTE:")
    print("Esta herramienta funciona únicamente con imágenes PNG.")
    print("Las imágenes JPG/JPEG comprimen los píxeles y destruyen los datos ocultos.\n")


# ==============================================
# LINEA SEPARADORA VISUAL
# Mejora la legibilidad del menú
# ==============================================

def linea():

    print(Fore.CYAN + "──────────────────────────────────────────────────────")


# ==============================================
# ESTADO DEL SISTEMA
# Muestra información actual de la herramienta
# ==============================================

def estado(imagen, mensaje):

    print(Fore.CYAN + "Estado del sistema\n")

    if imagen:
        print(Fore.GREEN + f"Imagen cargada  : {imagen}")
    else:
        print(Fore.YELLOW + "Imagen cargada  : NINGUNA")

    if mensaje:
        print(Fore.GREEN + "Mensaje cargado : SI")
    else:
        print(Fore.YELLOW + "Mensaje cargado : NO")

    print()


# ==============================================
# MENÚ VISUAL PRINCIPAL
# Muestra las opciones disponibles del programa
# ==============================================

def menu_visual(imagen, mensaje):

    linea()

    estado(imagen, mensaje)

    linea()

    print(Fore.WHITE + """
1 ▸ Cargar imagen
2 ▸ Escribir mensaje secreto
3 ▸ Ocultar mensaje
4 ▸ Extraer mensaje
5 ▸ Ocultar archivo en imagen
6 ▸ Extraer archivo de imagen
7 ▸ Salir
""")


# ==============================================
# MENSAJES VISUALES
# Permiten mostrar mensajes claros al usuario
# ==============================================

def ok(texto):

    print(Fore.GREEN + "✔ " + texto)


def error(texto):

    print(Fore.RED + "✖ " + texto)


def warning(texto):

    print(Fore.YELLOW + "⚠ " + texto)


def info(texto):

    print(Fore.CYAN + "➤ " + texto)
import os
from colorama import Fore, Style, init
import sys
import time

# ==============================================
# INICIALIZAR COLORAMA (permite colores consola)
# ==============================================
init(autoreset=True)

# ==============================================
# PAUSAR EJECUCIÓN (mejora UX)
# ==============================================
def pausa():
    input(Fore.GREEN + Style.BRIGHT + "\n[➤] Pulsa ENTER para continuar..." + Style.RESET_ALL)

# ==============================================
# LIMPIAR PANTALLA
# ==============================================
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


# ==============================================
# BANNER PRINCIPAL
# ==============================================
def banner():

    c_borde = Fore.GREEN + Style.BRIGHT
    c_texto = Fore.LIGHTGREEN_EX + Style.BRIGHT
    c_sub = Fore.WHITE + Style.DIM

    ancho = 54

    print()

    # Recuadro STEGOCORE perfectamente alineado

    linea = 46

    print(c_borde + "   ╭" + "─" * linea + "╮")

    texto1 = "STEGOCORE"
    padding = (linea - len(texto1)) // 2
    print(c_borde + "   │" + " " * padding + c_texto + texto1 + " " * (linea - len(texto1) - padding) + c_borde + "│")

    texto2 = "Advanced PNG Steganography Engine"
    padding = (linea - len(texto2)) // 2
    print(c_borde + "   │" + " " * padding + Fore.LIGHTGREEN_EX + texto2 + " " * (linea - len(texto2) - padding) + c_borde + "│")

    texto3 = "LSB Payload Injection & Extraction"
    padding = (linea - len(texto3)) // 2
    print(c_borde + "   │" + " " * padding + c_sub + texto3 + " " * (linea - len(texto3) - padding) + c_borde + "│")

    print(c_borde + "   ╰" + "─" * linea + "╯")

# ==============================================
# BOOT ANIMATION (ESTILO HERRAMIENTA PENTEST)
# ==============================================

def boot_stegocore():

    print(Fore.GREEN + Style.BRIGHT + "\n[ StegoCORE ] Initializing modules...\n")

    # Barra de progreso
    total = 26
    for i in range(total + 1):
        barra = "█" * i + " " * (total - i)
        porcentaje = int((i / total) * 100)

        sys.stdout.write(
            Fore.GREEN +
            f"\r[{barra}] {porcentaje}%"
        )
        sys.stdout.flush()

        time.sleep(0.03)

    print("\n")

    # Módulos cargando
    modulos = [
        ("Pixel Engine", "OK"),
        ("Payload Injector", "OK"),
        ("Extractor Module", "OK"),
        ("PNG Engine", "READY"),
    ]

    for nombre, estado in modulos:

        puntos = "." * (20 - len(nombre))

        sys.stdout.write(Fore.GREEN + f"{nombre} {puntos} ")
        sys.stdout.flush()

        time.sleep(0.25)

        if estado == "OK":
            print(Fore.LIGHTGREEN_EX + estado)
        else:
            print(Fore.CYAN + estado)

        time.sleep(0.15)

    print()


def mostrar_banner():
    ascii_art = """
  ██████╗ ██╗██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
  ██╔══██╗██║██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝
  ██║  ██║██║██████╔╝██║     ██║   ██║██║     █████╔╝
  ██║  ██║██║██╔══██╗██║     ██║   ██║██║     ██╔═██╗
  ██████╔╝██║██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗
  ╚═════╝ ╚═╝╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
"""
    print(Fore.GREEN + Style.BRIGHT + ascii_art)
    
    print(Fore.RED + Style.BRIGHT + "   [⚠ ] IMPORTANTE:")
    print(Fore.YELLOW + "   Esta herramienta funciona únicamente con imágenes " + Fore.WHITE + Style.BRIGHT + "PNG." + " " + "y" + " " + Fore.WHITE + Style.BRIGHT + "archivos.")
    print(Fore.YELLOW + "   Las imágenes JPG/JPEG comprimen los píxeles y destruyen los datos ocultos.\n")


# ==============================================
# LINEA SEPARADORA VISUAL
# ==============================================
def linea():
    print(Fore.GREEN + "━" * 56)

# ==============================================
# ESTADO DEL SISTEMA
# ==============================================
def estado(imagen, mensaje):
    print(Fore.GREEN + Style.BRIGHT + "\n   ❖ ESTADO DEL SISTEMA ❖\n")

    if imagen:
        print(Fore.LIGHTGREEN_EX + f"   [✔] Imagen cargada  : {Fore.WHITE}{imagen}")
    else:
        print(Fore.LIGHTRED_EX + "   [✖ ] Imagen cargada  : " + Fore.LIGHTBLACK_EX + "NINGUNA")

    if mensaje:
        print(Fore.LIGHTGREEN_EX + "   [✔] Mensaje cargado : " + Fore.WHITE + "SÍ")
    else:
        print(Fore.LIGHTRED_EX + "   [✖ ] Mensaje cargado : " + Fore.LIGHTBLACK_EX + "NO")
    print()

# ==============================================
# MENÚ VISUAL PRINCIPAL
# ==============================================
def menu_visual(imagen, mensaje):
    linea()
    estado(imagen, mensaje)
    linea()
    
    c_borde = Fore.GREEN + Style.BRIGHT
    c_num = Fore.LIGHTGREEN_EX + Style.BRIGHT
    c_texto = Fore.WHITE
    c_flecha = Fore.GREEN
    
    print(c_borde + "\n   ⚙  OPCIONES PRINCIPALES:\n")
    
    print(c_borde + "   ╭─────────────── CARGAR ───────────────╮")
    print(f"   {c_borde}│   {c_num}[1]{c_flecha} ➔ {c_texto}Cargar imagen{' ' * 16}{c_borde}│")
    print(c_borde + "   ╰──────────────────────────────────────╯")
    print()
    
    print(c_borde + "   ╭────────────── MENSAJES ──────────────╮")
    print(f"   {c_borde}│   {c_num}[2]{c_flecha} ➔ {c_texto}Escribir mensaje secreto{' ' * 5}{c_borde}│")
    print(f"   {c_borde}│   {c_num}[3]{c_flecha} ➔ {c_texto}Ocultar mensaje{' ' * 14}{c_borde}│")
    print(f"   {c_borde}│   {c_num}[4]{c_flecha} ➔ {c_texto}Extraer mensaje{' ' * 14}{c_borde}│")
    print(c_borde + "   ╰──────────────────────────────────────╯")
    print()
    
    print(c_borde + "   ╭────────────── ARCHIVOS ──────────────╮")
    print(f"   {c_borde}│   {c_num}[5]{c_flecha} ➔ {c_texto}Ocultar archivo en imagen{' ' * 4}{c_borde}│")
    print(f"   {c_borde}│   {c_num}[6]{c_flecha} ➔ {c_texto}Extraer archivo de imagen{' ' * 4}{c_borde}│")
    print(c_borde + "   ╰──────────────────────────────────────╯")
    print()
    
    print(c_borde + "   ╭──────────────────────────────────────╮")
    print(f"   {c_borde}│   {Fore.RED + Style.BRIGHT}[7]{c_flecha} ➔ {c_texto}Salir{' ' * 24}{c_borde}│")
    print(c_borde + "   ╰──────────────────────────────────────╯")
    print()

# ==============================================
# MENSAJES VISUALES
# ==============================================
def ok(texto):
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "[✔] " + Fore.WHITE + texto)

def error(texto):
    print(Fore.LIGHTRED_EX + Style.BRIGHT + "[✖] " + Fore.WHITE + texto)

def warning(texto):
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "[⚠] " + Fore.WHITE + texto)

def info(texto):
    print(Fore.GREEN + Style.BRIGHT + "[➤] " + Fore.WHITE + texto)
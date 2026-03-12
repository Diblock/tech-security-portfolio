import sys


def barra_progreso(actual, total):

    longitud = 30
    progreso = actual / total if total != 0 else 0

    bloques = int(longitud * progreso)

    verde = "\033[92m"
    verde_claro = "\033[32m"
    reset = "\033[0m"

    barra = verde + "█" * bloques + verde_claro + "░" * (longitud - bloques) + reset

    porcentaje = progreso * 100

    sys.stdout.write(f"\r[{barra}] {porcentaje:5.1f}%")
    sys.stdout.flush()
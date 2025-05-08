import os
from utils.Avion import Avion

def leer_archivo(file_option: str):
    archivos = {
        "1": "case1.txt",
        "2": "case2.txt",
        "3": "case3.txt",
        "4": "case4.txt"
    }

    chosen_file = archivos.get(file_option)
    if not chosen_file:
        print("Opción no válida.")
        return []

    ruta_archivo = os.path.join("cases", chosen_file)

    aviones = []
    with open(ruta_archivo, 'r') as f:
        num_aviones = int(f.readline().strip())

        for i in range(num_aviones):
            info = f.readline().strip().split()
            avion = Avion(
                id=i,
                early=int(info[0]),
                ideal=int(info[1]),
                late=int(info[2]),
                early_penalty=float(info[3]),
                late_penalty=float(info[4])
            )

            while len(avion.time_diffs) < num_aviones - 1:
                values = f.readline().strip().split()
                avion.time_diffs.extend([int(val) for val in values])

            aviones.append(avion)

    return aviones

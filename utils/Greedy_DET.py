from typing import List
from Avion import Avion

def calcular_penalizaciones(avion: Avion) -> int:
    """Calcula la cantidad de penalizaciones de un avión."""
    penalizaciones = 0
    if avion.time_diffs:
        for diff in avion.time_diffs:
            if diff < 0:  # Aterrizaje temprano
                penalizaciones += 1
            elif diff > 0:  # Aterrizaje tarde
                penalizaciones += 1
    return penalizaciones

def ordenar_aviones_determinista(aviones: List[Avion]) -> List[Avion]:
    """
    Ordena los aviones por cantidad de penalizaciones (mayor primero) y luego por tiempo ideal (menor primero).
    """
    return sorted(aviones, key=lambda avion: (calcular_penalizaciones(avion), avion.ideal), reverse=True)

def asignar_tiempos_aterrizaje_determinista(aviones_ordenados: List[Avion]) -> List[Avion]:
    """
    Asigna tiempos de aterrizaje a los aviones en el orden dado, validando los rangos early y late.
    """
    tiempo_actual = 0
    aviones_con_tiempos = []
    for avion in aviones_ordenados:
        tiempo_propuesto = max(tiempo_actual, avion.early)  # No podemos aterrizar antes del early
        if tiempo_propuesto <= avion.late:
            avion.landing_time = tiempo_propuesto
            tiempo_actual = tiempo_propuesto + 1  # Asumimos que cada aterrizaje toma 1 unidad de tiempo
        else:
            # Si el tiempo propuesto excede el late, intentamos aterrizar lo más cerca posible del late
            if tiempo_actual <= avion.late:
                avion.landing_time = avion.late
                tiempo_actual = avion.late + 1
            else:
                # Si incluso el late ya pasó, lo asignamos al tiempo actual y lo marcamos para revisión
                avion.landing_time = tiempo_actual
                print(f"¡Advertencia! El Avión {avion.id + 1} no pudo aterrizar dentro de su ventana (Early: {avion.early}, Late: {avion.late}). Se asignó el tiempo: {tiempo_actual}")
                tiempo_actual += 1
        aviones_con_tiempos.append(avion)
    return aviones_con_tiempos

def run_greed_determ(aviones: List[Avion]) -> List[Avion]:
    """
    Ejecuta el algoritmo greedy determinista para ordenar y asignar tiempos de aterrizaje a los aviones.
    """
    aviones_ordenados = ordenar_aviones_determinista(aviones)
    aviones_con_tiempos = asignar_tiempos_aterrizaje_determinista(aviones_ordenados)
    return aviones_con_tiempos
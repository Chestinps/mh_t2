from utils.LeerCasos import leer_archivo
from utils.Greedy_DET import run_greed_determ
# from utils.Greedy_EST import run_greed_estocast
# from utils.HC_DET import run_hillclimbing_determ
# from utils.HC_EST import run_hillclimbing_estocast
# from utils.TS import run_tabu_search

def main():
    opcion = input("Seleccione un caso de prueba (1-4): ")
    aviones = leer_archivo(opcion)
    
    if not aviones:
        print("No se pudieron cargar los aviones.")
        return
    
    
    print("\nEjecutando Greedy Determinista...\n")

    aviones_asignados = run_greed_determ(aviones)

    print("\nAsignaciones Deterministas:")
    for avion in aviones_asignados:
        print(avion)

    
    # Puedes descomentar estas partes si necesitas probar otros algoritmos
    # asignaciones_estocast = run_greed_estocast()
    # mejoradas_determ = run_hillclimbing_determ(asignaciones_determ)
    # mejoradas_estocast = run_hillclimbing_estocast(asignaciones_estocast)
    # final_tabu = run_tabu_search(asignaciones_determ, asignaciones_estocast)

if __name__ == "__main__":
    main()

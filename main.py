# main.py

import os
from utils.reader import read_planes_data
from utils.greedy import get_time_difference, is_valid_landing_time, sort_planes_by_priority, generate_stochastic_orders, calculate_total_cost
from utils.asignador import assign_real_times
from utils.optimizer import local_search_best_order
from utils.tabu import tabu_search
import matplotlib.pyplot as plt

def main():
    base_path = 'cases'
    case_files = {
        '1': 'case1.txt',
        '2': 'case2.txt',
        '3': 'case3.txt',
        '4': 'case4.txt'
    }

    print("Selecciona el caso de prueba que deseas ejecutar:")
    for key in case_files:
        print(f"  {key}) {case_files[key]}")

    selected = input("\nIngresa el número del caso (1-4): ").strip()

    if selected not in case_files:
        print("Opción no válida. Debes ingresar un número del 1 al 4.")
        return

    file_path = os.path.join(base_path, case_files[selected])
    print(f"\nProcesando archivo: {case_files[selected]}")
    planes = read_planes_data(file_path)


    sorted_planes = sort_planes_by_priority(planes)
    assign_real_times(sorted_planes)
    total_cost = calculate_total_cost(sorted_planes)

    # Generar las 10 soluciones estocásticas
    stochastic_orders = generate_stochastic_orders(planes)

    print("\nAplicando Tabu Search sobre las soluciones estocásticas:")

    tabu_size = 10
    iterations = 100

    best_global_cost = float('inf')
    best_global_order = None


    print("\nOrden de aterrizaje (determinista):")
    for plane in sorted_planes:
        print(f"Avión {plane['id']}: Ideal={plane['ideal']} → Real={plane['real']}")

    print(f"\nCosto total del orden determinista: {total_cost:.2f}")

    print("\nIniciando búsqueda local basada en swaps...")
    best_order, best_cost = local_search_best_order(sorted_planes)

    print("\nMejor orden encontrado tras búsqueda local:")
    for plane in best_order:
        print(f"Avión {plane['id']}: Ideal={plane['ideal']} → Real={plane['real']}")

    print(f"\nCosto total optimizado por búsqueda local: {best_cost:.2f}")


    print("\nAplicando Tabu Search sobre las soluciones estocásticas:")


    for idx, order in enumerate(stochastic_orders):
        print(f"\n--- Solución Estocástica {idx + 1} ---")
        assign_real_times(order)
        initial_cost = calculate_total_cost(order)
        print(f"Costo inicial: {initial_cost:.2f}")

        improved_order, improved_cost, cost_history = tabu_search(order, tabu_size=tabu_size, iterations=iterations)

        print(f"Costo tras Tabu Search: {improved_cost:.2f}")

        if improved_cost < best_global_cost:
            best_global_cost = improved_cost
            best_global_order = improved_order

    print("\n==============================")
    print(f"Mejor costo global tras Tabu Search: {best_global_cost:.2f}")



    all_histories = []

    for idx, order in enumerate(stochastic_orders):
        print(f"\n--- Solución Estocástica {idx + 1} ---")
        assign_real_times(order)
        initial_cost = calculate_total_cost(order)
        print(f"Costo inicial: {initial_cost:.2f}")

        improved_order, improved_cost, cost_history = tabu_search(order, tabu_size=tabu_size, iterations=iterations)
        all_histories.append(cost_history)

        print(f"Costo tras Tabu Search: {improved_cost:.2f}")

        if improved_cost < best_global_cost:
            best_global_cost = improved_cost
            best_global_order = improved_order


    # Gráfico de evolución del costo
    for idx, history in enumerate(all_histories):
        plt.plot(history, label=f"Solución {idx + 1}")

    plt.plot(cost_history)
    plt.title(f"Evolución del costo - Solución Estocástica {idx + 1}")
    plt.xlabel("Iteración")
    plt.ylabel("Costo Total")
    plt.grid(True)
    plt.show()

    

if __name__ == '__main__':
    main()

from collections import deque
from utils.asignar_tiempos import assign_real_times
from utils.greedy import calculate_total_cost
from utils.grasp import swap_planes
import copy

def split_planes_two_runways(order):
    """
    Divide los aviones entre dos pistas alternando por índice (pares e impares).
    """
    pista1 = [plane for idx, plane in enumerate(order) if idx % 2 == 0]
    pista2 = [plane for idx, plane in enumerate(order) if idx % 2 != 0]
    return pista1, pista2

def tabu_search(initial_order, tabu_size, iterations):
    current_order = initial_order.copy()
    assign_real_times(current_order)
    current_cost = calculate_total_cost(current_order)

    best_order = current_order
    best_cost = current_cost

    cost_history = [best_cost]
    tabu_list = deque(maxlen=tabu_size)

    for _ in range(iterations):
        best_neighbor = None
        best_neighbor_cost = float('inf')
        best_swap = None

        for i in range(len(current_order)):
            for j in range(i + 1, len(current_order)):
                swap_move = (i, j)

                # Crear nuevo vecino
                neighbor = swap_planes(current_order, i, j)
                assign_real_times(neighbor)
                neighbor_cost = calculate_total_cost(neighbor)

                # Criterio de aspiración
                if swap_move in tabu_list and neighbor_cost >= best_cost:
                    continue

                if neighbor_cost < best_neighbor_cost:
                    best_neighbor = neighbor
                    best_neighbor_cost = neighbor_cost
                    best_swap = swap_move

        if best_neighbor:
            current_order = best_neighbor
            current_cost = best_neighbor_cost
            tabu_list.append(best_swap)

            if current_cost < best_cost:
                best_order = current_order
                best_cost = current_cost

        cost_history.append(best_cost)

    return best_order, best_cost, cost_history

def tabu_search_two_runways(order, tabu_size, iterations):
    """
    Aplica Tabu Search sobre dos pistas de forma independiente y retorna el costo total combinado.
    """
    pista1, pista2 = split_planes_two_runways(order)

    best_pista1, cost1, history1 = tabu_search(pista1, tabu_size, iterations)
    best_pista2, cost2, history2 = tabu_search(pista2, tabu_size, iterations)

    total_cost = cost1 + cost2
    combined_order = best_pista1 + best_pista2

    return combined_order, total_cost, (history1, history2)
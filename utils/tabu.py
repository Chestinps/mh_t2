from collections import deque
from utils.asignador import assign_real_times
from utils.greedy import calculate_total_cost
from utils.optimizer import swap_planes
import copy

def tabu_search(initial_order, tabu_size, iterations):
    current_order = copy.deepcopy(initial_order)
    assign_real_times(current_order)
    current_cost = calculate_total_cost(current_order)

    best_order = copy.deepcopy(current_order)
    best_cost = current_cost

    tabu_list = deque(maxlen=tabu_size)
    cost_history = [current_cost]  # ← Aquí se almacena el costo en cada iteración

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

                # Criterio de aspiración: aceptar swap tabú si mejora el global
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
            cost_history.append(current_cost)  # ← Guardamos el costo en cada iteración

            if current_cost < best_cost:
                best_order = copy.deepcopy(current_order)
                best_cost = current_cost
        else:
            # Si no hay mejor vecino (muy raro), se repite el costo actual
            cost_history.append(current_cost)

    return best_order, best_cost, cost_history

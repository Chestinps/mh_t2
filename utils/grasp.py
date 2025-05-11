from utils.asignar_tiempos import assign_real_times
from utils.greedy import calculate_total_cost

def swap_planes(planes, i, j):
    new_order = planes.copy()
    new_order[i], new_order[j] = new_order[j], new_order[i]
    return new_order

def local_search_best_order(planes):
    current_order = planes.copy()
    assign_real_times(current_order)
    current_cost = calculate_total_cost(current_order)
    history = [current_cost]

    improved = True
    while improved:
        improved = False
        best_cost = current_cost
        best_order = current_order

        for i in range(len(current_order)):
            for j in range(i + 1, len(current_order)):
                swapped = swap_planes(current_order, i, j)
                assign_real_times(swapped)
                cost = calculate_total_cost(swapped)

                if cost < best_cost:
                    best_cost = cost
                    best_order = swapped
                    improved = True

        if improved:
            current_order = best_order
            current_cost = best_cost
            history.append(current_cost)

    return current_order, current_cost, history

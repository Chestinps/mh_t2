import random
import numpy as np

def get_time_difference(prev_plane, next_plane_index):
    return prev_plane['timeDiffs'][next_plane_index]

def is_valid_landing_time(plane, time):
    return plane['early'] <= time <= plane['late']

def sort_planes_by_priority(planes):

    def priority_key(plane):
        total_penalty = plane['earlyPenalty'] + plane['latePenalty']
        return (-total_penalty, plane['ideal'])

    return sorted(planes, key=priority_key)


def generate_stochastic_orders(planes, base_seed=42069, num_orders=10):
    """
    Genera `num_orders` órdenes estocásticos guiados por los tiempos ideales (ideal).
    """
    orders = []

    indexed_planes = list(enumerate(planes))

    ideals = np.array([plane['ideal'] for plane in planes])
    max_ideal = max(ideals)
    min_ideal = min(ideals)

    weights = max_ideal - ideals + 1

    for i in range(num_orders):
        seed = base_seed + i
        random.seed(seed)

        remaining = indexed_planes[:]
        remaining_weights = weights.copy()
        current_order = []

        while remaining:
            # Cálculo de pesos
            ids = [idx for idx, _ in remaining]
            local_weights = [remaining_weights[idx] for idx in ids]

            selected = random.choices(remaining, weights=local_weights, k=1)[0]
            current_order.append(selected[1]) 
            remaining.remove(selected)

        orders.append(current_order)

    return orders

def calculate_total_cost(planes):
    total_cost = 0.0
    for plane in planes:
        real = plane['real']
        ideal = plane['ideal']
        if real < ideal:
            cost = plane['earlyPenalty'] * (ideal - real)
        else:
            cost = plane['latePenalty'] * (real - ideal)
        total_cost += cost
    return total_cost


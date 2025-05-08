def grasp_hillclimbing(aviones, matriz, n_reinicios=10):
    mejor_sol = None
    mejor_costo = float('inf')
    for seed in range(n_reinicios):
        sol_inicial = greedy_estocastico_1pista(aviones, matriz, seed)
        refinada, costo = hill_climbing(sol_inicial, aviones, matriz)
        if costo < mejor_costo:
            mejor_sol = refinada
            mejor_costo = costo
    return mejor_sol, mejor_costo


def grasp_hillclimbing_2pistas(aviones, matriz, n_reinicios=10):
    mejor_sol = None
    mejor_costo = float('inf')
    for seed in range(n_reinicios):
        sol_inicial = greedy_estocastico_2pistas(aviones, matriz, seed)
        refinada, costo = hill_climbing_2pistas(sol_inicial, aviones, matriz)
        if costo < mejor_costo:
            mejor_sol = refinada
            mejor_costo = costo
    return mejor_sol, mejor_costo
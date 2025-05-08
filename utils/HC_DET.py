def hill_climbing(solucion_inicial, aviones, matriz, max_iter=100):
    actual = solucion_inicial.copy()
    mejor_costo = costo_total(actual, aviones)
    for _ in range(max_iter):
        vecinos = generar_vecinos(actual, aviones, matriz)
        mejora = False
        for vecino in vecinos:
            costo = costo_total(vecino, aviones)
            if costo < mejor_costo:
                actual = vecino
                mejor_costo = costo
                mejora = True
                break
        if not mejora:
            break
    return actual, mejor_costo


def hill_climbing_2pistas(sol_inicial, aviones, matriz, max_iter=100):
    actual = sol_inicial.copy()
    mejor_costo = costo_total(actual, aviones)
    for _ in range(max_iter):
        vecinos = generar_vecinos_2pistas(actual, aviones, matriz)
        mejora = False
        for vecino in vecinos:
            costo = costo_total(vecino, aviones)
            if costo < mejor_costo:
                actual = vecino
                mejor_costo = costo
                mejora = True
                break
        if not mejora:
            break
    return actual, mejor_costo
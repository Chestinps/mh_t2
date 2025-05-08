def es_valido(asignacion, avion, tiempo, matriz):
    for id_prev, t_prev in asignacion.items():
        if abs(tiempo - t_prev) < matriz[id_prev][avion['id']]:
            return False
    return True

def es_valido_2pistas(asignacion, avion, tiempo, pista, matriz):
    for (id_prev, pista_prev), t_prev in asignacion.items():
        if pista == pista_prev and abs(tiempo - t_prev) < matriz[id_prev][avion['id']]:
            return False
    return True


def greedy_estocastico_1pista(aviones, matriz, seed):
    random.seed(seed)
    asignados = {}
    ocupados = set()
    pendientes = aviones.copy()
    random.shuffle(pendientes)

    for avion in pendientes:
        candidatos = [t for t in range(avion['Ek'], avion['Lk'] + 1)
                       if t not in ocupados and es_valido(asignados, avion, t, matriz)]
        if candidatos:
            t = random.choice(candidatos)
        else:
            t = avion['Lk']
        asignados[avion['id']] = t
        ocupados.add(t)
    return asignados


def greedy_estocastico_2pistas(aviones, matriz, seed):
    random.seed(seed)
    asignados = {}
    ocupados = {0: set(), 1: set()}
    pendientes = aviones.copy()
    random.shuffle(pendientes)

    for avion in pendientes:
        candidatos = []
        for pista in [0, 1]:
            for t in range(avion['Ek'], avion['Lk'] + 1):
                if t not in ocupados[pista] and es_valido_2pistas(asignados, avion, t, pista, matriz):
                    candidatos.append((t, pista))

        if candidatos:
            t, pista = random.choice(candidatos)
        else:
            t, pista = avion['Lk'], 0
        asignados[(avion['id'], pista)] = t
        ocupados[pista].add(t)
    return asignados
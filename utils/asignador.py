def assign_real_times(ordered_planes):
    if not ordered_planes:
        return

    # El primer avión aterriza en su tiempo ideal (puedes ajustar a early si prefieres)
    ordered_planes[0]['real'] = max(ordered_planes[0]['early'], ordered_planes[0]['ideal'])

    for i in range(1, len(ordered_planes)):
        prev_plane = ordered_planes[i - 1]
        curr_plane = ordered_planes[i]

        # El índice del avión actual respecto al anterior
        prev_id = prev_plane['id']
        curr_id = curr_plane['id']

        # Tiempo mínimo de separación desde el anterior
        min_separation = prev_plane['timeDiffs'][curr_id]

        # Tiempo mínimo permitido para el actual según separación
        earliest_possible = prev_plane['real'] + min_separation

        # Se ajusta al ideal si es posible, pero nunca antes de early ni después de late
        assigned_time = max(curr_plane['early'], earliest_possible)
        assigned_time = min(assigned_time, curr_plane['late'])

        # Asignar tiempo real
        curr_plane['real'] = assigned_time

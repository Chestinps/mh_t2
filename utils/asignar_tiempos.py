def assign_real_times(ordered_planes):
    if not ordered_planes:
        return

    ordered_planes[0]['real'] = max(ordered_planes[0]['early'], ordered_planes[0]['ideal'])

    for i in range(1, len(ordered_planes)):
        prev_plane = ordered_planes[i - 1]
        curr_plane = ordered_planes[i]

        prev_id = prev_plane['id']
        curr_id = curr_plane['id']

        min_separation = prev_plane['timeDiffs'][curr_id]

        earliest_possible = prev_plane['real'] + min_separation

        # Ajuste del ideal si es posible, pero nunca antes de early ni después de late
        assigned_time = max(curr_plane['early'], earliest_possible)
        assigned_time = min(assigned_time, curr_plane['late'])

        curr_plane['real'] = assigned_time

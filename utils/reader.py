def read_planes_data(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    num_planes = int(lines[0].strip())
    planes = []
    i = 1
    plane_id = 0

    while i < len(lines):
        if len(planes) >= num_planes:
            break

        early, ideal, late, earlyPenalty, latePenalty = map(float, lines[i].strip().split())
        i += 1

        # Leer timeDiffs
        timeDiffs = []
        while len(timeDiffs) < num_planes:
            timeDiffs.extend(map(int, lines[i].strip().split()))
            i += 1

        plane = {
            'id': plane_id, 
            'early': int(early),
            'ideal': int(ideal),
            'late': int(late),
            'earlyPenalty': earlyPenalty,
            'latePenalty': latePenalty,
            'timeDiffs': timeDiffs,
            'real': None 
        }
        planes.append(plane)
        plane_id += 1

    return planes

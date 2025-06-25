def map_api_position_to_dvp_slots(pos):
    mapping = {
        'G': ['PG', 'SG'],
        'F': ['SF', 'PF'],
        'C': ['C'],
        'G-F': ['SG', 'SF'],
        'F-G': ['SF', 'SG'],
        'F-C': ['PF', 'C'],
        'C-F': ['C', 'PF']
    }
    return mapping.get(pos, [])

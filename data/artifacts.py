from utils.io import read_data_table


# For now, we simply put the swords data into nested dictionaries.
# We avoid the complexity of an "artifact object".
def initialize_artifacts():
    artifact_set_bonus = read_data_table('../data/artifacts.tsv')

    # 5 star artifacts at level 20.
    artifact_main_stats = {
        'ATK%/PHYS/ATK%': {'ATK': 311, 'ATK%': 0.932, 'HP': 4780, 'PDB': 0.583, 'CDB': 0, 'CR': 0, 'CD': 0},
        'ATK%/PHYS/CR': {'ATK': 311, 'ATK%': 0.466, 'HP': 4780, 'PDB': 0.583, 'CDB': 0, 'CR': 0.311, 'CD': 0},
        'ATK%/PHYS/CD': {'ATK': 311, 'ATK%': 0.466, 'HP': 4780, 'PDB': 0.583, 'CDB': 0, 'CR': 0, 'CD': 0.622},
        'ATK%/CRYO/ATK%': {'ATK': 311, 'ATK%': 0.932, 'HP': 4780, 'PDB': 0, 'CDB': 0.466, 'CR': 0, 'CD': 0},
        'ATK%/CRYO/+CR': {'ATK': 311, 'ATK%': 0.466, 'HP': 4780, 'PDB': 0, 'CDB': 0.466, 'CR': 0.311, 'CD': 0},
        'ATK%/CRYO/CD': {'ATK': 311, 'ATK%': 0.466, 'HP': 4780, 'PDB': 0, 'CDB': 0.466, 'CR': 0, 'CD': 0.622},
        'ATK%/ATK%/ATK%': {'ATK': 311, 'ATK%': 1.398, 'HP': 4780, 'PDB': 0, 'CDB': 0, 'CR': 0, 'CD': 0},
        'ATK%/ATK%/CR': {'ATK': 311, 'ATK%': 0.932, 'HP': 4780, 'PDB': 0, 'CDB': 0, 'CR': 0.311, 'CD': 0},
        'ATK%/ATK%/CD': {'ATK': 311, 'ATK%': 0.932, 'HP': 4780, 'PDB': 0, 'CDB': 0, 'CR': 0, 'CD': 0.622},
    }

    return artifact_set_bonus, artifact_main_stats


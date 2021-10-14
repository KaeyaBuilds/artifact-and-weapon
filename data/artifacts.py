# (c)2021 wolich

from utils.io import read_data_table


# For now, we simply put the swords data into nested dictionaries.
# We avoid the complexity of an "artifact object".
def initialize_artifacts(unit='kaeya'):
    if unit == 'albedo':
        artifact_set_bonus = read_data_table('../data/artifacts_albedo.tsv')

        # 5 star artifacts at level 20. Will need to modify flat HP and ATK for Defender's and Gambler.
        artifact_main_stats = {
            'ATK%/GEO/DEF%': {'ATK': 311, 'ATK%': 0.466, 'DEF%': 0.583, 'HP': 4780, 'GDB': 0.466, 'CR': 0, 'CD': 0},
            'ATK%/GEO/CR': {'ATK': 311, 'ATK%': 0.466, 'DEF%': 0, 'HP': 4780, 'GDB': 0.466, 'CR': 0.311, 'CD': 0},
            'ATK%/GEO/CD': {'ATK': 311, 'ATK%': 0.466, 'DEF%': 0, 'HP': 4780, 'GDB': 0.466, 'CR': 0, 'CD': 0.622},
            'DEF%/GEO/DEF%': {'ATK': 311, 'ATK%': 0, 'DEF%': 1.166, 'HP': 4780, 'GDB': 0.466, 'CR': 0, 'CD': 0},
            'DEF%/GEO/ATK%': {'ATK': 311, 'ATK%': 0.466, 'DEF%': 0.583, 'HP': 4780, 'GDB': 0.466, 'CR': 0, 'CD': 0},
            'DEF%/GEO/CR': {'ATK': 311, 'ATK%': 0, 'DEF%': 0.583, 'HP': 4780, 'GDB': 0.466, 'CR': 0.311, 'CD': 0},
            'DEF%/GEO/CD': {'ATK': 311, 'ATK%': 0, 'DEF%': 0.583, 'HP': 4780, 'GDB': 0.466, 'CR': 0, 'CD': 0.622},
            'DEF%/ATK%/DEF%': {'ATK': 311, 'ATK%': 0.466, 'DEF%': 1.166, 'HP': 4780, 'GDB': 0, 'CR': 0, 'CD': 0},
            'DEF%/ATK%/CR': {'ATK': 311, 'ATK%': 0.466, 'DEF%': 0.583, 'HP': 4780, 'GDB': 0, 'CR': 0.311, 'CD': 0},
            'DEF%/ATK%/CD': {'ATK': 311, 'ATK%': 0.466, 'DEF%': 0.583, 'HP': 4780, 'GDB': 0, 'CR': 0, 'CD': 0.622},
            'ATK%/DEF%/DEF%': {'ATK': 311, 'ATK%': 0.466, 'DEF%': 1.166, 'HP': 4780, 'GDB': 0, 'CR': 0, 'CD': 0},
            'ATK%/DEF%/CR': {'ATK': 311, 'ATK%': 0.466, 'DEF%': 0.583, 'HP': 4780, 'GDB': 0, 'CR': 0.311, 'CD': 0},
            'ATK%/DEF%/CD': {'ATK': 311, 'ATK%': 0.466, 'DEF%': 0.583, 'HP': 4780, 'GDB': 0, 'CR': 0, 'CD': 0.622},
            'DEF%/DEF%/DEF%': {'ATK': 311, 'ATK%': 0, 'DEF%': 1.749, 'HP': 4780, 'GDB': 0, 'CR': 0, 'CD': 0},
            'DEF%/DEF%/ATK%': {'ATK': 311, 'ATK%': 0.466, 'DEF%': 1.166, 'HP': 4780, 'GDB': 0, 'CR': 0, 'CD': 0},
            'DEF%/DEF%/CR': {'ATK': 311, 'ATK%': 0, 'DEF%': 1.166, 'HP': 4780, 'GDB': 0, 'CR': 0.311, 'CD': 0},
            'DEF%/DEF%/CD': {'ATK': 311, 'ATK%': 0, 'DEF%': 1.166, 'HP': 4780, 'GDB': 0, 'CR': 0, 'CD': 0.622},
        }
    # Default to Kaeya's artifacts.
    else:
        artifact_set_bonus = read_data_table('../data/artifacts_kaeya.tsv')

        # 5 star artifacts at level 20.
        artifact_main_stats = {
            'ATK%/PHYS/ATK%': {'ATK': 311, 'ATK%': 0.932, 'HP': 4780, 'PDB': 0.583, 'CDB': 0, 'CR': 0, 'CD': 0},
            'ATK%/PHYS/CR': {'ATK': 311, 'ATK%': 0.466, 'HP': 4780, 'PDB': 0.583, 'CDB': 0, 'CR': 0.311, 'CD': 0},
            'ATK%/PHYS/CD': {'ATK': 311, 'ATK%': 0.466, 'HP': 4780, 'PDB': 0.583, 'CDB': 0, 'CR': 0, 'CD': 0.622},
            'ATK%/CRYO/ATK%': {'ATK': 311, 'ATK%': 0.932, 'HP': 4780, 'PDB': 0, 'CDB': 0.466, 'CR': 0, 'CD': 0},
            'ATK%/CRYO/CR': {'ATK': 311, 'ATK%': 0.466, 'HP': 4780, 'PDB': 0, 'CDB': 0.466, 'CR': 0.311, 'CD': 0},
            'ATK%/CRYO/CD': {'ATK': 311, 'ATK%': 0.466, 'HP': 4780, 'PDB': 0, 'CDB': 0.466, 'CR': 0, 'CD': 0.622},
            'ATK%/ATK%/ATK%': {'ATK': 311, 'ATK%': 1.398, 'HP': 4780, 'PDB': 0, 'CDB': 0, 'CR': 0, 'CD': 0},
            'ATK%/ATK%/CR': {'ATK': 311, 'ATK%': 0.932, 'HP': 4780, 'PDB': 0, 'CDB': 0, 'CR': 0.311, 'CD': 0},
            'ATK%/ATK%/CD': {'ATK': 311, 'ATK%': 0.932, 'HP': 4780, 'PDB': 0, 'CDB': 0, 'CR': 0, 'CD': 0.622},
        }

    return artifact_set_bonus, artifact_main_stats


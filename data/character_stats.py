# (c)2021 wolich

from utils.io import read_data_table


class Kaeya:
    """
    Just a data placeholder right now.
    """

    def __init__(self):
        # Character stat from level 1 to 90.
        # Here we use the ascended stats at lvl 20, 40, 50, 60, 70 and 80.
        self.hp = {str(i + 1): 0 for i in range(90)}
        self.atk = {str(i + 1): 0 for i in range(90)}
        self.defense = {str(i + 1): 0 for i in range(90)}
        self.er = {str(i + 1): 0 for i in range(90)}

        # TODO: Actually provide data for every level.
        self.hp['80'] = 10830
        self.atk['80'] = 208
        self.defense['80'] = 737
        self.er['80'] = 0.267
        self.hp['90'] = 11636
        self.atk['90'] = 223
        self.defense['90'] = 792
        self.er['90'] = 0.267

        # Skill stat from level 1 to 11.
        self.skills = read_data_table('../data/skills_kaeya.tsv')


class Albedo:
    """
    Just a data placeholder right now.
    """

    def __init__(self):
        # Character stat from level 1 to 90.
        # Here we use the ascended stats at lvl 20, 40, 50, 60, 70 and 80.
        self.hp = {str(i + 1): 0 for i in range(90)}
        self.atk = {str(i + 1): 0 for i in range(90)}
        self.defense = {str(i + 1): 0 for i in range(90)}
        self.gdb = {str(i + 1): 0 for i in range(90)}

        # TODO: Actually provide data for every level.
        self.hp['80'] = 12296
        self.atk['80'] = 233
        self.defense['80'] = 815
        self.gdb['80'] = 0.288
        self.hp['90'] = 13226
        self.atk['90'] = 251
        self.defense['90'] = 876
        self.gdb['90'] = 0.288

        # Skill stat from level 1 to 11.
        self.skills = read_data_table('../data/skills_albedo.tsv')

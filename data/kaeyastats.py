from utils.read import read_data_table


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
        self.hp['90'] = 11636
        self.atk['90'] = 223
        self.defense['90'] = 792
        self.er['90'] = 0.267

        # Skill stat from level 1 to 11.
        self.skills = read_data_table('../data/kaeyaskills.tsv')

def initialize_allstats():
    flat_and_percent = ['ATK', 'DEF', 'HP', 'ATK%', 'DEF%', 'HP%']
    percent = ['CR',  # Crit rate.
               'CD',  # Crit dmg.
               'AACR',  # Normal attack crit rate.
               'CACR',  # Charged attack crit rate.
               'ESCR',  # Elemental skill crit rate.
               'EBCR',  # Elemental burst crit rate.
               'AACD',  # Normal attack crit dmg.
               'CACD',  # Charged attack crit dmg.
               'ESCD',  # Elemental skill crit dmg.
               'EBCD',  # Elemental burst crit dmg.
               'PDB',  # Physical dmg bonus.
               'FDP',  # Pyro dmg bonus.
               'CPD',  # Cryo dmg bonus.
               'EPD',  # Electro dmg bonus.
               'HPD',  # Hydro dmg bonus.
               'WPD',  # Anemo dmg bonus.
               'GPD',  # Geo dmg bonus.
               'AAPD',  # Normal attack dmg bonus.
               'CAPD',  # Charged attack dmg bonus.
               'ESPD',  # Elemental skill dmg bonus.
               'EBPS',  # Elemental burst dmg bonus.
               'APD',  # All dmg bonus.
              ]
    other = ['EM',  # Elemental mastery.
             'ER',  # Energy recharge.
             'AS',  # Attack speed.
            ]

    return flat_and_percent + percent + other


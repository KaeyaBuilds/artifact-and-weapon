from utils.io import read_data_table


# For now, we simply put the swords data into nested dictionaries.
# We avoid the complexity of a "sword object".
def initialize_swords():
    return read_data_table('../data/swords.tsv')


import os


def read_data_table(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_file = os.path.join(dir_path, filename)
    with open(data_file, 'r') as file:
        lines = file.readlines()
        lines = [line.strip('\n') for line in lines]

        table = dict()
        attributes = lines[0].split('\t')[1:]
        for line in lines[1:]:
            line = line.split('\t')
            table[line[0]] = dict()

            for attribute, value in zip(attributes, line[1:]):
                if attribute == 'Note':
                    table[line[0]][attribute] = value
                else:
                    table[line[0]][attribute] = float(value)
        return table

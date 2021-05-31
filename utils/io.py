# (c)2021 wolich at Kaeya Mains

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


def write_result_file(filename, column_names, all_results):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    result_file = os.path.join(dir_path, filename)
    with open(result_file, 'w') as file:
        file.write('\t'.join(column_names))
        file.write('\n')
        for result in all_results:
            file.write('\t'.join(result))
            file.write('\n')

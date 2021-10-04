import sys


def main():
    read_data()


def read_data():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip())
    return create_matrix(lines[0]), create_matrix(lines[1]), create_matrix(lines[2])


def create_matrix(input_line):
    rows = input_line[0]
    columns = input_line[1]


main()

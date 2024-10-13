import csv
import sys

from tabulate import tabulate


def read_csv(file_name: str) -> list[list[str]]:
    with open(file_name) as file:
        data_row = [row for row in csv.reader(file, delimiter="|")]
    return data_row


if __name__ == "__main__":
    data = read_csv(sys.argv[1])
    print(tabulate(data[0:5]))

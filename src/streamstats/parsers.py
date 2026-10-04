from pathlib import Path
import json
import csv

def parser_csv(ls):
    for file in ls:
        with file.open(mode = "r", encoding = "utf-8") as fl:
            for line_number, row in enumerate(csv.DictReader(fl), start = 1):
                print(line_number, row)
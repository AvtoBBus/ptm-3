import re
import json
import pandas as pd
import os
from checksum import calculate_checksum, serialize_result
from check_cols_func import check_data_col, check_ipv4, check_longitude
from typing import Callable

VARIANT = 10
CSV_PATH = f"{VARIANT}.csv"
PATTERNS_PATH = "patterns.json"


def read_patterns(path_to_file: str) -> json:
    patterns = []
    with open(path_to_file, 'r') as fp:
        patterns = json.load(fp)
    return patterns


def check_column(dataset: pd.DataFrame, column: str, pattern: str, check_correct: Callable[[str], bool] = lambda x: True) -> list[int]:
    result = []
    for i in range(len(dataset[column])):
        if not re.fullmatch(pattern, dataset[column][i], re.X) or not check_correct(dataset[column][i]):
            result.append(i)
    print(f"In '{column}' find {len(result)} incorrect cells")
    return result


if __name__ == "__main__":
    os.system("cls")
    dataset = pd.read_csv(CSV_PATH, sep=";", encoding="utf-16")
    patterns = []
    patterns = read_patterns(PATTERNS_PATH)
    result = []
    for col in dataset.columns:
        if col == "date":
            result.append(check_column(
                dataset, col, patterns[col], check_data_col))
        if col == "ip_v4":
            result.append(check_column(
                dataset, col, patterns[col], check_ipv4))
        if col == "longitude":
            result.append(check_column(
                dataset, col, patterns[col], check_longitude))
        else:
            result.append(check_column(dataset, col, patterns[col]))
    print(calculate_checksum(result))
    serialize_result(VARIANT, calculate_checksum(result))
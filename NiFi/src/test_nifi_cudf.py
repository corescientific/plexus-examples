import cudf as pd
import time
import sys
from collections import defaultdict
import pandas as pdcpu


def get_data(filename, rows=10):
    tic = time.perf_counter()
    df = pd.read_csv(filename, sep="|", header=None, nrows=rows)
    toc = time.perf_counter()
    seconds = toc - tic
    # print(seconds)
    return seconds, df


def fill_na(df):
    tic = time.perf_counter()
    df = df.fillna(0)
    toc = time.perf_counter()
    seconds = toc - tic
    # print(seconds)
    return seconds, df


def sort_data(df, col):
    tic = time.perf_counter()
    df = df.sort_values(str(col), ascending=False, axis=0)
    toc = time.perf_counter()
    seconds = toc - tic
    # print(seconds)
    return seconds, df


def group_data(df, col):
    tic = time.perf_counter()
    df = df.groupby(col).mean()
    toc = time.perf_counter()
    seconds = toc - tic
    # print(seconds)
    return seconds, df


def main():
    # path to file
    filename = "../data/perf/Performance_2000Q1.txt"
    output = "../data/results/gpu_nifi.csv"
    col = '4'
    grp = '0'

    sizes = [10, 100, 1e3, 1e4, 1e5, 1e6]

    time_dict = defaultdict(dict)
    tmp = pdcpu.DataFrame()
    for loop in range(50):
        print(loop)
        for s in sizes:
            print(s)
            time_dict[s]['get'], df = get_data(filename, s)
            time_dict[s]['fill'], df = fill_na(df)
            time_dict[s]['sort'], df = sort_data(df, col)
            time_dict[s]['group'], df = group_data(df, grp)
            # print(df.head(5))
            print(time_dict)
            print(df.shape)
        tmp = tmp.append(pdcpu.DataFrame.from_dict(time_dict))
    tmp.to_csv(output)
    tmp.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    main()


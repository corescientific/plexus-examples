import pandas as pd
import sys

def main():
    # argv1: path to file
    filename = str(sys.argv[1])
    data = pd.read_csv(filename)
    data.to_csv(sys.stdout, index=False)

if __name__ == "__main__":
    main()
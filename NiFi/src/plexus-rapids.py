import cudf as pd
import sys

def main():
    data = pd.read_csv(sys.stdin)
    ########### insert your code here. This is example works with the 'boston' dataset
    data = df.groupby('RAD').mean()
    ###########
    data.to_csv(sys.stdout, index=False)
if __name__ == "__main__":
    main()
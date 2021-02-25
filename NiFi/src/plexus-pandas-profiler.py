import pandas as pd
import pandas_profiling
from pandas_profiling.utils.cache import cache_file
import sys



def main():
    df = pd.read_csv(sys.stdin)
    ########### insert your code here. This example creates a pandas-profile of the data
    profile = df.profile_report(correlations={
             "pearson": {"calculate": False},
             "spearman": {"calculate": False},
             "kendall": {"calculate": False},
             "phi_k": {"calculate": False},
             "cramers": {"calculate": False},
         })

    profile.to_file("/home/acc/index.html")
    ###########


if __name__ == "__main__":
    main()
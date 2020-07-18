import pandas as pd

def df_to_long(df):
    tidy = pd.pivot(df)
    #tidy = tidy.astype({'size': 'int32', 'Noise Ratio':'float64'})
    return tidy


f = "parametersPerPersonSafeBU.csv"
dat = pd.read_csv(f, sep=",")

dat = df_to_long(dat)
print(dat)

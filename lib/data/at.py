import pandas as pd
from lib.plot import DEFAULT_COL_NAMES

temp = 10

def prepare_df():
    df = pd.read_csv('data/at/OGD_gest_kalwo_GEST_KALWOCHE_100.csv', sep=';', delimiter=None, )

    # Summe der Todesfälle pro Kalenderwoche
    group = df['F-ANZ-1'].groupby(df['C-KALWOCHE-0']).sum()

    frame = {'Anzahl Todesfälle': group }
    
    result_df = pd.DataFrame(frame).reset_index()

    # Spalte für Jahr
    result_df[DEFAULT_COL_NAMES.year] = result_df['C-KALWOCHE-0'].apply(lambda x: int(x[5:9]))

    # Spalte für KW
    result_df[DEFAULT_COL_NAMES.week] = result_df['C-KALWOCHE-0'].apply(lambda x: int(x[9:11]))

    result_df=result_df.rename(columns={ 'Anzahl Todesfälle' : 'deaths'})

    #result_df
    return result_df
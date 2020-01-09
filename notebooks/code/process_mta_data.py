import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_DIR = str(Path(__file__).resolve().parents[2])


def add_datetime(df):
    """
    adds a datetime column to the mta dataframes
    :param df:
    :return: a dataframe with a new datetime column, generated from

    """
    df = df.copy()
    time = df.DATE + ' ' + df.TIME
    df['datetime'] = pd.to_datetime(time, format='%m/%d/%Y %H:%M:%S') # TODO make format explicit
    return df

def convert_date_to_datetime(df):
    """
    converts column "DATE" to a datetime object
    :param df:
    :return: df with new column types
    """
    df = df.copy()

    df['DATE'] = pd.to_datetime(df['DATE'])
    return df


def clean_col_names(df):
    """
    cleans up the column names in the mta dataframe

    :param df: mta dataframe
    :return: mta dataframe with cleaned columns
    """
    df = df.copy()
    before = 'EXITS                                                               '
    df.rename(columns={before: 'EXITS', "C/A": "CA"}, inplace=True)
    return df

def remove_recovr_aud(df):
    """
    """
    return df[df['DESC'] != "RECOVR AUD"]

def add_ins_outs_to_df(df_in):
    """
    determines the difference of each row's ENTRIES count from the previous row's.
    It won't diff between different turnstiles, but make sure to run this before any sorting

    :param df: dataframe to manipulate (in place)
    """
    df = df_in.copy()
    mask = df.duplicated(['CA', 'UNIT', 'SCP', 'STATION'])
    df['INS'] = np.where(mask, df['ENTRIES'] - df['ENTRIES'].shift(1), np.nan)
    df['OUTS'] = np.where(mask, df['EXITS'] - df['EXITS'].shift(1), np.nan)
    return df


def remove_outliers(df):
    df = df[df['INS'] < 500000]
    return df[df['INS'] >= 0]

def apply_processing_sequence(df):
    df = clean_col_names(df)
    df = add_datetime(df)
    df = remove_recovr_aud(df)
    df = df.sort_values(['CA','UNIT','SCP','STATION','DATETIME'])
    df = add_ins_outs_to_df(df)
    df = remove_outliers(df)
    return df

#################################
## data has been processed and cleaned, now let's work on it:


def group_by_days(df):
    """
    """
    return df.groupby(['CA', 'UNIT', 'SCP', 'STATION', 'DATE']).agg({'INS': 'sum', 'OUTS': 'sum'})


def get_weekday_station_freqs(df):
    """
    apply to df after applying group_by_days
    """









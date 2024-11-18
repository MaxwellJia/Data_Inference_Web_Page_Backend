import pandas as pd
import numpy as np

from .global_variables import  MISSING_VARIABLE
from .global_variables import SPECIAL_SYMBOLS


def data_wrangling(df):
    """
    Cleans and formats the given DataFrame by standardizing missing values to NaN,
    removing leading and trailing whitespace from string columns, and eliminating special
    symbols except for date symbols (i.e., "-" and "/").

    Parameters:
    ----------
    df : pd.DataFrame
        The input DataFrame that requires cleaning and formatting.

    Returns:
    -------
    pd.DataFrame
        A cleaned DataFrame with standardized missing values and formatted string columns.
    """

    # Formalize missing values to NaN
    formalized_data = formalize_missing_values(df)

    for col in formalized_data.columns:
        # Solve the col is not string
        if df[col].dtype != 'object':
            continue

        # Remove the blank on the two sides
        formalized_data[col] = formalized_data[col].str.strip()

        # Remove special symbols but keep "-", "/" date symbols
        special_chars_pattern = ''.join([f'\\{char}' for char in SPECIAL_SYMBOLS])
        regex_pattern = rf'[^a-zA-Z0-9\s{special_chars_pattern}]'
        formalized_data[col] = formalized_data[col].str.replace(regex_pattern, '', regex=True)

    return formalized_data

def formalize_missing_values(df):
    """
    Standardizes various representations of missing data in the DataFrame, replacing them with NaN.

    Parameters:
    ----------
    df : pd.DataFrame
        The input DataFrame in which missing values will be standardized to NaN.

    Returns:
    -------
    pd.DataFrame
        The DataFrame with all specified missing values replaced by NaN.
    """

    # Replace all possible missing data to NaN
    missing_values = ['Not Available', 'N/A', 'null', '-', 'Data', 'NA', None] + MISSING_VARIABLE
    df.replace(missing_values, np.nan, inplace=True)
    return df

""""
Test
"""
# df = pd.read_csv('sample_data.csv')
# data_wrangled = data_wrangling(df)
# print(data_wrangled)
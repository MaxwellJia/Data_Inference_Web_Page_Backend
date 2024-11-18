import numpy as np
import pandas as pd

from .data_wrangling import data_wrangling
from .infer_functions import convert_column_if_date_format, convert_to_boolean, convert_to_categorical, \
    convert_to_complex
from .infer_functions import convert_to_int_optimal
from .infer_functions import convert_to_float_optimal
from .infer_functions import convert_to_timedelta

def infer_and_convert_data_types(df):
    """
        Infers and converts the data types of each column in a DataFrame to optimize storage and accuracy.

        The function follows a specific conversion order: it first cleans the data, then attempts to convert
        each column to an optimal data type in the following sequence: boolean, integer, float, datetime,
        category, complex, and timedelta. This order minimizes data loss and prevents unintended type
        conversions by handling simpler data types first.

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame containing columns with mixed data types to be inferred and converted.

        Returns
        -------
        pd.DataFrame
            The modified DataFrame with optimized data types, saved as a CSV file named "output.csv".
        """

    # Data wrangling first
    df = data_wrangling(df)

    # Attempt to convert
    for col in df.columns:
        raw_col = df[col]

        # If this column is bool type, just skip because there are no other possibilities
        if raw_col.dtype.name == 'bool':
            continue

        # Attempt to convert to bool
        converted_bool_col = convert_to_boolean(raw_col)
        if not raw_col.equals(converted_bool_col) or raw_col.dtype != converted_bool_col.dtype:
            df[col] = converted_bool_col
            continue

        # Attempt to convert to int8, int16, int32 or int64
        converted_int_col = convert_to_int_optimal(raw_col)
        if not raw_col.equals(converted_int_col) or raw_col.dtype != converted_int_col.dtype:
            df[col] = converted_int_col
            continue

        # Attempt to convert to float32 or float64 or float64
        converted_float_col = convert_to_float_optimal(raw_col)
        if not raw_col.equals(converted_float_col) or raw_col.dtype != converted_float_col.dtype:
            df[col] = converted_float_col
            continue

        # Attempt to convert to datetime in required format or no format (at least one can be convert to datetime)
        # NaN will be converted to NaT
        'Must be put after int and float, because it will convert simple int or float to datetime'
        converted_datetime_col = convert_column_if_date_format(raw_col)
        if not raw_col.equals(converted_datetime_col) or raw_col.dtype != converted_datetime_col.dtype:
            df[col] = converted_datetime_col
            continue

        # Attempt to convert to category type in required min and max
        converted_categorical_col = convert_to_categorical(raw_col)
        if not raw_col.equals(converted_categorical_col) or raw_col.dtype != converted_categorical_col.dtype:
            df[col] = converted_categorical_col
            continue

        # Attempt to convert to complex type
        converted_to_complex_col = convert_to_complex(raw_col)
        if not raw_col.equals(converted_to_complex_col) or raw_col.dtype != converted_to_complex_col.dtype:
            df[col] = converted_to_complex_col
            continue

        # Attempt to convert to timedelta[ns]
        # NaN will be converted to NaT
        'Must be be put after int and float, because it will convert int or float to timedelta'
        converted_timedelta_col = convert_to_timedelta(raw_col)
        if not raw_col.equals(converted_timedelta_col) or raw_col.dtype != converted_timedelta_col.dtype:
            df[col] = converted_timedelta_col
            continue

    return df
# Test
# df = pd.read_csv('processed_file.csv')
# infer_and_convert_data_types(df)
# print(df.dtypes)
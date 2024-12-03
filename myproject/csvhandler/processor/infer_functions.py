import copy

import numpy as np
import pandas as pd
from .global_variables import DATA_FORMAT, MAX_THRESHOLD, MIN_THRESHOLD, BOOLEAN_SET, TIME_UNITS


# from global_variables import BOOLEAN_SET

def convert_column_if_date_format(column):
    """
       Converts a column to datetime format if all non-null values can be successfully parsed as dates.

       Parameters
       ----------
       column : pd.Series
           The column to check and potentially convert to datetime.

       Returns
       -------
       pd.Series
           The column converted to datetime format if all values are date-compatible; otherwise, the original column.

       Notes
       -------
       Try to convert to datetime
       Checks if all value in the column can be successfully converted to date format, and converts the column
       NaN will be converted to NaT
       """

    # Check if all value (skipping NaN) can be converted to date format
    has_date = column.apply(lambda x: pd.notnull(x) and pd.to_datetime(x, errors='coerce') is not pd.NaT).all()

    if has_date:
        # If there is no required format, convert by default
        if DATA_FORMAT == "":
            column = pd.to_datetime(column, errors='coerce')
            return column
        else:
            # If there is format, try to convert by format, convert by default if failed
            # Convert the entire column to date format and turn the values that failed the conversion into NaT
            # Try to convert the date using the specified format, if that fails, use automatic parsing
            try_column = pd.to_datetime(column, format=DATA_FORMAT, errors='coerce')

            # If the entire column still cannot be parsed (i.e. all NaT), try automatic parsing without format
            if try_column.isna().all():
                column = pd.to_datetime(column, errors='coerce')
                return column

    return column


def convert_to_int_optimal(column):
    """
        Converts a column to the optimal integer type (Int8, Int16, Int32, or Int64) to save memory if possible.

        Parameters
        ----------
        column : pd.Series
            The column to check and potentially convert to an integer type.

        Returns
        -------
        pd.Series
            The column converted to an optimal integer type or the original column if conversion is not possible.

        Notes
       -------
       Determines and converts the column to the optimal int type
       NaN will be converted to <NA> or ""
       Save space to the maximum extent possible while retaining complete information
        """

    # Delete NaN
    temp_col_no_NaN = column.dropna()

    # Tried to convert the column to a numeric type, incorrectly converted to NaN
    converted_col_no_NaN = pd.to_numeric(temp_col_no_NaN, errors='coerce')

    # Check if there is a NaN in the column (non-integer or cannot be converted)
    if converted_col_no_NaN.isna().any():
        return column  # Returns the original column because it is not a pure integer column

    # Check if the decimal part is included
    if (converted_col_no_NaN % 1 != 0).any():
        return column  # Returns the original column, which cannot be an int because it contains decimals

    # Check int8 range
    int8_max = np.iinfo(np.int8).max
    int8_min = np.iinfo(np.int8).min

    if (converted_col_no_NaN.max() <= int8_max) and (converted_col_no_NaN.min() >= int8_min):
        return converted_col_no_NaN.astype('Int8').reindex_like(column)  # Convert to int8

    # Check int16 range
    int16_max = np.iinfo(np.int16).max
    int16_min = np.iinfo(np.int16).min

    if (converted_col_no_NaN.max() <= int16_max) and (converted_col_no_NaN.min() >= int16_min):
        return converted_col_no_NaN.astype('Int16').reindex_like(column)  # Convert to int16

    # Check int32 range
    int32_max = np.iinfo(np.int32).max
    int32_min = np.iinfo(np.int32).min

    if (converted_col_no_NaN.max() <= int32_max) and (converted_col_no_NaN.min() >= int32_min):
        return converted_col_no_NaN.astype('Int32').reindex_like(column)  # Convert to int32
    else:
        return converted_col_no_NaN.astype('Int64').reindex_like(column)  # Convert to int64



"""
Save space to the maximum extent possible while retaining complete information
Determine and convert the column to the optimal float type
Keep a maximum of six decimal places
"""
#
#
def convert_to_float_optimal(column):
    """
       Converts a column to the optimal float type (float32 or float64) to save memory if possible.

       Parameters
       ----------
       column : pd.Series
           The column to check and potentially convert to a float type.

       Returns
       -------
       pd.Series
           The column converted to an optimal float type or the original column if conversion is not possible.

       Notes
       -------
       Save space to the maximum extent possible while retaining complete information
       Determine and convert the column to the optimal float type
       Keep a maximum of six decimal places
       """
    # Tried to convert the column to a numeric type, incorrectly converted to NaN
    converted_col = pd.to_numeric(column, errors='coerce')

    # If all non-null values in the column are numeric types, proceed with the conversion
    if converted_col.notna().all():
        # Check if it's suitable to convert to float32
        float32_max = np.finfo(np.float32).max
        float32_min = np.finfo(np.float32).min

        if (converted_col.max() <= float32_max) and (converted_col.min() >= float32_min):
            return converted_col.astype('float32')  # Convert to float32
        else:
            return converted_col.astype('float64')  # Convert to float64
    else:
        # Otherwise, the original column is returned
        return column


def convert_to_boolean(column):
    """
       Converts a column to boolean type if it contains only two unique non-null values.

       Parameters
       ----------
       column : pd.Series
           The column to check and potentially convert to boolean.

       Returns
       -------
       pd.Series
           The column converted to boolean type or the original column if it does not meet the criteria.
       Notes
       -------
       Determine if a column is a Boolean or has only two non-null values
       The boolean values can be clarified in global_variables.BOOLEAN_SET
       """

    # Unique value after removing NaN and empty value
    unique_values = column.dropna().unique()

    # Determines whether it is a Boolean type or has only two non-null values
    boolean_set = {True, False, 0, 1}.union(BOOLEAN_SET)
    if column.dtype == 'bool' or (len(unique_values) == 2 and set(unique_values).issubset(boolean_set)):
        # Convert to a Boolean type directly
        return column.astype(bool)
    elif len(unique_values) == 2:
        # Map one of the two unique values to 1 and the other to 0
        value_map = {unique_values[0]: 0, unique_values[1]: 1}
        converted_column = column.map(value_map)
        # Convert the mapped column to boolean
        return converted_column.astype(bool)
    else:
        return column


def convert_to_categorical(column):
    """
        Converts a column to categorical type if the number of unique non-null values falls within a specified range.

        Parameters
        ----------
        column : pd.Series
            The column to check and potentially convert to categorical.

        Returns
        -------
        pd.Series
            The column converted to categorical type if within range, or the original column otherwise.
       Notes
       -------
       Determines whether it is possible for a column to be converted to a category type
        """


    # Gets the number of unique values in the column that are not null
    unique_count = column.nunique(dropna=True)

    # Determine whether the number of unique values is below the max threshold and bigger than the min threshold
    if MAX_THRESHOLD >= unique_count >= MIN_THRESHOLD:
            return column.astype('category')  # return category type if yes
    return column  # Or return the original column


def convert_to_complex(column):
    """
        Converts a column to complex type if all non-null values are parsable as complex numbers and not of type int or float.

        Parameters
        ----------
        column : pd.Series
            The column to check and potentially convert to complex type.

        Returns
        -------
        pd.Series
            The column converted to complex type or the original column if it does not meet the criteria.
       Notes
       -------
       Determine if the column is of type complex and convert it
        """

    # Check that each non-empty element in the column can be resolved to a complex type and is not of type int or float
    is_complex = column.dropna().apply(
        lambda x: isinstance(x, str) and try_convert_to_complex(x)
    ).all()

    if is_complex:
        # If all non-null values can resolve to complex, convert to the complex data type
        return column.apply(lambda x: complex(x) if pd.notnull(x) else x)
    else:
        # Otherwise, return to the original column
        return column


def try_convert_to_complex(x):
    """
        Checks if a given string can be converted to a complex number.

        Parameters
        ----------
        x : str
            The string to check.

        Returns
        -------
        bool
            True if the string can be converted to a complex number, False otherwise.
       Notes
       -------
       Define helper functions to attempt transformations
        """
    try:
        # Try converting the string to a complex type
        complex(x)
        return True
    except ValueError:
        # If the conversion fails, return False
        return False


def convert_to_timedelta(column):
    """
        Converts a column to timedelta type if any value in the column can be successfully parsed as timedelta.

        Parameters
        ----------
        column : pd.Series
            The column to check and potentially convert to timedelta type.

        Returns
        -------
        pd.Series
            The column converted to timedelta type if possible, or the original column otherwise.
       Notes
       -------
       NaN will be converted to NaT
       Must be put at the last, because it will convert int or float to timedelta
        """
    # Create a regular expression pattern that includes all the units in the TIME_UNITS
    time_units_pattern = '|'.join([f"{unit}s?" for unit in TIME_UNITS])

    # Check if contains 'days', 'hours', 'minutes' time units
    if column.str.contains(fr"\d+\s?(?:{time_units_pattern})", case=False, na=False).any():
        # Check if at least one value can be successfully converted to timedelta
        has_timedelta = column.apply(
            lambda x: pd.notnull(x) and pd.to_timedelta(x, errors='coerce') is not pd.NaT).any()

        if has_timedelta:
            # Convert the entire column to the timedelta type, and the non-convertible value becomes NaT
            column = pd.to_timedelta(column, errors='coerce')

    # Returns the original column (if it doesn't contain time units or can't be converted to timedelta type)
    return column
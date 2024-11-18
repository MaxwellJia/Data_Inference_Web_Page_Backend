import pandas as pd
from csvhandler.processor.infer_functions import *

def forced_to_bool(df, type_map):
    """
    Convert columns in a DataFrame to specific data types based on a given type mapping.

    This function iterates through a mapping of column names to target data types, and
    attempts to cast the specified columns in the DataFrame to the desired types. If a
    conversion fails (due to `ValueError` or `TypeError`), the column remains unchanged.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be converted.
        type_map (dict): A dictionary mapping column names to desired data types.

    Returns:
        pd.DataFrame: The modified DataFrame with columns converted to the specified types
                      wherever applicable.
    """

    # Iterate through the type_map to process and convert DataFrame columns
    for column, dtype in type_map.items():
        try:
            # Check if the column exists in the DataFrame
            if column in df.columns:
                # Handle integer conversions
                if dtype in ["Int64", "Int32", "Int16", "Int8"]:
                    df[column] = df[column].astype(int)
                # Handle float conversions
                elif dtype in ["float64", "float32"]:
                    df[column] = df[column].astype(float)
                # Handle datetime conversions
                elif dtype in ["datetime64[ns]", "datetime64[ns, UTC]"]:
                    df[column] = pd.to_datetime(df[column], errors='raise')
                # Handle boolean conversions
                elif dtype == "bool":
                    df[column] = df[column].astype(bool)
                # Handle category type conversions
                elif dtype == "category":
                    df[column] = df[column].astype('category')
                # Handle timedelta conversions
                elif dtype == "timedelta64[ns]":
                    df[column] = pd.to_timedelta(df[column], errors='raise')
                    print(f"Column {column} converted to {df[column].dtype}.")
                # Handle complex number conversions
                elif dtype == "complex128":
                    df[column] = df[column].astype(complex)
                # Handle object (string) conversions
                elif dtype == "object":
                    df[column] = df[column].astype(str)
                # Additional data types can be added here as needed
        except (ValueError, TypeError):
            # Log an error message if conversion fails and skip the column
            print(f"Column {column} could not be converted. Keeping its original type.")

    return df



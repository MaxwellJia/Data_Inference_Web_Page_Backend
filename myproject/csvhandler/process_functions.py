def map_dtypes_to_user_friendly_names(dtype_map):
    """
    Maps Pandas dtypes to user-friendly names.

    Parameters:
        dtype_map (dict): A dictionary where keys are column names and values are Pandas dtype strings.

    Returns:
        dict: A dictionary where keys are column names, and values are user-friendly type names.
    """
    # Define a mapping of dtypes to user-friendly names
    dtype_to_friendly_name = {
        "object": "Text",
        "Int64": "Integer64",
        "Int32": "Integer32",
        "Int16": "Integer16",
        "Int8": "Integer8",
        "float64": "Decimal64",
        "float32": "Decimal32",
        "datetime64[ns]": "Date",
        "datetime64[ns, UTC]": "Datetime(UTC)",
        "bool": "Boolean",
        "category": "Category",
        "timedelta64[ns]": "Time Interval",
        "complex128": "Complex Number",
    }

    # Convert the dtype_map to user-friendly names
    user_friendly_map = {
        column_name: dtype_to_friendly_name.get(dtype, "Unknown Type")
        for column_name, dtype in dtype_map.items()
    }

    return user_friendly_map

def map_user_friendly_names_to_dtypes(friendly_map):
    """
    Maps user-friendly type names to Pandas dtypes.

    Parameters:
        friendly_map (dict): A dictionary where keys are column names and values are user-friendly type names.

    Returns:
        dict: A dictionary where keys are column names, and values are Pandas dtype strings.
    """
    # Define a reverse mapping of user-friendly names to dtypes
    friendly_name_to_dtype = {
        "Text": "object",
        "Integer64": "Int64",
        "Integer32": "Int32",
        "Integer16": "Int16",
        "Integer8": "Int8",
        "Decimal64": "float64",
        "Decimal32": "float32",
        "Date": "datetime64[ns]",
        "Datetime(UTC)": "datetime64[ns, UTC]",
        "Boolean": "bool",
        "Category": "category",
        "Time Interval": "timedelta64[ns]",
        "Complex Number": "complex128",
    }

    # Convert the friendly_map to dtypes
    dtype_map = {
        column_name: friendly_name_to_dtype.get(friendly_name, "object")
        for column_name, friendly_name in friendly_map.items()
    }

    return dtype_map



def get_differences(updated_map, DTYPES_MAP):
    """
    Identify differences between the updated data type map and the original data type map.

    This function compares two dictionaries, `updated_map` and `DTYPES_MAP`, and returns
    a new dictionary containing keys where the values differ or are missing between the two maps.

    Args:
        updated_map (dict): The updated map of column names and their data types.
        DTYPES_MAP (dict): The original map of column names and their data types.

    Returns:
        dict: A dictionary containing the differences between the two maps. Keys that are
              different or missing in either map are included, along with their respective values.
    """
    result = {}

    # Iterate over updated_map to check for keys that differ or are missing in DTYPES_MAP
    for key, value in updated_map.items():
        if key not in DTYPES_MAP or DTYPES_MAP[key] != value:
            # Add differing or new keys from updated_map to the result
            result[key] = value

    # Iterate over DTYPES_MAP to check for keys missing in updated_map
    for key, value in DTYPES_MAP.items():
        if key not in updated_map:
            # Add missing keys from DTYPES_MAP to the result
            result[key] = value

    return result



# What empty value is represent in the data
MISSING_VARIABLE = ["not available", "NOT AVAILABLE", ""]

# Special symbols that you want to keep (all characters, numbers and empty string are already included)
# ':' '/' are datetime and timedelta[ns], '+' ',' are for complex data type
SPECIAL_SYMBOLS = [ '-', '/', '@', '.', '+', ':', ',', ' ']

# Datetime format
# Examples:
#
# Year-month-day format:
# "%Y-%m-%d": 2023-01-01
# "%Y/%m/%d": 2023/01/01
#
# Day-month-year format:
# "%d-%m-%Y": 01-01-2023
# "%d/%m/%Y": 01/01/2023
#
# Month-day-year format (common in the United States):
# "%m-%d-%Y": 01-01-2023
# "%m/%d/%Y": 01/01/2023
#
# Format with time:
# "%Y-%m-%d %H:%M:%S": 2023-01-01 14:30:00
# "%Y-%m-%d %I:%M %p": 2023-01-01 02:30 PM (12-hour format)
#
# Format with time zone:
# "%Y-%m-%d %H:%M:%S%z": 2023-01-01 14:30:00+0000
# "%Y-%m-%d %H:%M:%S %Z": 2023-01-01 14:30:00 UTC
#
# Contain only the date or time part:
# "%Y-%m": 2023-01 (year and month only)
# "%H:%M:%S": 14:30:00 (time only)
DATA_FORMAT = ""

# A representation of a Boolean value
BOOLEAN_SET = {"T", "F"}

# Min threshold and Max threshold for category, the number of unique values
# that are not null in what range will this column will be recognized as category (Equal included)
MIN_THRESHOLD = 3
MAX_THRESHOLD = 4

# global_variables.py
TIME_UNITS = ["days", "hours", "minutes", "seconds", "weeks"]
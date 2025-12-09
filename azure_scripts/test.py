from datetime import datetime

def string_to_datetime(date_string: str, date_format: str) -> datetime:
    """
    Convert a date string into a datetime object.

    :param date_string: The date as a string (e.g., "2025-12-07 14:30:00")
    :param date_format: The format of the date string (e.g., "%Y-%m-%d %H:%M:%S")
    :return: datetime object
    :raises ValueError: if the string doesn't match the format
    """
    try:
        # Parse the string into a datetime object
        dt_object = datetime.strptime(date_string, date_format)
        return dt_object
    except ValueError as e:
        raise ValueError(f"Invalid date or format: {e}")
    
def parse_date(value: str):
    return datetime.strptime(value, "%Y-%m-%d")

# Example usage
if __name__ == "__main__":
    # Example 1: Date and time
    date_str1 = "2025-12-07 14:30:00"
    format1 = "%Y-%m-%d %H:%M:%S"
    print("Converted datetime:", string_to_datetime(date_str1, format1))

    # Example 2: Date only
    date_str2 = "2025-02-13"
    format2 = "%Y-%m-%d"
    print("Converted datetime:", parse_date(date_str2))

from datetime import datetime

def date_converter(date_raw):
    """
        Convert datetime text to datetime object.
        Add this kind of comment to explain complex function or object
    """
    date_string_cleaned = date_raw.split(",")[1].strip().replace("WIB", "").strip()
    return datetime.strptime(date_string_cleaned, '%d %b %Y %H:%M')
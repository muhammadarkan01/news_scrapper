from datetime import datetime

# Mapping of Indonesian month abbreviations to English
MONTH_MAP = {
    "Jan": "Jan",  # January
    "Feb": "Feb",  # February
    "Mar": "Mar",  # March
    "Apr": "Apr",  # April
    "Mei": "May",  # May
    "Jun": "Jun",  # June
    "Jul": "Jul",  # July
    "Agu": "Aug",  # August
    "Sep": "Sep",  # September
    "Okt": "Oct",  # October
    "Nov": "Nov",  # November
    "Des": "Dec"   # December
}

def date_converter(date_raw):
    """
    Convert datetime text in Indonesian format to a datetime object.
    """
    try:
        # Extract and clean the date string
        date_string_cleaned = date_raw.split(",")[1].strip().replace("WIB", "").strip()

        # Replace Indonesian months with English equivalents
        for ind_month, eng_month in MONTH_MAP.items():
            date_string_cleaned = date_string_cleaned.replace(ind_month, eng_month)

        # Convert to datetime object
        return datetime.strptime(date_string_cleaned, '%d %b %Y %H:%M')
    except Exception as e:
        print(f"Error converting date: {date_raw} - {e}")
        raise
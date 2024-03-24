import re
from datetime import datetime, timedelta
from dateparser import parse


def extract_date_string(text):
    try:
        found = re.search(r'(\d+\D*)(?:\bago|\bnow)', text)
        if found:
            return found.group(1)
        else:
            return None
    except Exception as e:
        raise e


def replace_date_string(text):
    try:
        replacements = {
            r'(\d+)yr': r'\1 year',
            r'(\d+)mon': r'\1 month',
            r'(\d+)w': r'\1 week',
            r'(\d+)d': r'\1 day',
            r'(\d+)h': r'\1 hour',
            r'(\d+)m': r'\1 minute',
            r'(\d+)s': r'\1 second'
        }
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text)
        return text
    except Exception as e:
        raise e


def compare_with_today(text):
    now = datetime.now().date()
    try:
        date = parse(text, settings={'DATE_ORDER': 'DMY'}).date()
        difference = now - date
        exact_date = now - difference
        return date
    except Exception as e:
        raise e
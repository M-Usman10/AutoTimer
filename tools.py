from datetime import datetime

def get_time():
    """
    Returns time using system's current timezone and time data
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def get_date():
    """
    Returns the date in Day-Month-Year digital format
    """
    now = datetime.now()
    current_date = now.strftime("%d-%m-%Y")
    return current_date

def url_to_name(url):
    """
    Returns domain name of the given url
    """
    string_list = url.split('/')
    if len(string_list) >2:
        return string_list[2]
    return ""

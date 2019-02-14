from datetime import datetime

class DateConverter(object):
    @staticmethod
    def convert_to_datetime_from_string(date_string):
        date = datetime.strptime(date_string, "%Y-%m-%d")
        return date
        

    @staticmethod
    def convert_to_string_from_datetime(date):
        return date.strftime("%Y-%m-%d")
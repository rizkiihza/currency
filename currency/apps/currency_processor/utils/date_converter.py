from datetime import datetime

class DateConverter(object):
    @staticmethod
    def convert_to_datetime_from_string(date_string):
        try:
            date = datetime.strptime(date_string, "%Y-%m-%d")
        except:
            raise Exception("incorrect format")
        finally:
            return date
        

    @staticmethod
    def convert_to_string_from_datetime(date):
        return date.strftime("%Y-%m-%d")
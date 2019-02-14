from datetime import datetime

class DatetimeConverter(object):
    @staticmethod
    def convert_to_datetime_from_string(date_string):
        try:
            # convert string in formay YYYY-MM-DD to year
            date = datetime.strftime("%Y-%m-%d")
        except:
            raise Exception("Wrong date format")
        finally:
            return date
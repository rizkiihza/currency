from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.apps import apps
from django.utils import timezone

from currency.api.constant import DEFAULT_CURRENCY
from currency.api.utils.dictionary_converter import DictionaryConverter
from currency.apps.currency_processor.utils.date_converter import DateConverter
from currency.apps.currency_processor.processor.rate_processor import RateProcessor

class RateAPIView(APIView):
    
    def get(self, request):
        try:
            # parse date
            today = timezone.now().date()
            default_date = DateConverter.convert_to_string_from_datetime(today)
            date_string = request.GET.get("date", default_date)
            date = DateConverter.convert_to_datetime_from_string(date_string)

            # parse currency
            currency_from = request.GET.get("currency_from", DEFAULT_CURRENCY)
            currency_to = request.GET.get("currency_to", DEFAULT_CURRENCY)

            rate_data = RateProcessor.get_specific_rate_data(currency_from=currency_from,
                                                        currency_to=currency_to, date=date, with_historical_data=True)

            # convert all date in historical to string
            converted_rate_data = DictionaryConverter.convert_historical_data_date_to_string(rate_data)

            return Response(converted_rate_data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : str(e)}, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            # parse date
            today = timezone.now().date()
            default_date = DateConverter.convert_to_string_from_datetime(today)
            date_string = request.POST.get("date", default_date)
            date = DateConverter.convert_to_datetime_from_string(date_string)

            # parse currency
            currency_from = request.POST.get("currency_from", DEFAULT_CURRENCY)
            currency_to = request.POST.get("currency_to", DEFAULT_CURRENCY)

            # parse value
            value = float(request.POST.get("value"))

            RateProcessor.insert_rate_data(currency_from, currency_to, value, date)

            return Response({"message" : "success"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)

    

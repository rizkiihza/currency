from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.apps import apps
from django.utils import timezone

from currency.api.constant import DEFAULT_CURRENCY
from currency.api.utils.dictionary_converter import DictionaryConverter
from currency.apps.currency_processor.utils.date_converter import DateConverter
from currency.apps.currency_processor.processor.rate_processor import RateProcessor
from currency.api.serializer.rate import RateSerializer

class RateAPIView(APIView):
    
    def get(self, request):
        try:
            # parse date
            date_string = request.GET.get("date")
            date = DateConverter.convert_to_datetime_from_string(date_string)

            # parse currency
            currency_from = request.GET.get("currency_from")
            currency_to = request.GET.get("currency_to")

            rate_data = RateProcessor.get_specific_rate_data(currency_from=currency_from,
                                                        currency_to=currency_to, date=date.date(), with_historical_data=True)

            # convert all date in historical to string
            converted_rate_data = DictionaryConverter.convert_historical_data_date_to_string(rate_data)

            # add date to result
            converted_rate_data['date'] = date_string

            return Response(converted_rate_data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : "Parameter is incomplete"}, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            # parse date
            date_string = request.POST.get("date")
            date = DateConverter.convert_to_datetime_from_string(date_string)

            # parse currency
            currency_from = request.POST.get("currency_from")
            currency_to = request.POST.get("currency_to")

            # parse value
            value = float(request.POST.get("value"))

            rate = RateProcessor.insert_rate_data(currency_from, currency_to, value, date.date())
            serialized_data = RateSerializer(rate)
            
            return Response(serialized_data.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Parameter is incomplete"}, status.HTTP_400_BAD_REQUEST)

    

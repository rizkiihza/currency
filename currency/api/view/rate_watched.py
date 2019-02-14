from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.apps import apps
from django.utils import timezone

from currency.apps.currency_processor.utils.date_converter import DateConverter
from currency.apps.currency_processor.processor.rate_watched_processor import RateWatchedProcessor
from currency.api.utils.dictionary_converter import DictionaryConverter
from currency.api.constant import DEFAULT_CURRENCY

User = apps.get_model("currency_processor", "User")

class RateWatchedAPIView(APIView):

    def get(self, request):
        try:
            # parse date
            today = timezone.now().date()
            default_date = DateConverter.convert_to_string_from_datetime(today)
            date_string = request.GET.get("date", default_date)
            date = DateConverter.convert_to_datetime_from_string(date_string)

            # parse user id
            user_id = int(request.GET.get("user_id"))
            
            user, _ = User.objects.get_or_create(user_id=user_id)
            watchlist_data = RateWatchedProcessor.get_all_watched_rate_data_of_user(user, date)

            # convert all date in historical to string
            converted_rate_data = DictionaryConverter.convert_watchlist_data_date_to_string(watchlist_data)

            return Response(converted_rate_data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            # parse currency to add
            currency_from = request.POST.get("currency_from", DEFAULT_CURRENCY)
            currency_to = request.POST.get("currency_to", DEFAULT_CURRENCY)

            # parse user id
            user_id = int(request.POST.get("user_id"))
            
            RateWatchedProcessor.add_rate_to_watched_rate(user_id, currency_from, currency_to)

            return Response({"message": "success"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)
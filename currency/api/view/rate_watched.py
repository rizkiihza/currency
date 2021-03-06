from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.apps import apps
from django.utils import timezone
import json

from currency.apps.currency_processor.utils.date_converter import DateConverter
from currency.apps.currency_processor.processor.rate_watched_processor import RateWatchedProcessor
from currency.api.utils.dictionary_converter import DictionaryConverter
from currency.api.serializer.rate_watched import RateWatchedSerializer

User = apps.get_model("currency_processor", "User")

class RateWatchedAPIView(APIView):

    def get(self, request):
        try:
            # parse date
            date_string = request.GET.get("date")
            date = DateConverter.convert_to_datetime_from_string(date_string)

            # parse user id
            user_id = int(request.GET.get("user_id"))
            
            user, _ = User.objects.get_or_create(user_id=user_id)
            watchlist_data = RateWatchedProcessor.get_all_watched_rate_data_of_user(user, date.date())

            # convert all date in historical to string
            converted_rate_data = DictionaryConverter.convert_watchlist_data_date_to_string(watchlist_data)

            return Response(converted_rate_data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Parameter is incomplete"}, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            request_body = json.loads(request.body.decode("utf-8"))

            # parse currency to add
            currency_from = request_body["currency_from"]
            currency_to = request_body["currency_to"]

            # parse user id
            user_id = int(request_body["user_id"])
            
            rate_watched = RateWatchedProcessor.add_rate_to_watched_rate(user_id, currency_from, currency_to)

            serialized_data = RateWatchedSerializer(rate_watched)
            
            return Response(serialized_data.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid parameter"}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            request_body = json.loads(request.body.decode("utf-8"))

            # parse currency to delete
            currency_from = request_body["currency_from"]
            currency_to = request_body["currency_to"]

            # parse user id
            user_id = int(request_body["user_id"])

            rate_watched = RateWatchedProcessor.remove_rate_from_watched_rate(user_id, currency_from, currency_to)

            serialized_data = RateWatchedSerializer(rate_watched)

            return Response(serialized_data.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "wrong parameter or there is no object to be deleted"}, 
                                status.HTTP_400_BAD_REQUEST)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.apps import apps
from django.utils import timezone

class RateWatchedAPIView(APIView):

    def get(self, request):
        pass
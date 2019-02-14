from django.urls import path

from currency.api.view.rate_view import RateAPIView
from currency.api.view.rate_watched import RateWatchedAPIView

urlpatterns = [
    path('rate/',
            RateAPIView.as_view(),
            name='rate'),
    path('rate_watched/',
            RateWatchedAPIView.as_view(),
            name='teaser-animation'),
]

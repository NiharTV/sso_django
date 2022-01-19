import imp
from .views import showBookingView
from django.urls import path, include


urlpatterns = [
    path('bookings/', showBookingView.as_view())
]
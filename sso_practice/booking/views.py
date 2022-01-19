from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class showBookingView(APIView):
    def get(self, request):
        return Response({'Message':'You are in booking view'})
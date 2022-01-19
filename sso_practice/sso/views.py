from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User, BlackListedToken
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseForbidden
from django.http import JsonResponse

class VerifyToken(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        token = token.split(' ')
        is_blackListed = BlackListedToken.objects.filter(token=token[1]).exists()
        if is_blackListed:
            print('Blacklisted')
            return HttpResponseForbidden("Invalid Token")
        try:
            payload = jwt.decode(token[1], 'secret', algorithm=['HS256'])
            print('Token verified')
            return Response('None')
        except:
            print('Token unverified')
            return JsonResponse({'error': 'Some error'}, status=401)
            
        
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload ={
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256' ).decode('utf-8')
        user = authenticate(email=email, password=password)
        request.user = User.objects.get(email=email)
        print(request.user)
        response = Response()
        
        #response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt':token
        }
        
        return response
        
class UserView(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        token = token.split(' ')
        is_blackListed = BlackListedToken.objects.filter(token=token[1]).exists()
        if is_blackListed:
            return Response('Invalid Token')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token[1], 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = User.objects.filter(id = payload['id']).first()
        
        serializer = UserSerializer(user)
        
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        #response.delete_cookie('jwt')
        token = request.META.get('HTTP_AUTHORIZATION')
        token = token.split(' ')
        payload = jwt.decode(token[1], 'secret', algorithm=['HS256'])
        user = User.objects.filter(id = payload['id']).first()
        BlackListedToken.objects.create(token=token[1], user=user)
        
        response.data = {
            'Message':'success'
        }
        
        return response
from rest_framework.views import APIView
from rest_framework import generics,permissions
from django.http import HttpResponse , JsonResponse
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from knox.models import AuthToken
from django.middleware.csrf import get_token
from .serializers import *
# Create your views here.
class register(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = Response({
        "user": user_serializer(user, context=self.get_serializer_context()).data,
        })
        return response
class logine(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        response = super(logine, self).post(request, format=None)
        response.set_cookie("id",user.id,path="/",max_age=3600*24*365)
        response.set_cookie("username",user.username,path="/",max_age=3600*24*365)
        response.set_cookie("login_token",response.data["token"],path="/",max_age=3600*24*365)
        return response
class sellers_managing(APIView):
    def post(self , request):
        token = AuthToken.objects.get(token_key=request.COOKIES.get('login_token')[:8])
        request.data['User'] = token.user.id
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({'error':"error occured"}, status=400)
    def put(self , request):
        try:
            token = AuthToken.objects.get(token_key=request.COOKIES.get('login_token')[:8])
            Seller = seller.objects.get(User=token.user)
        except seller.DoesNotExist:
            return Response({'error': 'Seller not found'}, status=404)
        request.data['User'] = token.user.id
        serializer = SellerSerializer(Seller, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
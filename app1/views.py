from rest_framework.views import APIView
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from django.contrib.auth import login
from django.shortcuts import redirect
from django.conf import settings 
from .serializers import *
import requests
import stripe
import math
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
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        api_key = '14fb619c206de8f57d4f8f2b00d0bcab'
        url = f'http://api.ipstack.com/{ip}?access_key={api_key}'
        response = requests.get(url)
        data = response.json() 
        token = AuthToken.objects.get(token_key=request.COOKIES.get('login_token')[:8])
        request.data['User'] = token.user.id
        request.data['lat'] = data['latitude']
        request.data['lng'] = data['longitude']
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
class posts_managing(APIView):
    def post(self , request):
        try: 
            token = AuthToken.objects.get(token_key=request.COOKIES.get('login_token')[:8])
            Seller = seller.objects.get(User=token.user)
            request.data["seller"]=Seller.id
        except seller.DoesNotExist:
            return Response({'error': 'Seller not found'}, status=404)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=404)
    def put(self , request):
        try:
            post = Post.objects.get(id=request.data["id"])
            token = AuthToken.objects.get(token_key=request.COOKIES.get('login_token')[:8])
            Seller = seller.objects.get(User=token.user)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)
        request.data["seller"]=Seller.id
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'error':"error occured"}, status=400)
    def delete(self , request):
        try : 
            post = Post.objects.get(id=request.data["id"])
            post.delete()
            return Response(status=202)
        except:
            return Response({'error':"error occured"}, status=400)
class order_managing(APIView):
    def post(self , request):
        try : 
            token = AuthToken.objects.get(token_key=request.COOKIES.get('login_token')[:8])
            request.data["costumer"] = token.user.id
        except AuthToken.DoesNotExist:
            return Response({'error':"Token expired"}, status=400)
        serializer = OrderSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else :
            return Response({'error':"error occured"}, status=400)
    def put(self , request):
        try : 
            token = AuthToken.objects.get(token_key=request.COOKIES.get('login_token')[:8])
            request.data["costumer"] = token.user.id
        except AuthToken.DoesNotExist:
            return Response({'error':"Token expired"}, status=400)
        try :
            order = Order.objects.get(id= request.data["id"])
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)
        serializer = OrderSerializer(order , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else : 
             return Response({'error':"error occured"}, status=400)
    def delete(self , request):
        try : 
            order = Order.objects.get(id=request.data["id"])
            order.delete()
            return Response(status=202)
        except:
            return Response({'error':"error occured"}, status=400)
@api_view(['GET'])
def dashboard_data(request):
    try: 
        token = AuthToken.objects.get(token_key=request.COOKIES.get('login_token')[:8])
        Seller =  seller.objects.get(User=token.user)
        orders = Order.objects.filter(seller=Seller).count()
    except : 
        if Seller.DoesNotExist:
            return Response({"error":"Seller not found"})
        else :
            return Response({"error":"error occured"})
    response = Response({
        "visitors":Seller.nb_visitors,
        "clicks":Seller.clicks,
        "orders":orders,
        "reviews":0
    })
    return response
class reviews_managing(APIView):
    def post(self , request):
        try : 
            token = AuthToken.objects.get(token_key=request.COOKIES.get('login_token')[:8])
        except AuthToken.DoesNotExist:
            return Response({"error":"Token expired"})
        request.data["User"]=token.user.id
        serializer =  ReviewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        else :
            return Response({"error":"Error occured"})
    def put(self , request):
        try : 
            token = AuthToken.objects.get(token_key=request.COOKIES.get('login_token')[:8])
        except AuthToken.DoesNotExist:
            return Response({"error":"Token expired"})
        request.data["User"]=token.user.id
        try : 
            review =  reviews.objects.get(id=request.data["id"])
            serializer = ReviewsSerializer(review , data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else : 
                return Response({"error":"Error occured"})
        except reviews.DoesNotExist :
            return Response({"error":"Review not found"})
    def delete(self , request):
        try : 
            review =  reviews.objects.get(id=request.data["id"])
            review.delete()
            return Response(status=202)
        except review.DoesNotExist :
            return Response({"error":"Review not found"})
stripe.api_key = settings.STRIP_SECRET_KEY
class StripCheckoutView(APIView): 
    def post(self,request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                {
                    'price': 'price_1NVHVAGt8K1SPn6ZU4T8aMt9',
                    'quantity': 1,
                },
                ],
                payment_method_types =['card',],
                mode='subscription',
                success_url=settings.SITE_URL+ '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL+ '?canceled=true',
            )
        except Exception as e:
            return Response({"error":"quelque chose s'est mal passé lors de la création d'une session pour stripe checkout"+str(e)} , status = 500)
        return redirect(checkout_session.url)
def get_distance(lat1,lng1,lat2,lng2):
    radius = 3959  # Earth's radius in miles
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance
@api_view(['GET'])
def recommandation_location(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    api_key = '14fb619c206de8f57d4f8f2b00d0bcab'
    url = f'http://api.ipstack.com/{ip}?access_key={api_key}'
    response = requests.get(url)
    data = response.json() 
    lat1 =  data['latitude']
    lng1 = data['longitude']
    sellers = seller.objects.all() 
    for s in sellers:
        distance = get_distance(lat1, lng1,s.lat, s.lng)
        seller.distance = distance
    sellers = [seller for seller in sellers if seller.distance <= 1000]
    sellers = sorted(sellers, key=lambda seller: seller.distance)
    serializer = SellerSerializer(sellers , many=True)
    return Response(serializer.data , status = 200)
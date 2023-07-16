from rest_framework.views import APIView
from rest_framework import generics,permissions
from django.http import HttpResponse , JsonResponse
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from knox.models import AuthToken
from rest_framework.decorators import api_view
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
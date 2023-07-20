"""
URL configuration for revo_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , re_path , include
from app1.views import *
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from app1 import views
from asynch_notif import routing
urlpatterns = [
    path('register/',register.as_view()),
    path("login/", logine.as_view()),
    path("seller/", sellers_managing.as_view()),
    path("post/", posts_managing.as_view()),
    path("order/", order_managing.as_view()),
    path("statistics/",views.dashboard_data),
    path("post/reviews/",reviews_managing.as_view()),
    path("Stripe/",StripCheckoutView.as_view()),
    path("recomandation/sellers/",views.recommandation_location),
    path('admin/', admin.site.urls),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

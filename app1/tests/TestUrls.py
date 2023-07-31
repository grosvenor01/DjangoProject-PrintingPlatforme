from django.test import SimpleTestCase
from django.urls import reverse , resolve 
from app1.views import *

class TestUrls(SimpleTestCase):
    def test_register_url(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class,register)

    def test_login_url(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class,logine)
        
    def test_seller_url(self):
        url = reverse('seller')
        self.assertEquals(resolve(url).func.view_class, sellers_managing)

    def test_post_url(self):
        url = reverse('post')
        self.assertEquals(resolve(url).func.view_class, posts_managing)

    def test_order_url(self):
        url = reverse('order')
        self.assertEquals(resolve(url).func.view_class, order_managing)

    def test_reviews_url(self):
        url = reverse('reviews')
        self.assertEquals(resolve(url).func.view_class, reviews_managing)

    def test_stripe_url(self):
        url = reverse('stripe')
        self.assertEquals(resolve(url).func.view_class, StripCheckoutView)

    def test_statistics_url(self):
        url = reverse('statistics')
        self.assertEquals(resolve(url).func, dashboard_data)

    def test_recommandation_location_url(self):
        url = reverse('rec_location')
        self.assertEquals(resolve(url).func,recommandation_location)
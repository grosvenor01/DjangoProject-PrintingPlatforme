from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.forms import DateTimeInput
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
User = get_user_model()
class seller(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    photo= models.ImageField(upload_to="photos/sellers", null = True)
    specialiste = models.CharField(max_length = 400)
    available = models.CharField(max_length=10 , choices=(("True","True"),("False","False"))) # available for work
    address = models.CharField(max_length = 400)
    lat = models.FloatField()
    lng = models.FloatField()
    phone = PhoneNumberField()
    birthday = models.DateField()
    sex = models.CharField(max_length=10 , choices=(("Male","Male"),("Female","Female")))
    description = models.TextField()
    skills = models.CharField(max_length=400, blank=True)
    reviews = models.IntegerField()
    #Dashboard attributes
    nb_visitors = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
class Post(models.Model):
    seller = models.ForeignKey(seller , on_delete=models.CASCADE)
    post_video = models.FileField(upload_to="videos",null=True,validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    post_image = models.ImageField(upload_to="photos/posts", null=True )
    post_title = models.CharField(max_length=200)
    post_description = models.TextField()
    materials = MultiSelectField(max_length=100 , choices=(
                                        ("PLA (Polylactic Acid)","PLA (Polylactic Acid)"),
                                        ("ABS (Acrylonitrile Butadiene Styrene)","ABS (Acrylonitrile Butadiene Styrene)"),
                                        ("PET (Polyethylene Terephthalate)","PET (Polyethylene Terephthalate)"),
                                        ("NYLON","NYLON"),
                                        ("TPU (Thermoplastic Polyurethane)","TPU (Thermoplastic Polyurethane)"),
                                        ("Polycarbonate","Polycarbonate"),
                                        ("Metal","Metal"),
                                        ("Wood","Wood"),
                                        ("Carbon Fiber","Carbon Fiber"),
                                        ("Glass","Glass")
    ))
    post_keywords = models.CharField(max_length=300 , blank=True)
    maxSize_height = models.IntegerField()
    maxSize_width = models.IntegerField()
    nb_reviews = models.IntegerField(default = 0)
    free_delivery = models.CharField(max_length=20,choices=(("Available","Available"),("Not available","Not available")))
    return_delivery = models.CharField(max_length=20,choices=(("Available","Available"),("Not available","Not available")))
    date = models.DateTimeField(default=timezone.now)
class Order(models.Model):
    seller = models.ForeignKey(seller, on_delete=models.CASCADE) 
    date = models.DateTimeField(default=timezone.now)
    costumer = models.ForeignKey(User , on_delete=models.CASCADE)
    location = models.CharField(max_length=200) 
    total_amount = models.FloatField()
    status = models.CharField(max_length=100, choices=(('pending','pending'),('shipped','shipped'),('delivered','delivered')))
class reviews(models.Model):
    rating = models.IntegerField()
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    date=models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    
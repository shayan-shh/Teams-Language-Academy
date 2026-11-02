from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=40,default='')
    
    def __str__(self):
        return self.name
    

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=25, blank=True)
    address1 = models.CharField(max_length=250, blank=True)
    address2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=25, blank=True)
    state = models.CharField(max_length=25, blank=True)
    zipcode = models.CharField(max_length=25, blank=True)
    country = models.CharField(max_length=25, blank=True, default='Iran')
    oldCard = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to="images/")

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile,sender=User)

    
class Course(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500, default='', blank=True)
    price = models.DecimalField(default=0, decimal_places=0, max_digits=150)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    picture = models.ImageField(upload_to='upload/course/')  
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=14, decimal_places=0, null=True, blank=True)
    length = models.CharField(default=0, max_length=250)
    days = models.CharField(max_length=40,default='')
    teacher_name = models.CharField(max_length=40,default='')

    def __str__(self):
        return self.name



from django.db import models
from django.contrib.auth.models import User
from Course.models import Course


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    amount_paid = models.DecimalField(max_digits=13, decimal_places=0)
    date_ordered = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Order - {str(self.id)}' 
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=13,decimal_places=0)

    def __str__(self):
        return f'Order Item - {self.id}'

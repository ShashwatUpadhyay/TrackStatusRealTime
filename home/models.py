from django.db import models
from django.contrib.auth.models import User
import string
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# Create your models here.
class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    image = models.URLField(max_length=500, default='')

    def __str__(self):
        return self.name
    
order_maper = { 
    'Order Received': 10,
    'Baking': 30,
    'Baked': 60,
    'Out For Delivery': 80,
    'Order Delivered': 100,
}

class Order(models.Model):
    status_choices = [
        ('Order Received', 'Order Received'),
        ('Baking', 'Baking'),
        ('Baked', 'Baked'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Order Delivered', 'Order Delivered'),
    ]
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=status_choices, default='Order Received')
    
    @property
    def  get_prgress(self):
        return str(order_maper[self.status])
    
    def __str__(self):
        return self.pizza.name + " - " + self.status 
    
    def generateOrderId(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.order_id = self.generateOrderId()
        super(Order, self).save(*args, **kwargs)
        
    @staticmethod
    def give_order_detail(order_id):
        order = Order.objects.get(order_id=order_id)
        return {
            "order_id": order.order_id,
            "pizza": order.pizza.name,
            "amount": order.amount,
            "status": order.status,
            "date": str(order.order_date),
            "progress": order_maper[order.status],
        }
    
@receiver(post_save, sender=Order)
def order_status_handler(sender ,instance , created , **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {
            "order_id": instance.order_id,
            "pizza": instance.pizza.name,
            "amount": instance.amount,
            "status": instance.status,
            "date": str(instance.order_date),
            "progress": order_maper[instance.status],
        }
        
        async_to_sync(channel_layer.group_send)(    
            f'order_{instance.order_id}',
            {
                'type': 'order_status',
                'value': json.dumps(data),
            }
        )          
            
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Customer

User=get_user_model()

@receiver(post_save,sender=User)
def on_user_create(sender, instance, *args,**kwargs):
    print("user was created!!!")
    
    Customer.objects.get_or_create(
        user=instance
        
    )
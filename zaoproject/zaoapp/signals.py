from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Cart


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """Create a Cart automatically when a new User is created."""
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_cart(sender, instance, **kwargs):
    """Save the user's cart if it exists."""
    if hasattr(instance, 'cart'):
        instance.cart.save()

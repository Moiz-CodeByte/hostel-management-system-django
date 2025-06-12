from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from .models import HostelOwner
from django.contrib.auth import get_user_model
from django.db import transaction

@receiver(post_save, sender=SocialAccount)
def create_or_update_user_from_social_account(sender, instance, created, **kwargs):
    """
    Signal handler to create or update a HostelOwner profile when a user signs in with Google.
    """
    if instance.provider == 'google':
        # Get user data from the social account
        user = instance.user
        extra_data = instance.extra_data
        
        # Update user profile with Google data if available
        with transaction.atomic():
            # Update name if available
            if 'name' in extra_data and not user.name:
                user.name = extra_data.get('name', '')
            
            # Update email if available and not already set
            if 'email' in extra_data and not user.email:
                user.email = extra_data.get('email', '')
                
            # Set default empty values for required fields if they're not set
            if not user.phone_number:
                user.phone_number = ''
                
            if not user.address:
                user.address = ''
                
            user.save()
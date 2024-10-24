from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Uchumi-z!'
        message = f"Hi {instance.username},\n\nWelcome to our platform! We're glad to have you with us. my name is osbon the creator of uchumi-z and we are excited to have you abord and take your financial journey to the next level "
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

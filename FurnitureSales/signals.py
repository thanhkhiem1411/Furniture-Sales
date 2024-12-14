from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.conf import settings
from django.core.mail import send_mail 
from app.models import UserProfile, OtpToken


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def register_user(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('Profile created!')
    
        # email credentaials
        subject="Email Verification"
        message = f"""
        Hi {instance.username}, welcome to our website!
        You are register successfully. Now you are a member of our website.
        We hope you enjoy our service!
        """
        sender = settings.EMAIL_HOST_USER
        receiver = [instance.email]

        #send email
        send_mail(
            subject,
            message,
            
            sender,
            receiver,
            fail_silently=False,
        )
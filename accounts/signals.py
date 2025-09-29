from django.db.models.signals import post_save
from accounts.models import CustomUser
from django.dispatch import receiver
from .models import Profile

#新しいユーザーが作成された際に自動的にProfileを作成するためシグナルを利用
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
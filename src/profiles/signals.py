from django.db.models.signals import post_save , pre_delete
from django.contrib.auth.models import User 
from django.dispatch import receiver
from .models import Profile ,Relationship


@receiver(post_save , sender = User)
def post_save_create_profile(sender , instance , created , **kwargs):
    if created:
        Profile.objects.create(user=instance)



@receiver(post_save , sender = Relationship)
def post_save_add_to_friends(sender , instance , created , **kwargs):
    sender_ = instance.sender
    recevier_ = instance.recevier
    if instance.status =='accepted':
        sender_.friends.add(recevier_.user)
        recevier_.friends.add(sender_.user)
        sender_.save()
        recevier_.save()


@receiver(pre_delete , sender = Relationship)
def pre_delete_remove_from_friends(sender , instance ,**kwargs):
    sender = instance.sender
    recevier = instance.recevier
    sender.friends.remove(recevier.user)
    recevier.friends.remove(sender.user)
    sender.save()
    recevier.save()
# # We need to add Django signals so every new user has a default profile picture as well
#
# from django.db.models.signals import post_save  # import a post_save signal when a user is created
# from django.contrib.auth.models import User  # import the built-in User model, which is a sender
# from django.dispatch import receiver  # import the receiver
# from .models import UserProfile
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.user_profile.save()


# from django.db.models.signals import pre_delete, post_delete
# from .models import Student
# from django.dispatch import receiver
#
#
# @receiver(pre_delete, sender=Student)
# def pre_delete_profile(sender, **kwargs):
#     print("You are about to delete something")
#
#
# @receiver(post_delete, sender=Student)
# def delete_profile(sender, **kwargs):
#     print("You have just deleted a student")
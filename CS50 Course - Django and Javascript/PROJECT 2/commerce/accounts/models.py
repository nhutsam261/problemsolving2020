from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from autoslug import AutoSlugField
from auctions.models import Watchlist

# Create your models here.


class User(AbstractUser):
	pass


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profile_pics')
	slug = AutoSlugField(populate_from='user')
	bio = models.CharField(max_length=255, blank=True)
	friends = models.ManyToManyField("Profile", blank=True)

	def __str__(self):
		return str(self.user.username)

	def get_absolute_url(self):
		return "/accounts/user/{}".format(self.slug)


# make a profile as soon as we create the user
def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
	if created:
		try:
			Profile.objects.create(user=instance)
			Watchlist.objects.create(user=instance)
		except:
			pass
        
post_save.connect(post_save_user_model_receiver, sender=User)


class FriendRequest(models.Model):
	to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
	from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username, self.to_user.username)



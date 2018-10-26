from django.db import models
from registration.models import User
from registration.models import get_sentinel_user
from taggit.managers import TaggableManager
from django.utils.timezone import now
from django.urls import reverse

CATEGORIES = (
	('loc', 'Nacionales'),
	('int', 'Internacionales'),
	('opn', 'Opinión'),
	('ent', 'Entretenimiento'),
	('dep', 'Deportes'),
)

SECS_IN_HOUR = float(60 * 60)
GRAVITY = 1.2

class Link(models.Model):
	url = models.URLField(max_length=250)
	title = models.CharField(max_length=120)
	rank = models.FloatField(default=0.0)
	user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name='links')
	date = models.DateTimeField(auto_now_add=True)
	text = models.TextField(max_length=500)
	category = models.CharField(max_length=3, choices=CATEGORIES)
	tags = TaggableManager()

	def __unicode__(self):
		return self.title

	# votes divided by the age in hours to the gravityth power.
	def set_rank(self):
		votes = self.votes.count() - 1
		delta = now() - self.date
		link_hour_age = delta.total_seconds() // SECS_IN_HOUR
		self.rank = votes / pow((link_hour_age + 2), GRAVITY)
		self.save()

	def get_absolute_url(self):
		return reverse('link_detail', args=[str(self.id)])

class Vote(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
	link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='votes')

	def __unicode__(self):
		return "%s upvoted %s" % (self.voter.username, self.link.title)

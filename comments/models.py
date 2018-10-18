from django.db import models
from registration.models import get_sentinel_user
from registration.models import User
from links.models import Link

class Comment(models.Model):
	link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
	text = models.TextField(max_length=500)
	date = models.DateTimeField(auto_now_add=True)
	corr = models.IntegerField()
	deleted = models.BooleanField(default=False)
	hidden = models.BooleanField(default=False)

	def delete(self):
		self.deleted = True
		self.text = "El comentario ha sido eliminado."
		self.save()

class Point(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='points')
	value = models.IntegerField()


from django.contrib import admin
from comments.models import Comment, Point

class CommentAdmin(admin.ModelAdmin): pass
admin.site.register(Comment, CommentAdmin)

class PointAdmin(admin.ModelAdmin): pass
admin.site.register(Point, PointAdmin)


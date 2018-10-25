from django.urls import reverse
from django import template
from tld import get_fld
from hashlib import md5
from links.models import CATEGORIES
from django.conf import settings
register = template.Library()

# filters

@register.filter(name='domain')
def domain(value):
	return get_fld(value)

@register.filter(name='gravatar')
def gravatar(user, size=35):
    email = str(user.email.strip().lower()).encode('utf-8')
    email_hash = md5(email).hexdigest()
    url = "//www.gravatar.com/avatar/{0}?s={1}&d=identicon&r=PG"
    return url.format(email_hash, size)

@register.filter(name='comment_total_points')
def comment_total_points(query):
	positives = query.filter(value = 1).count()
	negatives = query.filter(value = -1).count()
	return positives + negatives

@register.filter(name='comment_karma')
def comment_karma(query):
	positives = query.filter(value = 1).count()
	negatives = query.filter(value = -1).count()
	return positives - negatives

from links.models import Vote
from comments.models import Point
@register.filter(name='user_karma')
def user_karma(user):
	# karma from link submissions
	user_links = user.links.all()
	links_karma = Vote.objects.filter(link__in=user_links).count()
	# karma from user comments
	user_comments = user.comments.all()
	positives = Point.objects.filter(comment__in=user_comments, value=1).count()
	negatives = Point.objects.filter(comment__in=user_comments, value=-1).count()
	comments_karma = positives - negatives
	# return total karma
	total_karma = links_karma + comments_karma
	return total_karma

## templatetags

# returns the name of the filtered category
@register.simple_tag(takes_context=True)
def page_title(context):
	request = context['request']
	cat = request.GET.get('cat', None)
	tag = request.GET.get('tag', None)
	path = request.path
	if cat is not None:
		page_title = dict(CATEGORIES)[cat]
	elif tag is not None:
		page_title = 'tag: ' + tag
	elif path == '/top/':
		page_title = 'Top de la semana'
	elif path == '/latest/':
		page_title = 'Últimas enviadas'
	else:
		page_title = "Portada"
	return page_title

# preserves existing querystring with pagination
@register.simple_tag(takes_context=True)
def params(context):
	request = context['request']
	params = request.GET.copy()
	params.pop('page', True)
	if len(params) >= 1:
		params = params.urlencode() + '&'
	else:
		params = ""
	return params

# returns button color for top and latest
@register.simple_tag(takes_context=True)
def color_btn(context):
	request = context['request']
	if request.path == reverse('link_latest'):
		return 'secondary'
	elif request.path == reverse('link_top'):
		return 'danger'
	else:
		return 'primary'

# returns button color for top and latest
@register.simple_tag(takes_context=True)
def color_txt(context):
	request = context['request']
	if request.path == reverse('link_latest'):
		return 'dark'
	elif request.path == reverse('link_top'):
		return 'danger'
	else:
		return 'primary'

# analytics on / off
@register.simple_tag()
def debug():
	debug = settings.DEBUG
	return debug

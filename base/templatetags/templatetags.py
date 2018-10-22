from django.urls import reverse
from django import template
from tld import get_fld
from hashlib import md5
from links.models import CATEGORIES
register = template.Library()

@register.filter(name='domain')
def domain(value):
	return get_fld(value)

@register.filter(name='gravatar')
def gravatar(user, size=35):
    email = str(user.email.strip().lower()).encode('utf-8')
    email_hash = md5(email).hexdigest()
    url = "//www.gravatar.com/avatar/{0}?s={1}&d=identicon&r=PG"
    return url.format(email_hash, size)

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

# returns the name of the filtered category
@register.simple_tag(takes_context=True)
def category(context):
	request = context['request']
	cat = request.GET.get('cat', None)
	if cat is not None:
		category = dict(CATEGORIES)[cat]
	else:
		category = "Portada"
	return category

@register.filter(name='sub')
def sub(value=0, arg=0):
	return value - arg

@register.filter(name='total')
def total(query):
	positives = query.filter(value = 1).count()
	negatives = query.filter(value = -1).count()
	return positives + negatives

@register.filter(name='karma')
def karma(query):
	positives = query.filter(value = 1).count()
	negatives = query.filter(value = -1).count()
	return positives - negatives

@register.simple_tag(takes_context=True)
def color_btn(context):
	request = context['request']
	if request.path == reverse('link_latest'):
		return 'secondary'
	elif request.path == reverse('link_top'):
		return 'danger'
	else:
		return 'primary'

@register.simple_tag(takes_context=True)
def color_txt(context):
	request = context['request']
	if request.path == reverse('link_latest'):
		return 'dark'
	elif request.path == reverse('link_top'):
		return 'danger'
	else:
		return 'primary'

from links.models import Link
from django import template
register = template.Library()

@register.inclusion_tag('links/_latest.html')
def latest():
	queryset = Link.objects.all().order_by('-date')[:10]
	return {'latest': queryset}

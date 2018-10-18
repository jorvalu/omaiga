from taggit.models import TaggedItem, Tag
from django import template
from django.db.models import Count, Sum

F_MIN = 10 # min font size 
F_MAX = 42 # max font size

register = template.Library()

from links.models import Link
from datetime import datetime, timedelta

def get_queryset(days_ago):
    # filter links submitted last month
    last_month = datetime.today() - timedelta(days_ago)
    links_ids = Link.objects.filter(date__gte=last_month)
    # retrieve tag items related to those links
    tagged_item = TaggedItem.objects.filter(object_id__in=links_ids)
    # group by name and count number of links
    return tagged_item.values('tag__name').annotate(num_times=Count('object_id'))

@register.inclusion_tag('links/_tagcloud.html')
def tagcloud(days_ago):
    queryset = get_queryset(days_ago)
    num_times = queryset.values_list('num_times', flat=True)
    for tag in queryset:
        size = (tag['num_times'] / max(num_times)) * (F_MAX - F_MIN) + F_MIN
        tag['size'] = int(size)
    return {'tags': queryset}
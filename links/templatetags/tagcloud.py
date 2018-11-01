from taggit.models import TaggedItem, Tag
from django.db.models import Count, Sum
from django.utils import timezone
from links.models import Link
from django import template

F_MIN = 10 # min font size
F_MAX = 42 # max font size

register = template.Library()

def get_queryset(days_ago):
    if days_ago is not None: # tagcloud of links submitted in the last x days
        num_days = timezone.now() - timezone.timedelta(days=days_ago)
        links_ids = Link.objects.filter(date__gte=num_days)
    else: # tagcloud of all links
        links_ids = Link.objects.all()
    tagged_item = TaggedItem.objects.filter(object_id__in=links_ids)
    tagged_item = tagged_item.values('tag__name').annotate(num_times=Count('object_id'))
    return tagged_item

@register.inclusion_tag('links/_tagcloud.html')
def tagcloud(days_ago):
    queryset = get_queryset(days_ago)
    num_times = queryset.values_list('num_times', flat=True)
    for tag in queryset:
        size = (tag['num_times'] / max(num_times)) * (F_MAX - F_MIN) + F_MIN
        tag['size'] = int(size)
    return {'tags': queryset}

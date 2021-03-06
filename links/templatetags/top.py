from datetime import datetime, timedelta
from django.db.models import Count
from links.models import Link
from django import template
register = template.Library()

@register.inclusion_tag('links/_top.html')
def top():
    queryset = Link.objects.all()
    date_filter = datetime.today() - timedelta(7)
    queryset = queryset.filter(date__gte=date_filter)
    queryset = queryset.annotate(num_votes=Count('votes')).order_by('-num_votes')[:10]
    return {'top': queryset}

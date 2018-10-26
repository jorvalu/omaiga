from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from links.models import Link

class LinkSitemap(Sitemap):

    def items(self):
        return Link.objects.all()

class StaticSitemap(Sitemap):

    def items(self):
        return ['about']

    def location(self, item):
        return reverse(item)

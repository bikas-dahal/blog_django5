from django.contrib.sitemaps import Sitemap

from .models import Post
from taggit.models import TaggedItem

class TagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return TaggedItem.objects.values_list('tag__name', flat=True).distinct()

    def location(self, obj):
        return f'/blog/tag/{obj}/'

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Post.published.all()
    def lastmod(self, obj):
        return obj.updated
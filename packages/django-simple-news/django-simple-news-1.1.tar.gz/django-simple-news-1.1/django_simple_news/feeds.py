from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django_simple_news.models import NewsItem


class NewsFeed(Feed):
    link = ''

    def title(self):
        return u"%s" % Site.objects.get_current().name

    def description(self):
        return u'Latest news from %s' % Site.objects.get_current().name

    def items(self):
        return NewsItem.on_site.published(5)

    def item_description(self, obj):
        return obj.snippet

    def item_pubdate(self, item):
        from datetime import datetime
        return datetime(item.date.year, item.date.month, item.date.day)


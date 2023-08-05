# Copyright (c) 2010 ActiveState Software Inc.

from django.contrib.syndication.feeds import Feed
from pluto.models import Entry

class EntriesFeed(Feed):
    def items(self):
        return Entry.objects.filter(is_public=True).order_by("-pub_date")
    
    def item_link(self, item):
        return item.link

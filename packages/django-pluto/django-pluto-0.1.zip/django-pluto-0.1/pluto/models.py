# Copyright (c) 2010 ActiveState Software Inc.

from django.db import models
from django.utils.translation import ugettext as _
import datetime, time
import feedparser
import re
from httplib2 import Http
from urlparse import urljoin

link_finder = re.compile(r"<link (.*?)/?>", re.DOTALL)
attr_parser = re.compile(r"\b(?P<name>\w+)\s*=\s*(?P<quote>\042|\047)(?P<value>.*?)(?P=quote)", re.DOTALL)

class NotRefreshedWarning(UserWarning): pass

class Entry(models.Model):
    """Every `Entry` represents one article/feed entry on the webpage.
    """
    link = models.URLField(_("Link"), verify_exists=False)
    
    feed_url = models.URLField(_("Feed URL"), verify_exists=False, blank=True)
    guid = models.CharField(_("GUID"), max_length=200, blank=True)
    is_public = models.BooleanField(_("Is public?"), default=False)
    
    title = models.CharField(_("Title"), max_length=200, blank=True)
    description = models.TextField(_("Description"), blank=True)
    pub_date = models.DateTimeField(_("Published Date"), null=True, blank=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Feed entry"
        verbose_name_plural = "Feed entries"
    
    def __unicode__(self):
        return _(u"'%s' from %s") % (
            self.title or _("(No title)"),
            self.feed_url or _("(No feed)")
        )
    
    def save(self):
        first_time = (not self.id)
        super(Entry, self).save()
        if first_time:
            try:
                self.refresh()
            except NotRefreshedWarning:
                pass  # no way to message the user, not my problem
    
    def refresh(self):
        """Tries to refresh the entry from the original feed. Raises a
        NotRefreshedWarning if the entry couldn't be refreshed.
        """
        if self.link and not self.feed_url:
            self._find_feed()
        
        if not (self.feed_url and (self.guid or self.link)):
            raise NotRefreshedWarning(_("Not enough information to retrieve the entry. Please provide the feed url <b>and</b> a link or GUID."))
        
        self._update_from_feed()
        self.save()
    
    def _find_feed(self):
        """Tries to find the location of the feed in the post.
        """
        resp, contents = Http().request(self.link)
        if resp.status != 200:
            return
        
        feeds = []
        for link_str in link_finder.findall(contents):
            attr_strs = attr_parser.finditer(link_str)
            attrs = dict((s.group('name'), s.group('value')) for s in attr_strs)
            if attrs.get("rel", None) == "alternate" and \
               attrs.get("type", None) in ("application/rss+xml",
                                           "application/atom+xml"):
                feeds.append(attrs["href"])
        
        if not feeds:
            return
        
        # just use the first found feed for now
        href = feeds[0]
        self.feed_url = urljoin(self.link, href)
    
    def _update_from_feed(self):
        """Reads the feed, tries to find the entry and updates itself.
        """
        feed = feedparser.parse(self.feed_url)
        if self.guid:
            for entry in feed.entries:
                if entry.id == self.guid:
                    break
            else:
                raise NotRefreshedWarning(_("GUID not found in feed. Maybe the post is too old and not in the feed anymore."))
        elif self.link:
            for entry in feed.entries:
                if entry.link == self.link:
                    break
            else:
                raise NotRefreshedWarning(_("Link not found in feed. Either the feed contains different links than the website or the feed url is wrong. Try to copy the links directly from the feed."))
        else:
            raise NotRefreshedWarning(_("Link and GUID are missing."))
        
        self.title = entry.title
        self.description = entry.description
        self.guid = entry.id
        pub_date = _firstof(entry, 'published_parsed', 'updated_parsed')
        self.pub_date = datetime.datetime.fromtimestamp(time.mktime(pub_date))


# utility functions

def _firstof(obj, *args):
    # returns the value of the first attribute in args that exists in obj or
    # returns None
    for arg in args:
        try:
            return getattr(obj, arg)
        except AttributeError:
            pass
    return None

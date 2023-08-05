# Copyright (c) 2010 ActiveState Software Inc.

from django.contrib import admin
from django.utils.translation import ugettext as _
from pluto.models import Entry, NotRefreshedWarning

def refresh_entries(modeladmin, request, queryset):
    for entry in queryset:
        try:
            entry.refresh()
        except NotRefreshedWarning, w:
            request.user.message_set.create(
                message=_("Warning: %s was not refreshed: %s") % (entry, w))
refresh_entries.short_description = "Refresh entries"

def publish_entries(modeladmin, request, queryset):
    queryset.update(is_public=True)
publish_entries.short_description = _("Publish entries")

class EntryAdmin(admin.ModelAdmin):
    model = Entry
    list_display = ('__unicode__', 'is_public')
    actions = (refresh_entries, publish_entries)

admin.site.register(Entry, EntryAdmin)

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Entry(models.Model):
    title = models.CharField(max_length = 40)
    snippet = models.CharField(max_length = 150, null=True, blank=True)
    body = models.CharField(max_length = 10000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add = True)
    date = models.DateField(null=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    remind = models.BooleanField(default=False)
    activity_type = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
	if self.title:
	    return unicode(self.creator) + u" - " + self.title
	else:
	    return unicord(self.creator) + u" - " + self.snippet[:40]

    def  short(self):
	if self.snippet:
	    return "<i>%s</i>" % (self.title, self.snippet)
	else:
	    return self.title
    short.allow_tags = True

    class Meta:
	verbose_name_plural = "entries"

##Admin

class EntryAdmin(admin.ModelAdmin):
    list_disply = ["creator", "date", "title", "snippet"]
    list_filter = ["creator"]


#admin.site.register(Entry, EntryAdmin)

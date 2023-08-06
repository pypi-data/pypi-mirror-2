import datetime

from django.db import models
from django.db.models.query import QuerySet
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from cms.utils.placeholder import PlaceholderNoAction

from cms.models import CMSPlugin

import tagging
from tagging.fields import TagField

from simple_translation.actions import SimpleTranslationPlaceholderActions
from djangocms_utils.fields import M2MPlaceholderField

class PublishedEntriesQueryset(QuerySet):
    
    def published(self):
        return self.filter(is_published=True, pub_date__lte=datetime.datetime.now())
        
class EntriesManager(models.Manager):
    
    def get_query_set(self):
        return PublishedEntriesQueryset(self.model)
                            
class PublishedEntriesManager(EntriesManager):
    """
        Filters out all unpublished and items with a publication date in the future
    """
    def get_query_set(self):
        return super(PublishedEntriesManager, self).get_query_set().published()
                    
CMSPLUGIN_BLOG_PLACEHOLDERS = getattr(settings, 'CMSPLUGIN_BLOG_PLACEHOLDERS', ('main',))
              
class Entry(models.Model):
    is_published = models.BooleanField(_('is published'))
    pub_date = models.DateTimeField(_('published'), default=datetime.datetime.now)
 
    placeholders = M2MPlaceholderField(actions=SimpleTranslationPlaceholderActions(), placeholders=CMSPLUGIN_BLOG_PLACEHOLDERS)
    
    tags = TagField()
    
    objects = EntriesManager()
    published = PublishedEntriesManager()
    
    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        ordering = ('-pub_date', )

tagging.register(Entry, tag_descriptor_attr='entry_tags')

class EntryTitle(models.Model):
    entry = models.ForeignKey(Entry, verbose_name=_('entry'))
    language = models.CharField(_('language'), max_length=15, choices=settings.LANGUAGES)
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True)
    author = models.ForeignKey('auth.User', null=True, blank=True)
    
    def __unicode__(self):
        return self.title
        
    def _get_absolute_url(self):
        language_namespace = 'cmsplugin_blog.middleware.MultilingualBlogEntriesMiddleware' in settings.MIDDLEWARE_CLASSES and '%s:' % self.language or ''
        return ('%sblog_detail' % language_namespace, (), {
            'year': self.entry.pub_date.strftime('%Y'),
            'month': self.entry.pub_date.strftime('%m'),
            'day': self.entry.pub_date.strftime('%d'),
            'slug': self.slug
        })
    get_absolute_url = models.permalink(_get_absolute_url)

    class Meta:
        verbose_name = _('entry title')
        verbose_name_plural = _('entry titles')
    
class LatestEntriesPlugin(CMSPlugin):
    """
        Model for the settings when using the latest entries cms plugin
    """
    limit = models.PositiveIntegerField(_('Number of entries items to show'), 
                    help_text=_('Limits the number of items that will be displayed'))
                    
    current_language_only = models.BooleanField(_('Only show entries for the current language'))

# -*- coding: utf-8 -*-
from Acquisition import Explicit
from zope.interface import implements
from zope.component import adapts
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plumi.content.browser.interfaces import IAbstractCatalogBrain
from interfaces import IPlumiVideoBrain, ITopicsProvider
from zope.component import getUtility
from Products.CMFCore.interfaces import IPropertiesTool
from collective.transcode.star.interfaces import ITranscodeTool

class PlumiVideoBrain( Explicit ):
    u"""Basic Plumi implementation of a video brain renderer.
    """
    
    implements(IPlumiVideoBrain)
    adapts(IAbstractCatalogBrain, ITopicsProvider)

    template = ViewPageTemplateFile('templates/video_brain.pt')
    __allow_access_to_unprotected_subobjects__ = True
    
    def __init__(self, context, provider):
        self.context = context
        self.video = context
        self.url = context.getURL()
        self.video_title = context.Title or context.id or 'Untitled'
        self.__parent__ = provider
        self.categories = provider.get_categories_info(context['getCategories'])
        self.countries = None
        self.request = getattr(self.context, "REQUEST", None)
        pprop = getUtility(IPropertiesTool)
        self.tt = getUtility(ITranscodeTool)

    def render_listing(self):
        return self.template.__of__(self.request)(show_title=True,feature_video=False)
    
    def render(self):
        return self.template.__of__(self.request)(show_title=False,feature_video=False)

    def render_feature_video(self):
        return self.template.__of__(self.request)(show_title=False,feature_video=True)

    @property
    def country_dict(self):
        return self.__parent__.get_country_info(self.video['getCountries'])

    @property
    def post_date(self):
        date = self.video.effective
        if not date or date.year() == 1000:
            date = self.video.created
        return self.context.toLocalizedTime(date)

    def transcoded(self, uid, profile):
        try:
            entry = self.tt[uid]['video_file'][profile]
            return '%s/%s' % (entry['address'], entry['path'])
        except:
            return False

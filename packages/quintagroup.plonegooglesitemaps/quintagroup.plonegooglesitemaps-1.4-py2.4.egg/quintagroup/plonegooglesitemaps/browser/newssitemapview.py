import re
from DateTime import DateTime
from commonview import *
from zope.component import getMultiAdapter
from plone.memoize.view import memoize

reTrailingParenthtical = re.compile("\s*\(.*\)\s*", re.S)

class NewsSitemapView(CommonSitemapView):
    """
    News Sitemap browser view
    """
    implements(ISitemapView)

    @property
    def additional_maps(self):
        return (
            ('publication_date', lambda x:DateTime(x.EffectiveDate).strftime("%Y-%m-%d")),
            ('keywords', lambda x:', '.join(x.Subject)),
            ('title', lambda x:x.Title or x.getId or x.id),
            ('name', lambda x:reTrailingParenthtical.sub("",x.Title)),
            ('language', lambda x:x.Language or self.default_language()),
            ('access', lambda x:x.gsm_access or ""),
            ('genres', lambda x:x and ", ".join(x.gsm_genres) or ""),
            ('stock', lambda x:x.gsm_stock or ""),
        )

    @memoize
    def default_language(self):
        pps = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        return pps.default_language

    def getFilteredObjects(self):
        path = self.portal.getPhysicalPath()
        portal_types = self.context.getPortalTypes()
        review_states = self.context.getStates()
        min_date = DateTime() - 3
        res = self.portal_catalog(path = path,
                portal_type = portal_types,
                review_state = review_states,
                effective = {"query": min_date,
                             "range": "min" })
        return res

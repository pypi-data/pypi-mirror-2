import logging
import time
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression

from Products.ZCatalog.ProgressHandler import ZLogHandler

from config import UPDATE_CATALOG

logger = logging.getLogger('quintagroup.seoptimizer')

def updateCatalog(context):
    """ Update Catalog to collect data for canonical_path metadata.
    """
    if not (context.readDataFile('plonegooglesitemap_install.txt') is not None \
            and UPDATE_CATALOG):
        return

    site = context.getSite()
    catalog = getToolByName(site, 'portal_catalog')

    elapse = time.time()
    c_elapse = time.clock()
    print "Start of catalog rebuilding : %s" % c_elapse
    catalog.refreshCatalog(clear=1)
    elapse = time.time() - elapse
    c_elapse = time.clock() - c_elapse
    print "Catalog Rebuild\nTotal time: %s\nTotal CPU time: %s" % (elapse, c_elapse) 

    


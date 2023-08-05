from Products.CMFCore.utils import getToolByName
from zope.component import queryMultiAdapter
import logging
logger = logging.getLogger('uwosh.simpleemergency: subscribers.py')


def touchFrontPage(event):
    uwosh_tools = queryMultiAdapter((event.context, event.request), name=u"uwosh_tools")
    if uwosh_tools:
        uwosh_tools.set_last_modified_header()


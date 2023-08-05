# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2008 by []
# Generator: ArchGenXML Version 2.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """T. Kim Nguyen <nguyen@uwosh.edu> <unknown>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('uwosh.simpleemergency: setuphandlers')
import os
from Products.CMFCore.utils import getToolByName
import transaction
from zope.component import getUtility
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage


def isNotuwosh_simpleemergencyProfile(context):
    return context.readDataFile("uwosh.simpleemergency_marker.txt") is None

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotuwosh_simpleemergencyProfile(context): return
    site = context.getSite()
    
    # hide the viewlet to start off with
    viewlet = "uwosh.simpleemergency"
    manager = "plone.portaltop"

    storage = getUtility(IViewletSettingsStorage)
    skinname = site.getCurrentSkinName()
    hidden = storage.getHidden(manager, skinname)
    
    if viewlet not in hidden:
        hidden = hidden + (viewlet,)
        storage.setHidden(manager, skinname, hidden)
    
    # XXX -- no longer add emergency group
    # add group that will manage emergency message
    #pg = site.portal_groups
    #allGroups = pg.getGroupIds()
    #for g in ('uwosh.simpleemergency: Emergency Message Managers', ):
    #    if (g not in allGroups):
    #        pg.addGroup(g)
    #pg.setRolesForGroup('uwosh.simpleemergency: Emergency Message Managers', ['uwosh.simpleemergency: Emergency Message Manager',])

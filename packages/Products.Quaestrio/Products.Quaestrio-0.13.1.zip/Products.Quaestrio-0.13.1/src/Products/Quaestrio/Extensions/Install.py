# -*- coding: utf-8 -*-
#
__author__ = """Makina <contact@makina-corpus.com>"""
__docformat__ = 'plaintext'


import sys
from StringIO import StringIO
from Products.Quaestrio.config import *
# CMF imports
from Products.CMFCore.utils import getToolByName
outStream = sys.stdout
portlets = []

def registerResources(self, out, toolname, resources):
    tool = getToolByName(self, toolname)
    existing = tool.getResourceIds()
    cook = False
    for resource in resources:
        if not resource['id'] in existing:
            # register additional resource in the specified registry...
            if toolname == "portal_css":
                tool.registerStylesheet(**resource)
            if toolname == "portal_javascripts":
                tool.registerScript(**resource)
            print >> out, "Added %s to %s." % (resource['id'], tool)
        else:
            # ...or update existing one
            parameters = tool.getResource(resource['id'])._data
            for key in [k for k in resource.keys() if k != 'id']:
                originalkey = 'original_'+key
                original = parameters.get(originalkey)
                if not original:
                    parameters[originalkey] = parameters[key]
                parameters[key] = resource[key]
                print >> out, "Updated %s in %s." % (resource['id'], tool)
                cook = True
    if cook:
        tool.cookResources()
    print >> out, "Successfuly Installed/Updated resources in %s." % tool

def install(portal,reinstal=True):
    outStream = StringIO()
    outStream.write('(Re)installing Quaestrio product')
    profile_names = ['profile-Products.Quaestrio:default']
    for profile_name in profile_names:
        #_applyProfile(portal, profile_name)
        print >> outStream , "Ran all import steps for %s" % profile_name
    registerResources(portal, outStream, 'portal_css', STYLESHEETS)
    return outStream.getvalue()

def uninstall(portal, reinstall=False):
    outStream = StringIO()
    outStream.write('Uninstalling Quaestrio product')
    profile_names = ['profile-Products.Quaestrio:uninstall']
    for profile_name in profile_names:
        #_applyProfile(portal, profile_name)
        print >> outStream , "Ran all uninstall steps for %s" % profile_name
    return outStream.getvalue()

def _applyProfile(context, profile_name):
    setup_tool = getToolByName(context, 'portal_setup')
    old_context = setup_tool.getImportContextID()
    setup_tool.setImportContext(profile_name)
    setup_tool.runAllImportSteps()
    setup_tool.setImportContext(old_context)


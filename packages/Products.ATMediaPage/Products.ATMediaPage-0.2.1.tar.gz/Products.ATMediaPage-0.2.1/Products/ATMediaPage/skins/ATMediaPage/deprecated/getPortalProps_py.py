## Script (Python) "getPortalProps_py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
#
# Version : 0.4
# Author  : T.Hinze (HiDeVis)
# Datum   : 05.01.2006
#
# parameter
#
#
# return value
#   dict - all properties from all sheets inside portal_properties
#
###########################################################
# Documentation
# -------------
#
# This script read out all properties from all sheets inside
# the portal_properties-tools and return the values as dictionary.
#
###########################################################

#---------
# imports
#---------
from Products.CMFCore.utils import getToolByName

#------
# init
#------
portalTool = getToolByName(context, 'portal_url')
portalObj = portalTool.getPortalObject()
propSheet = portalObj.portal_properties

#----------------------
# ident all sheet id's
#----------------------
propNames = []
for child in propSheet.getChildNodes():
    propNames.append(child.getId())

#---------------------
# read all properties
#---------------------
allProperties = {}
for prop in propNames:
    if hasattr(propSheet, prop):
        allProperties.update(dict(propSheet[prop].propertyItems()))

#-----------------
# return the list
#-----------------
return allProperties

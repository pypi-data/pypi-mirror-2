## Script (Python) "get_shinythings_properties"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.CMFCore.utils import getToolByName

shinythings_properties = getToolByName(context, 'portal_properties').shinythings_properties  
return shinythings_properties 
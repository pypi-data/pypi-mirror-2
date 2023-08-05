## Script (Python) "something"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Linkedin Picture Change Helper
##
from Products.CMFCore.utils import getToolByName
request = container.REQUEST
RESPONSE =  request.RESPONSE


current_member = getToolByName(context,  'portal_membership').getAuthenticatedMember()
lin_tool= context.restrictedTraverse('linkedin_tool')
result = lin_tool.set_user_pic_from_linkedin(current_member.id)
if result==False:
    return "This user's picture is not available"
else:
    return "Ok"

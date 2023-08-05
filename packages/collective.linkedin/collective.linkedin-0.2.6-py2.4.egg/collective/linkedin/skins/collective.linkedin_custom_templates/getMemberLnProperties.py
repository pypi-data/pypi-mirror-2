## Script (Python) "getMemberLnProperties"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=member_id
##title=Get Member Linkedin Properties
##
# Example code:

# Import a standard function, and get the HTML request and response objects.
from Products.PythonScripts.standard import html_quote
request = container.REQUEST
RESPONSE =  request.RESPONSE

mtool = context.portal_membership
member = mtool.getMemberById(member_id)
return member.getProperty('linkedin_profile')

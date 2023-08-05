from zope import schema
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlet.static.static import IStaticPortlet

from collective.linkedin import LinkedInMessageFactory as _


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """

class ICollectiveLinkedInManagement(Interface):
    """
    """
    company_insider_widget = schema.TextLine(
        title = _(u"Company Insider Widget"),
        required = False,
        description = _(u"Enter the company name"),
    )

    action_popup = schema.Bool(
        title = _(u"Site action pop up"),
        required = False,
        description = _(u"Check it if you want the site action popup"),
    )

    border = schema.Bool(
        title = _(u"Border"),
        required = False,
        description = _(u"Caution: if you enable popup, this needs to be checked."),
    )
    
    api_key  = schema.TextLine(
        title = _(u"Linkedin Api Key"),
        required = False,
        description = _(u"Api Key obtained from linkedin at https://www.linkedin.com/secure/developer"),
    )

    secret_key  = schema.TextLine(
        title = _(u"Linkedin Secret Key"),
        required = False,
        description = _(u"Secret Key obtained from linkedin along with API key"),
    )

    request_token = schema.TextLine(
        title = _(u"Linkedin generated Request Token"),
        required = False,
        description = _(u"Api Generated Key obtained from linkedin after running Generate Credentials"),
    )

    request_token_secret = schema.TextLine(
        title = _(u"Linkedin generated Request Token Secret"),
        required = False,
        description = _(u"Secret Generated Key obtained from linkedin after running Generate Credentials"),
    )

    access_token = schema.TextLine(
        title = _(u"Linkedin generated Access Token"),
        required = False,
        description = _(u"Api Generated Token obtained from linkedin after running Generate Credentials"),
    )

    access_token_secret = schema.TextLine(
        title = _(u"Linkedin generated Access Token Secret"),
        required = False,
        description = _(u"Secret Generated Token obtained from linkedin after running Generate Credentials"),
    )


    verification_number = schema.TextLine(
        title = _(u"Verification number"),
        required = False,
        description = _(u"Verification number obtained from Generate Credentials process."),
    )


class ILinkedinTool(Interface):
    """
    """
    def get_user_profile(self, user_profile_url):
        pass
    
    def set_user_pic_from_linkedin(self, user):
        pass



class ICompanyInfoPortlet(IStaticPortlet):
    """ Defines a new portlet "Company Info" which takes properties of the existing static text portlet. """
    pass

class IProfileInfoPortlet(IPortletDataProvider):
    """ Defines a new portlet "Profile Info" """
    profile_id = schema.TextLine(
            title=_(u"LinkedIn user id"),
            description=_(u"Id of the LinkedIn user to show information"),
            default=u"",
            required=True)
    name = schema.TextLine(
            title=_(u"LinkedIn Name"),
            description=_(u"The name of the person"),
            default=u"",
            required=True)

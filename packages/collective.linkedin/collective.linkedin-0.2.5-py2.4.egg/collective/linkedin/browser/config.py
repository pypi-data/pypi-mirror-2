from zope.app.component.hooks import getSite
from zope.component import getUtility
from zope.formlib import form
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from OFS.Image import Image 

from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.validators import null_validator
from plone.memoize.view import memoize, memoize_contextless

from collective.linkedin.browser.interfaces import ICollectiveLinkedInManagement, ILinkedinTool
from collective.linkedin import LinkedInMessageFactory as _

from linkedin import linkedin

import StringIO, urllib

ld_action_id = 'linkedin_company_info'
ci_url = "http://www.linkedin.com/companyInsider?script&useBorder=%s"

def add_company_info_js(portal,border=True,overwrite=False):
    pjs = portal.portal_javascripts

    if border:
        old_url = ci_url % "no"
        new_url = ci_url % "yes"
    else:
        old_url = ci_url % "yes"
        new_url = ci_url % "no"

    if overwrite:
        if pjs.getResource(old_url) is not None:
            pjs.manage_removeScript(id=old_url)
        if pjs.getResource(new_url) is None:
            pjs.manage_addScript(cacheable="False",compression="full",cookable="True",
                                 enabled="True", inline="True",id=new_url)
    else:
        if pjs.getResource(old_url) is None and pjs.getResource(new_url) is None:
            pjs.manage_addScript(cacheable="False",compression="full",cookable="True",
                                 enabled="True", inline="True",id=new_url)


def get_company_info_js_border(portal):
    pjs = portal.portal_javascripts
    if pjs.getResource(ci_url % "yes"):
        return True
    elif pjs.getResource(ci_url % "no"):
        return False
    else:
        return None

class LinkedInConfigurationForm(ControlPanelForm):
    form_fields = form.Fields(ICollectiveLinkedInManagement)
    label = _(u"LinkedIn settings form")
    description = _(u"Setup options of LinkedIn inside your plone")
    form_name = _(u"LinkedIn Settings")
    form_fields['request_token'].for_display = True
    form_fields['request_token_secret'].for_display = True
    form_fields['access_token'].for_display = True
    form_fields['access_token_secret'].for_display = True


    actions = ControlPanelForm.actions.copy()

    @form.action(_(u'Generate Linkedin Credentials'), name="generate_credentials" )
    def handle_generate_credentials_action(self, action, data):
        lin_conf = form_adapter(self)
        return_url = getSite().absolute_url() + '/@@manage_linkedin_response'
        lin_api = linkedin.LinkedIn(lin_conf.api_key, lin_conf.secret_key, return_url)
        request_token_result = lin_api.requestToken()
        if not request_token_result:
            #This means something went wrong
            print  lin_api.getRequestTokenError()
        lin_conf.request_token = unicode(lin_api.request_token)
        lin_conf.request_token_secret = unicode(lin_api.request_token_secret)
        self.request.response.redirect(lin_api.getAuthorizeURL(request_token = lin_api.request_token))
        

class MissingAction(Exception):
    pass

class LinkedInConfiguration(SimpleItem):
    implements(ICollectiveLinkedInManagement)
    company_insider_widget = FieldProperty(ICollectiveLinkedInManagement['company_insider_widget'])
    api_key = FieldProperty(ICollectiveLinkedInManagement['api_key'])
    secret_key = FieldProperty(ICollectiveLinkedInManagement['secret_key'])
    request_token = FieldProperty(ICollectiveLinkedInManagement['request_token'])
    request_token_secret = FieldProperty(ICollectiveLinkedInManagement['request_token_secret'])
    verification_number_storage = FieldProperty(ICollectiveLinkedInManagement['verification_number'])
    access_token = FieldProperty(ICollectiveLinkedInManagement['access_token'])
    access_token_secret = FieldProperty(ICollectiveLinkedInManagement['access_token_secret'])


    def set_action_popup(self,value):
        site = getSite()
        site_actions = getToolByName(site,'portal_actions').site_actions
        if ld_action_id not in site_actions.objectIds():
            # I could not make this code work. Some change on porta_actions :-/
            # site_actions.addAction(ld_action_id,ld_action_id,'','',('View',),'site_actions')
            raise MissingAction('%s action in site_actions is missing' % ld_action_id)
        site_actions[ld_action_id].visible = bool(value)

    def get_action_popup(self):
        site = getSite()
        site_actions = getToolByName(site,'portal_actions').site_actions
        return ld_action_id in site_actions.objectIds() and site_actions[ld_action_id].visible
    action_popup = property(get_action_popup, set_action_popup)

    def set_border(self,value):
        site = getSite()
        add_company_info_js(site,overwrite=True,border=value)

    def get_border(self):
        site = getSite()
        return bool(get_company_info_js_border(site))
    border = property(get_border, set_border)

    def set_verification_number(self, value):
        self.verification_number_storage = value
        lin_api = linkedin.LinkedIn(self.api_key, self.secret_key, 'http://www.linkedin.com')
        acc_token = lin_api.accessToken(request_token=self.request_token, \
                request_token_secret=self.request_token_secret, \
                    verifier = self.verification_number)
        self.access_token = unicode(lin_api.access_token)
        self.access_token_secret = unicode(lin_api.access_token_secret)


    def get_verification_number(self):
        return self.verification_number_storage
    verification_number = property(get_verification_number, set_verification_number)
    
    def linkedin_get_user(self, member_linkedin_profile):
        if self.request_token and self.request_token_secret and \
            self.verification_number and member_linkedin_profile:
            lin_api = linkedin.LinkedIn(self.api_key, self.secret_key, 'http://www.linkedin.com')
            lin_api.access_token = self.access_token
            lin_api.access_token_secret = self.access_token_secret
            profile_url = member_linkedin_profile[member_linkedin_profile.find("linkedin"):]
            profile_url = "http://www." + profile_url
            lin_person = lin_api.GetProfile(url=profile_url)
            return lin_person

class LinkedinTool(BrowserView): 
    implements(ILinkedinTool)

    def get_user_profile(self, user_profile_url):
        user_fields = ['current_status', 'educations', 'first_name', 'headline', 'honors',
        'industry', 'interests', 'last_name', 'location', 'picture_url', 'positions', 'public_url',
        'specialties', 'summary']
        dicter = lambda key,bogus: (key, getattr(user_profile, key))
        user_profile = form_adapter(self).linkedin_get_user(user_profile_url)
        return dict(map(dicter, user_fields, user_fields))

    def set_user_pic_from_linkedin(self, user_id):
        portal = getSite()
        user=portal.portal_membership.getMemberById(user_id)
        member_linkedin_profile = user.getProperty('linkedin_profile')
        profile_url = member_linkedin_profile[member_linkedin_profile.find("linkedin"):] 
        profile_url = "http://www." + profile_url
        picture_url = form_adapter(self).linkedin_get_user(profile_url).picture_url
        picture_connections = urllib.urlopen(picture_url)
        picture_object = picture_connections.read()
        picture_connections.close()
        picture_file = StringIO.StringIO(picture_object)
        picture_image = Image(id=user_id, file=picture_file, title='')
        portal.portal_memberdata._setPortrait(picture_image, user_id)



def form_adapter(context):
    return getUtility(ICollectiveLinkedInManagement, name='linkedin_config', context=context)

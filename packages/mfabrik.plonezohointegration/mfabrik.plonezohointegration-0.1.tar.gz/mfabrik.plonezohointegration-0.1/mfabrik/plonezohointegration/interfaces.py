from zope import schema

from plone.directives import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from mfabrik.plonezohointegration import _

class ISettings(form.Schema):
    """ Define schema for settings of the add-on product """


    username = schema.TextLine(title=_(u"Username"),
                               description=_(u"Your Zoho username. If you are using Google Apps integration this is your Google company hosted email address like firstname.lastname@company.com."),
                               required=True, 
                               default=u"",
                               )
    
    password = schema.TextLine(title=_(u"Password"),
                               description=_(u"Your Zoho password"),
                               required=True, 
                               default=u"",
                               )
    
    apikey = schema.TextLine(title=_(u"API key"),
                               description=_(u"Your Zoho API key"),
                               required=True,
                               default=u"",
                               )
    
    crm_lead_extra_data = schema.TextLine(title=_(u"CRM lead generation extra data"),
                               description=_(u"Extra fields which will be set for all new leads created through Zoho contact form. You can, for example, use these to identify the lead source. Use new line separated fieldname=value pairs. E.g. Lead Source=Web Contact Form"),
                               required=False, 
                               default=u"",
                               )
    
    
    
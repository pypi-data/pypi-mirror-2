from Products.Five.browser import BrowserView
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("collective.amberjack.core")
PMF = MessageFactory('plone')

class AmberjackDefaults(BrowserView): 
    def __call__(self, context, request):
        constants = """
            if (AmberjackPlone){
                AmberjackPlone.aj_plone_consts['Error'] = '%s';
                AmberjackPlone.aj_plone_consts['ErrorValidation'] = '%s';
                AmberjackPlone.aj_plone_consts['BrowseFile'] = '%s';
                
            }
        """ % (PMF(u'Error'),
               PMF(u'Please correct the indicated errors.'),
               _(u'Please select a file.'),
               )
        
        url = self.context.portal_url()
        return """
        function loadDefaults(){
            Amberjack.onCloseClickStay = true;
            Amberjack.doCoverBody = false;
            Amberjack.BASE_URL = '%s/';
            Amberjack.textOf = "%s";
            
            %s
        }
        """  % (url, 
                translate(_('separator-between-steps', default=u"of"),context=self.request),
                constants)
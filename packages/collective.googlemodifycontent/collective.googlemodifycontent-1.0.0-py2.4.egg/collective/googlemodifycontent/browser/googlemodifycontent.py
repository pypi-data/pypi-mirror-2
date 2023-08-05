__author__  = "D'Elia Federica"

from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from gdata.auth import AuthSubToken
from gdata.docs.service import DocsService

class GoogleModifyContent(BrowserView):
        
    def GetId(self,context):
        
        info=getattr(context,'file_filesystemstorage_info')
        gooId=getattr(info,'gooId')
        mimetype=getattr(info,'mimetype')
        if(mimetype=="application/vnd.ms-powerpoint"):
            mimetype="presentation"
        elif(mimetype=="text/comma-separated-values" or mimetype=="application/vnd.ms-excel" or mimetype=="application/vnd.oasis.opendocument.spreadsheet"):
            mimetype="spreadsheet"
        else:
            mimetype="document"
        
        header='http://docs.google.com/feeds/documents/private/full/'
        
        resource_id=header+mimetype+"%3A"+gooId
        
        return resource_id
        
    def GetDocument(self,gd_client,context):
        
        resource_id=self.GetId(context)
        
        
        feed = gd_client.GetDocumentListFeed()

        for entry in feed.entry:
            if entry.id.text==resource_id:
                return entry
    
    def Auth(self,context):
        
        membership_tool=getToolByName(context, 'portal_membership')
        member = membership_tool.getAuthenticatedMember()
        google_token=member.getProperty('google_token')
        
        # create an AuthSubToken object
        scope =['http://docs.google.com/feeds/','http://spreadsheets.google.com/feeds/']
        # scopes='http://docs.google.com/feeds/'
        authsub_token = AuthSubToken(scopes=scope)
        authsub_token.set_token_string(google_token)

        # create a client for the Google Documents service
        gd_client = DocsService()
        gd_client.auth_token = authsub_token
    
        gd_client.SetAuthSubToken(authsub_token)
        
        return gd_client
    
    def url_doc(self):

        context = aq_inner(self.context)
        
        gd_client=self.Auth(context)
        
        document=self.GetDocument(gd_client,context)
        
        link=document.GetHtmlLink().href+'&hl=en'
        
        return link
    
    def is_google_docs(self,context):
        
        info=getattr(context,'file_filesystemstorage_info',None)
        
        return hasattr(info,'gooId')


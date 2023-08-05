__author__  = "D'Elia Federica"

from gdata.auth import AuthSubToken
from gdata.docs.service import DocsService
from gdata.docs.service import DocumentQuery
from gdata.docs.service import DocumentAclQuery
from gdata.docs import DocumentListAclEntryFromString
from gdata.docs import DocumentListAclEntry
from gdata.docs import Scope
from gdata.docs import Role

from Products.CMFCore.utils import getToolByName

class GDataSharing(object):
    
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
        
        resource_id=mimetype+"%3A"+gooId
        
        return resource_id
    
    def GetAclFeed(self,gd_client,context):
        
        resource_id=self.GetId(context)
        
        query = DocumentAclQuery(resource_id)
        
        acl_feed = gd_client.GetDocumentListAclFeed(query.ToUri())
        
        return acl_feed

    def GetDocument(self,gd_client,context):
        
        resource_id=self.GetId(context)
        
        header='http://docs.google.com/feeds/documents/private/full/'
        
        resource_id=header+resource_id
        
        
        feed = gd_client.GetDocumentListFeed()

        for entry in feed.entry:
            if entry.id.text==resource_id:
                return entry
    
    def UpdateAclEntry(self,gd_client,acl_entry,role):
        acl_entry.role.value = role
        gd_client.Put(acl_entry, acl_entry.GetEditLink().href, converter=DocumentListAclEntryFromString)
    
    def DeleteAclEntry(self,gd_client,acl_entry):
        gd_client.Delete(acl_entry.GetEditLink().href)
        
    def AddAclEntry(self,gd_client,role,email,context):
        
        scope = Scope(value=email,type='user')
        role = Role(value=role)
        acl_entry = DocumentListAclEntry(scope=scope, role=role)
        
        document=self.GetDocument(gd_client,context)
        
        gd_client.Post(acl_entry, document.GetAclLink().href, converter=DocumentListAclEntryFromString)
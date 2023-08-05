__author__  = "D'Elia Federica"

from Products.Five.browser import BrowserView
from gdata.auth import AuthSubToken
from gdata.docs.service import DocsService
from gdata.auth import generate_auth_sub_url

class SessionToken(BrowserView):

    def convert_to_a_session_token(self,sigle_token):
        
        scope =['http://docs.google.com/feeds/','http://spreadsheets.google.com/feeds/']
        # create an AuthSubToken object
        authsub_token = AuthSubToken(scopes=scope)
        #authsub_token = AuthSubToken(scopes='http://docs.google.com/feeds/')  
        authsub_token.set_token_string(sigle_token)

        # create a client for the Google Documents service
        gd_client = DocsService()
        gd_client.auth_token = authsub_token
    
        # upgrades a single use AuthSub token to a session token
        gd_client.UpgradeToSessionToken(token=authsub_token)
        
        # estrae la stringa che rappresenta il session token
        session_token = gd_client.auth_token.get_token_string()
    
        return session_token
    

    def get_auth_sub_url(self,came_from):
        
        porturl=self.context.portal_url()
        
        if came_from==None:
            next=porturl+'/logged_in'
        else:
            next=porturl+'/logged_in?came_from='+came_from
        
        scope =['http://docs.google.com/feeds/','http://spreadsheets.google.com/feeds/']
        
        secure = False
        
        session = True
        
        gd_client = DocsService()
        
        return generate_auth_sub_url(next, scope, secure, session)

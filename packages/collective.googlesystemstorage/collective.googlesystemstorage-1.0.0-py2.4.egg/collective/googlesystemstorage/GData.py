"""
The GData class provides connection to GoogleDocs
"""

__author__  = 'federica'
__docformat__ = 'restructuredtext'

from Products.CMFCore.utils import getToolByName
from gdata.docs.service import DocsService
from gdata.docs.service import DocumentQuery
from gdata import MediaSource
from gdata.auth import AuthSubToken
from plone.memoize import ram
import shutil
import os

class GData(object):

    def Auth(self,instance):
        
        membership_tool=getToolByName(instance, 'portal_membership')
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
  
    def DocumentId(self,document):
        id=document.id.text
        id=id.split("%3A")
        return id[1]
    
    def Upload(self, gd_client, path_file, mimetype, name_file):
        
        ms = MediaSource()
        
        if(mimetype=="text/comma-separated-values"):
            mimetype="text/csv"
        if(mimetype=="application/vnd.oasis.opendocument.spreadsheet"):
            mimetype="application/x-vnd.oasis.opendocument.spreadsheet"
        if(mimetype=="application/rtf"):
            shutil.copy(path_file,path_file+".rtf")
            path_file=path_file+".rtf"
        
        ms.setFile(path_file,mimetype)
        
        tmp=name_file.split(".")
        filename=tmp[0]
        
        if(mimetype=="application/vnd.ms-powerpoint"):
            document=gd_client.UploadPresentation(ms,filename)
        elif(mimetype=="text/csv" or mimetype=="application/vnd.ms-excel" or mimetype=="application/x-vnd.oasis.opendocument.spreadsheet"):
            document=gd_client.UploadSpreadsheet(ms,filename)
        else:
            document=gd_client.UploadDocument(ms,filename)

        if(mimetype=="application/rtf"):
            os.remove(path_file)
            
        return self.DocumentId(document)
    
    def Delete(self,gd_client,document):
            gd_client.Delete(document.GetEditLink().href)

    def Retrieve(self,gd_client,mimetype):
        
        q = DocumentQuery()
        
        if mimetype=='application/vnd.ms-powerpoint':
            q.categories.append('presentation')
        elif mimetype=='text/comma-separated-values' or mimetype=='application/vnd.ms-excel' or mimetype=='application/vnd.oasis.opendocument.spreadsheet':
            q.categories.append('spreadsheet')
        else:
            q.categories.append('document')

        uri=q.ToUri()
        documents = gd_client.Query(uri)
        return documents

    def cache_key(funz,self,request,gd_client,id,title,mimetype,path):
        return request
    
    @ram.cache(cache_key)
    def Download(self,request,gd_client,id,title,mimetype,path):

        tmp=title.split(".")
        exportFormat=tmp[1]

        if mimetype=="application/vnd.ms-powerpoint" and exportFormat=='pps':
            exportFormat='ppt'
            url='http://docs.google.com/feeds/download/presentations/Export?docID='+id+'&exportFormat='+exportFormat
        elif mimetype=="application/vnd.ms-powerpoint" :
            url='http://docs.google.com/feeds/download/presentations/Export?docID='+id+'&exportFormat='+exportFormat
        elif mimetype=='text/comma-separated-values' :
            url='http://spreadsheets.google.com/feeds/download/spreadsheets/Export?key='+id+'&fmcmd=5&gid=0'
        elif mimetype=='application/vnd.ms-excel' :
            url='http://spreadsheets.google.com/feeds/download/spreadsheets/Export?key='+id+'&fmcmd=4'
        elif mimetype=='application/vnd.oasis.opendocument.spreadsheet' :
            url='http://spreadsheets.google.com/feeds/download/spreadsheets/Export?key='+id+'&fmcmd=13'
        else:
            url='http://docs.google.com/feeds/download/documents/Export?docID='+id+'&exportFormat='+exportFormat
        
        token=gd_client.auth_token
    
        response=token.perform_request(gd_client.http_client, 'GET', url)

        response_body=response.read()
        
        if os.path.exists(path):
            os.remove(path)
            
        fd=os.open(path,os.O_WRONLY|os.O_CREAT)
        os.write(fd,response_body)
        os.close(fd)
        
        size=os.path.getsize(path)
       
        return size
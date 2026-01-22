import os
from supabase import create_client, Client
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from urllib.parse import urljoin


class SupabaseStorage(Storage):
    """
    Custom Django storage backend for Supabase Storage
    """
    def __init__(self):
        self.supabase_url = os.environ.get('SUPABASE_URL')
        self.supabase_key = os.environ.get('SUPABASE_KEY')
        self.bucket_name = os.environ.get('SUPABASE_BUCKET', 'pdfs')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
    
    def _save(self, name, content):
        """
        Save file to Supabase Storage
        """
        try:
            # Read file content
            file_data = content.read()
            
            # Upload to Supabase
            res = self.client.storage.from_(self.bucket_name).upload(
                path=name,
                file=file_data,
                file_options={"content-type": "application/pdf"}
            )
            
            return name
        except Exception as e:
            raise IOError(f"Error uploading to Supabase: {str(e)}")
    
    def _open(self, name, mode='rb'):
        """
        Open file from Supabase Storage
        """
        try:
            res = self.client.storage.from_(self.bucket_name).download(name)
            return ContentFile(res)
        except Exception as e:
            raise IOError(f"Error downloading from Supabase: {str(e)}")
    
    def delete(self, name):
        """
        Delete file from Supabase Storage
        """
        try:
            self.client.storage.from_(self.bucket_name).remove([name])
        except Exception as e:
            print(f"Error deleting from Supabase: {str(e)}")
    
    def exists(self, name):
        """
        Check if file exists in Supabase Storage
        """
        try:
            files = self.client.storage.from_(self.bucket_name).list()
            return any(f['name'] == name for f in files)
        except:
            return False
    
    def url(self, name):
        """
        Return public URL for file
        """
        return self.client.storage.from_(self.bucket_name).get_public_url(name)
    
    def size(self, name):
        """
        Return file size
        """
        try:
            files = self.client.storage.from_(self.bucket_name).list()
            for f in files:
                if f['name'] == name:
                    return f.get('metadata', {}).get('size', 0)
            return 0
        except:
            return 0

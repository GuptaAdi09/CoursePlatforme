import cloudinary
from django.conf import settings
CLOUDNARY_CLOUD_NAME = settings.CLOUDNARY_CLOUD_NAME
CLOUDNARY_PUBLIC_API_KEY = settings.CLOUDNARY_PUBLIC_API_KEY
CLOUDNARY_SECRET_API_KEY = settings.CLOUDNARY_SECRET_API_KEY

def clouidnary_init():      
    cloudinary.config( 
        cloud_name = CLOUDNARY_CLOUD_NAME, 
        api_key =CLOUDNARY_PUBLIC_API_KEY, 
        api_secret = CLOUDNARY_SECRET_API_KEY, # Click 'View API Keys' above to copy your API secret
        secure=True
    )
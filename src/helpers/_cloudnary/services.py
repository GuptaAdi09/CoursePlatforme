from django.template.loader import get_template
from django.conf import settings


def get_cloudnary_image_object(instance,
                               as_html=False,field_name='image',width=200):
    if not hasattr(instance,field_name):
          return ""
    image_object = getattr(instance,field_name)
    if not image_object:
            return ""
    image_option ={
            "width":width
        }
    if as_html:
          return image_object.image(**image_option)
    url = image_object.build_url(**image_option)
    
    return url


video_html="""

"""

def get_cloudnary_video_object(instance,
                               as_html=False,field_name='video',sign_url=False,width=None,height=None
                               ,fetch_format="auto",quality="auto",controls=True,autoplay=True):
    if not hasattr(instance,field_name):
          return ""
    video_object = getattr(instance,field_name)
    if not video_object:
            return ""
    video_options ={
            
             'sign_url':sign_url,
             "fetch_format":fetch_format,
             "quality":quality,
             "controls":controls,
             "autoplay":autoplay,
             

             
        }
    if width is not None:
          video_options['width'] = width
    if height is not None:
          video_options['height'] = height
    if height and width:
          video_options['crop'] = "limit"
    
    url = video_object.build_url(**video_options)
    if as_html:
          template_name ="videos/embed.html"
          tmpl = get_template(template_name)
          cloud_name = settings.CLOUDNARY_CLOUD_NAME
          _html = tmpl.render({'video_url':url,'cloud_name':cloud_name})
          return _html
    
    return url
    
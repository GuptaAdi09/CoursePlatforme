from django.contrib import admin
from .models import Course,Lesson
from django.utils.html import format_html
from cloudinary import CloudinaryImage
import helpers


# Register your models here.
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0
    readonly_fields =['update','public_id','display_image','display_video']
    def display_image(Self,obj,*args, **kwargs):
        
        url = helpers.get_cloudnary_image_object(obj,field_name='thumbnail',
                                                 width=200)
        # cloudnary_id = str(obj.image)
        # clodnary_html= CloudinaryImage(cloudnary_id).image(width=200)
        return format_html(f" <img src='{url}' />")
    
    display_image.short_discription ="Current Image"

    def display_video(Self,obj,*args, **kwargs):
        
        video_embed_html = helpers.get_cloudnary_video_object(obj,field_name='video',as_html=True,
                                                 width=300)
        # cloudnary_id = str(obj.image)
        # clodnary_html= CloudinaryImage(cloudnary_id).image(width=200)
        return video_embed_html
    display_video.short_discription ="Current video"







@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ['title','id','status','access']
    list_filter = ['status','access']
    fields = ['public_id','title','discription','status','image','access','display_image']
    readonly_fields = ['display_image','public_id']

    def display_image(Self,obj,*args, **kwargs):
        
        url = helpers.get_cloudnary_image_object(obj,field_name='image',
                                                 width=200)
        # cloudnary_id = str(obj.image)
        # clodnary_html= CloudinaryImage(cloudnary_id).image(width=200)
        return format_html(f" <img src='{url}' />")
    display_image.short_discription ="Current Image"

    


    
# admin.site.register(Course)
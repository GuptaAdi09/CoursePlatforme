from django.db import models
import helpers
import uuid
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
helpers.clouidnary_init()



# Create your models here.
class AccessRequirment(models.TextChoices):
    ANYONE= "any","Anyone"
    EMAIL_REQUIRED =  "email_required"," Emial Require"
   

class PublishStatus(models.TextChoices):
    PUBLISH= "pub","Published"
    COMING_SOON =  "soon","Coming soon"
    DRAFT = "draft", "Draft"

def handle_upload(instance, filename):
    return f"{filename}"

def generate_public_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-","")
    if not title:
       return unique_id
    slug = slugify(title)
    unique_id_short = unique_id[:5]
    return f"{slug}-{unique_id_short}"
    

def get_public_id(instance,*args, **kwargs):
    if hasattr(instance,'path'):
        path = instance.path
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        return path
    public_id = instance.public_id
    model_class = instance.__class__
    model_name = model_class.__name__
    model_name_slug = slugify(model_name)
    if not public_id:
        return f"{model_name_slug}"
    
    return f"{model_name_slug}/{public_id}"

def get_display_name(instance,*args, **kwargs):
    if hasattr(instance,'get_display_name'):
        return instance.get_display_name()
    elif hasattr(instance,"title"):
        return instance.title
    model_class = instance.__class__
    model_name = model_class.__name__
    return f"{model_name} Uplaod"
# get_thumbnail_display_name = lambda instace:get_display_name(instance,is_thumbnail=True)

class Course(models.Model):
    title = models.CharField(max_length=120)
    public_id = models.CharField(max_length=130,null=True,blank=True,db_index=True)
    discription=models.TextField(blank=True,null=True)
    # image=models.ImageField(upload_to=handle_upload,blank=True,null=True)
    image= CloudinaryField("image",null=True,public_id_prefix= get_public_id,display_name=get_display_name,
                           tags=["course","thumbnail"])
    access= models.CharField(max_length=14,choices=AccessRequirment.choices,default=AccessRequirment.EMAIL_REQUIRED)
    status= models.CharField(max_length=14,choices=PublishStatus.choices,default=PublishStatus.DRAFT)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def save(self,*args, **kwargs):
        if self.public_id == '' or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    def get_absolute_path(self):
        return f"http://localhost:8000"+self.path
    
    @property
    def path(self):
        return f"/courses/{self.public_id}"
    

    def get_display_name(self):
        return f"{self.title} -Course"


    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISH
    
    
    # @property
    # def image_admin(self):
    #     return helpers.get_cloudnary_image_object(self,field_name="image",as_html=False,width=200)
        
    
 
    # def get_image_thumbnail(self , as_html=False ,width=200):
    #     return helpers.get_cloudnary_image_object(self,field_name="image",as_html=as_html,width=200)
    
    # def get_image_detail(self,as_html=False,width=550):
    #     return helpers.get_cloudnary_image_object(self,field_name="image",as_html=False,width=200)
    

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    public_id = models.CharField(max_length=130,null=True,blank=True,db_index=True)


    title = models.CharField(max_length=120)
    discription=models.TextField(blank=True,null=True)
    preview = models.BooleanField(default=False)
    thumbnail= CloudinaryField("image",blank=True,null=True,public_id_prefix= get_public_id,display_name=get_display_name,
                               tags=["image","thumbnail","lesson"])
    video = CloudinaryField("video",blank=True,null=True,resource_type='video',public_id_prefix= get_public_id,
                            display_name=get_display_name,type='private',
                            tags = ["video","lesson"])
    order = models.IntegerField(default=0)
    status= models.CharField(max_length=14,
                             choices=PublishStatus.choices,
                             default=PublishStatus.DRAFT)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    
    
    class Meta:
        ordering = ['-update','order']
    
    def save(self,*args, **kwargs):
        if self.public_id == '' or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(args, kwargs)

    def get_absolute_path(self):
        
        return self.path

    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith('/'):
            course_path = course_path[:-1]
        return f"{course_path}/lesson/{self.public_id}"
    

    def get_display_name(self):
        return f"{self.title} -{self.course.get_display_name()}"
    
    @property
    def is_comming_soon(self):
        return self.status == PublishStatus.COMING_SOON
    
    @property
    def has_video(self):
        return self.video is not None



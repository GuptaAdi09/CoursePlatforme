from django.shortcuts import render
from django.http import Http404,JsonResponse
# Create your views here.
from . import services
import helpers


def course_list_view(request):
    queryset = services.get_publish_courses()
    
    # return JsonResponse({'data':[x.id for x in queryset]})
    context={
        'object_list':queryset
    }
    return render(request,"courses/list.html",context)

def course_detail_view(request,course_id=None,*args, **kwargs):
    print("course_id",course_id)
    course_obj = services.get_course_detail(course_id=course_id)
    print(course_obj)
    if course_obj is None:
        raise Http404
    lesson_queryset = services.get_course_lessons(course_obj)
    context ={
        "object": course_obj,
        "lesson_queryet": lesson_queryset
    }
    # return JsonResponse({'data':course_obj.id,'lesson_id':[x.path  for x in lesson_queryset]})
    return render(request,"courses/detail.html",context)

def lesson_detail_view(request,lesson_id=None,course_id=None,*args, **kwargs):
    print(lesson_id,course_id)
    lesson_obj = services.get_lesson_detail(course_id=course_id,lesson_id=lesson_id)
    print(lesson_obj)
    

    if lesson_obj is None:
        raise Http404
    
    template_name = "courses/lesson_comming_soon.html"
    context ={
        "object": lesson_obj
    }
    if not lesson_obj.is_comming_soon:
        """
        Lesson is published ,Go forward
        """
        template_name = "courses/lesson.html"
    if lesson_obj.has_video:
            """
            Video is available.
            """
            video_embed_html = helpers.get_cloudnary_video_object(lesson_obj,field_name='video',as_html=True,
                                                 width=1250,height=500)
            context['video'] = video_embed_html
    
    return render(request,template_name,context)
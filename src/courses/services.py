from .models import Course,PublishStatus,AccessRequirment,Lesson
# from django.apps import apps


def get_publish_courses():
    # Course = apps.get_model('course','Course')
    return Course.objects.filter(status=PublishStatus.PUBLISH)

def get_course_detail(course_id= None):
    if course_id is None:
        return None
    obj =None
    try:
        obj =Course.objects.get(status=PublishStatus.PUBLISH,public_id=course_id)
        
    except:
        pass
    return obj

def get_course_lessons(course_obj=None):
    lessons = Lesson.objects.none()
    if not isinstance(course_obj, Course):
        return lessons
    lessons = course_obj.lesson_set.filter(
        course__status=PublishStatus.PUBLISH,
        status__in=[PublishStatus.PUBLISH, PublishStatus.COMING_SOON]
    )
    return lessons


def get_lesson_detail(course_id=None,lesson_id= None):
    if lesson_id is None and course_id is None:
        return None
    obj =None
    try:
        obj =Lesson.objects.get(
                                course__public_id= course_id,
                                course__status = PublishStatus.PUBLISH,
                                status__in = [PublishStatus.PUBLISH,PublishStatus.COMING_SOON],
                                public_id=lesson_id)
        
    except Lesson.DoesNotExist:
        print(f"No lesson found with lesson_id={lesson_id} and course_id={course_id}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None
    
    return obj
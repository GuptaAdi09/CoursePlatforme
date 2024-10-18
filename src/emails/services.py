from .models import Email,EmailVerification
from django.conf import settings
from django.core.mail import send_mail 
from django.utils import timezone


EMAIL_HOST_USER = settings.EMAIL_HOST_USER

def verify_email(email):
    qs = Email.objects.filter(email=email,active=False)
    return qs.exists()

def get_email_verification_msg(verification_instance, as_html=False):
      if not isinstance(verification_instance,EmailVerification):
            return None
      verify_link = verification_instance.get_link()
      if as_html:
            return f"""<h1>Verify your email with following:</h1>
            <p><a href='{verify_link}'>{verify_link}</a></p>"""

            
      return f"""verify your email with followig:\n
      {verify_link}"""

def start_verification_event(email):
        
        email_obj , created = Email.objects.get_or_create(email=email)
        obj=EmailVerification.objects.create(
            parent = email_obj, email=email
        )
        sent = send_verification_event(obj.id)
        return obj,sent
      
def send_verification_event(verify_obj_id):
      verify_obj = EmailVerification.objects.get(id=verify_obj_id)
      email = verify_obj.email
      subject = "Verify your email "
      text_msg = get_email_verification_msg(verify_obj,as_html=False)
      text_html = get_email_verification_msg(verify_obj,as_html=True)
      from_user_email_addr = EMAIL_HOST_USER 
      to_user_email = email

        

      return send_mail(
            subject,
            text_msg,
            from_user_email_addr,
            [to_user_email],
            fail_silently=False,
            html_message=text_html

        )
      
def verify_token(token, max_attempt=5):
      qs =  EmailVerification.objects.filter(token=token)
      
      if not qs.exists() and not qs.count() == 1:
            return False , "Invaild token", None
      
      has_email_expired = qs.filter(expired=True)

      if  has_email_expired.exists():
            return False, "Token expired,try again ",None
      
      max_attempt_reached = qs.filter(attempts__gte=max_attempt)
      if max_attempt_reached.exists():
            """ update max attempts +1"""

            return False, "Token expired, used too many times" ,None
      obj = qs.first()
      obj.attempts += 1
      obj.last_attempts_at = timezone.now()
      if obj.attempts > max_attempt:

            obj.expired = True
            obj.expired_at = timezone.now()

      obj.save()
      email_obj = obj.parent
      

      return True ,"Welcome" , email_obj
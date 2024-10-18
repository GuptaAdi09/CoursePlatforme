from django.shortcuts import render
from emails.forms import EmailForm
from django.conf import settings
from emails.models import Email,EmailVerification
from emails import services as email_services

email_Add = settings.EMAIL_ADDRESS


def Home_view(request,*args, **kwargs):
    
    form = EmailForm(request.POST or None)
    context = {
        'form':form,
        'message':''
    }
    if form.is_valid():
        email_val = form.cleaned_data.get('email')
        obj = email_services.start_verification_event(email_val)
        print(obj)
        context['form'] = EmailForm()
        context['message']="success! Check your email for verification"
    else:
        print(form.errors)
    
    print('email_id',request.session.get('email_id'))

    

    return render(request,'home.html',context)

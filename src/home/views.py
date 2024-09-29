from django.shortcuts import render
from emails.forms import EmailForm
from django.conf import settings


email_Add = settings.EMIAL_ADDRESS


def Home_view(request,*args, **kwargs):
    print(request.POST)
    form = EmailForm(request.POST or None)
    context = {
        'form':form,
        'message':''
    }
    if form.is_valid():
        obj=form.save()
        print(obj)
        context['form'] = EmailForm
        context['message']="success! Check your email for verification"


    return render(request,'home.html',context)
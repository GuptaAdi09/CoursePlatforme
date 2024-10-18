from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import services
from django.contrib import messages
from .forms import EmailForm
from django.conf import settings
from django_htmx.http import HttpResponseClientRedirect

EMAIL_ADDRESS = settings.EMAIL_ADDRESS

def logout_hx_btn_view(request):
    if not request.htmx:
        return redirect('/')

    if request.method == 'POST':
        try:
            del request.session['email_id']
        except:
            pass
        
        email_id_in_session = request.session.get("email_id")
        if not email_id_in_session:
            return HttpResponseClientRedirect('/')

    return render(request,"email/hx/logout-btn.html",{})



def email_token_login_view(request):
    if not request.htmx:
        return redirect('/')
    email_id_in_session = request.session.get("email_id")
    form = EmailForm(request.POST or None)
    context = {
        'form':form,
        'message':'',
        'show_form': not email_id_in_session,
    }
    if form.is_valid():
        email_val = form.cleaned_data.get('email')
        obj = services.start_verification_event(email_val)
        
        context['form'] = EmailForm()
        context['message']=f"success! Check your email for verification {email_val}"
    else:
        print(form.errors)
    

    return render(request,'email/hx/form.html',context)




def verify_email_token_view(request,token,*args, **kwargs):
    did_verify, msg ,email_obj = services.verify_token(token)
    
    if not did_verify:
        try:
            del request.session['email_id']

        except:
            pass
        messages.error(request,msg)
        return redirect("/login/")
    messages.success(request,msg)
    
    request.session['email_id'] = f"email_id {email_obj.id}"

    next_url = request.session.get('next_url') or "/"
    if not next_url.startswith("/"):
        next_url = "/"

    return redirect(next_url)
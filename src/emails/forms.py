from django import forms

from . import css,services

class EmailForm(forms.Form):
    email = forms.EmailField(
        widget= forms.EmailInput(
            attrs = {
                "id":"email-login-input",
                "class": css.EMAIL_FIELD_CSS
            }
        )
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        verified = services.verify_email(email)
        # qs = Email.objects.filter(email=email , active = False)
        if verified:
            raise forms.ValidationError("Invaild emial please try again ")
        return email
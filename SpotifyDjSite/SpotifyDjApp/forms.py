from .models import user
from django import forms

class userForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(userForm, self).__init__(*args, **kwargs)
            ## add a "form-control" class to each form input
            ## for enabling bootstrap
            for name in self.fields.keys():
                self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
        class Meta:
            model = user
            fields = ("__all__")
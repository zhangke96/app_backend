from django import forms
from django.db import transaction
from .models import vedios

class VedioForm(forms.Form):
    vedio = forms.FileField(required=True)

    def save(self):
        file = self.cleaned_data['vedio']
        newvedio = vedios(filename=file.name, content_type=file.content_type, document=file)
        newvedio.save()
        return newvedio
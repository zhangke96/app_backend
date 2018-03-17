from django import forms
from django.db import transaction
from .models import vedios

class VedioForm(forms.Form):
    vedio = forms.FileField(required=True)
    description = forms.CharField(required=True)

    def save(self):
        file = self.cleaned_data['vedio']
        newvedio = vedios(filename=file.name, content_type=file.content_type, document=file,
                          description=self.cleaned_data['description'])
        newvedio.save()
        return newvedio

class NoteForm(forms.Form):
    vedioId = forms.IntegerField(label="视频id", required=True)
    note = forms.CharField(required=True)
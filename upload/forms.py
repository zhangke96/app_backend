from django import forms
from django.db import transaction
from .models import UploadFile

class UploadFileForm(forms.Form):
    description = forms.CharField(max_length=1024, required=True)
    file = forms.FileField(required=True)

    def save(self, user):
        if not self.is_valid():
            return False
        cd = self.cleaned_data
        desc = cd['description']
        file = cd['file']
        with transaction.atomic():
            newFile = UploadFile(
                creator = user,
                description = desc,
                filename = file.name,
            )
            newFile.save()
            return True, newFile.id
        return False
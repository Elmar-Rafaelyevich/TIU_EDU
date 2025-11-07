from django import forms
from .models import Group, Presentation

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'notes']

class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['file', 'description']

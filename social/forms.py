from django import forms

from .models import Cirlce

class CircleForm(forms.ModelForm):
    class Meta:
        model = Circle

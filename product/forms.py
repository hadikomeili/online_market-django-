from django import forms
from .validators import *
from .models import *


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []
        widgets = [

        ]
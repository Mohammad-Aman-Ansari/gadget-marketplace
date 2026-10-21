from django import forms
from .models import Gadget


class GadgetForm(forms.ModelForm):
    class Meta:
        model = Gadget
        fields = ['category', 'title', 'brand', 'condition', 'price', 'stock', 'description', 'image']
        
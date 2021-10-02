from django.forms import ModelForm
from .models import *


class PostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'content']

from django.forms import ModelForm
from django import forms
from .models import *


class PostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'content']


class CommentModelForm(ModelForm):
    # Edit the css and widgets while displaying the form.
    body = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Add a comment...',
                'rows': 2,
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['body']

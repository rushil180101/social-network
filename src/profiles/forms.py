from django.forms import ModelForm
from .models import *


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'country', 'avatar']

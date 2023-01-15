from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Zone

class ZoneForm(ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
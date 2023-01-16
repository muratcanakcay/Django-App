from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Zone, User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'handle', 'email', 'password1', 'password2']

class ZoneForm(ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'handle', 'email', 'bio']



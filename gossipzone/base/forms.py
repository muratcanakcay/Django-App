from django.forms import ModelForm
from .models import Zone, User

class ZoneForm(ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
from django.contrib import admin
from .models import Zone, Topic, Gossip, User

admin.site.register(Zone)
admin.site.register(Topic)
admin.site.register(Gossip)
admin.site.register(User)
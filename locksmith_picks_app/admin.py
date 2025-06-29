from django.contrib import admin
from .models import Player, Team, DVP, MailingListSubscriber

# Register your models here.

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(DVP)
admin.site.register(MailingListSubscriber)
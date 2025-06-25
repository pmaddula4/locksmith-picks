from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Team, DVP, Player
import random

class Command(BaseCommand):
    help = 'delete teams'

    def handle(self, *args, **kwargs):
        Team.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("teams deleted"))

        for dvp in DVP.objects.all():
            print(dvp.team.get_name_display())

        self.stdout.write(self.style.SUCCESS("DVP list"))


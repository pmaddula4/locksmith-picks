from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Team, Player

class Command(BaseCommand):
    help = "create 10 players"

    def handle(self, *args, **kwargs):
        Player.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("players deleted"))

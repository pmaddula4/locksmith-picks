from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Player

class Command(BaseCommand):
    help = 'update player stats for l10 and season'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('starting update'))

        players = Player.objects.all()
        for player in players:
            player.ppg -= 1
            player.ppg10 -= 0.5
            player.save()

        self.stdout.write(self.style.SUCCESS('updated successfully'))

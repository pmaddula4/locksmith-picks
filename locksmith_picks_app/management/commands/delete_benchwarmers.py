from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Player

class Command(BaseCommand):
    help = 'delete benchwarmers'

    def handle(self, *args, **kwargs):
        players = Player.objects.all()
        count = 0
        for warmer in players:
            if warmer.ppg + warmer.rpg + warmer.apg + warmer.bpg + warmer.spg < 10:
                self.stdout.write(f"deleting {warmer.name} with stats")
                warmer.delete()
                count += 1
        self.stdout.write(f"Deleted {count} benchwarmers.")

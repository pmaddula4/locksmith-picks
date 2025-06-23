from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Team, DVP, Player
import random

class Command(BaseCommand):
    help = 'initialize DVP'

    def handle(self, *args, **kwargs):
        DVP.objects.all().delete()
        positions = Player.POSITIONS

        for team in Team.objects.all():
            for code, label in positions:
                dvp, created = DVP.objects.get_or_create(
                    team=team,
                    position=code,
                    defaults={
                        'points_allowed': round(random.uniform(20, 25), 2),
                        'rebounds_allowed': round(random.uniform(8, 10), 2),
                        'assists_allowed': round(random.uniform(4, 6), 2),
                        'steals_allowed': round(random.uniform(1, 2), 2),
                        'blocks_allowed': round(random.uniform(0.5, 1.5), 2)
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Created: {team.get_name_display()} vs. {label}"
                    ))

        self.stdout.write(self.style.SUCCESS("DVP initialized"))

from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Team, DVP, Player

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
                        'points_allowed': 0.0,
                        'rebounds_allowed': 0.0,
                        'assists_allowed': 0.0,
                        'steals_allowed': 0.0,
                        'blocks_allowed': 0.0,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Created: {team.get_name_display()} vs. {label}"
                    ))

        self.stdout.write(self.style.SUCCESS("DVP initialized"))

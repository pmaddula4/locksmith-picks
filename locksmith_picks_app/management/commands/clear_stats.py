from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Player, DVP

class Command(BaseCommand):
    help = "clear all stats"

    def handle(self, *args, **kwargs):
        for player in Player.objects.all():
            player.ppg = 0.0
            player.rpg = 0.0
            player.apg = 0.0
            player.spg = 0.0
            player.bpg = 0.0

            player.ppg10 = 0.0
            player.rpg10 = 0.0
            player.apg10 = 0.0
            player.spg10 = 0.0
            player.bpg10 = 0.0

            player.pts_summary = []
            player.reb_summary = []
            player.ast_summary = []
            player.stl_summary = []
            player.blk_summary = []

            player.save()

        for dvp in DVP.objects.all():
            dvp.points_allowed_avg = 0.0
            dvp.rebounds_allowed_avg = 0.0
            dvp.assists_allowed_avg = 0.0
            dvp.steals_allowed_avg = 0.0
            dvp.blocks_allowed_avg = 0.0

            dvp.points_allowed_total = 0
            dvp.rebounds_allowed_total = 0
            dvp.assists_allowed_total = 0
            dvp.steals_allowed_total = 0
            dvp.blocks_allowed_total = 0

            dvp.gameLogs = 0

            dvp.save()

        self.stdout.write(self.style.SUCCESS("all stats cleared"))

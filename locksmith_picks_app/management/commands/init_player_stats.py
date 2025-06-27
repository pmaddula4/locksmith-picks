import requests, os
import time
from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Player
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = "update player stats with API"

    def handle(self, *args, **options):
        url = "https://api-nba-v1.p.rapidapi.com/players/statistics"
        
        headers = {
            "x-rapidapi-key": os.environ["RAPIDAPI_KEY"],
            "x-rapidapi-host": os.environ["RAPIDAPI_HOST"]
        }

        player_ids = Player.objects.values_list('playerID', flat=True)
        updated_count = 0

        for player_id in player_ids:
            try:
                player = Player.objects.get(playerID=player_id)
                self.stdout.write(self.style.SUCCESS(f"updating {player.name} with id {player.playerID}"))

                querystring = {"id": player.playerID, "season": "2024"}

                response = requests.get(url, headers=headers, params=querystring)
                response.raise_for_status()

                time.sleep(6.5)

                data = response.json()
                gamelogs = data.get("response", [])
                self.stdout.write(self.style.SUCCESS(f"got {len(gamelogs)} games for {player.name} with id {player.playerID}"))

                if not gamelogs:
                    self.stdout.write(self.style.WARNING(f"no stats for {player.name}"))
                    continue

                gamelogs = sorted(gamelogs, key=lambda g: g["game"]["id"])

                player.pts_summary = [g.get("points", 0) for g in gamelogs]
                player.reb_summary = [g.get("totReb", 0) for g in gamelogs]
                player.ast_summary = [g.get("assists", 0) for g in gamelogs]
                player.stl_summary = [g.get("steals", 0) for g in gamelogs]
                player.blk_summary = [g.get("blocks", 0) for g in gamelogs]

                num_games = len(player.pts_summary)
                if num_games:
                    player.ppg = round(sum(player.pts_summary) / num_games, 1)
                    player.rpg = round(sum(player.reb_summary) / num_games, 1)
                    player.apg = round(sum(player.ast_summary) / num_games, 1)
                    player.spg = round(sum(player.stl_summary) / num_games, 1)
                    player.bpg = round(sum(player.blk_summary) / num_games, 1)

                    l10_pts = player.pts_summary[-10:]
                    l10_reb = player.reb_summary[-10:]
                    l10_ast = player.ast_summary[-10:]
                    l10_stl = player.stl_summary[-10:]
                    l10_blk = player.blk_summary[-10:]

                    if len(l10_pts):
                        player.ppg10 = round(sum(l10_pts) / len(l10_pts), 1)
                        player.rpg10 = round(sum(l10_reb) / len(l10_reb), 1)
                        player.apg10 = round(sum(l10_ast) / len(l10_ast), 1)
                        player.spg10 = round(sum(l10_stl) / len(l10_stl), 1)
                        player.bpg10 = round(sum(l10_blk) / len(l10_blk), 1)

                player.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"updated {player.name} with id {player.playerID}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"error updating {player.name} with id {player_id}: error: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"updated {updated_count} players with stats"))

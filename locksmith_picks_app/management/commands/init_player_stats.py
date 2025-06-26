import requests, os
from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Player
from dotenv import load_dotenv
import time

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

                time.sleep(8)

                data = response.json()
                gamelogs = data.get("response", [])

                if not gamelogs:
                    self.stdout.write(self.style.WARNING(f"no stats for {player.name}"))
                    continue

                total_pts = 0
                total_reb = 0
                total_ast = 0
                total_stl = 0
                total_blk = 0

                for game in gamelogs:
                    total_pts += game.get("points", 0)
                    total_reb += game.get("totReb", 0)
                    total_ast += game.get("assists", 0)
                    total_stl += game.get("steals", 0)
                    total_blk += game.get("blocks", 0)

                num_games = len(gamelogs)
                if num_games > 0:
                    player.ppg = round(total_pts / num_games, 1)
                    player.rpg = round(total_reb / num_games, 1)
                    player.apg = round(total_ast / num_games, 1)
                    player.spg = round(total_stl / num_games, 1)
                    player.bpg = round(total_blk / num_games, 1)

                last10 = sorted(gamelogs, key=lambda g: g["game"]["id"], reverse=True)[:10]
                l10_pts = 0
                l10_reb = 0
                l10_ast = 0
                l10_stl = 0
                l10_blk = 0

                for game in last10:
                    l10_pts += game.get("points", 0)
                    l10_reb += game.get("totReb", 0)
                    l10_ast += game.get("assists", 0)
                    l10_stl += game.get("steals", 0)
                    l10_blk += game.get("blocks", 0)

                if last10:
                    player.ppg10 = round(l10_pts / len(last10), 1)
                    player.rpg10 = round(l10_reb / len(last10), 1)
                    player.apg10 = round(l10_ast / len(last10), 1)
                    player.spg10 = round(l10_stl / len(last10), 1)
                    player.bpg10 = round(l10_blk / len(last10), 1)

                player.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"updated {player.name} with id {player.playerID}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"error updating {player.name} with id {player_id}: error: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"updated {updated_count} players with stats"))

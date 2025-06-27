import requests, os
from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Team, Player
from dotenv import load_dotenv
from locksmith_picks_app.utils import map_api_position_to_dvp_slots
import time

load_dotenv()

class Command(BaseCommand):
    help = 'initialize players with API'

    def handle(self, *args, **kwargs):
        url = "https://api-nba-v1.p.rapidapi.com/players"

        headers = {
            "x-rapidapi-key": os.environ["RAPIDAPI_KEY"],
            "x-rapidapi-host": os.environ["RAPIDAPI_HOST"]
        }

        team_ids = Team.objects.values_list('teamID', flat=True)
        playerCount = 0
        teamCount = 0

        for teamID in team_ids:

            querystring = {"team":teamID,"season":"2024"}
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()

            time.sleep(7)
            
            data = response.json()
            players = data.get('response', [])

            self.stdout.write(self.style.SUCCESS(f"retrieved {len(players)} players from teamID {teamID} from API"))

            try:
                team = Team.objects.get(teamID=teamID)
            except Team.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"team with teamID {teamID} not found, skipping"))
                continue

            for player in players:
                name = player["firstname"] + " " + player["lastname"]
                position = player.get("leagues", {}).get("standard", {}).get("pos")
                if not position:
                    self.stdout.write(self.style.WARNING(f"player {name} has no position, skipping"))
                    continue
                playerid = player["id"]
                playerTeam = team

                Player.objects.create(
                    name = name,
                    position = position,
                    playerID = playerid,
                    team = playerTeam
                )

                playerCount += 1

            teamCount += 1

        self.stdout.write(self.style.SUCCESS(f"created {playerCount} players from {teamCount} teams from API"))
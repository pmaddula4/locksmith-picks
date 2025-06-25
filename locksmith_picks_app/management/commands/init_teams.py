import requests, os
from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Team
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'initialize teams with API'

    def handle(self, *args, **kwargs):
        url = "https://api-nba-v1.p.rapidapi.com/teams"

        headers = {
            "x-rapidapi-key": os.environ["RAPIDAPI_KEY"],
            "x-rapidapi-host": os.environ["RAPIDAPI_HOST"]
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        teams = data.get('response', [])

        self.stdout.write(self.style.SUCCESS(f"Retrieved {len(teams)} teams from API"))

        Team.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Deleted existing teams"))

        teamCount = 0
        for team in teams:
            if not team["nbaFranchise"]:
                continue

            code = team["code"]
            id = team["id"]
            
            if not code or not id:
                continue

            Team.objects.create(
                name = code,
                teamID = id
            )
            teamCount += 1

        self.stdout.write(self.style.SUCCESS(f"created {teamCount} teams from API"))
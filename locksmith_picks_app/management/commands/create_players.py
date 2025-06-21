from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Team, Player

class Command(BaseCommand):
    help = "create 10 players"

    def handle(self, *args, **kwargs):
        Player.objects.all().delete()

        players_data = [
            {
                "name": "Shai Gilgeous-Alexander",
                "position": "PG",
                "team_name": "Oklahoma City Thunder",
                "ppg": 32.7, "rpg": 5, "apg": 6.4, "spg": 1.2, "bpg": 0.5,
                "ppg10": 30.9, "rpg10": 4.8, "apg10": 5.9, "spg10": 1.8, "bpg10": 1
            },
            {
                "name": "Donovan Mitchell",
                "position": "SG",
                "team_name": "Cleveland Cavaliers",
                "ppg": 24, "rpg": 4.5, "apg": 5, "spg": 1.3, "bpg": 0.2,
                "ppg10": 28.5, "rpg10": 4.8, "apg10": 4.1, "spg10": 1.9, "bpg10": 0.3
            },
            {
                "name": "LeBron James",
                "position": "SF",
                "team_name": "Los Angeles Lakers",
                "ppg": 24.4, "rpg": 7.8, "apg": 8.2, "spg": 1, "bpg": 0.6,
                "ppg10": 24.2, "rpg10": 6.6, "apg10": 5.7, "spg10": 1.6, "bpg10": 0.9
            },
            {
                "name": "Giannis Antetokounmpo",
                "position": "PF",
                "team_name": "Milwaukee Bucks",
                "ppg": 30.4, "rpg": 11.9, "apg": 6.5, "spg": 0.9, "bpg": 1.2,
                "ppg10": 31.9, "rpg10": 14.4, "apg10": 9.3, "spg10": 0.9, "bpg10": 1
            },
            {
                "name": "Nikola Jokic",
                "position": "C",
                "team_name": "Denver Nuggets",
                "ppg": 29.6, "rpg": 12.7, "apg": 10.2, "spg": 1.8, "bpg": 0.6,
                "ppg10": 25.3, "rpg10": 12.4, "apg10": 6.9, "spg10": 1.9, "bpg10": 1
            },
            {
                "name": "Tyrese Haliburton",
                "position": "PG",
                "team_name": "Indiana Pacers",
                "ppg": 18.6, "rpg": 3.5, "apg": 9.2, "spg": 1.4, "bpg": 0.7,
                "ppg10": 17, "rpg10": 5.6, "apg10": 8.2, "spg10": 2, "bpg10": 0.6
            },
            {
                "name": "Anthony Edwards",
                "position": "SG",
                "team_name": "Minnesota Timberwolves",
                "ppg": 27.6, "rpg": 5.7, "apg": 4.5, "spg": 1.2, "bpg": 0.6 ,
                "ppg10": 24.6, "rpg10": 7.5, "apg10": 5.1, "spg10": 1.1, "bpg10": 0.9
            },
            {
                "name": "Jayson Tatum",
                "position": "SF",
                "team_name": "Boston Celtics",
                "ppg": 26.8, "rpg": 8.7, "apg": 6, "spg": 1.1, "bpg": 0.5,
                "ppg10": 27.3, "rpg10": 10.7, "apg10": 5.6, "spg10": 1.8, "bpg10": 0.7
            },
            {
                "name": "Kevin Durant",
                "position": "PF",
                "team_name": "Phoenix Suns",
                "ppg": 26.6, "rpg": 6, "apg": 4.2, "spg": 0.8, "bpg": 1.2,
                "ppg10": 24.6, "rpg10": 5.5, "apg10": 3.7, "spg10": 0.6, "bpg10": 0.9
            },
            {
                "name": "Joel Embiid",
                "position": "C",
                "team_name": "Philadelphia 76ers",
                "ppg": 23.8, "rpg": 8.2, "apg": 4.5, "spg": 0.7, "bpg": 0.9,
                "ppg10": 26, "rpg10": 9.2, "apg10": 5, "spg10": 0.8, "bpg10": 1
            }
        ]

        for player in players_data:
            team = None
            for code, display in Team.TEAMS:
                if display == player["team_name"]:
                    team = Team.objects.get(name=code)
                    break
            if not team:
                self.stdout.write(self.style.ERROR(f"team DNE"))
                continue

            p = Player.objects.create(
                name=player["name"],
                position=player["position"],
                ppg=player["ppg"],
                rpg=player["rpg"],
                apg=player["apg"],
                spg=player["spg"],
                bpg=player["bpg"],
                ppg10=player["ppg10"],
                rpg10=player["rpg10"],
                apg10=player["apg10"],
                spg10=player["spg10"],
                bpg10=player["bpg10"],
                team=team
            )

            self.stdout.write(self.style.SUCCESS(
                f"created {p.name} ({p.get_position_display()}) for {team.get_name_display()}"
            ))

        self.stdout.write(self.style.SUCCESS("players made"))

from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Team, Player
import random

class Command(BaseCommand):
    help = "create 10 players"

    def handle(self, *args, **kwargs):

        player_names = [
            "Stephen Curry", "Luka Doncic", "James Harden", "Jimmy Butler", "Devin Booker",
            "Trae Young", "Damian Lillard", "Ja Morant", "Karl-Anthony Towns", "Zion Williamson",
            "Paul George", "Kawhi Leonard", "Bradley Beal", "Chris Paul", "De'Aaron Fox",
            "Pascal Siakam", "Bam Adebayo", "Rudy Gobert", "Jrue Holiday", "CJ McCollum",
            "Brandon Ingram", "Jalen Brunson", "Desmond Bane", "LaMelo Ball", "Tyler Herro",
            "DeMar DeRozan", "Zach LaVine", "Mikal Bridges", "Darius Garland", "Fred VanVleet",
            "OG Anunoby", "Miles Bridges", "Jarrett Allen", "Jaden Ivey", "Jabari Smith Jr.",
            "Alperen Sengun", "Franz Wagner", "Paolo Banchero", "Scottie Barnes", "Cade Cunningham",
            "Josh Giddey", "RJ Barrett", "Jordan Poole", "Austin Reaves", "Dillon Brooks",
            "Michael Porter Jr.", "Norman Powell", "Terry Rozier", "Buddy Hield", "Harrison Barnes",
            "Herbert Jones", "Jonas Valanciunas", "Clint Capela", "Mitchell Robinson", "Robert Williams III",
            "Brook Lopez", "Bobby Portis", "Marcus Smart", "Derrick White", "Al Horford",
            "Malcolm Brogdon", "Grant Williams", "Isaiah Hartenstein", "Quentin Grimes", "Immanuel Quickley",
            "Donte DiVincenzo", "Aaron Gordon", "Bruce Brown", "Kentavious Caldwell-Pope", "Kyle Kuzma",
            "Kristaps Porzingis", "Monte Morris", "Corey Kispert", "Daniel Gafford", "Andrew Wiggins",
            "Kevon Looney", "Jonathan Kuminga", "Gary Payton II", "Draymond Green", "Jordan Clarkson",
            "Collin Sexton", "Walker Kessler", "Kelly Olynyk", "Jarred Vanderbilt", "Talen Horton-Tucker",
            "Malik Beasley", "D'Angelo Russell", "Rui Hachimura", "Mo Bamba", "Lonnie Walker IV",
            "Patrick Beverley", "Alex Caruso", "Ayo Dosunmu", "Coby White", "Nikola Vucevic",
            "Andre Drummond", "P.J. Washington", "Mark Williams", "Dennis Smith Jr.", "Gordon Hayward",
            "Tobias Harris", "De'Anthony Melton", "Tyrese Maxey", "P.J. Tucker", "Matisse Thybulle",
            "Jaylen Brown", "Robert Covington", "Ivica Zubac", "Reggie Jackson", "John Wall",
            "Russell Westbrook", "Austin Rivers", "Eric Gordon", "Jalen Green", "Kevin Porter Jr.",
            "Sengun Aydin", "Kenyon Martin Jr.", "Usman Garuba", "Tari Eason", "Jae'Sean Tate",
            "Victor Oladipo", "Max Strus", "Gabe Vincent", "Caleb Martin", "Duncan Robinson",
            "Cam Johnson", "Moses Moody", "Dyson Daniels", "Precious Achiuwa", "Davion Mitchell",
            "Obi Toppin", "Naz Reid", "Isaiah Joe", "Saddiq Bey", "Josh Hart"
        ]


        for i in range(135):
            teams = Team.objects.all()
            if not teams:
                self.stdout.write(self.style.ERROR("No teams found. Please create teams first."))
                return
            team = random.choice(teams)
            position = random.choice(["PG", "SG", "SF", "PF", "C"])

            ppg = round(random.uniform(10, 35), 1)
            rpg = round(random.uniform(3, 15), 1)
            apg = round(random.uniform(2, 12), 1)
            spg = round(random.uniform(0.5, 2.5), 1)
            bpg = round(random.uniform(0.5, 2.5), 1)

            p = Player.objects.create(
                name=player_names[i],
                position=position,
                team=team,
                ppg=ppg,
                rpg=rpg,
                apg=apg,
                spg=spg,
                bpg=bpg,
                ppg10=round(random.uniform(ppg - 7, ppg + 7), 1),
                rpg10=round(random.uniform(rpg - 5, rpg + 5), 1),
                apg10=round(random.uniform(apg - 5, apg + 5), 1),
                spg10=round(random.uniform(spg - 2, spg + 2), 1),
                bpg10=round(random.uniform(bpg - 2, bpg + 2), 1),
            )

            self.stdout.write(self.style.SUCCESS(
                f"created {p.name} ({p.get_position_display()}) for {team.get_name_display()}"
            ))

        self.stdout.write(self.style.SUCCESS("players made"))

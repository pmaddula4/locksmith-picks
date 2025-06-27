from django.db import models
from django.contrib.postgres.fields import ArrayField

class Team(models.Model):
    HAWKS = 'ATL'
    CELTICS = 'BOS'
    NETS = 'BKN'
    HORNETS = 'CHA'
    BULLS = 'CHI'
    CAVALIERS = 'CLE'
    MAVERICKS = 'DAL'
    NUGGETS = 'DEN'
    WARRIORS = 'GSW'
    ROCKETS = 'HOU'
    PACERS = 'IND'
    CLIPPERS = 'LAC'
    LAKERS = 'LAL'
    GRIZZLIES = 'MEM'
    HEAT = 'MIA'
    BUCKS = 'MIL'
    TIMBERWOLVES = 'MIN'
    PELICANS = 'NOP'
    KNICKS = 'NYK'
    THUNDER = 'OKC'
    MAGIC = 'ORL'
    SIXERS = 'PHI'
    SUNS = 'PHX'
    BLAZERS = 'POR'
    KINGS = 'SAC'
    SPURS = 'SAS'
    RAPTORS = 'TOR'
    JAZZ = 'UTA'
    WIZARDS = 'WAS'
    PISTONS = 'DET'
    TEAMS = [
        (HAWKS, 'Atlanta Hawks'),
        (CELTICS, 'Boston Celtics'),
        (NETS, 'Brooklyn Nets'),
        (HORNETS, 'Charlotte Hornets'),
        (BULLS, 'Chicago Bulls'),
        (CAVALIERS, 'Cleveland Cavaliers'),
        (MAVERICKS, 'Dallas Mavericks'),
        (NUGGETS, 'Denver Nuggets'),
        (WARRIORS, 'Golden State Warriors'),
        (ROCKETS, 'Houston Rockets'),
        (PACERS, 'Indiana Pacers'),
        (CLIPPERS, 'Los Angeles Clippers'),
        (LAKERS, 'Los Angeles Lakers'),
        (GRIZZLIES, 'Memphis Grizzlies'),
        (HEAT, 'Miami Heat'),
        (BUCKS, 'Milwaukee Bucks'),
        (TIMBERWOLVES, 'Minnesota Timberwolves'),
        (PELICANS, 'New Orleans Pelicans'),
        (KNICKS, 'New York Knicks'),
        (THUNDER, 'Oklahoma City Thunder'),
        (MAGIC, 'Orlando Magic'),
        (SIXERS, 'Philadelphia 76ers'),
        (SUNS, 'Phoenix Suns'),
        (BLAZERS, 'Portland Trail Blazers'),
        (KINGS, 'Sacramento Kings'),
        (SPURS, 'San Antonio Spurs'),
        (RAPTORS, 'Toronto Raptors'),
        (JAZZ, 'Utah Jazz'),
        (WIZARDS, 'Washington Wizards'),
        (PISTONS, 'Detroit Pistons')
    ]
    name = models.CharField(max_length = 3, choices = TEAMS)
    teamID = models.IntegerField(null = True, blank = True)
    
    def __str__(self):
        return self.name

class Player(models.Model):
    POSITIONS = [
        ('G', 'Guard'),
        ('F', 'Forward'),
        ('C', 'Center'),
        ('G-F', 'Guard-Forward'),
        ('F-G', 'Forward-Guard'),
        ('F-C', 'Forward-Center'),
        ('C-F', 'Center-Forward')
    ]
    name = models.CharField(max_length = 25)
    position = models.CharField(max_length = 4, choices = POSITIONS)
    playerID = models.IntegerField(null = True, blank = True)
    team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name = 'players')

    ppg = models.FloatField(default = 0.0)
    rpg = models.FloatField(default = 0.0)
    apg = models.FloatField(default = 0.0)
    spg = models.FloatField(default = 0.0)
    bpg = models.FloatField(default = 0.0)

    ppg10 = models.FloatField(default = 0.0)
    rpg10 = models.FloatField(default = 0.0)
    apg10 = models.FloatField(default = 0.0)
    spg10 = models.FloatField(default = 0.0)
    bpg10 = models.FloatField(default = 0.0)

    pts_summary = ArrayField(models.IntegerField(), default=list, blank=True)
    reb_summary = ArrayField(models.IntegerField(), default=list, blank=True)
    ast_summary = ArrayField(models.IntegerField(), default=list, blank=True)
    stl_summary = ArrayField(models.IntegerField(), default=list, blank=True)
    blk_summary = ArrayField(models.IntegerField(), default=list, blank=True)

    def __str__(self):
        return self.name
    
class DVP(models.Model):
    DVP_POSITIONS = [
        ('PG', 'Point Guard'),
        ('SG', 'Shooting Guard'),
        ('SF', 'Small Forward'),
        ('PF', 'Power Forward'),
        ('C', 'Center')
    ]
    team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name = 'dvp')
    position = models.CharField(max_length = 2, choices = DVP_POSITIONS)

    points_allowed_avg = models.FloatField(default = 0.0)
    rebounds_allowed_avg = models.FloatField(default = 0.0)
    assists_allowed_avg = models.FloatField(default = 0.0)
    steals_allowed_avg = models.FloatField(default = 0.0)
    blocks_allowed_avg = models.FloatField(default = 0.0)

    points_allowed_total = models.IntegerField(default = 0)
    rebounds_allowed_total = models.IntegerField(default = 0)
    assists_allowed_total = models.IntegerField(default = 0)
    steals_allowed_total = models.IntegerField(default = 0)
    blocks_allowed_total = models.IntegerField(default = 0)

    gameLogs = models.IntegerField(default = 0)
    
    class Meta:
        unique_together = ('team', 'position')

    def __str__(self):
        return f"{self.team.name} - {self.get_position_display()}"
    
class MailingListSubscriber(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    favorite_team = models.ForeignKey(Team, on_delete = models.SET_NULL, null = True, blank = True)
    email = models.EmailField(unique = True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    


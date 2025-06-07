from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length = 100)
    ptsAvg = models.FloatField(default = 0.0)
    rebsAvg = models.FloatField(default = 0.0)
    astsAvg = models.FloatField(default = 0.0)
    stlsAvg = models.FloatField(default = 0.0)
    blksAvg = models.FloatField(default = 0.0)
    ptsl10 = models.FloatField(default = 0.0)
    rebsl10 = models.FloatField(default = 0.0)
    astsl10 = models.FloatField(default = 0.0)
    stlsl10 = models.FloatField(default = 0.0)
    blksl10 = models.FloatField(default = 0.0)
    team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name = 'players')

    def __str__(self):
        return self.name
    
    def points(self):
        return self.ptsAvg
    
    def rebounds(self):
        return self.rebsAvg
    
    def assists(self):
        return self.astsAvg   
    
    def steals(self):
        return self.stlsAvg
    
    def blocks(self):
        return self.blksAvg
    
    def points_l10(self):
        return self.ptsl10
    
    def rebounds_l10(self):
        return self.rebsl10
    
    def assists_l10(self):
        return self.astsl10
    
    def steals_l10(self):
        return self.stlsl10
    
    def blocks_l10(self):
        return self.blksl10
    

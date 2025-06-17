from django.shortcuts import render
from .forms import MailingListForm
from .models import Team

# Create your views here.
def index(request):
    return render(request, 'locksmith_picks_app/index.html')

def defvpos(request):
    return render(request, 'locksmith_picks_app/defvpos.html')

def hotandcold(request):
    return render(request, 'locksmith_picks_app/hotandcold.html')

def l10(request):
    return render(request, 'locksmith_picks_app/l10.html')

def mailinglist(request):
    form = MailingListForm()
    teams = list(Team.objects.all())
    teams.sort(key = lambda t: t.get_name_display())
    return render(request, 'locksmith_picks_app/mailinglist.html', {'form': form, 'teams': teams})
from django.shortcuts import render, redirect
from .forms import MailingListForm
from .models import Team, MailingListSubscriber, DVP

# Create your views here.
def index(request):
    return render(request, 'locksmith_picks_app/index.html')

def defvpos(request):
    position = request.GET.get('position', 'PG')
    stats = DVP.objects.filter(position = position)

    return render(request, 'locksmith_picks_app/defvpos.html', {'stats': stats, 'selected': position})

def hotandcold(request):
    return render(request, 'locksmith_picks_app/hotandcold.html')

def l10(request):
    return render(request, 'locksmith_picks_app/l10.html')

def mailinglist(request):
    form = MailingListForm()
    teams = list(Team.objects.all())
    teams.sort(key = lambda t: t.get_name_display())

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        favorite_team_id = request.POST.get('favorite_team')
        email = request.POST.get('email')
        if favorite_team_id:
            try:
                favorite_team = Team.objects.get(id=favorite_team_id)
            except Team.DoesNotExist:
                favorite_team = None
        else:
            favorite_team = None
        MailingListSubscriber.objects.create(
            first_name = first_name,
            last_name = last_name,
            favorite_team = favorite_team,
            email = email
        )
        return redirect('index')
    
    return render(request, 'locksmith_picks_app/mailinglist.html', {'form': form, 'teams': teams})
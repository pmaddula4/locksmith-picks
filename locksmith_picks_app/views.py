from django.shortcuts import render, redirect
from .forms import MailingListForm
from .models import Team, MailingListSubscriber, DVP, Player

# Create your views here.
def index(request):
    return render(request, 'locksmith_picks_app/index.html')

def defvpos(request):
    position = request.GET.get('position', 'PG')
    sort = request.GET.get('sort', 'team__name')
    order = request.GET.get('order', 'asc')

    sort_options = [
        'team__name',
        'points_allowed',
        'rebounds_allowed',
        'assists_allowed',
        'steals_allowed',
        'blocks_allowed'
    ]

    if sort not in sort_options:
        sort = 'team__name'
    if order == 'asc':
        sort_field = sort
    else:
        sort_field = f"-{sort}"

    stats = DVP.objects.filter(position = position).order_by(sort_field)

    return render(request, 'locksmith_picks_app/defvpos.html', {'stats': stats, 'selected': position, 'current_sort': sort, 'current_order': order})

def hotandcold(request):
    return render(request, 'locksmith_picks_app/hotandcold.html')

def l10(request):
    players = Player.objects.all()

    return render(request, 'locksmith_picks_app/l10.html', {'players': players})

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
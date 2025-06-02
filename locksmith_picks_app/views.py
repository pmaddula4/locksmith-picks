from django.shortcuts import render

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
    return render(request, 'locksmith_picks_app/mailinglist.html')
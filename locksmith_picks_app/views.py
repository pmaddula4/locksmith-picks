from django.shortcuts import render, redirect
from .forms import MailingListForm
from .models import Team, MailingListSubscriber, DVP, Player
from collections import OrderedDict
import numpy as np
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

def index(request):
    return render(request, 'locksmith_picks_app/index.html')

def defvpos(request):
    try:
        position = request.GET.get('position', 'PG')
        sort = request.GET.get('sort', 'team__name')
        order = request.GET.get('order', 'asc')

        stat_fields = [
            'points_allowed_avg',
            'rebounds_allowed_avg',
            'assists_allowed_avg',
            'steals_allowed_avg',
            'blocks_allowed_avg',
        ]
        sort_options = ['team__name'] + stat_fields

        if sort not in sort_options:
            sort = 'team__name'
        if order == 'asc':
            sort_field = sort
        else:
            sort_field = f"-{sort}"

        stats = DVP.objects.filter(position = position).order_by(sort_field)

        stats_list = list(stats)
        means = {}
        stddevs = {}

        for stat in stat_fields:
            values = [getattr(obj, stat) for obj in stats_list]
            means[stat] = np.mean(values)
            stddevs[stat] = np.std(values)

        for obj in stats_list:
            obj.flags = {}
            for stat in stat_fields:
                val = getattr(obj, stat)
                mean = means[stat]
                stddev = stddevs[stat]
                if val > mean + stddev:
                    obj.flags[stat] = 'high'
                elif val < mean - stddev:
                    obj.flags[stat] = 'low'
                else:
                    obj.flags[stat] = 'normal'

        context = {'stats': stats_list, 'selected': position, 'current_sort': sort, 'current_order': order}

        return render(request, 'locksmith_picks_app/defvpos.html', context)
    except Exception as e:
        return HttpResponse(f"<pre>{e}</pre>")

def hotandcold(request):
    try:
        players = Player.objects.all()
        hotpts = {}
        coldpts = {}
        hotreb = {}
        coldreb = {}
        hotast = {}
        coldast = {}
        hotstl = {}
        coldstl = {}
        hotblk = {}
        coldblk = {}
        for player in players:
            if player.ppg10 - player.ppg > 5:
                if len(hotpts) < 5:
                    hotpts[player] = round(player.ppg10 - player.ppg, 1)
                else:
                    min_player = min(hotpts, key=hotpts.get)
                    if player.ppg10 - player.ppg > hotpts[min_player]:
                        del hotpts[min_player]
                        hotpts[player] = round(player.ppg10 - player.ppg, 1)
            elif player.ppg10 - player.ppg < -5:
                if len(coldpts) < 5:
                    coldpts[player] = round(player.ppg10 - player.ppg, 1)
                else:
                    max_player = max(coldpts, key=coldpts.get)
                    if player.ppg10 - player.ppg < coldpts[max_player]:
                        del coldpts[max_player]
                        coldpts[player] = round(player.ppg10 - player.ppg, 1)
            if player.rpg10 - player.rpg > 3:
                if len(hotreb) < 5:
                    hotreb[player] = round(player.rpg10 - player.rpg, 1)
                else:
                    min_player = min(hotreb, key=hotreb.get)
                    if player.rpg10 - player.rpg > hotreb[min_player]:
                        del hotreb[min_player]
                        hotreb[player] = round(player.rpg10 - player.rpg, 1)
            elif player.rpg10 - player.rpg < -3:
                if len(coldreb) < 5:
                    coldreb[player] = round(player.rpg10 - player.rpg, 1)
                else:
                    max_player = max(coldreb, key=coldreb.get)
                    if player.rpg10 - player.rpg < coldreb[max_player]:
                        del coldreb[max_player]
                        coldreb[player] = round(player.rpg10 - player.rpg, 1)
            if player.apg10 - player.apg > 2.5:
                if len(hotast) < 5:
                    hotast[player] = round(player.apg10 - player.apg, 1)
                else:
                    min_player = min(hotast, key=hotast.get)
                    if player.apg10 - player.apg > hotast[min_player]:
                        del hotast[min_player]
                        hotast[player] = round(player.apg10 - player.apg, 1)
            elif player.apg10 - player.apg < -2.5:
                if len(coldast) < 5:
                    coldast[player] = round(player.apg10 - player.apg, 1)
                else:
                    max_player = max(coldast, key=coldast.get)
                    if player.apg10 - player.apg < coldast[max_player]:
                        del coldast[max_player]
                        coldast[player] = round(player.apg10 - player.apg, 1)
            if player.spg10 - player.spg > 0.8:
                if len(hotstl) < 5:
                    hotstl[player] = round(player.spg10 - player.spg, 1)
                else:
                    min_player = min(hotstl, key=hotstl.get)
                    if player.spg10 - player.spg > hotstl[min_player]:
                        del hotstl[min_player]
                        hotstl[player] = round(player.spg10 - player.spg, 1)
            elif player.spg10 - player.spg < -0.8:
                if len(coldstl) < 5:
                    coldstl[player] = round(player.spg10 - player.spg, 1)
                else:
                    max_player = max(coldstl, key=coldstl.get)
                    if player.spg10 - player.spg < coldstl[max_player]:
                        del coldstl[max_player]
                        coldstl[player] = round(player.spg10 - player.spg, 1)
            if player.bpg10 - player.bpg > 0.8:
                if len(hotblk) < 5:
                    hotblk[player] = round(player.bpg10 - player.bpg, 1)
                else:
                    min_player = min(hotblk, key=hotblk.get)
                    if player.bpg10 - player.bpg > hotblk[min_player]:
                        del hotblk[min_player]
                        hotblk[player] = round(player.bpg10 - player.bpg, 1)
            elif player.bpg10 - player.bpg < -0.8:
                if len(coldblk) < 5:
                    coldblk[player] = round(player.bpg10 - player.bpg, 1)
                else:
                    max_player = max(coldblk, key=coldblk.get)
                    if player.bpg10 - player.bpg < coldblk[max_player]:
                        del coldblk[max_player]
                        coldblk[player] = round(player.bpg10 - player.bpg, 1)

        hotpts = OrderedDict(sorted(hotpts.items(), key=lambda item: item[1], reverse=True))
        coldpts = OrderedDict(sorted(coldpts.items(), key=lambda item: item[1]))
        hotreb = OrderedDict(sorted(hotreb.items(), key=lambda item: item[1], reverse=True))
        coldreb = OrderedDict(sorted(coldreb.items(), key=lambda item: item[1]))
        hotast = OrderedDict(sorted(hotast.items(), key=lambda item: item[1], reverse=True))
        coldast = OrderedDict(sorted(coldast.items(), key=lambda item: item[1]))
        hotstl = OrderedDict(sorted(hotstl.items(), key=lambda item: item[1], reverse=True))
        coldstl = OrderedDict(sorted(coldstl.items(), key=lambda item: item[1]))
        hotblk = OrderedDict(sorted(hotblk.items(), key=lambda item: item[1], reverse=True))
        coldblk = OrderedDict(sorted(coldblk.items(), key=lambda item: item[1]))

        context = {
            'hotpts': hotpts,
            'coldpts': coldpts,
            'hotreb': hotreb,
            'coldreb': coldreb,
            'hotast': hotast,
            'coldast': coldast,
            'hotstl': hotstl,
            'coldstl': coldstl,
            'hotblk': hotblk,
            'coldblk': coldblk
        }

        return render(request, 'locksmith_picks_app/hotandcold.html', context)
    except Exception as e:
        return HttpResponse(f"<pre>{e}</pre>")

@cache_page(3600, cache="default")
def l10(request):
    try:
        query = request.GET.get('search', '')
        
        if query:
            players = Player.objects.filter(name__icontains=query).order_by('name')
        else:
            players = Player.objects.all().order_by('name')
        
        return render(request, 'locksmith_picks_app/l10.html', {'players': players, 'search_query': query})
    except Exception as e:
        return HttpResponse(f"<pre>{type(e).__name__}: {e}</pre>")

def subscribe_to_mailinglist(email, first_name, last_name, favorite_team_name):
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": settings.MAILCHIMP_API_KEY,
        "server": settings.MAILCHIMP_SERVER_PREFIX
    })

    try:
        response = client.lists.add_list_member(settings.MAILCHIMP_AUDIENCE_ID, {
            "email_address": email,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": first_name,
                "LNAME": last_name,
                "FTEAM": favorite_team_name
            }
        })
        return response
    except ApiClientError as error:
        if "permanently deleted" in error.text:
            print("User must manually re-subscribe.")
        else:
            print(f"Mailchimp error: {error.text}")
        return None

def mailinglist(request):
    try:
        form = MailingListForm()
        teams = list(Team.objects.all())
        teams.sort(key = lambda t: t.get_name_display())

        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            favorite_team_id = request.POST.get('favorite_team')
            email = request.POST.get('email')

            favorite_team = Team.objects.filter(id=favorite_team_id).first() if favorite_team_id else None
            favorite_team_name = favorite_team.get_name_display() if favorite_team else None

            MailingListSubscriber.objects.create(
                first_name=first_name,
                last_name=last_name,
                favorite_team=favorite_team,
                email=email
            )

            subscribe_to_mailinglist(email, first_name, last_name, favorite_team_name)

            return redirect('index')

        return render(request, 'locksmith_picks_app/mailinglist.html', {'form': form, 'teams': teams})
    except Exception as e:
        return HttpResponse(f"<pre>{e}</pre>")
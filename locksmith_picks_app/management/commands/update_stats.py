import requests, os
import time
from django.core.management.base import BaseCommand
from locksmith_picks_app.models import Player, DVP, Team
from locksmith_picks_app.utils import map_api_position_to_dvp_slots
from dotenv import load_dotenv
from datetime import date

load_dotenv()

class Command(BaseCommand):
    help = "update player stats with API daily"

    def handle(self, *args, **options):
        urlDay = "https://api-nba-v1.p.rapidapi.com/games"
        urlGame = "https://api-nba-v1.p.rapidapi.com/players/statistics"
        
        headers = {
            "x-rapidapi-key": os.environ["RAPIDAPI_KEY"],
            "x-rapidapi-host": os.environ["RAPIDAPI_HOST"]
        }

        querystringDay = {"date": date.today()}

        response = requests.get(urlDay, headers=headers, params=querystringDay)
        response.raise_for_status()

        time.sleep(6)

        data = response.json()
        gameIDs = data.get("response", [])
        self.stdout.write(self.style.SUCCESS(f"got {len(gameIDs)} games for today"))

        if not gameIDs:
            self.stdout.write(self.style.WARNING("no games for today"))
            return
        
        for game in gameIDs:
            try:
                gameID = game["id"]
                visitor_team = game["teams"]["visitor"]["id"]
                home_team = game["teams"]["home"]["id"]
                self.stdout.write(self.style.SUCCESS(f"updating game with id {gameID}"))

                querystringGame = {"game": gameID}

                response = requests.get(urlGame, headers=headers, params=querystringGame)
                response.raise_for_status()

                time.sleep(6)

                data = response.json()
                gameData = data.get("response", [])
                self.stdout.write(self.style.SUCCESS(f"got {len(gameData)} players for game {gameID}"))

                if not gameData:
                    self.stdout.write(self.style.WARNING(f"no stats for game {gameID}"))
                    continue

                for player_data in gameData:
                    try:
                        player_id = player_data["player"]["id"]
                        player_team_id = player_data["team"]["id"]

                        minutes = player_data.get("min")
                        if minutes is None or minutes == "" or minutes == "0:00":
                            self.stdout.write(self.style.WARNING(f"player {player_id} has no minutes played, skipping"))
                            continue

                        opponent_team_id = home_team if player_team_id == visitor_team else visitor_team
                        player_obj = Player.objects.get(playerID=player_id)

                        player_obj.pts_summary.append(player_data.get("points", 0))
                        player_obj.reb_summary.append(player_data.get("totReb", 0))
                        player_obj.ast_summary.append(player_data.get("assists", 0))
                        player_obj.stl_summary.append(player_data.get("steals", 0))
                        player_obj.blk_summary.append(player_data.get("blocks", 0))

                        num_games = len(player_obj.pts_summary)
                        if num_games:
                            player_obj.ppg = round(sum(player_obj.pts_summary) / num_games, 1)
                            player_obj.rpg = round(sum(player_obj.reb_summary) / num_games, 1)
                            player_obj.apg = round(sum(player_obj.ast_summary) / num_games, 1)
                            player_obj.spg = round(sum(player_obj.stl_summary) / num_games, 1)
                            player_obj.bpg = round(sum(player_obj.blk_summary) / num_games, 1)

                            l10_pts = player_obj.pts_summary[-10:]
                            l10_reb = player_obj.reb_summary[-10:]
                            l10_ast = player_obj.ast_summary[-10:]
                            l10_stl = player_obj.stl_summary[-10:]
                            l10_blk = player_obj.blk_summary[-10:]

                            if len(l10_pts):
                                player_obj.ppg10 = round(sum(l10_pts) / len(l10_pts), 1)
                                player_obj.rpg10 = round(sum(l10_reb) / len(l10_reb), 1)
                                player_obj.apg10 = round(sum(l10_ast) / len(l10_ast), 1)
                                player_obj.spg10 = round(sum(l10_stl) / len(l10_stl), 1)
                                player_obj.bpg10 = round(sum(l10_blk) / len(l10_blk), 1)
                        
                        try:
                            opponent_team = Team.objects.get(teamID=opponent_team_id)
                        except Team.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f"team with id {opponent_team} does not exist"))
                            continue

                        positions_to_be_updated = map_api_position_to_dvp_slots(player_obj.position)
                        for pos in positions_to_be_updated:
                            try:
                                dvp = DVP.objects.get(team=opponent_team, position=pos)
                                dvp.points_allowed_total += player_data.get("points", 0)
                                dvp.rebounds_allowed_total += player_data.get("totReb", 0)
                                dvp.assists_allowed_total += player_data.get("assists", 0)
                                dvp.steals_allowed_total += player_data.get("steals", 0)
                                dvp.blocks_allowed_total += player_data.get("blocks", 0)

                                dvp.gameLogs += 1

                                dvp.points_allowed_avg = round(dvp.points_allowed_total / dvp.gameLogs, 1)
                                dvp.rebounds_allowed_avg = round(dvp.rebounds_allowed_total / dvp.gameLogs, 1)
                                dvp.assists_allowed_avg = round(dvp.assists_allowed_total / dvp.gameLogs, 1)
                                dvp.steals_allowed_avg = round(dvp.steals_allowed_total / dvp.gameLogs, 1)
                                dvp.blocks_allowed_avg = round(dvp.blocks_allowed_total / dvp.gameLogs, 1)

                                dvp.save()
                                self.stdout.write(self.style.SUCCESS(f"updated dvp for {opponent_team.name} with position {pos}"))

                            except DVP.DoesNotExist:
                                self.stdout.write(self.style.ERROR(f"dvp for {opponent_team.name} with position {pos} does not exist"))
                                continue
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(f"error updating DVP for {opponent_team.name} with position {pos}: {str(e)}"))
                                continue

                        player_obj.save()
                        self.stdout.write(self.style.SUCCESS(f"updated player {player_obj.name} with id {player_obj.playerID}"))

                    except Player.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"{player_obj} does not exist"))
                        continue
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"error updating player {player_id}: {str(e)}"))
                        continue

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"error updating game {gameID}: {str(e)}"))
                continue

        self.stdout.write(self.style.SUCCESS("successfully updated player stats and DVPs for all games today"))
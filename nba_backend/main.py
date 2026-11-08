from fastapi import FastAPI
from fastapi import HTTPException
from nba_api.stats.static import teams
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonteamroster, commonplayerinfo, commonallplayers, scoreboardv2
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import traceback
import requests


#Creates a FastAPI object
app = FastAPI()
#To allow React to talk to Fast API
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Points to current season
CURRENT_SEASON = "2026-27"

ESPN_API = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"

def get_espn_teams():
    response = requests.get(f"{ESPN_API}/teams", timeout=10)
    response.raise_for_status()

    data = response.json()

    return [
        item["team"]
        for item in data["sports"][0]["leagues"][0]["teams"]
    ]


def find_espn_team(nba_team):
    espn_teams = get_espn_teams()

    for team in espn_teams:
        if team.get("displayName", "").lower() == nba_team["full_name"].lower():
            return team

    return None

#Teams category
@app.get("/teams")
def read_root():
    nba_teams = teams.get_teams()

    team_info = [
        {
        "Team ID": t["id"],
        "Team Name": t["full_name"],
        "Abbreviation": t["abbreviation"],
        "City": t["city"],
        "Nickname": t["nickname"],
        "State": t["state"],
        "Year Founded": t["year_founded"]
        }
    for t in nba_teams
    ]
    return team_info

#Players category
@app.get("/players")
def get_players():
    try:
        # Get all NBA teams from ESPN
        teams_url = f"{ESPN_API}/teams"
        response = requests.get(teams_url, timeout=10)
        response.raise_for_status()

        data = response.json()
        teams_list = data["sports"][0]["leagues"][0]["teams"]

        player_info = []
        seen_ids = set()

        # Loop through each NBA team
        for team_data in teams_list:
            team_id = team_data["team"]["id"]

            # Get the team's roster
            roster_url = f"{ESPN_API}/teams/{team_id}/roster"
            roster_response = requests.get(roster_url, timeout=10)
            roster_response.raise_for_status()

            roster_data = roster_response.json()

            for athlete in roster_data.get("athletes", []):
                player_id = athlete["id"]

                if player_id not in seen_ids:
                    seen_ids.add(player_id)

                    player_info.append({
                        "Full Name": athlete["fullName"],
                        "ID": player_id,
                        "Is Active": True
                    })

        # Sort players alphabetically
        player_info.sort(key=lambda x: x["Full Name"])

        return player_info

    except requests.RequestException as e:
        print(f"Error fetching players: {e}")
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve NBA players from ESPN."
        )


#Looking at players on a specific team
@app.get("/teams/{team_nickname}/players")
def get_team_players(team_nickname: str):
    nba_team = next(
        (
            t for t in teams.get_teams()
            if t["nickname"].lower() == team_nickname.lower()
        ),
        None
    )
    if nba_team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    try:
        espn_team = find_espn_team(nba_team)
        if espn_team is None:
            raise HTTPException(
                status_code=404,
                detail="Team not found in ESPN"
            )
        response = requests.get(
            f"{ESPN_API}/teams/{espn_team['id']}/roster",
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        player_info = []

        for player in data.get("athletes", []):
            player_info.append({
                "Player ID": player.get("id"),
                "Player Name": player.get("displayName"),
                "Jersey Number": player.get("jersey", ""),
                "Position": player.get("position", {}).get("abbreviation", ""),
                "Height": player.get("displayHeight", ""),
                "Weight": player.get("displayWeight", ""),
                "College Attended": (
                    player.get("college", {}).get("name", "")
                    if isinstance(player.get("college"), dict)
                    else ""
                )
            })
        return {
            "team_name": nba_team["full_name"],
            "team_id": nba_team["id"],
            "players": player_info
        }
    except requests.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"ESPN API error: {str(e)}"
        )

@app.get("/players/{player_id}/stats")
def get_player_stats(player_id: int):
    try:
        url = (
            "https://site.web.api.espn.com/apis/common/v3/"
            f"sports/basketball/nba/athletes/{player_id}/stats"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Retrieve player name from ESPN
        player_name = "Unknown Player"

        # Find the player using ESPN's Celtics roster
        # Find the player's team from their ESPN statistics
        team_id = None

        for category in data.get("categories", []):
            if category.get("name") != "averages":
                continue
            for statistic in reversed(category.get("statistics", [])):
                team_id = statistic.get("teamId")
                if team_id:
                    break
            if team_id:
                break

        roster_url = f"{ESPN_API}/teams/{team_id}/roster"
        roster_response = requests.get(roster_url, timeout=10)
        roster_response.raise_for_status()

        roster_data = roster_response.json()

        for player in roster_data.get("athletes", []):
            if str(player.get("id")) == str(player_id):
                player_name = player.get("displayName", "Unknown Player")
                break

        # Retrieve ESPN statistics
        categories = data.get("categories", [])
        season_stats = []

        for category in categories:
            if category.get("name") != "averages":
                continue

            names = category.get("names", [])

            for statistic in category.get("statistics", []):
                values = statistic.get("stats", [])
                row = dict(zip(names, values))

                season = statistic.get("season", {})
                team_slug = statistic.get("teamSlug", "")
                team_id = statistic.get("teamId", "")
                print("TEAM SLUG:", team_slug)
                print("TEAM ID:", team_id)
                

                season_id = (
                    season.get("displayName", "")
                    if isinstance(season, dict)
                    else str(season)
                )

                team_abbreviations = {
                    "atlanta-hawks": "ATL",
                    "boston-celtics": "BOS",
                    "brooklyn-nets": "BKN",
                    "charlotte-hornets": "CHA",
                    "chicago-bulls": "CHI",
                    "cleveland-cavaliers": "CLE",
                    "dallas-mavericks": "DAL",
                    "denver-nuggets": "DEN",
                    "detroit-pistons": "DET",
                    "golden-state-warriors": "GSW",
                    "houston-rockets": "HOU",
                    "indiana-pacers": "IND",
                    "los-angeles-clippers": "LAC",
                    "los-angeles-lakers": "LAL",
                    "memphis-grizzlies": "MEM",
                    "miami-heat": "MIA",
                    "milwaukee-bucks": "MIL",
                    "minnesota-timberwolves": "MIN",
                    "new-orleans-pelicans": "NOP",
                    "new-york-knicks": "NYK",
                    "oklahoma-city-thunder": "OKC",
                    "orlando-magic": "ORL",
                    "philadelphia-76ers": "PHI",
                    "phoenix-suns": "PHX",
                    "portland-trail-blazers": "POR",
                    "sacramento-kings": "SAC",
                    "san-antonio-spurs": "SAS",
                    "toronto-raptors": "TOR",
                    "utah-jazz": "UTA",
                    "washington-wizards": "WAS"
                }

                team_abbreviation = team_abbreviations.get(
                    team_slug, team_slug.upper()
                )

                season_stats.append({
                    "SEASON_ID": season_id,
                    "TEAM_ABBREVIATION": team_abbreviation,
                    "GP": int(float(row.get("gamesPlayed", 0))),
                    "PPG": float(row.get("avgPoints", 0)),
                    "APG": float(row.get("avgAssists", 0)),
                    "RPG": float(row.get("avgRebounds", 0)),
                    "SPG": float(row.get("avgSteals", 0)),
                    "BPG": float(row.get("avgBlocks", 0))
                })

        # Calculate career averages weighted by games played
        total_gp = sum(season["GP"] for season in season_stats)

        career_average = {}

        if total_gp > 0:
            career_average = {
                stat: round(
                    sum(
                        season[stat] * season["GP"]
                        for season in season_stats
                    ) / total_gp,
                    1
                )
                for stat in ["PPG", "APG", "RPG", "SPG", "BPG"]
            }

        return {
            "player_name": player_name,
            "career_average": career_average,
            "stats": season_stats,
            "message": (
                "" if season_stats
                else "No stats available for this player yet."
            )
        }

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve player statistics from ESPN."
        )
#Helper method to get player names (including rookies)
def get_player_name_helper(player_id: int) -> str:
    player = players.find_player_by_id(player_id)
    if player:
        return player["full_name"]
    try:
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        df = career_stats.get_data_frames()[0]
        if not df.empty and "PLAYER_NAME" in df.columns:
            return df["PLAYER_NAME"].iloc[0]
    except Exception:
        pass
    try:
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        df = player_info.get_data_frames()[0]
        return df["DISPLAY_FIRST_LAST"].iloc[0]
    except Exception:
        pass
    return "Unknown Player"

@app.get("/games/today")
def get_games_today():
    try:
        url = f"{ESPN_API}/scoreboard"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        games = []

        for event in data.get("events", []):
            competition = event["competitions"][0]
            competitors = competition.get("competitors", [])

            home = next(
                team for team in competitors
                if team["homeAway"] == "home"
            )

            away = next(
                team for team in competitors
                if team["homeAway"] == "away"
            )

            home_record = next(
                (record["summary"] for record in home.get("records", [])
                if record.get("type") == "total"),
                "N/A"
            )

            away_record = next(
                (record["summary"] for record in away.get("records", [])
                if record.get("type") == "total"),
                "N/A"
            )

            matchup = {
                "Game ID": event["id"],
                "Home Team": home["team"]["abbreviation"],
                "Away Team": away["team"]["abbreviation"],
                "Home Team ID": home["team"]["id"],
                "Away Team ID": away["team"]["id"],
                "Game Time": event["date"],
                "Arena": competition.get("venue", {}).get(
                    "fullName", "Unknown Arena"
                ),
                "Status": event["status"]["type"]["description"],
                "Home Score": home.get("score", "0"),
                "Away Score": away.get("score", "0"),
                "Home Record": home_record,
                "Away Record": away_record,
                "Quarter": event["status"].get("period", 0),
                "Clock": event["status"].get("displayClock", "0:00")
            }

            games.append(matchup)

        return {
            "date": data.get("day", {}).get("date", ""),
            "games": games,
            "message": "" if games else "No games today."
        }

    except requests.RequestException as e:
        print(f"Error fetching today's games: {e}")
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve today's NBA games from ESPN."
        )
    
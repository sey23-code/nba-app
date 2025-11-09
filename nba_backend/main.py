from fastapi import FastAPI
from nba_api.stats.static import teams
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonteamroster, commonplayerinfo, commonallplayers, scoreboardv2
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import traceback


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
def read_root():
    static_players = players.get_active_players()
    static_ids = {player["id"] for player in static_players}
    try:
        #Rookies
        live_df = commonallplayers.CommonAllPlayers(is_only_current_season=1).get_data_frames()[0]
        #Active players
        live_df = live_df[live_df["ROSTERSTATUS"] == 1]
        active_players = live_df[["PERSON_ID", "DISPLAY_FIRST_LAST"]].rename(
            columns={
                "PERSON_ID": "id",
                "DISPLAY_FIRST_LAST": "Full Name"
            }).to_dict(orient="records")
        
        rookies = [player for player in active_players if player["id"] not in static_ids]
        all_players = static_players + rookies
    except Exception as e:
        print(f"Could not fetch active rookies: {e}")
        return [
            {
                "Full Name": p["full_name"],
                "ID": p["id"],
                "Is Active": p["is_active"]
            }
            for p in static_players
        ]
    player_info = [
        {
        "Full Name": p["full_name"] if "full_name" in p else p["Full Name"],
        "ID": p["id"],
        "Is Active": p.get("is_active", True)
        }
        for p in all_players
    ]
    
    player_info = sorted(player_info, key=lambda x: x["Full Name"])
    return player_info

#Looking at players on a specific team
@app.get("/teams/{team_nickname}/players")
def get_team_players(team_nickname: str):
    nba_teams = teams.get_teams()
    team = next((t for t in nba_teams if t["nickname"].lower() == team_nickname.lower()), None)
    if team is None:
        return {"error": "No team found"}
    #Actual roster - list of players
    roster = commonteamroster.CommonTeamRoster(team_id=team["id"], season="2025-26")
    players = roster.get_data_frames()[0]
    player_info = [
        {
           "Player ID": row["PLAYER_ID"],
           "Player Name": row["PLAYER"],
           "Jersey Number": row["NUM"], 
           "Position": row["POSITION"],
           "Height": row["HEIGHT"],
           "Weight": row["WEIGHT"],
           "College Attended": row["SCHOOL"]
        }
        for _, row in players.iterrows()
    ]
    return {
        "team_name": team["full_name"],
        "team_id": team["id"],
        "players": player_info
    }

@app.get("/players/{player_id}/stats")
def get_player_stats(player_id: int):
    try:
        player_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        career = player_stats.get_data_frames()[0]
        player_name = get_player_name_helper(player_id)

        if career.empty:
            return {
                "player_name": player_name,
                "career_average": {},
                "stats": [],
                "message": "There are currently no stats for this player."
            }
        career = career[career["TEAM_ABBREVIATION"] != "TOT"]
        career["PPG"] = (career["PTS"] / career["GP"]).round(1)
        career["APG"] = (career["AST"] / career["GP"]).round(1)
        career["RPG"] = (career["REB"] / career["GP"]).round(1)
        career["SPG"] = (career["STL"] / career["GP"]).round(1)
        career["BPG"] = (career["BLK"] / career["GP"]).round(1)
        total_gp = career["GP"].sum()
        career_average = {}
        if total_gp > 0:
            career_average = {
                "PPG": (career["PTS"].sum() / career["GP"].sum()).round(1),
                "APG": (career["AST"].sum() / career["GP"].sum()).round(1),
                "RPG": (career["REB"].sum() / career["GP"].sum()).round(1),
                "SPG": (career["STL"].sum() / career["GP"].sum()).round(1),
                "BPG": (career["BLK"].sum() / career["GP"].sum()).round(1)
            }

        return {
            "player_name": player_name,
            "career_average": career_average,
            "stats": career.to_dict(orient="records"),
            "message": ""
        }
    except Exception as e:
        return {
            "player_name": player_name,
            "career_average": {},
            "stats": [],
            "message": f"No stats available for this player yet."
        }
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
        today = datetime.now().strftime("%m/%d/%Y")
        print(today)

        games = scoreboardv2.ScoreboardV2(game_date=today)
        df = games.game_header.get_data_frame()
        print(df.columns.tolist())   
        print(df.head())
        if df.empty:
            return {"message": "No games today."}
        matchups = []
        TEAM_ID_MAP = {t["id"]: t["abbreviation"] for t in teams.get_teams()}

        for _, row in df.iterrows():
            home_team = TEAM_ID_MAP.get(row["HOME_TEAM_ID"], "UNK")
            away_team = TEAM_ID_MAP.get(row["VISITOR_TEAM_ID"], "UNK")
            matchup = {
                "Game ID": row["GAME_ID"],
                "Home Team": home_team,
                "Away Team": away_team,
                "Home Team ID": row["HOME_TEAM_ID"], 
                "Away Team ID": row["VISITOR_TEAM_ID"],
                "Game Time": row["GAME_DATE_EST"],
                "Arena": row["ARENA_NAME"],
                "Status": row["GAME_STATUS_TEXT"],
            }
            matchups.append(matchup)
        return {"date": today, "games": matchups}
    except Exception as e:
        print(f"Error fetching today's games.")
        traceback.print_exc()
        return {"error": f"Couldn't fetch games today: {str(e)}"}
    
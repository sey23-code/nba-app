from fastapi import FastAPI
from nba_api.stats.static import teams
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonteamroster
from fastapi.middleware.cors import CORSMiddleware


#Creates a FastAPI object
app = FastAPI()
#To allow React to talk to Fast API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app origin
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
    nba_players = players.get_active_players()
    player_info = [
        {
        "Full Name": p["full_name"],
        "ID": p["id"],
        "Is Active": p["is_active"]
        }
        for p in nba_players
    ]
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
        player = players.find_player_by_id(player_id)

        if career.empty:
            return {
                "player_name": player["full_name"] if player else "Unknown Player",
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
            "player_name": player["full_name"] if player else "Unknown Player",
            "career_average": career_average,
            "stats": career.to_dict(orient="records"),
            "message": ""
    }
    except Exception as e:
        return {
            "player_name": "Unknown",
            "career_average": {},
            "stats": [],
            "message": f"No stats available for this player yet."
        }
    
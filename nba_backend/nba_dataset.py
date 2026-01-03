from nba_api.stats.endpoints import leaguegamefinder
from datetime import datetime
import pandas as pd

#Fetch games
games = leaguegamefinder.LeagueGameFinder(
    season_nullable="2025-26",
    season_type_nullable="Regular Season").get_data_frames()[0]
games = games.sort_values(["TEAM_ID", "GAME_DATE"]).reset_index(drop=True)
#Home variable
games["is_home"] = games["MATCHUP"].apply(lambda x: 1 if isinstance(x, str) and "vs." in x else 0)

#Back-to-back games feature
games["GAME_DATE"] = pd.to_datetime(games["GAME_DATE"])
delta = games["GAME_DATE"].diff().dt.days
games["back_to_back"] = delta.apply(lambda x: 1 if x == 1 else 0)
#Rest days feature
games["REST_DAYS"] = (delta - 1).apply(lambda x: x if x > 0 else 0)
games["REST_DAYS"] = pd.to_numeric(games["REST_DAYS"], downcast='integer')
#Winning streak feature
games["WL"] = games["WL"].apply(lambda x: 1 if x == "W" else 0) #Turns W -> 1 and L -> 0
group_games = games.groupby("TEAM_ID")
grouper = (group_games["WL"].transform(lambda x: x != x.shift())).cumsum()
games["WIN_STREAK"] = games.groupby(grouper)["WL"].cumsum()

#Calculate rolling stats of teams (15 games)
group_recent_games = games.groupby("TEAM_ID")
#Rolling Avg Pts
games["avg_pts_last_15"] = group_recent_games["PTS"].transform(lambda x: x.rolling(window=15).mean().shift(1)).round(1)
#Rolling Avg Reb
games["avg_reb_last_15"] = group_recent_games["REB"].transform(lambda x: x.rolling(window=15).mean().shift(1)).round(1)
#Rolling Avg Ast
games["avg_ast_last_15"] = group_recent_games["AST"].transform(lambda x: x.rolling(window=15).mean().shift(1)).round(1)
#Rolling Stl Ast
games["avg_stl_last_15"] = group_recent_games["STL"].transform(lambda x: x.rolling(window=15).mean().shift(1)).round(1)
#Rolling Blk Ast
games["avg_blk_last_15"] = group_recent_games["BLK"].transform(lambda x: x.rolling(window=15).mean().shift(1)).round(1)
#Rolling Avg Fg Pct
games["avg_fgpct_last_15"] = (group_recent_games["FG_PCT"].transform(lambda x: x.rolling(window=15).mean().shift(1)) * 100).round(1)
#Rolling Avg +/-
games["avg_pm_last_15"] = group_recent_games["PLUS_MINUS"].transform(lambda x: x.rolling(window=15).mean().shift(1)).round(1)
#Rolling 3pt Made
games["avg_3pm_last_15"] = group_recent_games["FG3M"].transform(lambda x: x.rolling(window=15).mean().shift(1)).round(1)
#Rolling Turnovers
games["avg_tov_last_15"] = group_recent_games["TOV"].transform(lambda x: x.rolling(window=15).mean().shift(1)).round(1)
#Rolling Fg Made
games["avg_fgm_last_15"] = group_recent_games["FGM"].transform(lambda x: x.rolling(window=15).mean().shift(1)).round(1)

#Calculate rolling stats of teams (5 games)
#Rolling Avg Pts
games["avg_pts_last_5"] = group_recent_games["PTS"].transform(lambda x: x.rolling(window=5).mean().shift(1)).round(1)
#Rolling Avg Reb
games["avg_reb_last_5"] = group_recent_games["REB"].transform(lambda x: x.rolling(window=5).mean().shift(1)).round(1)
#Rolling Avg Ast
games["avg_ast_last_5"] = group_recent_games["AST"].transform(lambda x: x.rolling(window=5).mean().shift(1)).round(1)
#Rolling Stl Ast
games["avg_stl_last_5"] = group_recent_games["STL"].transform(lambda x: x.rolling(window=5).mean().shift(1)).round(1)
#Rolling Blk Ast
games["avg_blk_last_5"] = group_recent_games["BLK"].transform(lambda x: x.rolling(window=5).mean().shift(1)).round(1)
#Rolling Avg Fg Pct
games["avg_fgpct_last_5"] = (group_recent_games["FG_PCT"].transform(lambda x: x.rolling(window=5).mean().shift(1)) * 100).round(1)
#Rolling Avg +/-
games["avg_pm_last_5"] = group_recent_games["PLUS_MINUS"].transform(lambda x: x.rolling(window=5).mean().shift(1)).round(1)
#Rolling 3pt Made
games["avg_3pm_last_5"] = group_recent_games["FG3M"].transform(lambda x: x.rolling(window=5).mean().shift(1)).round(1)
#Rolling Turnovers
games["avg_tov_last_5"] = group_recent_games["TOV"].transform(lambda x: x.rolling(window=5).mean().shift(1)).round(1)
#Rolling Fg Made
games["avg_fgm_last_5"] = group_recent_games["FGM"].transform(lambda x: x.rolling(window=5).mean().shift(1)).round(1)

#lakers = games[games["TEAM_ID"] == 1610612747]
#print(lakers[["GAME_DATE", "avg_pts_last_5", "avg_reb_last_5", "back_to_back", "REST_DAYS", "WIN_STREAK", "LOSE_STREAK"]])

predictive_columns = [
    "TEAM_ID",
    "GAME_ID",
    "GAME_DATE",
    "MATCHUP",
    "is_home",
    "back_to_back",
    "REST_DAYS",
    "WIN_STREAK",
    "WL",
    "avg_pts_last_15",
    "avg_pts_last_5",
    "avg_reb_last_15",
    "avg_reb_last_5",
    "avg_ast_last_15",
    "avg_ast_last_5",
    "avg_stl_last_15",
    "avg_stl_last_5",
    "avg_blk_last_15",
    "avg_blk_last_5",
    "avg_fgpct_last_15",
    "avg_fgpct_last_5",
    "avg_pm_last_15",
    "avg_pm_last_5",
    "avg_fgm_last_15",
    "avg_fgm_last_5",
    "avg_tov_last_15",
    "avg_tov_last_5",
    "avg_3pm_last_15",
    "avg_3pm_last_5"
    ]

games = games[predictive_columns]
home_games = games[games["is_home"] == 1]
away_games = games[games["is_home"] == 0]
merged_games = pd.merge(home_games, away_games, on="GAME_ID", suffixes=("_HOME", "_AWAY"))
merged_games["HOME_WIN"] = merged_games["WL_HOME"].apply(lambda x: 1 if x == "W" else 0)
merged_games = merged_games.drop(columns=["WL_HOME", "WL_AWAY", "GAME_DATE_AWAY"])
merged_games = merged_games.dropna()
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', 100)

merged_games.to_csv("nba_training_data.csv", index=False)


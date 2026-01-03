import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv('nba_training_data.csv')
#Sorting data by date
data["GAME_DATE_HOME"] = pd.to_datetime(data["GAME_DATE_HOME"])
data = data.sort_values('GAME_DATE_HOME')

X = data.drop(columns=["TEAM_ID_HOME", "GAME_ID", "GAME_DATE_HOME", "MATCHUP_HOME", "TEAM_ID_AWAY", 
                       "MATCHUP_AWAY", "is_home_HOME", "is_home_AWAY", "HOME_WIN"])
y = data["HOME_WIN"]

#Momentum variables
data["momentum_pts_HOME"] = data["avg_pts_last_5_HOME"] - data["avg_pts_last_15_HOME"]
data["momentum_pts_AWAY"] = data["avg_pts_last_5_AWAY"] - data["avg_pts_last_15_AWAY"]
data["momentum_reb_HOME"] = data["avg_reb_last_5_HOME"] - data["avg_reb_last_15_HOME"]
data["momentum_reb_AWAY"] = data["avg_reb_last_5_AWAY"] - data["avg_reb_last_15_AWAY"]
data["momentum_ast_HOME"] = data["avg_ast_last_5_HOME"] - data["avg_ast_last_15_HOME"]
data["momentum_ast_AWAY"] = data["avg_ast_last_5_AWAY"] - data["avg_ast_last_15_AWAY"]
data["momentum_stl_HOME"] = data["avg_stl_last_5_HOME"] - data["avg_stl_last_15_HOME"]
data["momentum_stl_AWAY"] = data["avg_stl_last_5_AWAY"] - data["avg_stl_last_15_AWAY"]
data["momentum_blk_HOME"] = data["avg_blk_last_5_HOME"] - data["avg_blk_last_15_HOME"]
data["momentum_blk_AWAY"] = data["avg_blk_last_5_AWAY"] - data["avg_blk_last_15_AWAY"]
data["momentum_fgpct_HOME"] = data["avg_fgpct_last_5_HOME"] - data["avg_fgpct_last_15_HOME"]
data["momentum_fgpct_AWAY"] = data["avg_fgpct_last_5_AWAY"] - data["avg_fgpct_last_15_AWAY"]
data["momentum_pm_HOME"] = data["avg_pm_last_5_HOME"] - data["avg_pm_last_15_HOME"]
data["momentum_pm_AWAY"] = data["avg_pm_last_5_AWAY"] - data["avg_pm_last_15_AWAY"]
data["momentum_fgm_HOME"] = data["avg_fgm_last_5_HOME"] - data["avg_fgm_last_15_HOME"]
data["momentum_fgm_AWAY"] = data["avg_fgm_last_5_AWAY"] - data["avg_fgm_last_15_AWAY"]
data["momentum_tov_HOME"] = data["avg_tov_last_5_HOME"] - data["avg_tov_last_15_HOME"]
data["momentum_tov_AWAY"] = data["avg_tov_last_5_AWAY"] - data["avg_tov_last_15_AWAY"]
data["momentum_3pm_HOME"] = data["avg_3pm_last_5_HOME"] - data["avg_3pm_last_15_HOME"]
data["momentum_3pm_AWAY"] = data["avg_3pm_last_5_AWAY"] - data["avg_3pm_last_15_AWAY"]

#Trend variables
data["trend_pts_HOME"] = data["avg_pts_last_5_HOME"] / data["avg_pts_last_15_HOME"]
data["trend_pts_AWAY"] = data["avg_pts_last_5_AWAY"] / data["avg_pts_last_15_AWAY"]
data["trend_reb_HOME"] = data["avg_reb_last_5_HOME"] / data["avg_reb_last_15_HOME"]
data["trend_reb_AWAY"] = data["avg_reb_last_5_AWAY"] / data["avg_reb_last_15_AWAY"]
data["trend_ast_HOME"] = data["avg_ast_last_5_HOME"] / data["avg_ast_last_15_HOME"]
data["trend_ast_AWAY"] = data["avg_ast_last_5_AWAY"] / data["avg_ast_last_15_AWAY"]
data["trend_stl_HOME"] = data["avg_stl_last_5_HOME"] / data["avg_stl_last_15_HOME"]
data["trend_stl_AWAY"] = data["avg_stl_last_5_AWAY"] / data["avg_stl_last_15_AWAY"]
data["trend_blk_HOME"] = data["avg_blk_last_5_HOME"] / data["avg_blk_last_15_HOME"]
data["trend_blk_AWAY"] = data["avg_blk_last_5_AWAY"] / data["avg_blk_last_15_AWAY"]
data["trend_fgpct_HOME"] = data["avg_fgpct_last_5_HOME"] / data["avg_fgpct_last_15_HOME"]
data["trend_fgpct_AWAY"] = data["avg_fgpct_last_5_AWAY"] / data["avg_fgpct_last_15_AWAY"]
data["trend_pm_HOME"] = data["avg_pm_last_5_HOME"] / data["avg_pm_last_15_HOME"]
data["trend_pm_AWAY"] = data["avg_pm_last_5_AWAY"] / data["avg_pm_last_15_AWAY"]
data["trend_fgm_HOME"] = data["avg_fgm_last_5_HOME"] / data["avg_fgm_last_15_HOME"]
data["trend_fgm_AWAY"] = data["avg_fgm_last_5_AWAY"] / data["avg_fgm_last_15_AWAY"]
data["trend_tov_HOME"] = data["avg_tov_last_5_HOME"] / data["avg_tov_last_15_HOME"]
data["trend_tov_AWAY"] = data["avg_tov_last_5_AWAY"] / data["avg_tov_last_15_AWAY"]
data["trend_3pm_HOME"] = data["avg_3pm_last_5_HOME"] / data["avg_3pm_last_15_HOME"]
data["trend_3pm_AWAY"] = data["avg_3pm_last_5_AWAY"] / data["avg_3pm_last_15_AWAY"]


data = data.replace([np.inf, -np.inf], np.nan)

#Spliting games -> 80% train / 20% test
split_index = int(len(data) * 0.8)
#Using 199 games to train
X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:] #Rest is testing games
y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

#Logistic Regression algorithm
model = LogisticRegression(max_iter=5000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
#48 -> 60% Accuracy score
print(f"Accuracy score: {accuracy * 100}%")
#print(report)

print(f"y_pred distribution:\n{pd.Series(y_pred).value_counts()}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

#Random Forest algorithm
#model2 = RandomForestClassifier(n_estimators=500, random_state=42)
#model2.fit(X_train, y_train)
#y_pred = model2.predict(X_test)
#accuracy = accuracy_score(y_pred, y_test)
#48% -> 50% Accuracy score
#print(f"Accuracy score: {accuracy * 100}%")

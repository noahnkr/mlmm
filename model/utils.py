import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

MATCHUPS_PATH = "./data/matchups.csv"

STATS_PATH = "./data/stats.csv"

MODELS = {
	"Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
	"SVM": SVC(kernel="linear", class_weight="balanced"),
	"Random Forest": RandomForestClassifier(n_estimators=100),
	"KNN": KNeighborsClassifier(),
	"Naive Bayes": GaussianNB()
}

SEED_ORDER = [
	(1, 16),
	(8, 9),
	(5, 12),
	(4, 13),
	(6, 11),
	(3, 14),
	(7, 10),
	(2, 15)
]

def get_team_vector(year, team, seed, team_stats):
	row = team_stats[(team_stats["year"] == year) & (team_stats["team"] == team)].copy()
	if row.empty:
		return None
	row["seed"] = seed
	return row.drop(columns=["year", "team"]).values.flatten() # Remove redundant features, convert to np array

def load_tournament_data():
	matchups = pd.read_csv(MATCHUPS_PATH)
	team_stats = pd.read_csv(STATS_PATH)
	return matchups, team_stats

def load_dataset(train_years=[], test_year=None):
	X_train, y_train = [], []
	X_test, y_test, info_test = [], [], []

	matchups, stats = load_tournament_data()

	for _, row in matchups.iterrows():
		v_a = get_team_vector(row["year"], row["team_a"], row["team_a_seed"], stats)
		v_b = get_team_vector(row["year"], row["team_b"], row["team_b_seed"], stats)

		if v_a is None or v_b is None:
			continue
		
		dv = v_a - v_b  # Feature = stat diff vector
		label = 1 if row["winner"] == row["team_a"] else 0

		if row["year"] in train_years:
			X_train.append(dv)
			y_train.append(label)
		elif row["year"] == test_year:
			X_test.append(dv)
			y_test.append(label)
			info_test.append({
				"year": row["year"],
				"round": row["round"],
				"region": row["region"],
				"team_a": row["team_a"],
				"team_a_seed": row["team_a_seed"],
				"team_b": row["team_b"],
				"team_b_seed": row["team_b_seed"],
				"winner": row["winner"]
			})

	return X_train, y_train, X_test, y_test, info_test

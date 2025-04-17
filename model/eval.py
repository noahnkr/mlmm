import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from model.utils import MODELS,SEED_ORDER, load_tournament_data, get_team_vector
from scraper.utils import REGIONS, ROUNDS, print_matchup

def print_classification_report(X_train, X_test, y_train, y_test):
	scaler = StandardScaler()
	X_train_scl = scaler.fit_transform(X_train)
	X_test_scl = scaler.transform(X_test)

	for name, model in MODELS.items():
		print(f"\nTraining model: {name}")
		
		if name in ["Logistic Regression", "SVM", "KNN"]:
			model.fit(X_train_scl, y_train)
			preds = model.predict(X_test_scl)
		else:
			model.fit(X_train, y_train)
			preds = model.predict(X_test)
		
		print(classification_report(y_test, preds))

def print_correct_upsets(preds, y_test, info_test):
	for pred, true, info in zip(preds, y_test, info_test):
		if pred != true:
			continue

		# Determine predicted winner and their seed
		predicted_winner = info["team_a"] if pred == 1 else info["team_b"]
		predicted_seed = info["team_a_seed"] if pred == 1 else info["team_b_seed"]
		opponent_seed = info["team_b_seed"] if pred == 1 else info["team_a_seed"]

		# If predicted winner is a higher seed (lower ranked team wins)
		if predicted_seed > opponent_seed:
			print(f"{info["year"]} {info["round"]} {info["region"]}")
			print(f"{info["team_a"]} ({info["team_a_seed"]}) vs {info["team_b"]} ({info["team_b_seed"]})")
			print(f"Predicted: {predicted_winner} | Correct: {info["winner"]}")
			print("---")
		
def evaluate_models(X_train, X_test, y_train, y_test):
	scaler = StandardScaler()
	X_train_scl = scaler.fit_transform(X_train)
	X_test_scl = scaler.transform(X_test)

	model_acc = {}
	for name, model in MODELS.items():
		if name in ["Logistic Regression", "SVM", "KNN"]:
			model.fit(X_train_scl, y_train)
			preds = model.predict(X_test_scl)
		else:
			model.fit(X_train, y_train)
			preds = model.predict(X_test)

		acc = round(accuracy_score(y_test, preds), 3)
		model_acc[name] = acc
	
	return model_acc

def simulate_tournament(year, model):
	matchups, stats = load_tournament_data()

	# Collect and sort all first round games by year
	matchups = matchups[(matchups["year"] == year) & (matchups["round"] == "First")].drop("winner", axis=1) 
	matchups = pd.DataFrame(_order_matchups(matchups))

	advancing_teams = []
	print(f"--- Simulating {year} NCAA March Madness Tournament ---")
	for i, round_name in enumerate(ROUNDS):
		print(f"--- Simulating {round_name} Round ---")
		advancing_teams = _simulate_tournament_round(round_name, matchups, stats, model)

		if len(advancing_teams) == 1:
			region, team, seed = advancing_teams[0]
			print(f"--- {year} National Champions: ({seed}) {team} ---")
			return 

		winner_matchups = list(zip(advancing_teams[::2], advancing_teams[1::2]))
		new_matchups = []
		for winner_a, winner_b in winner_matchups:
			region_a, team_a, team_a_seed = winner_a
			region_b, team_b, team_b_seed = winner_b

			region = "National" if region_a != region_b else region_a
			next_round = ROUNDS[i + 1] if i < len(ROUNDS) else "National Championship"
			new_matchups.append({
				"year": year,
				"region": region,
				"round": next_round,
				"team_a": team_a,
				"team_b": team_b,
				"team_a_seed": team_a_seed,
				"team_b_seed": team_b_seed,
			})
		
		matchups = pd.DataFrame(new_matchups)

def _simulate_tournament_round(round, matchups, stats, model):
	advancing_teams = []

	regions = ["National"] if round in ROUNDS[-2:] else REGIONS[:-1]
	for region in regions:
		print(f"--- Simulating {region} Region ---")
		region_matchups = matchups[(matchups["region"] == region)]

		for _, matchup in region_matchups.iterrows():
			winner = _simulate_tournament_matchup(matchup, stats, model)
			seed = matchup["team_a_seed"] if winner == matchup["team_a"] else matchup["team_b_seed"]
			advancing_teams.append((region, winner, seed))
	
	return advancing_teams

def _simulate_tournament_matchup(matchup, stats, model):
	v_a = get_team_vector(matchup["year"], matchup["team_a"], matchup["team_a_seed"], stats)
	v_b = get_team_vector(matchup["year"], matchup["team_b"], matchup["team_b_seed"], stats)

	if v_a is None or v_b is None:
		print(f"Unable to find team vector for {matchup["year"]} {matchup["team_a"]} vs. {matchup["team_b"]}")
		return None
	
	dv = v_a - v_b
	pred = model.predict([dv])[0]
	winner = matchup["team_a"] if pred == 1 else matchup["team_b"]
	print_matchup(matchup["team_a"], matchup["team_b"], matchup["team_a_seed"], matchup["team_b_seed"], winner)

	return winner

def _order_matchups(matchups):
	ordered_matchups = []
	for region in REGIONS:
		region_matchups = matchups[matchups["region"] == region]

		# For each seed pair in the correct bracket order
		for team_a_seed, team_b_seed in SEED_ORDER:
			game = region_matchups[
				((region_matchups["team_a_seed"] == team_a_seed) & (region_matchups["team_b_seed"] == team_b_seed)) |
				((region_matchups["team_a_seed"] == team_b_seed) & (region_matchups["team_b_seed"] == team_a_seed))
			]

			if not game.empty:
				ordered_matchups.append(game.iloc[0])

	return ordered_matchups



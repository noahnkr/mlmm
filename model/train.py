import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from model.utils import load_dataset
from model.eval import print_correct_upsets, simulate_tournament

X, y, info = load_dataset()
print(f"Loaded dataset with {len(X)} examples.")

X_train, X_test, y_train, y_test, info_train, info_test = train_test_split(
    X, y, info, test_size=0.2, random_state=42
)
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

scaler = StandardScaler()
X_train_scl = scaler.fit_transform(X_train)
X_test_scl = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_scl, y_train)

preds = model.predict(X_test_scl)
#print_correct_upsets(preds, y_test, info_test)

simulate_tournament(2025, model)

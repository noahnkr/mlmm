from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from utils import MODELS, load_dataset

X, y = load_dataset()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scl = scaler.fit_transform(X_train)
X_test_scl = scaler.fit_transform(X_test)

for name, model in MODELS.items():
    if name in ["Logistic Regerssion", "SVM", "KNN"]:
        model.fit(X_train_scl, y_train)
        acc = accuracy_score(y_test, model.predict(X_test_scl))
    else:
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test))
    print(f"{name} Accuracy: {acc:.3f}")
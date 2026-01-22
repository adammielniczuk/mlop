import joblib
from sklearn.datasets import fetch_openml
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import numpy as np

def train():
    X, y = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False)
    X = X / 255.0
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)

    clf = MLPClassifier(hidden_layer_sizes=(50,), max_iter=20, alpha=1e-4,
                        solver='sgd', verbose=10, random_state=1,
                        learning_rate_init=.1)

    clf.fit(X_train, y_train)

    print(f"Test score: {clf.score(X_test, y_test)}")

    model_path = "model.joblib"
    joblib.dump(clf, model_path)

if __name__ == "__main__":
    train()

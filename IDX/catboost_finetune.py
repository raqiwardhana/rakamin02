import os
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import roc_auc_score
import joblib

def main():
    # 1. Load Preprocessed Data
    # Replace these paths with your actual processed data files
    print("Loading data...")
    X_train = pd.read_csv("X_train.csv")
    y_train = pd.read_csv("y_train.csv").squeeze()
    X_test = pd.read_csv("X_test.csv")
    y_test = pd.read_csv("y_test.csv").squeeze()

    # Define categorical features if applicable
    cat_features = X_train.select_dtypes(include=['object', 'category']).columns.tolist()

    # 2. Hyperparameters
    best_params = {
        "iterations": 1000,
        "learning_rate": 0.04833296533797083,
        "depth": 5,
        "l2_leaf_reg": 9.752111570982535,
        "random_strength": 0.00220093652826492,
        "bagging_temperature": 0.23462812268863875,
        "border_count": 210,
        "eval_metric": "AUC",
        "auto_class_weights": "Balanced",
        "random_seed": 42,
        "verbose": 100,
    }

    # 3. Model Training
    print("Training final CatBoost model...")
    final_cb_model = CatBoostClassifier(**best_params)
    final_cb_model.fit(
        X_train,
        y_train,
        cat_features=cat_features if cat_features else None,
        eval_set=(X_test, y_test),
        early_stopping_rounds=50,
    )

    # 4. Evaluation
    y_pred_proba_final = final_cb_model.predict_proba(X_test)[:, 1]
    roc_auc = roc_auc_score(y_test, y_pred_proba_final)
    gini = 2 * roc_auc - 1

    print("\n--- Final Model Evaluation ---")
    print(f"ROC-AUC: {roc_auc:.4f} | Gini: {gini:.4f}")

    # 5. Save the Trained Model
    model_filename = "catboost_model.cbm"
    final_cb_model.save_model(model_filename)
    print(f"Model successfully saved to {model_filename}")

if __name__ == "__main__":
    main()
import os
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import average_precision_score, roc_auc_score, precision_recall_curve
from xgboost import XGBClassifier

from features import load_feature_matrix, time_split, FEATURES

RULE_RECALL = 0.439   # Phase 3 baseline, for a like-for-like comparison

def evaluate(name, y_true, scores):
    pr_auc  = average_precision_score(y_true, scores)
    roc_auc = roc_auc_score(y_true, scores)
    prec, rec, _ = precision_recall_curve(y_true, scores)
    idx = np.argmin(np.abs(rec - RULE_RECALL))     # precision at the rules' recall
    print(f"{name:20s} PR-AUC={pr_auc:.3f}  ROC-AUC={roc_auc:.3f}  "
          f"precision@{rec[idx]*100:.0f}%recall={prec[idx]*100:.1f}%")
    return pr_auc

def main():
    df = load_feature_matrix()
    train, test = time_split(df)
    X_train, y_train = train[FEATURES], train["is_fraud"]
    X_test,  y_test  = test[FEATURES],  test["is_fraud"]

    # Logistic Regression – scaled + class-balanced
    logreg = make_pipeline(
        StandardScaler(),
        LogisticRegression(class_weight="balanced", max_iter=1000),
    )
    logreg.fit(X_train, y_train)
    evaluate("LogisticRegression", y_test, logreg.predict_proba(X_test)[:, 1])

    # XGBoost – imbalance via scale_pos_weight
    spw = (y_train == 0).sum() / (y_train == 1).sum()
    xgb = XGBClassifier(
        n_estimators=300, max_depth=6, learning_rate=0.1,
        scale_pos_weight=spw, eval_metric="aucpr",
        tree_method="hist", n_jobs=-1,
    )
    xgb.fit(X_train, y_train)
    evaluate("XGBoost", y_test, xgb.predict_proba(X_test)[:, 1])

    print("\nRule baseline (Phase 3):       precision=17.0%  recall=43.9%")

    # Feature importance
    print("\nTop features (XGBoost):")
    for i in np.argsort(xgb.feature_importances_)[::-1][:6]:
        print(f"  {FEATURES[i]:18s} {xgb.feature_importances_[i]:.3f}")

    # Save for the dashboard – store feature order alongside the model
    os.makedirs("models", exist_ok=True)
    joblib.dump({"model": xgb, "features": FEATURES}, "models/xgb_fraud.pkl")
    print("\nSaved models/xgb_fraud.pkl")

if __name__ == "__main__":
    main()
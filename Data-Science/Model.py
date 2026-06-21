from pathlib import Path
import pickle

import pandas as pd
from xgboost import XGBRegressor

data_path = Path(r"C:\Users\HP\Downloads\Data-Science\Data-Science\car_prediction_data.csv")
model_path = Path(__file__).resolve().parent / "models" / "xgb_car_price_model.pkl"

print("Starting model training...")
cars_df = pd.read_csv(data_path)

X = pd.get_dummies(
    cars_df[["Year", "Present_Price", "Kms_Driven", "Fuel_Type", "Seller_Type", "Transmission", "Owner"]],
    drop_first=True,
)
y = cars_df["Selling_Price"]

xgb_model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.2,
    max_depth=6,
)

xgb_model.fit(X, y)

model_path.parent.mkdir(parents=True, exist_ok=True)
with open(model_path, "wb") as f:
    pickle.dump(xgb_model, f)
print(f"Model saved to {model_path}")



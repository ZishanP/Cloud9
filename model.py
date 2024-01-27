import requests
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta
import time

def fetch_data_for_date(date):
    """Fetch flight data for a specific date from the Heroku app."""
    url = f'https://cloud9-data-8c815c4bd89c.herokuapp.com/flights?date={date}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {date}, Status code: {response.status_code}")
        return []

def flatten_data(df):
    """Flatten nested JSON data in the DataFrame."""
    if not df.empty and 'aircraft' in df.columns:
        # Extract nested 'passengerCapacity.total' into a new column
        df['aircraft.passengerCapacity.total'] = df['aircraft'].apply(lambda x: x.get('passengerCapacity', {}).get('total', None))
    return df

def enrich_date_features(df):
    """Add date-related features to the DataFrame."""
    df['departureTime'] = pd.to_datetime(df['departureTime'], utc=True, errors='coerce')
    df.dropna(subset=['departureTime'], inplace=True)
    df['month'] = df['departureTime'].dt.month
    df['day_of_week'] = df['departureTime'].dt.dayofweek
    df['hour_of_day'] = df['departureTime'].dt.hour
    df['season'] = df['month'] % 12 // 3 + 1
    return df

def create_synthetic_target(df):
    """Generate a synthetic target variable for the model."""
    df['points_price'] = df['distance'] / df['aircraft.passengerCapacity.total'] + df['season'] * 10
    return df

def main():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 31)
    delta = timedelta(days=1)

    all_data = []
    start_time = time.time()

    while start_date <= end_date:
        date_str = start_date.strftime('%Y-%m-%d')
        daily_data = fetch_data_for_date(date_str)
        all_data.extend(daily_data)
        start_date += delta

    elapsed_time = time.time() - start_time
    print(f"Data loading completed in {elapsed_time:.2f} seconds")

    df = pd.DataFrame(all_data)
    df = flatten_data(df)  # Flatten nested JSON data
    df = enrich_date_features(df)
    df = create_synthetic_target(df)

    features = ['distance', 'aircraft.passengerCapacity.total', 'month', 'day_of_week', 'hour_of_day', 'season']
    X = df[features]
    y = df['points_price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    params = {
        'max_depth': 5,
        'eta': 0.1,
        'objective': 'reg:squarederror',
        'eval_metric': 'rmse'
    }

    train_start_time = time.time()
    num_rounds = 150
    bst = xgb.train(params, dtrain, num_rounds)
    train_elapsed_time = time.time() - train_start_time
    print(f"Model training completed in {train_elapsed_time:.2f} seconds")

    y_pred = bst.predict(dtest)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    print(f"RMSE: {rmse}")

if __name__ == "__main__":
    main()

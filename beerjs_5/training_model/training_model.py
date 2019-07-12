import pandas as pd
import xgboost as xgb
import dill
import argparse
import dill as pickle
import numpy as np

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def main(args):
    train_path = args.train_path
    test_path = args.test_path
    
    print("Loading data...")
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    
    print(train.head(5))
    
    train = pd.get_dummies(train)
    test = pd.get_dummies(test)
    
    training_cols = [x for x in train.columns if x != "charges"]
    target = "charges"

    model = xgb.XGBRegressor(max_depth=10,
                              n_estimators=300,
                              subsample=0.8,
                              colsample_bytree=0.8,
                              colsample_bylevel=0.8,
                              learning_rate=0.01,
                              silent=True)
    
    print("Training model")
    model.fit(train[training_cols],
              train[target],
              verbose=False,
              eval_metric="rmse")
    
    test_predictions = model.predict(test[training_cols])
    error = mean_absolute_percentage_error(test[target], test_predictions)
    
    print("Model MAPE {0} % ".format(error))
    
    print("Model stored as model.pkl")
    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BeerJS training example')
    parser.add_argument('--train_path', type=str)
    parser.add_argument('--test_path', type=str)
    args = parser.parse_args()
    main(args)
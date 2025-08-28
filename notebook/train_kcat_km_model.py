import numpy as np
import pandas as pd
import pickle
from scipy.stats import pearsonr
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

def Kcat_predict(features, labels, params):
    kf = KFold(n_splits=5, shuffle=True)
    all_predicted_labels = [None] * len(features)  # Initialize predicted labels list
    all_actual_labels = [None] * len(features)  # Initialize actual labels list

    train_rmse_list = []
    test_rmse_list = []

    for train_index, test_index in kf.split(features, labels):
        train_data, train_labels = features[train_index], labels[train_index]
        test_data, test_labels = features[test_index], labels[test_index]
        
        model = ExtraTreesRegressor(**params)
        model.fit(train_data, train_labels)
        
        train_predicted_labels = model.predict(train_data)
        test_predicted_labels = model.predict(test_data)
        
        train_rmse = mean_squared_error(train_labels, train_predicted_labels, squared=False)
        test_rmse = mean_squared_error(test_labels, test_predicted_labels, squared=False)
        
        train_rmse_list.append(train_rmse)
        test_rmse_list.append(test_rmse)
        
        for i, idx in enumerate(test_index):
            all_predicted_labels[idx] = test_predicted_labels[i]
            all_actual_labels[idx] = test_labels[i]

    # Remove None values from the lists
    all_predicted_labels = [x for x in all_predicted_labels if x is not None]
    all_actual_labels = [x for x in all_actual_labels if x is not None]

    avg_train_rmse = np.mean(train_rmse_list)
    avg_test_rmse = np.mean(test_rmse_list)

    return all_predicted_labels, all_actual_labels, avg_train_rmse, avg_test_rmse

with open("data/Kcat_Km/feature_esm1b.pkl", "rb") as f:  # Use 'rb' mode (read binary)
    features = pickle.load(f)

with open("data/Kcat_Km/label.pkl", "rb") as f:  # Use 'rb' mode (read binary)
    labels = pickle.load(f)

print('(1) Using the dataset with esm1b predicted features')
params = {
    "n_jobs": 12,
}

predicted_values, actual_values, avg_train_rmse, avg_test_rmse = Kcat_predict(features, labels, params)

# Calculate the Pearson correlation coefficient
pcc, _ = pearsonr(actual_values, predicted_values)
print(f"Pearson correlation coefficient (pcc): {pcc}")

print(f"Average Train RMSE: {avg_train_rmse}")
print(f"Average Test RMSE: {avg_test_rmse}")

"""Compute MAE, RMSE, and R-squared on a printed forecast example."""

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

actual = np.array([10, 12, 8, 11, 9, 13, 10, 12, 9, 11], dtype=float)
forecast = np.array([9, 11, 10, 12, 8, 14, 9, 11, 10, 10], dtype=float)

mae = mean_absolute_error(actual, forecast)
rmse = float(np.sqrt(mean_squared_error(actual, forecast)))
r2 = r2_score(actual, forecast)

print("Mean Absolute Error (MAE): {:.2f}".format(mae))
print("Root Mean Squared Error (RMSE): {:.2f}".format(rmse))
print("R-squared: {:.3f}".format(r2))
print("R-squared has a best value of 1.0 and can be negative.")

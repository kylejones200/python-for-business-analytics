"""Compute MAPE and sMAPE on the printed forecast example.

MAPE = (100 / n) * sum(|y - yhat| / |y|) and is undefined at y = 0.
This sMAPE uses the 0-to-200 percent convention:
sMAPE = (100 / n) * sum(2 * |y - yhat| / (|y| + |yhat|)).
A 0/0 pair contributes 0 rather than NaN.
"""

import numpy as np

actual = np.array([10, 12, 8, 11, 9, 13, 10, 12, 9, 11], dtype=float)
forecast = np.array([9, 11, 10, 12, 8, 14, 9, 11, 10, 10], dtype=float)

def mean_absolute_percentage_error(y, yhat):
    y = np.asarray(y, dtype=float)
    yhat = np.asarray(yhat, dtype=float)
    if np.any(np.isclose(y, 0.0)):
        raise ValueError("MAPE is undefined when an actual value is zero.")
    return float(np.mean(np.abs((y - yhat) / y)) * 100.0)

def symmetric_mean_absolute_percentage_error(y, yhat):
    y = np.asarray(y, dtype=float)
    yhat = np.asarray(yhat, dtype=float)
    denom = np.abs(y) + np.abs(yhat)
    term = np.zeros_like(y)
    nonzero = ~np.isclose(denom, 0.0)
    term[nonzero] = 2.0 * np.abs(y[nonzero] - yhat[nonzero]) / denom[nonzero]
    return float(np.mean(term) * 100.0)

mape = mean_absolute_percentage_error(actual, forecast)
smape = symmetric_mean_absolute_percentage_error(actual, forecast)
print("Mean Absolute Percentage Error (MAPE): {:.2f}%".format(mape))
print("Symmetric MAPE (0-200% convention): {:.2f}%".format(smape))
print("Zero/zero sMAPE pairs are treated as 0.")

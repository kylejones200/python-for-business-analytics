"""Compute non-seasonal MASE (m=1) on the printed forecast example.

The denominator is the MAE of a one-step naive forecast. That is the
non-seasonal case. A seasonal series would use |y_i - y_{i-m}|.
"""

import numpy as np

actual = np.array([10, 12, 8, 11, 9, 13, 10, 12, 9, 11], dtype=float)
forecast = np.array([9, 11, 10, 12, 8, 14, 9, 11, 10, 10], dtype=float)

def mean_absolute_scaled_error(y, yhat, m=1):
    y = np.asarray(y, dtype=float)
    yhat = np.asarray(yhat, dtype=float)
    mae_forecast = float(np.mean(np.abs(y - yhat)))
    naive = float(np.mean(np.abs(y[m:] - y[:-m])))
    return mae_forecast / naive

mase = mean_absolute_scaled_error(actual, forecast, m=1)
print("Mean Absolute Scaled Error (MASE, m=1): {:.3f}".format(mase))
if mase < 1:
    print("The example forecast beats a one-step naive baseline.")
else:
    print("The example forecast does not beat a one-step naive baseline.")

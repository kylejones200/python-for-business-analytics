"""Import the Python libraries used for time series analysis in this chapter."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error, mean_squared_error

print("Loaded pandas, numpy, matplotlib, seaborn, statsmodels, and scikit-learn")
print("pandas", pd.__version__, "numpy", np.__version__, "statsmodels", sm.__version__)
_ = (plt, sns, mean_absolute_error, mean_squared_error)

# increasing user acquisition costs will lead to a higher user retention rate which will
# in turn lead to a increased profit

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

class UserRetentionAnalysis:
    def __init__(self, acquisition_costs, retention_rates, profits):
        self.acquisition_costs = acquisition_costs
        self.retention_rates = retention_rates
        self.profits = profits
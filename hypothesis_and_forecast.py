import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

class ForeCast:
    def __init__(self, df):
        self.df = df

    def test_hypothesis(self):
        # calculate correlation between acquisition costs and retention rates
        correlation = np.corrcoef(self.df['user_acquisition_cost_usd'], self.df['retension_rate'])[0, 1]
        print(f"Correlation between acquisition costs and retention rates: {correlation}")

        # perform linear regression between acquisition costs and retention rates
        X = sm.add_constant(self.df['user_acquisition_cost_usd'])
        model = sm.OLS(self.df['retension_rate'], X).fit()
        # print(model.summary())

        # calculate predicted retention rates based on the regression model
        predicted_retention_rates = model.predict(X)
        plt.scatter(self.df['user_acquisition_cost_usd'],self.df['retension_rate'])
        plt.plot(self.df['user_acquisition_cost_usd'], predicted_retention_rates, color='red')
        plt.xlabel("Acquisition Costs")
        plt.ylabel("Retention Rates")
        plt.title("Acquisition Costs vs. Retention Rates")
        plt.show()

        # calculate correlation between retention rates and profits
        correlation = np.corrcoef(self.df['retension_rate'], self.df['profit_usd'])[0, 1]
        print(f"Correlation between retention rates and profits: {correlation}")

        # perform linear regression between retention rates and profits
        X = sm.add_constant(self.df['retension_rate'])
        model = sm.OLS(self.df['profit_usd'], X).fit()
        # print(model.summary())

        # calculate predicted profits based on the regression model
        predicted_profits = model.predict(X)
        plt.scatter(self.df['retension_rate'], self.df['profit_usd'])
        plt.plot(self.df['retension_rate'], predicted_profits, color='red')
        plt.xlabel("Retention Rates")
        plt.ylabel("Profits")
        plt.title("Retention Rates vs. Profits")
        plt.show()


    def check_hypothesis(self):
        print('Perform hypothesis testing between acquisition costs and retention rates')
        print('')
        alpha = 0.05
        print('Null hypothesis: increasing user acquisition costs do not lead to a higher user retention rate')
        print('Alternative hypothesis: increasing user acquisition costs lead to a higher user retention rate')
        print('')
        X = self.df['user_acquisition_cost_usd']
        y = self.df['retension_rate']
        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()
        p_value = model.pvalues[1]
        if p_value < alpha:
            print(
                "Reject the null hypothesis. There is evidence that increasing user acquisition costs lead to a higher user retention rate.")
        else:
            print(
                "Fail to reject the null hypothesis. There is no evidence that increasing user acquisition costs lead to a higher user retention rate.")

        print('')
        print('Perform hypothesis testing between profit and retention rates')
        print('')
        alpha = 0.05
        print('Null hypothesis: increasing user retention does not lead to a higher profits')
        print('Alternative hypothesis: increasing user retension lead to a higher profits')
        print('')
        X = self.df['retension_rate']
        y = self.df['profit_usd']
        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()
        p_value = model.pvalues[1]
        if p_value < alpha:
            print(
                "Reject the null hypothesis. There is evidence that increasing user retension leads to a higher profits.")
        else:
            print(
                "Fail to reject the null hypothesis. There is no evidence that increasing retension leads to a higher profits.")

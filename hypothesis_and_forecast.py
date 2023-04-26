import numpy as np
import statsmodels.api as sm
from data_analytics import regressions_charts


class ForeCast:
    def __init__(self, df):
        self.df = df

    def test_hypothesis(self):
        """
        Tests the hypothesis that user acquisition costs and retention rates are correlated with profits.

        Calculates the correlation between acquisition costs and retention rates, and between retention rates and
        profits. Performs linear regression for each correlation and calculates the predicted values. Generates
        regression charts for each regression.

        :return: None
        :rtype: None
        """
        # calculate correlation between acquisition costs and retention rates
        correlation = np.corrcoef(self.df['user_acquisition_cost_usd'], self.df['retension_rate'])[0, 1]
        print(f"Correlation between acquisition costs and retention rates: {correlation}")

        # perform linear regression between acquisition costs and retention rates
        x = sm.add_constant(self.df['user_acquisition_cost_usd'])
        model = sm.OLS(self.df['retension_rate'], x).fit()
        # print(model.summary())

        # calculate predicted retention rates based on the regression model
        predicted_retention_rates = model.predict(x)
        regressions_charts(x=self.df['user_acquisition_cost_usd'], y=self.df['retension_rate'],
                           prediction=predicted_retention_rates,
                           xlabel="Acquisition Costs", ylabel="Retention Rates",
                           title="Acquisition Costs vs. Retention Rates")

        # calculate correlation between retention rates and profits
        correlation = np.corrcoef(self.df['retension_rate'], self.df['profit_usd'])[0, 1]
        print(f"Correlation between retention rates and profits: {correlation}")

        # perform linear regression between retention rates and profits
        x = sm.add_constant(self.df['retension_rate'])
        model = sm.OLS(self.df['profit_usd'], x).fit()
        # print(model.summary())

        # calculate predicted profits based on the regression model
        predicted_profits = model.predict(x)
        regressions_charts(x=self.df['retension_rate'], y=self.df['profit_usd'],
                           prediction=predicted_profits,
                           xlabel="Rates", ylabel="Profits",
                           title="Retention Rates vs. Profits")

    def check_hypothesis(self):
        """
        Perform hypothesis testing between acquisition costs and retention rates, and between profit and retention
        rates.

           :return: None
           :rtype: None
           """
        print('Perform hypothesis testing between acquisition costs and retention rates')
        print('')
        alpha = 0.05
        print('Null hypothesis: increasing user acquisition costs do not lead to a higher user retention rate')
        print('Alternative hypothesis: increasing user acquisition costs lead to a higher user retention rate')
        print('')
        x = self.df['user_acquisition_cost_usd']
        y = self.df['retension_rate']
        x = sm.add_constant(x)
        model = sm.OLS(y, x).fit()
        p_value = model.pvalues[1]
        if p_value < alpha:
            print(
                "Reject the null hypothesis. There is evidence that increasing user acquisition costs lead to a "
                "higher user retention rate.")
        else:
            print(
                "Fail to reject the null hypothesis. There is no evidence that increasing user acquisition costs lead "
                "to a higher user retention rate.")

        print('')
        print('Perform hypothesis testing between profit and retention rates')
        print('')
        alpha = 0.05
        print('Null hypothesis: increasing user retention does not lead to a higher profits')
        print('Alternative hypothesis: increasing user retension lead to a higher profits')
        print('')
        x = self.df['retension_rate']
        y = self.df['profit_usd']
        x = sm.add_constant(x)
        model = sm.OLS(y, x).fit()
        p_value = model.pvalues[1]
        if p_value < alpha:
            print(
                "Reject the null hypothesis. There is evidence that increasing user retension leads to a higher "
                "profits.")
        else:
            print(
                "Fail to reject the null hypothesis. There is no evidence that increasing retension leads to a higher "
                "profits.")

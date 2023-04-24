import pandas as pd
import matplotlib.pyplot as plt


class DataCleaning:

    def __init__(self, data, columns):
        self.data = data
        self.columns = columns

    def check_duplicates(self):
        # Check for duplicates
        num_duplicates = self.data.duplicated().sum()
        if num_duplicates > 0:
            print(f"Found {num_duplicates} duplicate records.")
            # Drop duplicates and reset index
            self.data.drop_duplicates(inplace=True)
            self.data.reset_index(drop=True, inplace=True)
        else:
            print("No duplicate records found.")

    def fill_missing_values(self):
        # Loop through columns in DataFrame
        for col in self.columns:
            # Check if column is numeric
            if pd.api.types.is_numeric_dtype(self.data[col]):
                # Fill in missing values with column mean
                self.data[col].fillna(self.data[col].mean(), inplace=True)
            else:
                # Fill in missing values with empty string
                self.data[col].dropna(inplace=True)

        # Check for any remaining missing values and print row index and column name
        missing_values = self.data.isnull().any(axis=1)
        if missing_values.any():
            print("Rows with missing values:")
            print(self.data[missing_values])

    def check_for_outliers(self,remove_outliers=False):
        outliers = {}

        for col in self.columns:
            if self.data[col].dtype in ['int64', 'float64'] and 'id' not in col.lower():
                # Calculate the interquartile range (IQR)
                q1 = self.data[col].quantile(0.25)
                q3 = self.data[col].quantile(0.75)
                iqr = q3 - q1

                # Calculate the lower and upper bounds for outliers
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                # Find the number of outliers for this column
                num_outliers = len(self.data[(self.data[col] < lower_bound) | (self.data[col] > upper_bound)])
                outliers[col] = num_outliers
                if remove_outliers:
                    self.data = self.data[(self.data[col] >= lower_bound) & (self.data[col] <= upper_bound)]

        return outliers

class DataAnalytics:
    def __init__(self, adspend_df, installs_df, payouts_df, revenue_df):
        self.adspend_df = adspend_df
        self.installs_df = installs_df
        self.payouts_df = payouts_df
        self.revenue_df = revenue_df

    def user_acquisition_costs(self, groupby_column = 'network_id'):
        # Aggregate adspend data by network_id
        adspend_per_network = self.adspend_df.groupby(['network_id', 'country_id', 'event_date'])['value_usd'].sum()

        # Merge with installs data on network_id
        installs_per_network = self.installs_df.groupby(['network_id', 'country_id', 'event_date'])[
            'install_id'].count().reset_index()
        installs_with_adspend = pd.merge(installs_per_network, adspend_per_network,
                                         on=['network_id', 'country_id', 'event_date'], how = 'left')
        installs_with_adspend.fillna(0, inplace=True)

        # Calculate user acquisition cost per network
        installs_with_adspend['user_acquisition_cost_usd'] = installs_with_adspend['value_usd'] / \
                                                             installs_with_adspend['install_id']

        # Aggregate user acquisition cost by network
        user_acquisition_costs_per_network = installs_with_adspend.groupby(groupby_column)[
            'user_acquisition_cost_usd'].mean().reset_index()

        return user_acquisition_costs_per_network
    def revenue_generated_per_install(self, groupby_column= 'install_id'):
        # Merge revenue and installs data on install_id
        agregated_revenue = self.revenue_df.groupby(['install_id', 'event_date'])['value_usd'].sum().reset_index()
        revenue_with_installs = pd.merge(agregated_revenue, self.installs_df, on='install_id')
        revenue_with_installs = revenue_with_installs.rename(columns = {'value_usd':'revenue_per_install_usd'})

        # Aggregate revenue per user by country
        revenue_generated_per_user = revenue_with_installs.groupby(groupby_column)['revenue_per_install_usd'].mean().reset_index()

        return revenue_generated_per_user

    def total_payouts_made_per_install(self, groupby_column= 'install_id'):
        # Aggregate payouts data by install_id
        payouts_per_install = self.payouts_df.groupby(groupby_column)['value_usd'].sum()

        return payouts_per_install

    # def user_retention_rate(self):
    #     # Calculate the number of users who installed the app on day 0
    #     users_day_0 = self.installs_df[self.installs_df['event_date'] == self.installs_df['event_date'].min()][
    #         'install_id'].unique()
    #
    #     # Calculate the number of users who returned on day 1
    #     users_day_1 = \
    #     self.installs_df[self.installs_df['event_date'] == self.installs_df['event_date'].min() + pd.Timedelta(days=1)][
    #         'install_id'].unique()
    #
    #     # Calculate user retention rate from day 0 to day 1
    #     user_retention_rate = len(set(users_day_0) & set(users_day_1)) / len(users_day_0)
    #
    #     return user_retention_rate


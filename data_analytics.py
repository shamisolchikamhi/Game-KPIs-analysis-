import pandas as pd
import matplotlib.pyplot as plt
from data_wrangling import DataCleaning

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

        process_df = DataCleaning(data=user_acquisition_costs_per_network,
                                  columns=list(user_acquisition_costs_per_network.columns))
        process_df.id_columns_to_object()
        user_acquisition_costs_per_network = process_df.data

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
        # payouts_per_install = self.payouts_df.groupby(groupby_column)['value_usd'].sum()

        # Merge revenue and installs data on install_id
        agregated_payouts = self.revenue_df.groupby(['install_id', 'event_date'])['value_usd'].sum().reset_index()
        payouts_with_installs = pd.merge(agregated_payouts, self.installs_df, on='install_id')
        payouts_with_installs = payouts_with_installs.rename(columns={'value_usd': 'payouts_per_install_usd'})

        # Aggregate revenue per user by country
        payouts_per_install = payouts_with_installs.groupby(groupby_column)[
            'payouts_per_install_usd'].mean().reset_index()

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

class ChartMaker:
    @staticmethod
    def bar_chart(data, x_column, y_column, title=''):
        data[x_column] = data[x_column].astype(str).astype('category')
        plt.bar(data[x_column], data[y_column])
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(title)
        plt.show()

    @staticmethod
    def pie_chart(data, label_column, value_column, title=''):
        plt.pie(data[value_column], labels=data[label_column], autopct='%1.1f%%')
        plt.title(title)
        plt.show()

    @staticmethod
    def time_series_chart(data, x_column, y_column, title=''):
        plt.plot(data[x_column], data[y_column])
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(title)
        plt.show()

    @staticmethod
    def hist_chart(data, column, title=''):
        plt.hist(data[column].astype(str).astype('category'))
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.title(title)
        plt.show()

    import matplotlib.pyplot as plt
    @staticmethod
    def time_series_breakdown(data, x_column, y_column, breakdown_column, title=''):
        # Get unique values in breakdown column
        breakdown_values = data[breakdown_column].unique()

        # Create a figure and axis object
        fig, ax = plt.subplots()

        # Loop over unique values and plot a line for each value
        for value in breakdown_values:
            # Filter data for current value
            subset = data[data[breakdown_column] == value]

            # Plot a line for current value
            ax.plot(subset[x_column], subset[y_column], label=value)

        # Set labels and title
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(title)

        # Add legend
        ax.legend()

        # Show the plot
        plt.show()



import pandas as pd
import matplotlib.pyplot as plt
from data_wrangling import DataCleaning

class KpiAnalytics:
    def __init__(self, adspend_df, installs_df, payouts_df, revenue_df):
        self.adspend_df = adspend_df
        self.installs_df = installs_df
        self.payouts_df = payouts_df
        self.revenue_df = revenue_df

    def user_acquisition_costs(self, groupby_column = 'network_id', mean = True):
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
        installs_with_adspend = DataCleaning.break_down_date(installs_with_adspend)

        # Aggregate user acquisition cost by network
        if mean:
            user_acquisition_costs_per_network = installs_with_adspend.groupby(groupby_column)[
                'user_acquisition_cost_usd'].mean().reset_index()
        else:
            user_acquisition_costs_per_network = installs_with_adspend.groupby(groupby_column)[
                'user_acquisition_cost_usd'].sum().reset_index()


        process_df = DataCleaning(data=user_acquisition_costs_per_network,
                                  columns=list(user_acquisition_costs_per_network.columns))
        process_df.id_columns_to_object()
        user_acquisition_costs_per_network = process_df.data

        return user_acquisition_costs_per_network

    def revenue_generated_per_install(self, groupby_column= 'install_id', mean = True):
        # Merge revenue and installs data on install_id
        agregated_revenue = self.revenue_df.groupby(['install_id', 'event_date'])['value_usd'].sum().reset_index()
        revenue_with_installs = pd.merge(agregated_revenue, self.installs_df, on=['install_id', 'event_date'], how = 'outer')
        revenue_with_installs = revenue_with_installs.rename(columns = {'value_usd':'revenue_per_install_usd'})

        # Aggregate revenue per user by country
        if mean:
            revenue_generated_per_user = revenue_with_installs.groupby(groupby_column)[
                'revenue_per_install_usd'].mean().reset_index()
        else:
            revenue_generated_per_user = revenue_with_installs.groupby(groupby_column)[
                'revenue_per_install_usd'].sum().reset_index()

        return revenue_generated_per_user

    def total_payouts_made_per_install(self, groupby_column= 'install_id', mean = True):
        # Aggregate payouts data by install_id
        # payouts_per_install = self.payouts_df.groupby(groupby_column)['value_usd'].sum()

        # Merge revenue and installs data on install_id
        agregated_payouts = self.payouts_df.groupby(['install_id', 'event_date'])['value_usd'].sum().reset_index()
        payouts_with_installs = pd.merge(agregated_payouts, self.installs_df, on=['install_id', 'event_date'], how = 'outer')
        payouts_with_installs = payouts_with_installs.rename(columns={'value_usd': 'payouts_per_install_usd'})

        # Aggregate revenue per user by country
        if mean:
            payouts_per_install = payouts_with_installs.groupby(groupby_column)[
                'payouts_per_install_usd'].mean().reset_index()
        else:
            payouts_per_install = payouts_with_installs.groupby(groupby_column)[
                'payouts_per_install_usd'].sum().reset_index()

        return payouts_per_install

    def user_retention_rate(self, groupby_column= 'network_id', days_active = False):
        # Calculate the number of users who installed the app on day 0

        payouts_df = self.payouts_df.groupby(['install_id', 'year and month'])['event_date'].max().reset_index()
        revenue_df = self.revenue_df.groupby(['install_id', 'year and month'])['event_date'].max().reset_index()
        installs_df = self.installs_df.rename(columns={'event_date': 'install_date', 'year and month':'install_year and month'})

        df = pd.merge(installs_df, payouts_df, on='install_id', how = 'left')
        df = pd.merge(df, revenue_df, on='install_id', how = 'left' )
        df['last_active'] = df[['event_date_x', 'event_date_y']].max(axis=1)
        df['days_active'] = (df['last_active'] - df['install_date']).dt.days
        df['days_active'] = df['days_active'].fillna(0)

        if days_active:
            df = df.groupby(groupby_column)['days_active'].mean().reset_index()
        else:
            n_installs = df.groupby(groupby_column)['install_id'].nunique().reset_index()
            n_installs = n_installs.rename(columns={'install_id':'total_users'})
            n_retained = df.loc[df['days_active'] == 0].groupby(groupby_column)['install_id'].nunique().reset_index()
            n_retained = n_retained.rename(columns={'install_id': 'retained_users'})
            df = pd.merge(n_installs, n_retained, on = groupby_column, how = 'left')
            df = df.fillna(0)
            df ['retension_rate'] = df['retained_users']/df['total_users'] * 100

        return df

    def total_profit(self):
        # Get user acquisition costs
        cols = ['network_id', 'country_id', 'event_date']
        user_acquisition_costs = self.user_acquisition_costs(groupby_column=cols, mean=False)
        # Get revenue generated per install
        revenue_generated_per_install = self.revenue_generated_per_install(groupby_column=cols, mean=False)
        # Get total payouts made per install
        total_payouts_made_per_install = self.total_payouts_made_per_install(groupby_column=cols, mean=False)
        # Get user retention rate
        cols_ret = ['network_id', 'country_id', 'install_date']
        user_retention_days_active = self.user_retention_rate(groupby_column=cols_ret)
        user_retention_days_active = user_retention_days_active.rename(columns={'install_date': 'event_date'})
        user_retention_rate = self.user_retention_rate(groupby_column=cols_ret, days_active=True)
        user_retention_rate = user_retention_rate.rename(columns={'install_date': 'event_date'})

        # Merge data frames
        df = pd.merge(user_acquisition_costs, revenue_generated_per_install, on=cols, how='left')
        df = pd.merge(df, total_payouts_made_per_install, on=cols, how='left')
        df = pd.merge(df, user_retention_rate, on=cols, how='left')
        df = pd.merge(df, user_retention_days_active, on=cols)

        # Calculate profit
        df['profit_usd'] = df['revenue_per_install_usd'] - df['payouts_per_install_usd'] - df[
            'user_acquisition_cost_usd']
        # # Rename columns
        df = df.rename(columns={'revenue_per_install_usd': 'revenue', 'payouts_per_install_usd': 'payouts'})
        df = DataCleaning.break_down_date(df)

        return df

    def grouped_profit(self, groupby_column, mean = True):
        df = self.total_profit()
        if mean:
            df = df.groupby(groupby_column)[
                'profit_usd'].mean().reset_index()
        else:
            df = df.groupby(groupby_column)[
                'profit_usd'].sum().reset_index()

        return df




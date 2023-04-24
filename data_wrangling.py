import pandas as pd
import matplotlib.pyplot as plt


class DataCleaning:

    def __init__(self, data, columns):
        self.data = data
        self.columns = columns

    def id_columns_to_object(self):
        for col in self.data.columns:
            if 'id' in col:
                self.data[col] = self.data[col].astype('object')

    def date_column_type(self):
        for col in self.data.columns:
            if 'date' in col:
                self.data[col] = pd.to_datetime(self.data[col])

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
            if self.data[col].dtype in ['int64', 'float64']:
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

# New column
# feature_engineering
def break_down_date(df):
    for col in df.columns:
        if 'date' in col:
            df['year'] = df[col].dt.year
            df['month'] = df[col].dt.month
            df['year and month'] = df[col].dt.to_period('M').dt.to_timestamp()
            df['day_of_week'] = df[col].dt.day_name()

    return df

# import adata

adspend_df = pd.read_csv('adspend.csv')
installs_df = pd.read_csv('installs.csv')
payouts_df = pd.read_csv('payouts.csv')
revenue_df = pd.read_csv('revenue.csv')

adspend = DataCleaning(data = adspend_df,columns=list(adspend_df.columns))
adspend.id_columns_to_object()
adspend.date_column_type()
# adspend.check_duplicates()
adspend.fill_missing_values()
adspend.check_for_outliers()
adspend_df = break_down_date(adspend.data)

installs = DataCleaning(data = installs_df, columns= list(installs_df.columns))
installs.id_columns_to_object()
installs.date_column_type()
# installs.check_duplicates()
installs.fill_missing_values()
installs.check_for_outliers()
installs_df = break_down_date(installs.data)

payouts = DataCleaning(data = payouts_df, columns = list(payouts_df.columns))
payouts.id_columns_to_object()
payouts.date_column_type()
# payouts.check_duplicates()
payouts.fill_missing_values()
payouts.check_for_outliers()
payouts_df = break_down_date(payouts.data)

revenue = DataCleaning(data= revenue_df, columns = list(revenue_df.columns))
revenue.id_columns_to_object()
revenue.date_column_type()
# revenue.check_duplicates()
revenue.fill_missing_values()
revenue.check_for_outliers()
revenue_df = break_down_date(revenue.data)

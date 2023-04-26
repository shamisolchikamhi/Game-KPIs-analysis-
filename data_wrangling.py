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
    @staticmethod
    def break_down_date(df):
        df['year'] = df['event_date'].dt.year
        df['month'] = df['event_date'].dt.month
        df['year and month'] = df['event_date'].dt.to_period('M').dt.to_timestamp()
        df['day_of_week'] = df['event_date'].dt.day_name()

        return df

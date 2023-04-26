import pandas as pd
import matplotlib.pyplot as plt


class DataCleaning:

    def __init__(self, data, columns):
        self.data = data
        self.columns = columns

    def id_columns_to_object(self):
        """
        Convert all columns containing 'id' in the column name to object data type.

        :return: None
        :rtype: None
        """
        for col in self.data.columns:
            if 'id' in col:
                self.data[col] = self.data[col].astype('object')

    def date_column_type(self):
        """
        This function converts any columns containing the word 'date' to a datetime format using pandas'
        to_datetime method.

        :return: None
        :rtype: None
        """
        for col in self.data.columns:
            if 'date' in col:
                self.data[col] = pd.to_datetime(self.data[col])

    def check_duplicates(self):
        """
        This function checks for duplicates in a pandas DataFrame and removes them if found. If duplicates are
        found, the function prints the number of duplicates found, drops the duplicates, and resets the index of
        the DataFrame. If no duplicates are found, the function prints a message saying so.

        :return: None
        :rtype: None
        """
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
        """
        This function fills in missing values in a pandas DataFrame with either the mean value (for numeric columns)
        or an empty string (for non-numeric columns). If any missing values remain after filling, the function
        prints the row index and column name where the missing values are located.

        :return: None
        :rtype: None
        """
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
        """
        This function checks for outliers in a pandas DataFrame and returns a dictionary with the number of outliers
        for each numeric column. If remove_outliers is set to True, the function will remove the outliers from the
        DataFrame and return the same dictionary.

        :param remove_outliers: A boolean indicating whether to remove outliers or not. Default is False.
        :type remove_outliers: bool
        :return: A dictionary with the number of outliers for each numeric column.
        :rtype: dict
        """

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
        """
        This function takes in a pandas DataFrame with a 'date' column and adds four new columns to the DataFrame: 'year',
        'month', 'year and month', and 'day_of_week'. The 'year' column contains the year of each date, the 'month'
        column contains the month of each date, the 'year and month' column contains the first day of each month in the
        format 'YYYY-MM-DD', and the 'day_of_week' column contains the name of the day of the week for each date.

        :param df: A pandas DataFrame object with a 'date' column.
        :type df: pandas.DataFrame
        :return: The input DataFrame with four new columns added.
        :rtype: pandas.DataFrame
        """
        df['year'] = df['event_date'].dt.year
        df['month'] = df['event_date'].dt.month
        df['year and month'] = df['event_date'].dt.to_period('M').dt.to_timestamp()
        df['day_of_week'] = df['event_date'].dt.day_name()

        return df

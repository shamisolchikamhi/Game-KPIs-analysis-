import pandas as pd
import matplotlib.pyplot as plt
from data_wrangling import DataCleaning


class AnalyticsCharts:
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



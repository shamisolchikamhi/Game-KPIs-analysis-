import matplotlib.pyplot as plt


def bar_chart(data, x_column, y_column, title=''):
    """
    Create a bar chart using the specified data, x and y columns, and title.

    :param data: the DataFrame containing the data to be plotted
    :type data: pandas.DataFrame
    :param x_column: the name of the column to be plotted on the x-axis
    :type x_column: str
    :param y_column: the name of the column to be plotted on the y-axis
    :type y_column: str
    :param title: the title of the chart (optional)
    :type title: str
    :return: None
    :rtype: None
    """
    data[x_column] = data[x_column].astype(str).astype('category')
    plt.bar(data[x_column], data[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(title)
    plt.show()


def pie_chart(data, label_column, value_column, title=''):
    """
    Create a pie chart using the specified data, label column, value column, and title.

    :param data: the DataFrame containing the data to be plotted
    :type data: pandas.DataFrame
    :param label_column: the name of the column containing the labels
    :type label_column: str
    :param value_column: the name of the column containing the values
    :type value_column: str
    :param title: the title of the chart (optional)
    :type title: str
    :return: None
    :rtype: None
    """
    plt.pie(data[value_column], labels=data[label_column], autopct='%1.1f%%')
    plt.title(title)
    plt.show()


def time_series_chart(data, x_column, y_column, title=''):
    """
    Create a time series chart from a pandas DataFrame.

    :param data: A pandas DataFrame with columns `x_column` and `y_column`.
    :type data: pandas.DataFrame
    :param x_column: The name of the column containing the x-axis values.
    :type x_column: str
    :param y_column: The name of the column containing the y-axis values.
    :type y_column: str
    :param title: The title of the chart.
    :type title: str
    :return: None
    :rtype: None
    """
    plt.plot(data[x_column], data[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(title)
    plt.show()


def hist_chart(data, column, title=''):
    """
    Create a histogram chart of a given column in a dataset.

    :param data: The dataset to use.
    :type data: pandas DataFrame
    :param column: The name of the column to create the histogram for.
    :type column: str
    :param title: Optional title for the chart.
    :type title: str
    :return: None
    :rtype: None
    """
    plt.hist(data[column].astype(str).astype('category'))
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.title(title)
    plt.show()


def time_series_breakdown(data, x_column, y_column, breakdown_column, title=''):
    """
    Plots a time series chart for a data set, broken down by a given column.

    :param data: A Pandas DataFrame containing the data.
    :type data: pandas.DataFrame
    :param x_column: The name of the column containing the x-axis values.
    :type x_column: str
    :param y_column: The name of the column containing the y-axis values.
    :type y_column: str
    :param breakdown_column: The name of the column to break down the data by.
    :type breakdown_column: str
    :param title: The title of the chart. Default is an empty string.
    :type title: str
    :return: None
    :rtype: None
    """
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


def regressions_charts(x, y, prediction, xlabel, ylabel, title):
    """
    Plots a scatter plot of `X` versus `Y` and a regression line based on `prediction`.

    :param x: The input variable values.
    :type x: numpy array or list
    :param y: The output variable values.
    :type y: numpy array or list
    :param prediction: The predicted output variable values.
    :type prediction: numpy array or list
    :param xlabel: The label for the X axis.
    :type xlabel: str
    :param ylabel: The label for the Y axis.
    :type ylabel: str
    :param title: The title for the plot.
    :type title: str
    :return: None
    """
    plt.scatter(x, y)
    plt.plot(x, prediction, color='red')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

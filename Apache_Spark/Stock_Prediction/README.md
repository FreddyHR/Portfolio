#Stock Price Prediction using PySpark

This Python script uses PySpark to build a simple linear regression model to predict stock prices based on historical data fetched from Yahoo Finance API.

##Prerequisites
Before running the script, ensure you have the following installed:

Apache Spark
FindSpark
PySpark
yfinance
Instructions

##Clone the repository and install the required libraries using the following command:
Copy code
pip install findspark pyspark yfinance

1) Execute the script in your Python environment.
2) Input the list of stock symbols you want to fetch data for (separate symbols with a comma).
3) Provide the initial date, final date, and a date for which you want to make a prediction.

##Code Description
The code fetches historical stock data from Yahoo Finance for the specified stock symbols. It then prepares the data by extracting features from the date (Year, Month, Day) and stock closing price. The script uses PySpark's Linear Regression to build a prediction model based on this data.

The predict() function allows you to make predictions for a specific date by providing the year, month, and day as inputs.

Note:
Ensure that you have proper internet connectivity to fetch data from Yahoo Finance.

Happy stock prediction! 🚀
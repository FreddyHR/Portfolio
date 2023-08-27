import findspark
findspark.init()

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import yfinance as yf
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
import os

# Creating a spark context class
sc = SparkContext()

# Creating a spark session
spark = SparkSession \
    .builder \
    .appName("Creating a SparkML Model").getOrCreate()

# Replace 'AAPL' with the stock symbol you want to get data for
stock_symbol = input('Introduce a list of stock symbols (The symbols must be separated by a comma. e.i.: "AAPL"):')

# Fetch historical data for the stock
start_date=input('Introduce initial date (YYYY-MM-DD):')
end_date=input('Introduce final date (YYYY-MM-DD):')
prediction_date=input('Introduce a date to make a prediction (YYYY-MM-DD):')
prediction_date=prediction_date.split("-")
prediction_date[0]=int(prediction_date[0])
prediction_date[1]=int(prediction_date[1])
prediction_date[2]=int(prediction_date[2])

stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
stock_data=stock_data.reset_index()

# Extracting data from 'Date'
stock_data['Year']=stock_data['Date'].dt.year
stock_data['Month']=stock_data['Date'].dt.month
stock_data['Day']=stock_data['Date'].dt.day

stock_price=stock_data[['Year','Month','Day','Close']]

# Creating Spark DataFrame
spark_df=spark.createDataFrame(stock_price)

# Using the VectorAssembler() function to convert the dataframe columns into feature vectors
assembler = VectorAssembler(
    inputCols=["Year","Month","Day"],
    outputCol="features")
data = assembler.transform(spark_df).select('features','Close')

# Create a LR model
lr = LinearRegression(featuresCol='features', labelCol='Close', maxIter=10)
lr.setRegParam(0.1)

# Fit the model
lrModel = lr.fit(data)

#Saving the model
current_dir = os.getcwd()
model_path = os.path.join(current_dir, 'stockprediction.model')
lrModel.write().overwrite().save(model_path)

# You need LinearRegressionModel to load the model
from pyspark.ml.regression import LinearRegressionModel

model = LinearRegressionModel.load('stockprediction.model')

#Making prediction

# This function converts a scalar number into a dataframe that can be used by the model to predict.
def predict(year, month, day):
    assembler = VectorAssembler(inputCols=["Year", "Month", "Day"],outputCol="features")
    data = [[year, month, day]]
    columns = ["Year", "Month", "Day"]
    df = spark.createDataFrame(data, columns)
    df = assembler.transform(df)
    predictions = model.transform(df)
    predictions.select('prediction').show()

predict(prediction_date[0],prediction_date[1],prediction_date[2])

#FIRST ETL

import glob                         # this module helps in selecting files 
import pandas as pd                 # this module helps in processing CSV files
import xml.etree.ElementTree as ET  # this module helps in processing XML files.
from datetime import datetime

!wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/datasource.zip

!unzip datasource.zip -d dealership_data

tmpfile    = "dealership_temp.tmp"               # file used to store all extracted data
logfile    = "dealership_logfile.txt"            # all event logs will be stored in this file
targetfile = "dealership_transformed_data.csv"   # file where transformed data is stored

# Add the CSV extract function below
def extract_from_csv(file_to_process):
    dataframe=pd.read_csv(file_to_procces)
    return dataframe

# Add the JSON extract function below
def extract_from_json(file_to_process):
    dataframe=pd.read_json(file_to_process,lines=True)
    return dataframe

# Add the XML extract function below, it is the same as the xml extract function above but the column names need to be renamed.
def extract_from_xml(file_to_process):
    dataframe=pd.Dataframe(columns=['car_model','year_of_manufacture','price','fuel'])
    tree=ET.parse(file_to_process)
    root=tree.getroot()
    for item in root:
        car_model=item.find('car_model').text
        year_of_manufacture=int(item.find('year_of_manufacture').text)
        price=float(item.find('price').text)
        fuel=item.find('fuel').text
        dataframe=dataframe.append({'car_model':car_model,'year_of_manufacture':year_of_manufacture,'price':price,'fuel':fuel}, ignore_index=True)
        return dataframe

def extract():
    extracted_data = pd.DataFrame(columns=['car_model','year_of_manufacture','price', 'fuel']) # create an empty data frame to hold extracted data
    
    #process all csv files
    for csvfile in glob.glob("dealership_data/*.csv"):
        extracted_data = extracted_data.append(extract_from_csv(csvfile), ignore_index=True)
        
    #process all json files
    for jsonfile in glob.glob("dealership_data/*.json"):
        extracted_data = extracted_data.append(extract_from_json(jsonfile), ignore_index=True)
    
    #process all xml files
    for xmlfile in glob.glob("dealership_data/*.xml"):
        extracted_data = extracted_data.append(extract_from_xml(xmlfile), ignore_index=True)
        
    return extracted_data


# Add the transform function below
def transform(data):
    data['price']=round(data.price,2)
    return data


# Add the load function below
def load(targetfile,data_to_load):
    data_to_load.to_csv(targetfile)


# Add the log function below
def log(message):
    timestamp_format='%H:%M:%S-%h-%d-%Y'
    now=datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open ("dealership_logfile.txt" ,'a') as f:
        f.write(timestamp + ','+ message +'\n')



        # Log that you have started the ETL process
log('ETL process initiated')

# Log that you have started the Extract step
log('Extracting data')
# Call the Extract function
extracted_data = extract()
# Log that you have completed the Extract step
log('Extraction completed')

# Log that you have started the Transform step
log('Starting Transformations')
# Call the Transform function
transformed_data=transform(extracted_data)
# Log that you have completed the Transform step
log('Transformation completed')

# Log that you have started the Load step
log('Loading data')
# Call the Load function
load(targetfile,transformed_data)
# Log that you have completed the Load step
log('The data has been loaded')

# Log that you have completed the ETL process
log('ETL process finished')

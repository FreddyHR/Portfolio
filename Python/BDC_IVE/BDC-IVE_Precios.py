#Installing libraries
import html5lib
import pandas as pd
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime

start1 = time.process_time()
print('------------------------------EXTRACTOR DE PRECIOS v0.2------------------------------')
#PATH
path=os.path.abspath(os.getcwd())
output_path=(os.path.join(path,'Output'))
logpath=os.path.join(output_path,'logfile.txt')
errorpath=os.path.join(output_path,'errorfile.txt')

#Input
CSV_file_path=input('Ingresar ruta del archivo de códigos: ')
sep=input('Ingresar delimitador del archivo (","/";"): ')
DB_year=str(input('Año: '))
if len(str(DB_year))==4:
    DB_year=DB_year[2:4]
    
province={'Alicante':1,'Castellón':2,'Valencia':3,'Andalucía':4,'Aragón':5,'Asturias':6,'Baleares':7,'Canarias':8,'Cantabria':9,'Castilla y León':10,'Castilla La Mancha':11,'Cataluña':12,'Comunidad Valenciana':13,'Extremadura':14,'Galicia':15,'Madrid':16,'Murcia':17,'Navarra':18,'País Vasco':19,'La Rioja':20}    
print(province)
DB_province=input('Selecciona la provincia: ')

if len(DB_province)>2:
    print(type(DB_province))
    DB_province=province[DB_province]

code_price=[]
empty=[]
price_codes=pd.read_csv(CSV_file_path,sep=sep)                     #If necessary add engine='python' as a parameter

#Checking existing files/directories
if os.path.exists(logpath)==True:
    a1=input('Existe un archivo de registro de eventos. ¿Deseas sobreescribirlo? (S/N): ')
    a1=a1.upper()
    if a1=='S':
        with open(logpath,'r+') as file1:
            file1.seek(0,0)
            file1.truncate()

if os.path.exists(os.path.join(output_path,'Codes_prices.csv'))==True:
    b1=input('Existe un archivo de códigos/precios. ¿Deseas sobreescribirlo? (S/N): ')
    b1=b1.upper()
    if b1=='S':
        with open(logpath,'r+') as file2:
            file2.seek(0,0)
            file2.truncate()
if os.path.exists(output_path)==False:
    os.mkdir(output_path)


#Timestamp for logging
timestamp_format='%d-%h-%y-%H:%M:%S'                                                                        
with open(logpath,'a') as f:
    now=datetime.now()
    start2=now
    timestamp=now.strftime(timestamp_format)
    f.write(timestamp+', iniciando proceso de extracción\n')

#Getting Selenium ready
options = Options()
options.add_argument('headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#option=webdriver.ChromeOptions()
#option.add_argument('headless')
#chromedriver_path=os.path.join(path,'chromedriver')
#driver=webdriver.Chrome(chromedriver_path,options=option)


i=1
total1=str(len(price_codes.columns))


#Scraping
for code in price_codes:
    print('-----------'+code+'-----------'+'('+str(i)+'/'+total1+')')
    url=str('https://bdc.f-ive.es/BDC'+DB_year+'/'+DB_province+'/'+code)
    with open(logpath,'a') as f:
        now=datetime.now()
        timestamp=now.strftime(timestamp_format)
        f.write(timestamp+', extrayendo precio de la unidad '+code+'\n')
    driver.get(url)                                                     #Requesting HTML
    time.sleep(2)
    htmlSource=driver.page_source                                    
    soup=BeautifulSoup(htmlSource,'html5lib')                           #Parsing HTML
    data=soup.find_all('div', {'class':'col-md-2 text-right'})          #Filtering
    data_extracted=""

    for value in data:
        y=len(value.text)

        if y>2:   
            data_extracted=value.text
            print('Len: '+str(y))
    
    with open(logpath,'a') as f:
        now=datetime.now()
        timestamp=now.strftime(timestamp_format)
        f.write(timestamp+', precio de la unidad '+code+' extraído\n')
    results=[code,data_extracted]
    code_price.append(results)
    #print('DATA')
    #print(data)
    print('DATA_EXTRACTED')
    print(data_extracted)


    i=i+1
    
df=pd.DataFrame(code_price,columns=['Codes','Prices'])
df_code_price=df.set_index('Codes')

rows_with_nan = [index for index, row in df_code_price.iterrows() if row.isnull().any()]       #Checking missing values

driver.quit()


with open(logpath,'a') as f:
    now=datetime.now()
    timestamp=now.strftime(timestamp_format)
    f.write(timestamp+', proceso de extracción finalizado\n')
with open(logpath,'a') as f:
    now=datetime.now()
    timestamp=now.strftime(timestamp_format)
    f.write(timestamp+', generando archivo de CSV con códigos y precios\n')

df.to_csv(os.path.join(path,'Output','Codes_prices.csv'),index=False)
with open(logpath,'a') as f:
    now=datetime.now()
    timestamp=now.strftime(timestamp_format)
    f.write(timestamp+', archivo CSV generado\n')
    f.write('Tiempo total de ejecución sin esperas: '+str(time.process_time() - start1)+'s\n')
    f.write('Tiempo total de ejecución con esperas: '+str(now - start2)+'\n')

if rows_with_nan != []:
    conf=input('Se han conseguido archivos sin precios. ¿Deseas listar esos archivos? (S/N): ')
    conf=conf.upper()
    if conf=='S':
        with open(logpath,'a') as f:
            now=datetime.now()
            timestamp=now.strftime(timestamp_format)
            f.write(timestamp+', generando archivo de CSV con códigos sin precios\n')
        empty=pd.DataFrame(rows_with_nan,columns='Codes')
        empty.to_csv(os.path.join(path,'Output','Codes_prices.csv'),index=False)
        with open(logpath,'a') as f:
            now=datetime.now()
            timestamp=now.strftime(timestamp_format)
            f.write(timestamp+', archivo CSV con precios faltantes, generado\n')
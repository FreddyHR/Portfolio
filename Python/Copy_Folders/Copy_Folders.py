import os
import pandas as pd
import shutil
from datetime import datetime

##INPUTS

codes_path=input('Enter the path to the CSV file containing the name of the required folders: ')
if (codes_path[0]=='"' and codes_path[-1]=='"'):
    codes_path=codes_path.replace('"','')
sep=input('Enter the delimiter of the .csv file (","/";"): ')
source_path=input('Enter the Source folder path: ')
if (source_path[0]=='"' and source_path[-1]=='"'):
    source_path=source_path.replace('"','')
codes=list(pd.read_csv(codes_path,sep=sep))
output_path=input('Enter the Destination folder path: ')
if (output_path[0]=='"' and output_path[-1]=='"'):
    output_path=output_path.replace('"','')
    
##GETTING LIST OFDIRECTORIES
items=os.listdir(source_path)

##CREATING EMPTY LISTS
dir=[]
dir_copy=[]
dir_copy_path=[]
dir_error=[]
solved_codes=[]

##FINDING CODES WITHIN THE LIST OF DIRECTORIES
for i in items:
    p=os.path.join(source_path,i)
    if os.path.isdir(p):
        dir.append((i,p))
source=pd.DataFrame(dir,columns=['Folders','Path'])

##ESTABLISHING PARAMETERS FOR LOOPING
x=source.shape[0]
j=0

##LOOPING
for i in codes:
    
    print('Verifying code: '+str(i))
    source['Verif']= source['Folders'].str.find(i)
    
    for j in range(x):
        vf=source.loc[j,'Verif']


    
        if vf!=-1:
            
            timestamp_format='%d-%h-%y-%H:%M:%S'  
            now=datetime.now()
            timestamp=now.strftime(timestamp_format)
            print(timestamp+', adding the code '+i+' to the list of codes to be copied\n')
            
            f=source.loc[j,'Folders']
            s=source.loc[j,'Path']
            d=os.path.join(output_path,i)

            dir_copy.append(f)
            dir_copy_path.append((s,d))
            solved_codes.append(i)
        j=j+1
df=pd.DataFrame(dir_copy_path,columns=['Copy','Paste'])
print(df)
##UNSOLVED CODES
print(df.loc[1,'Copy'])
dir_error=[i for i in codes if i not in solved_codes]

##ESTABLISHING PARAMETERS FOR LOOPING
y=df.shape[0]

##COPYING FOLDERS

for i in range(y):
    try:   
        copy=str(df.loc[i,'Copy'])
        paste=str(df.loc[i,'Paste'])

        timestamp_format='%d-%h-%y-%H:%M:%S'  
        now=datetime.now()
        timestamp=now.strftime(timestamp_format)
        print(timestamp+', copying the folder '+str(i)+' from '+copy+'to '+paste+'\n')

        shutil.copytree(copy,paste )
    except FileExistsError:
        print('The destination file already has folders inside')

print('Missing folders:')
print(dir_error)

input('Press [Enter] or any key to continue.')

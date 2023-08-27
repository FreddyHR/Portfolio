import pandas as pd
import numpy as np

ppkk_path='/Users/vanderslof/Documents/Python/Projects/Find_Coord/Input/PPKK_ADIF_v2.xlsx'
walls_path='/Users/vanderslof/Documents/Python/Projects/Find_Coord/Input/Tablas.xlsx'

ppkk=pd.read_excel(io=ppkk_path,sheet_name='PPKK_ADIF')
walls=pd.read_excel(io=walls_path,sheet_name='Table 1')


print(walls)

for row in walls:

    walls[coord_i_x]=1
    walls[aux]
    walls[coord_i_y]=2
    walls[coord_f_x]=1
    walls[coord_f_y]=2

##COPY FOLDER

This is a small routine for copying folder from 'Source' directory to 'Destination' directory. 

By running the script, you will be able to find by the names and copy a list of folders, and the files inside, from point 'A' to point 'B'.

The script will take a list of names/codes, look in the 'Source' folder and make a copy of the folders whose names appear in the list, then paste the copy into the 'Destination' folder.

Inputs required: CSV file including the codes or folder names.
Input Format: folder_name_1,folder_name_2,folder_name_3,...

##MAKE SURE THE DESTINATION FOLDER IS EMPTY##

#Example

Folders_required(codes).csv : folder_1, folder_2, folder_3
List of folder inside the Destination directory: folder_1, folder_3, folder_25

The routine will copy the folders 'folder_1, folder_3 and folder_25 (Note that the name of folder_2 is embedded in the name of folder_25)



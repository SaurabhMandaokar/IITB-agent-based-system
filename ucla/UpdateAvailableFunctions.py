import sys
from DownloadableFunctions import *

py_file_name=sys.argv[1]
#print(py_file_name)
##py_file_name='Single_Mechine_Sequencing_Considering_Maintenace_Action'
Introduction_Data=eval(py_file_name+".introduction()")
#print(Introduction_Data)



avaialable_function_table={}
avaialable_function_file = open("AvailableFunctions.txt")
avaialable_function_file_contents = avaialable_function_file.read()
Lines = avaialable_function_file_contents.splitlines()
for line in Lines:
        key_values=line.split("=>")
        key=key_values[0]
        value=(key_values[1]).split("|")
        avaialable_function_table[key] = value

#print(avaialable_function_table)

if Introduction_Data['Function Type'] in avaialable_function_table:
        if py_file_name not in avaialable_function_table[Introduction_Data['Function Type']]:
                avaialable_function_table[Introduction_Data['Function Type']].append(py_file_name)
else:
        avaialable_function_table[Introduction_Data['Function Type']]=[py_file_name]

Output_file = open("AvailableFunctions.txt", "w")
for key in avaialable_function_table:
        value_text=""
        for each_func in avaialable_function_table[key]:
                value_text+=each_func+"|"
        text=key+"=>"+value_text[:-1]
        Output_file.write(text)
        Output_file.write("\n")
Output_file.close()

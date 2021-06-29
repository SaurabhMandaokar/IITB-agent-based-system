import sys
from DownloadableFunctions import *

py_file_name=sys.argv[1]
#print(py_file_name)
Introduction_Data=eval(py_file_name+".introduction()")
#print(Introduction_Data)
activeORpassive = str(Introduction_Data['Active or Passive'])


if activeORpassive == 'Active':
        active_function_table={}
        active_function_file = open("ActiveFunctionsList.txt")
        active_function_file_contents = active_function_file.read()
        Lines = active_function_file_contents.splitlines()
        for line in Lines:
                key, value=line.split("=>")
                active_function_table[key] = value

##        print(active_function_table)

        active_function_table[py_file_name]='0'

        print(active_function_table)

        Output_file = open("ActiveFunctionsList.txt", "w")
        for key in active_function_table:
                text=key+"=>"+active_function_table[key]
                Output_file.write(text)
                Output_file.write("\n")
        Output_file.close()

else:
        passive_function_table={}
        passive_function_file = open("PassiveFunctionsList.txt")
        passive_function_file_contents = passive_function_file.read()
        Lines = passive_function_file_contents.splitlines()
        for line in Lines:
                key, value=line.split("=>")
                passive_function_table[key] = value

##        print(passive_function_table)

        passive_function_table[py_file_name]='0'

        print(passive_function_table)

        Output_file = open("PassiveFunctionsList.txt", "w")
        for key in passive_function_table:
                text=key+"=>"+passive_function_table[key]
                Output_file.write(text)
                Output_file.write("\n")
        Output_file.close()
        

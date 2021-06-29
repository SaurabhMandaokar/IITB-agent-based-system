import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from DownloadableFunctions import *

def open_file():
        try:
            root.filepath =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = [('Python Files', '*.py')])
            print (root.filepath)
            py_file_name = root.filepath.split("/")[-1]
            #print (py_file_name)                       
            py_file = open(root.filepath,"r+")
            py_file_content=py_file.read()
            #print(py_file_content)
            path_to_save='DownloadableFunctions\\'
            file_to_write = open(path_to_save+py_file_name,"w")
            file_to_write.write(py_file_content)
            file_to_write.close()
            #print(py_file_name[:-3])
            #print("Current Working Directory " , os.getcwd())
            db_dir = "DataBase/"
            os.mkdir(db_dir+py_file_name[:-3])
            os.system('python UpdateAvailableFunctions.py '+py_file_name[:-3])
            os.system('python UpdateFunctionDependency.py '+py_file_name[:-3])
            os.system('python UpdateActivePassiveFunctionsLists.py '+py_file_name[:-3])
            directory = "GeeksforGeeks"
        except:
            pass

root = Tk()
root.geometry('200x100')                     

btn = Button(root, text ='Install Function File', command = lambda:open_file())
btn.pack(side = TOP, pady = 10)

mainloop()

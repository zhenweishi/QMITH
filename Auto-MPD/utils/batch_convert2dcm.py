# -*- coding: utf-8 -*-
"""
@author: Tianchen Luo

Rename those dcm file without extension
"""




import os

directory = '/Users/luotianchen/Desktop/VOPQD0NP/'
files = os.listdir(directory)
for file in files:

    file_name, file_extension = os.path.splitext(file)
    if(file_extension == ""):
        pre_name = directory + file
        new_name = directory + file + '.dcm'
        os.rename(pre_name,new_name)
    


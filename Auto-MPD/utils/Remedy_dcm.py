# -*- coding: utf-8 -*-
"""
@author: Tianchen Luo
不小心路径选错了可以用这个修复
Rename those dcm file without extension
"""




import os

directory = '/Users/luotianchen/Desktop/'
files = os.listdir(directory)
for file in files:

    file_name, file_extension = os.path.splitext(file)
    if(file_extension == ".dcm"):
        pre_name = directory + file
        new_name = directory + file_name 
        os.rename(pre_name,new_name)
    


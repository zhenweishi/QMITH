import os
from glob import glob
import nrrd 
import nibabel as nib #pip install nibabel, if nibabel is not already installed
import numpy as np

baseDir = os.path.normpath('/Users/luotianchen/Desktop/nrrd2nii')
files = glob(baseDir+'/*.nrrd')
print(baseDir)
for file in files:
#load nrrd 
  file_name, file_extension = os.path.splitext(file)
  _nrrd = nrrd.read(file)
  data = _nrrd[0]
  header = _nrrd[1]

#save nifti
  img = nib.Nifti1Image(data, np.eye(4))
  nib.save(img,os.path.join(baseDir, file_name + '.nii'))
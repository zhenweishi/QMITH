import pydicom as dicom
import GUI_Functions as funcs

file_path = '/Users/luotianchen/Desktop/LUNG1-020/resources/LUNG1-020_dcm/files/1.3.6.1.4.1.40744.29.98391516339017251875583405891209756382.dcm'

patients_dcm_path = funcs.batch_collect_patients_dcm_path(file_path)

dcm = dicom.read_file(patients_dcm_path[0], force=True)
print(dcm)
'''



try:
    print(dcm.InstitutionName)
except:
    print("FileDataset object has no attribute 'InstitutionName' ")

try:
    print(dcm.SOPInstanceUID)
except:
    print("FileDataset object has no attribute 'SOP Instance UID' ")

try:
    print(dcm.StudyDate)
except:
    print("FileDataset object has no attribute 'Study Date' ")

try:
    print(dcm.AcquisitionDate)
except:
    print("FileDataset object has no attribute 'Acquisition Date' ")

try:
    print(dcm.ManufacturerModelName)
except:
    print("FileDataset object has no attribute 'Manufacturers Model Name' ")

try:
    print(dcm.ImagePositionPatient)
except:
    print("FileDataset object has no attribute 'Image Position (Patient)' ")

try:
    print(dcm.Rows)
except:
    print("FileDataset object has no attribute 'Rows' ")

try:
    print(dcm.Columns)
except:
    print("FileDataset object has no attribute 'Columns' ")

try:
    print(dcm.PixelSpacing)
except:
    print("FileDataset object has no attribute 'Pixel Spacing' ")

try:
    print(dcm.SliceThickness)
except:
    print("FileDataset object has no attribute 'Slice Thickness' ")

try:
    print(dcm.StudyDescription)
except:
    print("FileDataset object has no attribute 'Study Description' ")

try:
    print(dcm.SeriesDescription)
except:
    print("FileDataset object has no attribute 'Series Description' ")

'''





#print(dcm)




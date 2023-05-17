import pydicom as dicom

file_path = '/Users/luotianchen/Desktop/LUNG1-020/resources/LUNG1-020_dcm/files/1.3.6.1.4.1.40744.29.98391516339017251875583405891209756382.dcm'
dcm = dicom.read_file(file_path, force=True)

#print(dcm.get(('7fe0', '0010')))
# (7fe0, 0010) Pixel Data                          OW: Array of 524288 elements

print(dcm.items())
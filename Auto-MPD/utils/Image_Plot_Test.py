import cv2
import os
import glob
import numpy as np
import pydicom as dicom
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# convert to Hounsfield Unit (HU) by multiplying rescale slope and adding intercept
def get_pixels_hu(scans):  
    image = np.stack([s.pixel_array for s in scans])
    image = image.astype(np.int16)  # convert to int16
            # the code below checks if the image has slope and intercept
            # since MRI images often do not provide these
    try:
        intercept = scans[0].RescaleIntercept
        slope = scans[0].RescaleSlope
    except AttributeError:
        pass
    else:
        if slope != 1:
            image = slope * image.astype(np.float64)
            image = image.astype(np.int16)
        image += np.int16(intercept)
    
    return np.array(image, dtype=np.int16)
        
        # Read scans under the specified path
def Read_scan(path):  
    scan = [dicom.dcmread(s, force=True) for s in glob.glob(os.path.join(path, '*.dcm'))]
    try:
        scan.sort(key=lambda x: int(x.ImagePositionPatient[2]))  # sort slices based on Z coordinate
    except:
        print('AttributeError: Cannot read scans')
    return scan


def add_colored_mask(image, mask_image):
    mask_image_gray = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
    
    mask = cv2.bitwise_and(mask_image, mask_image, mask=mask_image_gray)
    
    mask_coord = np.where(mask!=[0,0,0])

    mask[mask_coord[0],mask_coord[1],:]=[0,255,0]

    ret = cv2.addWeighted(image, 0.7, mask, 0.3, 0)

    return ret


file_path = "../72CT/1-001.dcm"
dirname = os.path.dirname(file_path)
scans = Read_scan(dirname)
HU = get_pixels_hu(scans)   # <class 'numpy.ndarray'>   (127, 512, 512)

gray = np.array(HU[50, :, :], dtype=np.uint8)
IMG_OUT = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)


colored = add_colored_mask(HU[50, :, :], IMG_OUT)

#plt.imshow(IMG_OUT) # 显示图片
#plt.imshow(HU[50, :, :],plt.cm.gray) # 显示图片

plt.imshow(colored)

plt.axis('off') # 不显示坐标轴
plt.show()

#cv2.imwrite('try.png',HU[50, :, :],plt.cm.gray)
#print(HU[50, :, :])



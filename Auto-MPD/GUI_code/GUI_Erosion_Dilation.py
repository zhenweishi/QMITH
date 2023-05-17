from ast import parse
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import erosion, dilation
import matplotlib.pyplot as plt
import skimage.transform as skTrans
import nibabel as nib
import os
import numpy as np
import copy
import random
from skimage.measure import label
from scipy import ndimage
import yaml
import pydicom as dicom
from skimage import draw
from skimage.io import imread, imshow


def clean_list(files):
        tmp = files.copy()
        for i in range(len(files)):
            if files[i] == '.DS_Store':
                tmp.pop(i)

        return tmp

def plot_compare_2d(before, after,figure_size):
    """
    :param before: left sub img
    :param after: right sub img
    :param figure_size: sub img size
    
    Works for 2D gray-scale img
    This function will plot 2 sub imgs, left is raw img without any transform operation
                                        right is the img after transform operation
    

    """
    fig, axes = plt.subplots(1, 2, figsize=(figure_size, figure_size))
    ax = axes.ravel()

    ax[0].imshow(before)
    ax[0].set_axis_off()
    
    ax[1].imshow(after)
    ax[1].set_axis_off()
    
    
def getLargestCC(mask):
    """
    :param mask: 2d numpy array
    
    This function will retain the main connected component and drop other small pixels
    

    """
    labels = label(mask)
    assert( labels.max() != 0 ) # assume at least 1 CC
    largestCC = labels == np.argmax(np.bincount(labels.flat)[1:])+1
    return largestCC

def to_one(array,threshold):
    """
    :param array: input 2d numpy array
    :param threshold: threshold
    
    Works for 2D gray-scale img
    This function will round all val > threshold to 1, otherwise 0 
    return the array after operation
    
    """
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] > threshold: # random
                array[i][j] = 1
            else:
                array[i][j] = 0
    return array

def get_border(img, pad):    
    """
    :param img: input raw image
    :param pad: padding value
    
    Works for 2D gray-scale img
    This function will calculate the index of top, bottom, left, right indices of mask (return)
    Then, crop the mask into a small 2d numpy array
    """
    
    top = [0,False]
    left = [0,False]
    right = [0,False]
    bottom = [0,False]

    for i in range(len(img[0])):
        # for j in range(len(img[0])):
        row_sum = np.sum(img[i,:])
        if  row_sum > 0 and i > pad-1 and not top[1]:
            top[0] = i-pad
            top[1] = True
        
        if  top[1] and row_sum == 0 and i > pad-1 and not bottom[1]:
            bottom[0] = i+pad
            bottom[1] = True
            
            break
            
    for i in range(len(img)):
    
        col_sum = np.sum(img[:,i])
        if  col_sum > 0 and i > pad-1 and not left[1]:
            left[0] = i-pad
            left[1] = True
            
        if  left[1] and col_sum == 0 and i > pad-1 and not right[1]:
            right[0] = i+pad
            right[1] = True
            
            break
    
    return int(top[0]), int(bottom[0]), int(left[0]), int(right[0])     


def mask_elastic_deformation(mask, ALPHA, THRESHOLD):
    """
    :param mask: The mask after cropped
    :param ALPHA: parameters to control the extent of elastic deformation. (positive correlation)
    
    This function will randomly apply elastic deformation to the mask after cropped.
    Use parameter ALPHA to control the extent
    return the deformed mask
    
  
    """
    size_large = 1024
    original_height = len(mask)
    original_width = len(mask[0])
    
    resize = np.expand_dims(skTrans.resize(mask, (size_large,size_large), order=0, preserve_range=True), 0)
    t = ElasticDeformation(np.random.RandomState(), spline_order=0, alpha=ALPHA, execution_probability=1)
    deformed_ = t(resize)[0]
    
    deformed__ = to_one(skTrans.resize(deformed_ ,(original_height,original_width), order=0, preserve_range=True), THRESHOLD)
    
    deformed___ = getLargestCC(deformed__)

    deformed = ndimage.binary_fill_holes(deformed___).astype(int)
    
    return deformed


def random_mask_generator(mask, padding, ALPHA, threshold):
    """
    :param mask: The raw mask 
    :param ALPHA: parameters to control the extent of elastic deformation. (positive correlation)
    :param padding: padding of cropped mask
    :param Threshold: round all val > threshold to 1, otherwise 0 
    
    This function will randomly generate a deformed mask based on input raw mask, act as dummy data augmentation .
    """
    
    top,bottom,left,right = get_border(mask,padding)
    print(top,bottom,left,right)
    cropped_mask = np.array(mask[top:bottom, left:right])
    deformed_mask = mask_elastic_deformation(cropped_mask, ALPHA, threshold)
    tmp_mask = copy.copy(mask)
    tmp_mask[top:bottom, left:right] = deformed_mask
    return tmp_mask

def batch_generate(mask, padding, batch_nums, alpha_choice, threshold_choice, path, see_random_state):
    """
    Batch generate some dummy_mask with elastic deformation
    Each time, randomly select the value of Alpha and threshold
    """
    
    for i in range(batch_nums):
        rand_alpha = random.randint(0,len(alpha_choice)-1)
        rand_threshold = random.randint(0,len(threshold_choice)-1)
        if see_random_state:
            print('Random ALPHA = ', alpha_choice[rand_alpha])
            print('Random Threshold = ', threshold_choice[rand_threshold])
            print('----------------------------------------------------')
        
        dummy_mask = random_mask_generator(mask, padding, alpha_choice[rand_alpha], threshold_choice[rand_threshold])
        nifti_file = nib.Nifti1Image(dummy_mask, affine=np.eye(4))
        dummy_name = 'dummy_'+str(i)+'.nii.gz'
        nib.save(nifti_file, os.path.join(path, dummy_name))
        
def arr2nii_and_save(arr, path):
    nifti_file = nib.Nifti1Image(arr, affine=np.eye(4))
    nib.save(nifti_file,path)
    

def record_tumor_index_from_mask(mask):
    """
    return a list that contains all slices have tumor 
    """
    record = []
    
    z = mask[0][0].shape[0]
    
    for i in range(z):
        if np.sum(mask[:,:,i]) != 0 :
            record.append(i)
    
    return record
        

def get_border_3D(mask):    
    """
    return the max border for tumor from a 3D mask, then, crop each with it
    """
    slices_with_tumor = record_tumor_index_from_mask(mask)
    top = 10000
    bottom = 0
    left = 10000
    right = 0

    for i in slices_with_tumor:
        
        top_,bottom_,left_,right_ = get_border(mask[:,:,i],5)
        
        if top_<top: top = top_
        if left_<left: left = left_
        if bottom_ > bottom: bottom = bottom_
        if right_>right: right = right_
    
    return top,bottom,left,right  

def crop_tumor(input):
    top,bottom,left,right = get_border(input,2)
    return [input[top:bottom, left:right], [top,bottom,left,right]]


def random_erosion_and_dilation_deformation_2d(mask, kernel_size = 7, operation_times = 5, diff_kernel = True, amplify_size = 256, threshold = 0.5):
    crop_mask, coordinate = crop_tumor(mask)
    cropped_mask = np.array(crop_mask)
    original_height = len(cropped_mask)
    original_width = len(cropped_mask[0])
    cropped_mask = skTrans.resize(cropped_mask ,(amplify_size, amplify_size), order=0, preserve_range=True)
    
    kernel = np.random.randint(0,2,(kernel_size,kernel_size))
    
    for i in range(0,operation_times):
        if i ==0:
            eroded = erosion(cropped_mask, kernel)
        else:
            eroded = erosion(eroded, kernel)
            
    if diff_kernel: kernel = np.random.randint(0,2,(kernel_size,kernel_size))
    
    for i in range(0,operation_times-1):
        if i ==0:
            dilated = dilation(eroded, kernel)
        else:
            dilated = dilation(dilated, kernel)
            
    result = skTrans.resize(dilated, (original_height,original_width), order=0, preserve_range=True)
    
    return to_one(result, threshold)

def random_erosion_and_dilation_deformation_3d(mask, save_path, kernel_size = 7, operation_times = 9, diff_kernel = True, amplify_size = 512, threshold = 0.3):


        slices_with_tumor = record_tumor_index_from_mask(mask)
        top,bottom,left,right = get_border_3D(mask)
        tmp_tumor = []
        # crop every slice
        for i in slices_with_tumor:
                tmp_tumor.append(mask[:,:,i][top:bottom, left:right])
        tmp_tumor = np.array(tmp_tumor)

        original_height = len(tmp_tumor)
        original_width = len(tmp_tumor[0])
        original_z = tmp_tumor[0][0].shape[0]
        tumor_array = np.expand_dims(np.random.randint(0,2,(original_height,original_width)),2)

        for index in range(original_z):
                
                cropped_mask = skTrans.resize(tmp_tumor[:,:,index] ,(amplify_size, amplify_size), order=0, preserve_range=True)

                kernel = np.random.randint(0,2,(kernel_size,kernel_size))
        
                for i in range(0,operation_times):
                        if i ==0:
                                eroded = erosion(cropped_mask, kernel)
                        else:
                                eroded = erosion(eroded, kernel)
                        
                if diff_kernel: kernel = np.random.randint(0,2,(kernel_size,kernel_size))
                
                for i in range(0,operation_times-1):
                        if i ==0:
                                dilated = dilation(eroded, kernel)
                        else:
                                dilated = dilation(dilated, kernel)
                        
                result = skTrans.resize(dilated, (original_height,original_width), order=0, preserve_range=True)
                
                result = to_one(result, threshold)
                
                tumor_array = np.dstack((tumor_array, result))

        cut = copy.copy(tumor_array[:,:,1:original_z+1]) 
        tmp_mask = copy.copy(mask)

        for i in range(len(slices_with_tumor)):
                tmp_mask[:,:,slices_with_tumor[i]][top:bottom, left:right] = cut[i]     
                
        print('---- Saving ----')
        arr2nii_and_save(tmp_mask, save_path)   
        

def compare_img_small_size(right, left):
    linecolor = 'red'
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].imshow(left, cmap = 'gray');
    ax[0].set_title('Before', fontsize = 19)
    ax[0].axvline(x = 13, color = linecolor)
    ax[0].axvline(x = 25, color = linecolor)
    ax[0].axhline(y = 13, color = linecolor)
    ax[0].axhline(y = 25, color = linecolor)
    ax[1].imshow(right, cmap = 'gray');
    ax[1].set_title('After', fontsize = 19)
    ax[1].axvline(x = 13, color = linecolor)
    ax[1].axvline(x = 25, color = linecolor)
    ax[1].axhline(y = 13, color = linecolor)
    ax[1].axhline(y = 25, color = linecolor)
    
    


def erosion_patch(patches, kernel_size, prob):
    tmp_erosion = copy.copy(patches)
    for patch in range(len(tmp_erosion)):
    
        random_num = np.random.random()

        if random_num > (1-prob):
            kernel = np.random.randint(0,2,(kernel_size,kernel_size))
            
            while np.sum(kernel) == 0: 
                kernel = np.random.randint(0,2,(kernel_size,kernel_size))
                
            eroded = erosion(patches[patch], kernel)

            tmp_erosion[patch] = eroded
            
        else:
            tmp_erosion[patch] = patches[patch]
            
    return tmp_erosion

def dilation_patch(patches, kernel_size, prob):
    tmp_dilated = copy.copy(patches)
    for patch in range(len(tmp_dilated)):
    
        random_num = np.random.random()

        if random_num > (1-prob):
            kernel = np.random.randint(0,2,(kernel_size,kernel_size))
            
            while np.sum(kernel) == 0: 
                kernel = np.random.randint(0,2,(kernel_size,kernel_size))
            
            dilated = dilation(patches[patch], kernel)

            tmp_dilated[patch] = dilated
            
        else:
            tmp_dilated[patch] = patches[patch]
            
    return tmp_dilated

def combine_patches(mask, patches, x_list, y_list):
    tmp_img = copy.copy(mask)
    cnt = 0
    tmp_x = 0
    tmp_y = 0
    
    for i in x_list:
        tmp_y = 0
        for j in y_list:
            # print(cnt)
            # print((np.array(tmp_img[tmp_x:tmp_x+i, tmp_y:tmp_y+j]).shape,'---',np.array(patches[cnt]).shape))
            # print(([tmp_x,tmp_x+i, tmp_y,tmp_y+j],'---',np.array(patches[cnt]).shape))
            tmp_img[tmp_x:tmp_x+i, tmp_y:tmp_y+j] = patches[cnt]
            
            cnt += 1
            tmp_y += j
        tmp_x += i
        
    return tmp_img


def spilt_cropped_into_patch_2D(mask, patch_size):

    img = mask
    x,y = img.shape
    x_q, x_r = divmod(x, patch_size)
    y_q, y_r = divmod(y, patch_size)

    x_list = [patch_size for i in range(x_q)]
    x_list[-1] += x_r

    y_list = [patch_size for i in range(y_q)]
    y_list[-1] += y_r
    
    patches = []
    tmp_x = 0
    tmp_y = 0
    for i in x_list:
        tmp_y = 0
        for j in y_list:
            patches.append(img[tmp_x:tmp_x+i, tmp_y:tmp_y+j])
            tmp_y += j
        tmp_x += i
    
    return patches, x_list, y_list

def patch_erosion_and_dilation_2D(mask, prob, num_iteration, padding, expand_size, patch_size, kernel_size):
    
    # Crop mask:
    top,bottom,left,right = get_border(mask, padding)
    if(top == 0 and bottom == 0):
        top = left
        bottom = right
    cropped_mask = np.array(mask[top:bottom, left:right])
    original_height,original_width = cropped_mask.shape
    # print('Border is:  ----  ',(top,bottom,left,right))
    # print('Cropped mask shape is:  ----  ',cropped_mask.shape)
    cropped_mask = skTrans.resize(cropped_mask, (expand_size, expand_size), order=0, preserve_range=True)  
    tmp_mask = copy.copy(cropped_mask)
    
    for i in range(num_iteration):
        
        # Stage-1: spilt -> erosion -> combine
        
        patches, x_list, y_list = spilt_cropped_into_patch_2D(tmp_mask, patch_size)
        eroded_patch = erosion_patch(patches, kernel_size, prob)
        combined = combine_patches(cropped_mask, eroded_patch, x_list, y_list)
        # combined = ndimage.binary_fill_holes(combined).astype(int) # fill holes
        
        # print('---------Iteration ', i ,'------------')
        
        # Stage-2: spilt -> dilation -> combine
        patches, x_list, y_list = spilt_cropped_into_patch_2D(combined, patch_size)
        dilated_patch = dilation_patch(patches, kernel_size, prob)
        combined = combine_patches(cropped_mask, dilated_patch, x_list, y_list)
        # combined = ndimage.binary_fill_holes(combined).astype(int) # fill holes
        
        tmp_mask = copy.copy(combined)
    
    # Put the cropped mask back to the image
    resized_back = skTrans.resize(tmp_mask, (original_height,original_width), order=0, preserve_range=True)
    threshold = np.round(np.random.uniform(0.2,0.7),2)
    result = to_one(resized_back, threshold)
    
    mask_ = copy.copy(mask)
    mask_[top:bottom, left:right] = result
    
    return mask_   

def patch_erosion_and_dilation_3D(mask, prob, num_iteration, padding, expand_size, patch_size, kernel_size, save_path):
    slices_with_tumor = record_tumor_index_from_mask(mask)
    x,y,z = mask.shape
    tmp_mask = copy.copy(mask)
    
    for i in range(len(slices_with_tumor)):
        mask_2d = tmp_mask[:,:,slices_with_tumor[i]]
        mask_result = patch_erosion_and_dilation_2D(mask_2d, prob, num_iteration, padding, expand_size, patch_size, kernel_size)
        
        tmp_mask[:,:,slices_with_tumor[i]] = mask_result
    
    print('Finished')
    arr2nii_and_save(tmp_mask, save_path)
    
def takeSecond(elem):
    return elem[1]

    
def grid_search(mask, probability, num_iteration, padding, expand_size, patch_size, kernel_size, save_path, mask_num, from_, to_):
    
    tmp_saver = []
    
    for prob in probability:
        for iteration in num_iteration:
            for expand in expand_size:
                for patch in patch_size:
                    for kernel in kernel_size:
                        attempt_result =  patch_erosion_and_dilation_2D(mask, prob, iteration, padding, expand, patch, kernel)
                        dice_score = dice_metric(mask, attempt_result)
                        
                        if dice_score <= to_ and dice_score >= from_:   # qualified mask
                            tmp_saver.append([attempt_result, dice_score])
                            
    tmp_saver.sort(key=takeSecond)
    qualified = []
    
    for i in reversed(tmp_saver):
        qualified.append(i[0])
        
        if(len(qualified) == mask_num):
            return qualified
    
    return qualified

    
def patch_erosion_and_dilation_3D_grid_search(mask_path, probability, num_iteration, padding, expand_size, patch_size, kernel_size, save_folder, mask_num, from_, to_):
    # dcm = dicom.read_file(mask_path, force=True)
    ptid = mask_path[-15:-7]
    mask = nib.load(mask_path).get_fdata()
    slices_with_tumor = record_tumor_index_from_mask(mask)

    tmp_mask_3d = [copy.copy(mask) for i in range(int(mask_num))]
    tmp_mask_2d = copy.copy(mask)

    for i in range(len(slices_with_tumor)-1):
        print('Start: ', i)

        mask_2d = tmp_mask_2d[:,:,slices_with_tumor[i]]
        
        
        # Grid search to generate many 2D mask, and return the best mask_num masks
        # Return mask_num (amount) masks
        qualified = grid_search(mask_2d, probability, num_iteration, padding, expand_size, patch_size, kernel_size, save_folder, mask_num, from_, to_)
        
        print('The length of candidates is: ',len(qualified))
        if len(qualified) >= mask_num:
            num_ = mask_num
        else:
            num_ = len(qualified)

        for j in range(num_):
            tmp_mask_3d[j][:,:,slices_with_tumor[i]] = qualified[j]
    
    save_path = os.path.join(save_folder, ptid)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
        print("Directory " , save_path ,  " Created ")
    else:    
        print("Directory " , save_path ,  " already exists")
        
    for i in range(mask_num):
        name = ptid+'_dummy'+str(i)+'.nii.gz'

        arr2nii_and_save(tmp_mask_3d[i], os.path.join(save_path, name))
        

def dice_metric(inputs, target):
    try:
        up = 2.0 * (target * inputs).sum()
    except:
        print('The size of two mask is different')
        
    down = target.sum() + inputs.sum()
    if target.sum() == 0 and inputs.sum() == 0:
        return 1.0

    return up / down   

def gogogo():
    print('Worked ! ')

def get_float_list(from_, to_, inter):
    from_ = np.round(from_,1)
    to_ = np.round(to_,1)
    elems = np.arange(from_, to_+0.01, inter)
    return elems

def get_int_list(from_, to_,inter):
    from_ = np.round(from_,1)
    to_ = np.round(to_,1)
    elems = np.arange(from_, to_+1, inter)
    return  list(map(int, elems)) 

def read_config2dict(file_path):

    with open(file_path, 'r') as stream:
        try:
            parsed_yaml = yaml.safe_load (stream)
            # print (parsed_yaml)
        except yaml.YAMLError as exc:
            print(exc)

    return parsed_yaml

def find_tumor_index(mask_array):
    index = 0
    x,y,z = mask_array.shape

    for i in range(z):
        if np.sum(mask_array[:,:,i]) != 0:
            index = i
            break

    return index

if __name__ == "__main__":
    # config_folder = '../config'
    # config_name = 'config1.yml'
    # yaml_save_path = os.path.join(config_folder, config_name)

    # test_dict = read_config2dict(yaml_save_path)

    # print(test_dict['probability_from'])
    # mask_path = '../Mask_folder'
    # mask_list = clean_list(os.listdir(mask_path)) # remove DS.Store
    

    # path = os.path.join(mask_path, mask_list[0])
    # print(path[-15:-7])

    # dcm = dicom.read_file(path, force=True)
    
    # image_input_path = '../masks/BBox4Tumor_PreT_Label_10099473.nii.gz'
    # mask = nib.load(image_input_path).get_fdata()
    # x,y,z = mask.shape
    # # print(mask[:,:,0].shape)
    # print(find_tumor_index(mask))


    dummy_list = clean_list(os.listdir('../outputs/first'))
    print(dummy_list)
    
    # print(dcm)
# required package
import os
import copy
import pandas as pd
import re
import argparse
import cc3d
import cv2
from os import listdir
from os.path import isfile, join, exists
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.morphology import binary_fill_holes



EROSION_KERNEL_SIZE = 9
EPSILON = 0.0000001

class FCM():
    def __init__(self, image, image_bit, n_clusters, m, epsilon, max_iter):
        '''Modified Fuzzy C-means clustering

        <image>: 2D array, grey scale image.
        <n_clusters>: int, number of clusters/segments to create.
        <m>: float > 1, fuzziness parameter. A large <m> results in smaller
             membership values and fuzzier clusters. Commonly set to 2.
        <max_iter>: int, max number of iterations.
        '''

        #-------------------Check inputs-------------------
        if np.ndim(image) != 2:
            raise Exception("<image> needs to be 2D (gray scale image).")
        if n_clusters <= 0 or n_clusters != int(n_clusters):
            raise Exception("<n_clusters> needs to be positive integer.")
        if m < 1:
            raise Exception("<m> needs to be >= 1.")
        if epsilon <= 0:
            raise Exception("<epsilon> needs to be > 0")

        self.image = image
        self.image_bit = image_bit
        self.n_clusters = n_clusters
        self.m = m
        self.epsilon = epsilon
        self.max_iter = max_iter

        self.shape = image.shape # image shape
        self.X = image.flatten().astype('float') # flatted image shape: (number of pixels,1) 
        self.numPixels = image.size
       
    #--------------------------------------------- 
    def initial_U(self):
        U=np.zeros((self.numPixels, self.n_clusters))
        idx = np.arange(self.numPixels)
        # U[0:int(self.numPixels/3),0]=1
        # U[int(self.numPixels/3):int(self.numPixels/3)*2,1]=1
        # U[int(self.numPixels/3)*2:self.numPixels,2]=1
        for ii in range(self.n_clusters):
            idxii = idx%self.n_clusters==ii
            U[idxii,ii] = 1        
        return U
    
    def update_U(self):
        '''Compute weights'''
        c_mesh,idx_mesh = np.meshgrid(self.C,self.X)
        power = 2./(self.m-1)
        p1 = abs(idx_mesh-c_mesh)**power
        p2 = np.sum((1./(abs(idx_mesh-c_mesh)+ EPSILON)**power),axis=1)
        
        return 1./(p1*p2[:,None] + EPSILON)

    def update_C(self):
        '''Compute centroid of clusters'''
        numerator = np.dot(self.X,self.U**self.m)
        denominator = np.sum(self.U**self.m,axis=0)
        return numerator/denominator
                       
    def form_clusters(self):      
        '''Iterative training'''        
        d = 100
        self.U = self.initial_U()
        if self.max_iter != -1:
            i = 0
            while True:             
                self.C = self.update_C()
                old_u = np.copy(self.U)
                self.U = self.update_U()
                d = np.sum(abs(self.U - old_u))
                # print("Iteration %d : cost = %f" %(i, d))

                if d < self.epsilon or i > self.max_iter:
                    break
                i+=1
        else:
            i = 0
            while d > self.epsilon:
                self.C = self.update_C()
                old_u = np.copy(self.U)
                self.U = self.update_U()
                d = np.sum(abs(self.U - old_u))
                # print("Iteration %d : cost = %f" %(i, d))

                if d < self.epsilon or i > self.max_iter:
                    break
                i+=1
        self.segmentImage()


    def deFuzzify(self):
        return np.argmax(self.U, axis = 1)

    def segmentImage(self):
        '''Segment image based on max weights'''

        result = self.deFuzzify()
        self.result = result.reshape(self.shape).astype('int')

        return self.result 
class ARGS():

    def get_args(self):
        # =================FCM parameter=================
        parser = argparse.ArgumentParser(description="Tissue Segmentation Using Modified Fuzzy C-Means Algorithm on Mammography.")
        #-----------------Algorithm-----------------
        parser.add_argument('-a', '--algorithm', default='FCM', choices=['FCM', 'EnFCM', 'MFCM'], type=str,
                            help="Choose a fuzzy c-means clustering algorithm. (FCM, EnFCM, MFCM)")
        parser.add_argument('--num_bit', default=16, type=int,
                            help="number of bits of input images")
        #-----------------Fundamental parameters-----------------
        parser.add_argument('-c', '--num_cluster', default='3', type=int,
                            help="Number of cluster")
        parser.add_argument('-m', '--fuzziness', default='2', type=int,
                            help="fuzziness degree")
        parser.add_argument('-i', '--max_iteration', default='100', type=int,
                            help="max number of iterations.")
        parser.add_argument('-e', '--epsilon', default='0.05', type=float,
                            help="threshold to check convergence.")
        #-----------------User parameters-----------------
        parser.add_argument('--plot_show', default=1, choices=[0,1],
                            help="Show plot about result")
        parser.add_argument('--plot_save', default=1, choices=[0,1],
                            help="Save plot about result")
        #-----------------Parametesr for MFCM/EnFCM-----------------
        parser.add_argument('-w', '--win_size', default='5', type=int,
                            help="Window size of MFCM/EnFCM algorithm")
        parser.add_argument('-n', '--neighbour_effect', default='3', type=float,
                            help="Effect factor of the graylevel which controls the influence extent of neighbouring pixels.")
        parser.add_argument('-s', '--save_type', default='png', choices=['png', 'nii'], type=str,
                            help="the saved type of output image")
        parser.add_argument('-r', '--runipynb', default='go', type=str)
            
        return parser.parse_args(['--runipynb','go'])


class BPE_functions():

    def __init__(self, Root_Unenhances_Dirs, Root_Enhanced_Dirs, 
    Origin_Breast_Mask_Dirs, LESION_INFO_CSV_PATH, FCM_OUTPUT_DIR, 
    BPE_OUTPUT_DIR,CSV_file_name, Patient_list,ARGS):
        
        self.Root_Unenhances_Dirs = Root_Unenhances_Dirs
        self.Root_Enhanced_Dirs = Root_Enhanced_Dirs
        self.Origin_Breast_Mask_Dirs = Origin_Breast_Mask_Dirs
        self.LESION_INFO_CSV_PATH = LESION_INFO_CSV_PATH
        self.FCM_OUTPUT_DIR = FCM_OUTPUT_DIR
        self.BPE_OUTPUT_DIR = BPE_OUTPUT_DIR
        self.CSV_file_name = CSV_file_name
        self.Patient_list = Patient_list
        self.ARGS = ARGS
        self.IS_SAVE = ARGS.plot_save
        self.IS_PLOT = ARGS.plot_show
        self.EPSILON = 0.0000001
        self.EROSION_KERNEL_SIZE = 9
        self.LI_DF = pd.read_csv(self.LESION_INFO_CSV_PATH, index_col='ID')

    # =================Function=================
    def makedirs(self,path):
        if not exists(path):
            # print(" [*] Make directories : {}".format(path))
            os.makedirs(path)
        return path

    # ZW new resample function based one spacingbetweenslices
    def resample_image(self,itk_image, thick, out_spacing=[1.0,1.0,1.0]):
        #slice_thickness =
        resamplemethod = sitk.sitkBSpline

        print('--Image resampling to [1mm,1mm,1mm]--')
        resampler = sitk.ResampleImageFilter()
        originSize = itk_image.GetSize()  # 原来的体素块尺寸
        originSpacing = itk_image.GetSpacing()

        original_spacing = itk_image.GetSpacing()
        thick = np.float32(thick)
        # print("original spacing is：", original_spacing[0], original_spacing[1], thick, "\nprocessed spacing is:",
        #       out_spacing)
        original_size = itk_image.GetSize()

        # 根据输出out_spacing设置新的size
        out_size = [
            int(np.round(original_size[0] * original_spacing[0] / out_spacing[0])),
            int(np.round(original_size[1] * original_spacing[1] / out_spacing[1])),
            int(np.round(original_size[2] * thick / out_spacing[2]))
            # int(np.round(original_size[2] * original_spacing[2] / out_spacing[2])),
        ]

        newSize = np.array(out_size, float)
        factor = originSize / newSize
        newSpacing = originSpacing * factor
        newSize = newSize.astype(np.int16)  # spacing肯定不能是整数

        resampler.SetReferenceImage(itk_image)  # 需要重新采样的目标图像
        resampler.SetSize(newSize.tolist())
        resampler.SetOutputSpacing(newSpacing.tolist())
        resampler.SetTransform(sitk.Transform(3, sitk.sitkIdentity))
        resampler.SetInterpolator(resamplemethod)
        itk_img_res = resampler.Execute(itk_image)  # 得到重新采样后的图像
        print('--Image resampling Done--')
        return itk_img_res

    def resample_image(self,itk_image, thick, out_spacing=[1.0,1.0,1.0]):
        #slice_thickness =
        resamplemethod = sitk.sitkBSpline

        print('--Image resampling to [1mm,1mm,1mm]--')
        resampler = sitk.ResampleImageFilter()
        originSize = itk_image.GetSize()  # 原来的体素块尺寸
        originSpacing = itk_image.GetSpacing()

        original_spacing = itk_image.GetSpacing()
        thick = np.float32(thick)
        # print("original spacing is：", original_spacing[0], original_spacing[1], thick, "\nprocessed spacing is:",
        #       out_spacing)
        original_size = itk_image.GetSize()

        # 根据输出out_spacing设置新的size
        out_size = [
            int(np.round(original_size[0] * original_spacing[0] / out_spacing[0])),
            int(np.round(original_size[1] * original_spacing[1] / out_spacing[1])),
            int(np.round(original_size[2] * thick / out_spacing[2]))
            # int(np.round(original_size[2] * original_spacing[2] / out_spacing[2])),
        ]

        newSize = np.array(out_size, float)
        factor = originSize / newSize
        newSpacing = originSpacing * factor
        newSize = newSize.astype(np.int16)  # spacing肯定不能是整数

        resampler.SetReferenceImage(itk_image)  # 需要重新采样的目标图像
        resampler.SetSize(newSize.tolist())
        resampler.SetOutputSpacing(newSpacing.tolist())
        resampler.SetTransform(sitk.Transform(3, sitk.sitkIdentity))
        resampler.SetInterpolator(resamplemethod)
        itk_img_res = resampler.Execute(itk_image)  # 得到重新采样后的图像
        print('--Image resampling Done--')
        return itk_img_res

    def read_dcm(self,filepath):
        series_reader = sitk.ImageSeriesReader()
        series_files_path = series_reader.GetGDCMSeriesFileNames(filepath)
        series_reader.SetFileNames(series_files_path)
        images = series_reader.Execute() 
        
        file_reader = sitk.ImageFileReader()
        file_reader.SetFileName(series_files_path[6])
        file_reader.ReadImageInformation()
        
        thick = file_reader.GetMetaData("0018|0050")
        manufacturer = file_reader.GetMetaData("0008|0070") if file_reader.HasMetaDataKey("0008|0070") else "unknown"

        images = self.resample_image(images,thick)
        dcm_3d_array = sitk.GetArrayFromImage(images)
        
        if bool(re.match('GE', manufacturer, re.IGNORECASE)):
            dcm_3d_array = dcm_3d_array[:, ::-1][:, :, ::-1]
        
        return dcm_3d_array, manufacturer

    #-----------------read breast mask and erosion-----------------
    def erosion_process(self,mask_path, kernel_size, manufacturer, iter=1):
        image = sitk.ReadImage(mask_path)
        # image = resample_image(image, thick=thick)
        nparr = sitk.GetArrayFromImage(image)
        
        if bool(re.match('GE', manufacturer, re.IGNORECASE)):
            nparr = nparr[:, ::-1][:, :, ::-1]
        
        d, w, h = nparr.shape
        erode_nparr = np.zeros((d, w, h))
        slice_ = np.zeros((w, h))
        kernel_ = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        # kernel_ = np.ones((kernel_size, kernel_size), np.uint8)
        
        for i in range(d):
            slice_ = nparr[i, :, :]
            erosion = cv2.erode(slice_, kernel_, iterations=iter)
            erosion = binary_fill_holes(erosion)
            erode_nparr[i, : , :] = erosion
            
        erode_nparr = np.int16(erode_nparr)
        erode_nparr = cc3d.connected_components(erode_nparr)
        
        return erode_nparr

    def get_breast_box(self,mask_array):
        mask_voxel_coords = np.where(mask_array)
        minzidx = int(np.min(mask_voxel_coords[0]))
        maxzidx = int(np.max(mask_voxel_coords[0])) + 1
        minxidx = int(np.min(mask_voxel_coords[1]))
        maxxidx = int(np.max(mask_voxel_coords[1])) + 1
        bbox = [[minzidx, maxzidx], [minxidx, maxxidx]]
        resizer = (slice(bbox[0][0], bbox[0][1]), slice(bbox[1][0], bbox[1][1]))
        return resizer

    # ----------------------
    def get_result(self,img_arr, args):
        # --------------Clustering--------------  
        cluster = FCM(img_arr, image_bit=args.num_bit, n_clusters=args.num_cluster, m=args.fuzziness, epsilon=args.epsilon, max_iter=args.max_iteration)
        cluster.form_clusters()
        result=cluster.result
        
        # --------------Pixel value standardizing--------------
        Ap_mask = copy.deepcopy(result)
        Bp_mask = copy.deepcopy(result)
        Cp_mask = copy.deepcopy(result)
        
        Ap_mask[Ap_mask != 0] = 1
        Ap_mask = 1 - Ap_mask

        Bp_mask[Bp_mask != 1] = 0

        Cp_mask[Cp_mask != 2] = 0
        Cp_mask[Cp_mask == 2] = 1
        
        Apart = img_arr * Ap_mask
        Bpart = img_arr * Bp_mask
        Cpart = img_arr * Cp_mask
        
        
        part_tuple = [
            [Ap_mask, Apart],
            [Bp_mask, Bpart],
            [Cp_mask, Cpart]
        ]
        
        background_, fat_, gland_ = sorted(part_tuple, key=lambda part_: part_[1].sum() / (part_[1][part_[1]>0].size + self.EPSILON))

        final_mask = gland_[0]   

        return final_mask

    def img_plot_show(self,img, result, LoR):
        if self.IS_PLOT:      
            
            fig=plt.figure(figsize=(12,8),dpi=100)
        
            ax1=fig.add_subplot(1,2,1)
            ax1.imshow(img,cmap='gray')
            ax1.set_title('image : %s part'%(LoR))
        
            ax2=fig.add_subplot(1,2,2)
            ax2.imshow(result)
            ax2.set_title('args: ' + 'num_cluster=' + str(self.ARGS.num_cluster) + ',fuzziness=' + str(self.ARGS.fuzziness))
            
            plt.show(block=False)
            plt.close()
            
    def get_mask_plot(self,result, patient_id):
        if self.IS_SAVE:
            PLot_output_dir = join(self.FCM_OUTPUT_DIR, 'Method_%s'%(self.ARGS.algorithm))
            self.makedirs(PLot_output_dir)
            seg_result_path = join(PLot_output_dir,"Mammary_Glands_Mask_%s.nii.gz"%(patient_id))
            sitk.WriteImage(sitk.GetImageFromArray(result), seg_result_path)
            
    def FCM_process(self,img_nparr, origin_shape, box_size):
        fcm_result = self.get_result(img_nparr, self.ARGS)
        entry_mask = np.zeros(origin_shape, dtype=np.int16)
        entry_mask[box_size] = fcm_result
        return entry_mask
            
    # =================BPE Function=================
    # BPE calculation formula 1: voxel by voxel
    def get_VbV_BPE(self,PE, gland_size):
        avg_bpe = PE / gland_size
        return round(avg_bpe, 7)

    # BPE calculation formula 2: mean intensition subtraction
    def get_MI_BPE(self,UnE_Gland, E_Gland, gland_size):
        UnE_Gland_Intensities = UnE_Gland.sum() / gland_size
        E_Gland_Intensities = E_Gland.sum() / gland_size
        
        Mean_Intensities_BPE = (E_Gland_Intensities - UnE_Gland_Intensities) / UnE_Gland_Intensities 
        return round(Mean_Intensities_BPE, 7)

    # Calculate 95% CI of all intensities to remove outliers
    def get_m95p_mask(self,ori_gland, ori_mask):
        gland = copy.deepcopy(ori_gland)
        gland_ = gland[ori_mask == 1]
        gland_.sort()
        index_ = gland_.size
        p2_5 = gland_[int(index_*0.025)-1]
        p97_5 = gland_[int(index_*0.975)-1]
        gland[gland<p2_5] = 0
        gland[gland>p97_5] = 0   
        gland[gland>0] = 1    
        return gland

    # Calculate Parenchyma Enhancement (PE)
    def get_PE(self,UnE_Gland, E_Gland):
        voxel_PE = (E_Gland - UnE_Gland) / (UnE_Gland)
        
        voxel_PE[voxel_PE<0.1] = 0
        
        return voxel_PE

    # Calculate the volume of PE
    def get_BPE_volume(self,BPE, p_list):
        v_list = []
        for p in p_list:
            v = BPE[BPE>p].size
            v_list.append(v)
        
        return v_list

    #????
    def get_glands_value(self,lg, rg, bg_mask):
        lm, rm = np.array_split(bg_mask, 2, axis=2)
        lv = lg[lm == 1]
        rv = rg[rm == 1]
        return lv, rv



    def start_cal(self, bpe):

        Patient_BPE_Result_List = []

        for patient_ID in self.Patient_list:
            print('Patient ID : [%s]'%(patient_ID))
            patient_BPE_info = [patient_ID]
            patient_right_BPE_info = []
            patient_left_BPE_info = []
            '''
                1. Data Preprocess
            '''
            print('Start preprocessing ...')
            # -------------read dicom file-------------
            dcm_3d_nparr, manufacturer = self.read_dcm(join(self.Root_Unenhances_Dirs, patient_ID))
            dcm_3d_nparr = dcm_3d_nparr.astype(np.int16)
            print(f'The Manufacturer is {manufacturer}')
            
            # -------------get eroded origin mask-------------
            origin_mask_filename = 'breast_' + patient_ID + '.nii.gz'
            origin_mask_path = join(self.Origin_Breast_Mask_Dirs, origin_mask_filename)    
            eroded_mask_nparr = self.erosion_process(origin_mask_path, EROSION_KERNEL_SIZE, manufacturer=manufacturer).astype(np.int16)
            eroded_mask_nparr[eroded_mask_nparr > 1] = 1
            
            # -------------get breast region using mask -------------
            breast_region_3d_nparr = dcm_3d_nparr * eroded_mask_nparr
            print('Preprocessing Done')
            
            # -------------get health side-------------
            
            # ========================================= #
            '''
                2. FCM Process
            '''   
            
            print('Start FCM Processing ...')
            
            # -------------slices iterative processing-------------
            Slice_result_list = []
            for slice_2d in breast_region_3d_nparr:
                left_breast_2d_nparr, right_breast_2d_nparr = np.array_split(slice_2d, 2, axis=1)
                left_shape = left_breast_2d_nparr.shape
                right_shape = right_breast_2d_nparr.shape
                
                if left_breast_2d_nparr.sum() != 0:
                    left_box_size = self.get_breast_box(left_breast_2d_nparr)
                    left_box_region = left_breast_2d_nparr[left_box_size]
                    left_part_2d_result = self.FCM_process(left_box_region, left_shape, left_box_size)
                else:
                    left_part_2d_result = left_breast_2d_nparr
                    
                if right_breast_2d_nparr.sum() != 0:
                    right_box_size = self.get_breast_box(right_breast_2d_nparr)
                    right_box_region = right_breast_2d_nparr[right_box_size]
                    right_part_2d_result = self.FCM_process(right_box_region, right_shape, right_box_size)
                else:
                    right_part_2d_result = right_breast_2d_nparr
                    
                Slice_result = np.hstack((left_part_2d_result, right_part_2d_result))
                Slice_result_list.append(Slice_result)
                pass
                
                # -------------get current patient mammary glands mask-------------
            FCM_3d_mask_result = np.stack(Slice_result_list, axis=0)
            
            # -------------save current patient mammary glands mask-------------
            self.get_mask_plot(FCM_3d_mask_result, patient_ID)
            
            print('Glands Segmentation Done!')
            print('-------------------------------------------------------------------')

            if bpe:
                '''
                3. BPE 
                '''     
                print('Start BPE Calculation ...')
                # -------------read unehanced dcm -------------
                Unenhanced_dcm_nparr = dcm_3d_nparr
                # -------------read ehanced dcm -------------
                Enhanced_dcm_nparr, _ = self.read_dcm(join(self.Root_Enhanced_Dirs, patient_ID))
                Enhanced_dcm_nparr = Enhanced_dcm_nparr.astype(np.int16)
                # -------------read mammary glands mask-------------
                MG_mask_nparr = FCM_3d_mask_result
                MG_mask_nparr[MG_mask_nparr>0] = 1
                
                # -------------get mid 50% mammary glands mask-------------
                MG_mask_nparr[:int(MG_mask_nparr.shape[0]/4), :, :] = 0
                MG_mask_nparr[int(MG_mask_nparr.shape[0]/4*3):, :, :] = 0
                
                # -------------get origin mammary glands-------------
                origin_UnE_gland  = Unenhanced_dcm_nparr * MG_mask_nparr
                E_gland = Enhanced_dcm_nparr * MG_mask_nparr
                
                # -------------get mid 95% value gland mask (unenhanced)-------------
                m95p_UnE_gland_mask  = self.get_m95p_mask(origin_UnE_gland, MG_mask_nparr)
                UnE_gland = Unenhanced_dcm_nparr * m95p_UnE_gland_mask
                
                # -------------left and right part glands-------------
                UnE_right_gland, UnE_left_gland = np.array_split(UnE_gland, 2, axis=2)
                E_right_gland, E_left_gland = np.array_split(E_gland, 2, axis=2)
                
                # -------------glands flatten-------------
                UnE_right_value, UnE_left_value =self.get_glands_value(UnE_right_gland, UnE_left_gland, m95p_UnE_gland_mask)
                E_right_value, E_left_value = self.get_glands_value(E_right_gland, E_left_gland, m95p_UnE_gland_mask)
                
                # -------------get gland volume-------------
                right_gland_size = m95p_UnE_gland_mask[:, :, :int(m95p_UnE_gland_mask.shape[2]/2)].sum()
                left_gland_size = m95p_UnE_gland_mask[:, :, int(m95p_UnE_gland_mask.shape[2]/2):].sum()
                
                # -------------get PE and Voxel by Voxel BPE result-------------
                E_left_value_copy = copy.deepcopy(E_left_value)
                E_right_value_copy = copy.deepcopy(E_right_value)

                right_PE = self.get_PE(UnE_right_value, E_right_value_copy)
                left_PE = self.get_PE(UnE_left_value, E_left_value_copy)
                
                right_side_VbVBPE = self.get_VbV_BPE(right_PE.sum(), right_gland_size)
                left_side_VbVBPE = self.get_VbV_BPE(left_PE.sum(), left_gland_size)
                
                patient_right_BPE_info.append(right_side_VbVBPE)
                patient_left_BPE_info.append(left_side_VbVBPE)
                
                # -------------get Voxel by Voxel BPE volume-------------
                
                BPE_volume_right_list = self.get_BPE_volume(right_PE, [0.1, 0.25, 0.5, 0.75])
                BPE_volume_left_list = self.get_BPE_volume(left_PE, [0.1, 0.25, 0.5, 0.75])
                
                patient_right_BPE_info.extend(BPE_volume_right_list)
                patient_left_BPE_info.extend(BPE_volume_left_list)
                
                # -------------get health side label and result-------------
                if self.LI_DF['lesion_side'][int(patient_ID)] == 'R':
                    pass
                
                # -------------append Patient_BPE_Result-------------
                patient_BPE_info.extend(patient_right_BPE_info)
                patient_BPE_info.extend(patient_left_BPE_info)
                
                # -------------get health side label and result-------------
                if self.LI_DF['lesion_side'][int(patient_ID)] == 'R':
                    patient_BPE_info.extend(['Left', left_side_VbVBPE])
                    patient_BPE_info.extend(BPE_volume_left_list)
                elif self.LI_DF['lesion_side'][int(patient_ID)] == 'L':
                    patient_BPE_info.extend(['Right', right_side_VbVBPE])
                    patient_BPE_info.extend(BPE_volume_right_list)
                    pass
                
                Patient_BPE_Result_List.append(patient_BPE_info)
                
                print('BPE Calculation Done!')
                print(f'# ====================={patient_ID} DONE! ====================== #')
                        
                # ===============export results in a csv ===============

                columns_set = ['Patient_ID', 'Right_Side_VbVBPE', 'R10perBPE_Volume', 'R25perBPE_Volume', 'R50perBPE_Volume', 'R75perBPE_Volume', 
                            'Left_Side_VbVBPE', 'L10perBPE_Volume', 'L25perBPE_Volume', 'L50perBPE_Volume', 'L75perBPE_Volume', 'Health_Side',
                            'Health_Side_VbVBPE', 'H10perBPE_Volume', 'H25perBPE_Volume', 'H50perBPE_Volume', 'H75perBPE_Volume']

                dt = pd.DataFrame(Patient_BPE_Result_List, columns=columns_set)
                dt.to_csv(join(self.BPE_OUTPUT_DIR, self.CSV_file_name), index=0)
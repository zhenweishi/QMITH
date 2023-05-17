'''
# -*- coding: utf-8 -*-
@author: Tianchen Luo: ltc8498@qq.com
'''
import os
import shutil
import glob
import pydicom as dicom



class Functions():

    def __init__(self,root_dir):
        self.root_dir = root_dir

     
    
    '''
    files   : list[] contains path in MacOS system
    return  : list[] without  '.DS_Store' file
    '''
    def clean_list(self,files):
        tmp = files.copy()
        for i in range(len(files)):
            if files[i] == '.DS_Store':
                tmp.pop(i)

        return tmp

    # 批量获取病人数据中的dcm用做病人信息展示
    '''
    root_dir  : directory that store patients' data
    return    : ramdom single .dcm file from every patient in order to collect metadata
    '''
    def batch_collect_patients_info(self,root_dir):

        dcm_list = []
        itk_list = [] # 当需要用到ITK时，可以在这个func里面添加一个return val

        patients = self.clean_list(os.listdir(root_dir))
        for patient in patients:
            patient_path = os.path.join(root_dir, patient)
            for root, subdirs, files in os.walk(patient_path):
                for filename in files:    
                    file_path = os.path.join(root, filename)
                    if(file_path.endswith(".nii") or file_path.endswith(".nii.gz")):
                        itk_list.append(file_path)

                    if(file_path.endswith(".dcm") or file_path.endswith(".DCM")):
                        #print(file_path)
                        dcm_list.append(file_path)
                        break
        return dcm_list

    '''
    root_dir   : directory that store patients' data
    return     : list with all patient's directory path
    '''
    def get_patients(self, root_dir):
        val = []
        patients = self.clean_list(os.listdir(root_dir))
        for patient in patients:
            val.append(os.path.join(root_dir, patient))
        return val

     
    '''
    patient_path : image path (end with .dcm files) 
    return       : patient's ID 
    '''
    def get_patientsID(self, patient_path):
        
        for root, subdirs, files in os.walk(patient_path):
            for filename in files: 
                file_path = os.path.join(patient_path, filename)
                if(file_path.endswith(".dcm") or file_path.endswith(".DCM")):
                    dcm = dicom.read_file(file_path, force=True)
                    try:    
                        id = dcm.PatientID
                        return id
                    except:
                        print('No Patient ID')


    '''
    path      : any abs path
    return    : the pure file name from the abs path
    '''
    def get_files_name(self, path):
        return os.path.split(path)[1]            
    
    '''
    ITKWorkingDir : ITK(mask) temp working directory
    return        : list[] with abs path
    '''
    def get_ITKList(self, ITKWorkingDir):
        val = []
        for root, subdirs, files in os.walk(ITKWorkingDir):
            clean_list =  self.clean_list(files)
            for file in clean_list:
                val.append(os.path.join(ITKWorkingDir, file))
        return val


                
                        


    def move_CTScans(self,patient_path,CTWorkingDir,ITKWorkingDir):
        
        # Clean all before moving
        ct_files = glob.glob(os.path.join(CTWorkingDir,'*'))
        itk_files = glob.glob(os.path.join(ITKWorkingDir,'*'))
        for f in ct_files:
            os.remove(f)
        for f in itk_files:
            os.remove(f)

        print('Moving')
        try:
            for root, subdirs, files in os.walk(patient_path):
                for filename in files:    
                    file_path = os.path.join(root, filename)

                    if(file_path.endswith(".nii")):
                        name, extension = os.path.splitext(filename)
                        shutil.copy2(file_path,os.path.join(ITKWorkingDir,name+".nii")) 

                    if(file_path.endswith(".nii.gz")):
                        name, extension = os.path.splitext(filename)
                        shutil.copy2(file_path,os.path.join(CTWorkingDir,name+".nii.gz")) 
                        
                    if(file_path.endswith(".dcm") or file_path.endswith(".DCM")):
                        name, extension = os.path.splitext(filename)
                        if name != 'VERSION':
                            shutil.copy2(file_path,os.path.join(CTWorkingDir,name+".dcm"))  
        except:
            print("Can't move data to temp working dirs, something wrong with data storage") 
        
    def count_files_amount(self,path,type):
        dirname = os.path.abspath(os.path.dirname(path))
        cnt = 0
        for root, subdirs, files in os.walk(dirname):
            for file in files:
                if(file.endswith(type)):
                    cnt += 1
        print(cnt)
        return cnt

    

    def get_patients_info(self, path_list):

        debug = False
        patientId =[]
        sex =[]
        modality =[]
        studyDate =[]
        studyDescription =[]
        count =[]
        size = []
        warning_info = []

        for index in range(len(path_list)):

            dcm = dicom.read_file(path_list[index], force=True)

            try:
                modality_ = (dcm.Modality)
            except:
                modality_ = 'Unknown'
                warning_info.append("FileDataset object has no attribute 'Modality' ")
                print("FileDataset object has no attribute 'Modality' ") 

            try:
                patid = (dcm.PatientID)
                
            except:
                patid = 'Unknown'
                warning_info.append("FileDataset object has no attribute 'Patient ID' ")
                print("FileDataset object has no attribute 'Patient ID' ")

            try:
                studydate = (dcm.StudyDate)
    
            except:
                studydate = 'Unknown'
                warning_info.append("FileDataset object has no attribute 'Study Date' ")
                print("FileDataset object has no attribute 'Study Date' ")  

            try:
                sex_ = dcm.Sex
            except:
                sex_ = 'Unknown'
                warning_info.append("FileDataset object has no attribute 'Sex' ")
                print("FileDataset object has no attribute 'Sex' ")    

            try:
                description = dcm.BodyPartExamined
            except:
                description = 'Unknown'
                warning_info.append("FileDataset object has no attribute 'BodyPartExamined' ")
                print("FileDataset object has no attribute 'BodyPartExamined' ")  

            try:
                row = dcm.Rows
                col = dcm.Columns
            except:
                row = 'Unknown'
                col = 'Unknown'
                warning_info.append("FileDataset object has no attribute 'Rows and Columns' ")
                print("FileDataset object has no attribute 'Rows and Columns' ") 
            
            # append dcm image数量
            count.append(self.count_files_amount(path_list[index], ".dcm"))
            modality.append(modality_)
            sex.append(sex_)
            patientId.append(patid)
            studyDate.append(studydate)
            studyDescription.append(description)
            size.append(str(row) + 'x'+ str(col))

        if debug: 
            print(count)
            print(modality)
            print(sex)
            print(patientId)
            print(studyDate)
            print(studyDescription)
            print(size)

        return patientId, sex, modality, studyDate, studyDescription, count, size, warning_info

if __name__ == "__main__":
    file_path = '../Data'
    fc = Functions(file_path)
    # patients_dcm_path = fc.batch_collect_patients_info(file_path)
    # #fc.count_files_amount(patients_dcm_path[2],".dcm")
    # #fc.get_patients_info(patients_dcm_path)
    # fc.move_CTScans('../Data/Lung1/VOPQD0NP','../tmp_CTFolder','../tmp_ITKFolder')

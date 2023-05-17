'''
# -*- coding: utf-8 -*-
@author: Tianchen Luo: ltc8498@gmail.com

'''
import tkinter as tk
import SimpleITK as sitk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from PIL import Image, ImageTk
import os
import numpy as np
from tkinter import filedialog
from tkinter import font as tkFont
from subprocess import call
import pandas
import GUI_Main as main
from GUI_Functions import Functions
from GUI_BPEFUNCTION import FCM, BPE_functions, ARGS
# import radiomics
# from radiomics import featureextractor
import logging


class Radiomics(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f0efeb', width=1600, height=680)
        self.controller = controller
        self.controller.title('MetaMedAI')
        self.controller.state('normal')
        self.columnconfigure(0, minsize=500, weight=1)
        self.columnconfigure(1, minsize=500, weight=1)
        self.rowconfigure(0, minsize=650, weight=1)
        self.rowconfigure((0, 10), minsize=40, weight=1)
        self.columnconfigure([0, 1, 2, 3, 4], minsize=60, weight=1)
        # -------------- 在这里设置左边的文字 -----------------
        btn_txt1 = '待定'
        btn_txt2 = '待定'
        btn_txt3 = '待定'
        btn_txt4 = '待定'
        btn_txt5 = '待定'
        radio_btn_txt1 = '     待定'
        radio_btn_txt2 = '     待定'
        label_txt1 = '待定'
        label_txt2 = '待定'
        default_input1 = r'../data/testcase/Pre_Treatment/'
        default_input2 = r'../data/testcase/PreT_Breast_Mask'
        default_input3 = r'../metadata/info.csv'
        default_output1 = r'../output/Glands_mask'
        default_output2 = r'../output/'



        def rad_main():
            # User parameter setting
            ########
            outPath = '../output/RF'
            CaseTablePath = '../casetable/'
            CasetableFile = 'CaseTable_test_CT.csv'
            outputFile = 'MMA_RadiomicsTable.csv' 
            SettingFile = 'exampleCT.yaml'
            ########

            inputCSV = os.path.join(CaseTablePath,CasetableFile)
            outputFilepath = os.path.join(outPath, outputFile)
            params = os.path.join('../Radiomics_Settings', SettingFile)

            progress_filename = os.path.join(outPath,'./pyrad_log.txt') # save processing log info

            # Configure logging
            rLogger = logging.getLogger('radiomics')

            # Set logging level
            # rLogger.setLevel(logging.INFO)  # Not needed, default log level of logger is INFO

            # Create handler for writing to log file
            handler = logging.FileHandler(filename=progress_filename, mode='w')
            handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
            rLogger.addHandler(handler)

            # Initialize logging for batch log messages
            logger = rLogger.getChild('batch')

            # Set verbosity level for output to stderr (default level = WARNING)
            radiomics.setVerbosity(logging.INFO)

            logger.info('pyradiomics version: %s', radiomics.__version__)
            logger.info('Loading CSV')

            # ####### Up to this point, this script is equal to the 'regular' batchprocessing script ########

            try:
                # Use pandas to read and transpose ('.T') the input data
                # The transposition is needed so that each column represents one test case. This is easier for iteration over
                # the input cases
                flists = pandas.read_csv(inputCSV).T
            except Exception:
                logger.error('CSV READ FAILED', exc_info=True)
                exit(-1)

            logger.info('Loading Done')
            logger.info('Patients: %d', len(flists.columns))

            if os.path.isfile(params):
                extractor = featureextractor.RadiomicsFeatureExtractor(params)
            else:  # Parameter file not found, use hardcoded settings instead
                settings = {}
                settings['binWidth'] = 25
                settings['resampledPixelSpacing'] = None  # [3,3,3]
                settings['interpolator'] = sitk.sitkBSpline
                settings['enableCExtensions'] = True

                extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
                # extractor.enableInputImages(wavelet= {'level': 2})

            logger.info('Enabled input images types: %s', extractor.enabledImagetypes)
            logger.info('Enabled features: %s', extractor.enabledFeatures)
            logger.info('Current settings: %s', extractor.settings)

            # Instantiate a pandas data frame to hold the results of all patients
            results = pandas.DataFrame()

            for entry in flists:  # Loop over all columns (i.e. the test cases)
                logger.info("(%d/%d) Processing Patient (Image: %s, Mask: %s)",
                            entry + 1,
                            len(flists),
                            flists[entry]['Image'],
                            flists[entry]['Mask'])

                imageFilepath = flists[entry]['Image']
                maskFilepath = flists[entry]['Mask']
                label = flists[entry].get('Label', None)

                if str(label).isdigit():
                    label = int(label)
                else:
                    label = None

                if (imageFilepath is not None) and (maskFilepath is not None):
                    featureVector = flists[entry]  # This is a pandas Series
                    featureVector['Image'] = os.path.basename(imageFilepath)
                    featureVector['Mask'] = os.path.basename(maskFilepath)

                try:
                    # PyRadiomics returns the result as an ordered dictionary, which can be easily converted to a pandas Series
                    # The keys in the dictionary will be used as the index (labels for the rows), with the values of the features
                    # as the values in the rows.
                    result = pandas.Series(extractor.execute(imageFilepath, maskFilepath, label))
                    featureVector = featureVector.append(result)
                except Exception:
                    logger.error('FEATURE EXTRACTION FAILED:', exc_info=True)

                # To add the calculated features for this case to our data frame, the series must have a name (which will be the
                # name of the column.
                featureVector.name = entry
                # By specifying an 'outer' join, all calculated features are added to the data frame, including those not
                # calculated for previous cases. This also ensures we don't end up with an empty frame, as for the first patient
                # it is 'joined' with the empty data frame.
                results = results.join(featureVector, how='outer')  # If feature extraction failed, results will be all NaN

            logger.info('Extraction complete, writing CSV')
            # .T transposes the data frame, so that each line will represent one patient, with the extracted features as columns
            results.T.to_csv(outputFilepath, index=False, na_rep='NaN')
            logger.info('CSV writing complete')
        

        # ------------------ Background -------------------------
        #设置背景颜色
        bg_color = "#181A27" 

        canvas_rad = tk.Canvas(
            self, bg=bg_color, height=main.height, width=main.width,
            bd=0, highlightthickness=0)

        canvas_rad.place(x=0, y=0)

        thickness = 60
        length = main.width
        rec_x_ = 0
        rec_y_ = 0
        canvas_rad.create_rectangle(rec_x_, rec_y_, rec_x_ + length, rec_y_ + thickness, fill="#FFFFFF", outline="")

        # logo图像
        global logo_fair
        logo_fair = tk.PhotoImage(file="../GUI_material/icon6.png")
        logo_img = canvas_rad.create_image(200, 32, image=logo_fair)

        metamedai=canvas_rad.create_text(163, 17,font=("Arial-BoldMT", 24),anchor="nw",fill = 'white',tags='home_page')   
        canvas_rad.insert(metamedai,1,"MetaMedAI")

        # ------------------ 右侧信息输出框 ------------------------

        # 处理进度      

        # progress_txt_x = 1300
        # progress_txt_y = 85

        # progress_text = tk.Label(self,
        #     text="处理进度", bg=bg_color,
        #     fg="#8FBEDF", font=("Arial-BoldMT", int(23.0)))
        # progress_text.place(x=progress_txt_x, y=progress_txt_y)


        text_scroll = Scrollbar()
        output_blank = Text(self, bg=bg_color, fg = 'white',font=("Helvetica", 20))

        
        output_blank.config(yscrollcommand=text_scroll.set) 
        output_blank.place(x = 1030, y = 380)
        output_blank.place(width = 540, height = 250)
        output_blank.configure(highlightbackground='#8FBEDF')
        output_blank.configure(highlightthickness = 2)
        text_scroll.config(command=output_blank.yview) 

        def enter_fair():
            controller.show_frame('FAIR')

        def enter_bpe():
            controller.show_frame('BPE')

        def enter_home_page(event):                  
            controller.show_frame('Welcome_Page')
        
        def enter_about_us(event):                  
            controller.show_frame('About_Us')

        def enter_contact(event):                  
            controller.show_frame('Contact')

        def enter_instruction(event):                  
            controller.show_frame('Instruction')

        def enter_deformation():                  
            controller.show_frame('Deformation')
    
        def no():
            print('Worked!!!!')

        label_inter = 70
        start_x = 1050
        bar_y = 29
        text_color = '#000000'

        home_page=canvas_rad.create_text(start_x, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='home_page')
        canvas_rad.tag_bind(home_page, '<ButtonPress-1>', enter_home_page)   
        canvas_rad.insert(home_page,1,"首页")

        about_us=canvas_rad.create_text(start_x + label_inter, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='about_us_')
        canvas_rad.tag_bind(about_us, '<ButtonPress-1>', enter_about_us)   
        canvas_rad.insert(about_us,1,"关于我们")

        instruction=canvas_rad.create_text(start_x + label_inter*4, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='instruction')
        canvas_rad.tag_bind(instruction, '<ButtonPress-1>', enter_instruction)   
        canvas_rad.insert(instruction,1,"软件介绍")

        contact=canvas_rad.create_text(start_x + label_inter*5+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='contact')
        canvas_rad.tag_bind(contact, '<ButtonPress-1>', enter_contact)   
        canvas_rad.insert(contact,1,"联系方式")

        # 下拉框
        global box_img
        box_img = ImageTk.PhotoImage(Image.open('../GUI_material/box2.png'))
        kk = canvas_rad.create_image(main.box_x, main.box_y, image=box_img)
        l1 = canvas_rad.create_line(1230, 102, 1350, 102, fill='#E0E0E0')
        l2 = canvas_rad.create_line(1230, 131, 1350, 131, fill='#E0E0E0')
        l3 = canvas_rad.create_line(1230, 138+23, 1350, 138+23, fill='#E0E0E0')
        l4 = canvas_rad.create_line(1230, 138+23*2+5, 1350, 138+23*2+5, fill='#E0E0E0')
        canvas_rad.itemconfig(kk, state='hidden')
        canvas_rad.itemconfig(l1, state='hidden')
        canvas_rad.itemconfig(l2, state='hidden')
        canvas_rad.itemconfig(l3, state='hidden')
        canvas_rad.itemconfig(l4, state='hidden')

        # 下拉按钮
        global blank_img19
        blank_img19 = tk.PhotoImage(file="../GUI_material/blank.png")
        gofair_btn = tk.Button(self,
                             image=blank_img19, borderwidth=0, highlightthickness=0,
                             command=enter_fair, relief="flat", text="MMA-FAIR Image", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))
        
        global blank_img29
        blank_img29 = tk.PhotoImage(file="../GUI_material/blank.png")
        gobreast_btn = tk.Button(self,
                             image=blank_img29, borderwidth=0, highlightthickness=0,
                             command=enter_bpe, relief="flat", text="MMA-Breast", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))

        global blank_img39
        blank_img39 = tk.PhotoImage(file="../GUI_material/blank.png")
        godeformation_btn = tk.Button(self,
                             image=blank_img39, borderwidth=0, highlightthickness=0,
                             command=enter_deformation, relief="flat", text="MMA-Deform", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))

        global blank_img49
        blank_img49 = tk.PhotoImage(file="../GUI_material/blank.png")
        radiomics_btn = tk.Button(self,
                             image=blank_img49, borderwidth=0, highlightthickness=0,
                             command=no, relief="flat", text="MMA-Radiomics", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))

        switcher_ = tk.StringVar()
        switcher_.set(-1)

        arrow_label = tk.Label(self, text=" v ",fg = '#000000',compound="center",bg = '#FFFFFF')
        

        sub_btn_x = 1230
        sub_btn_y = 82
        sub_btn_inter = 30

        def show_test(e):
            val = int(switcher_.get())
            if  val == -1:
                gofair_btn.place(x = sub_btn_x+4, y = sub_btn_y+sub_btn_inter*2-4)
                gofair_btn.place(width=116, height=17)
                

                gobreast_btn.place(x = sub_btn_x+4, y = sub_btn_y)
                gobreast_btn.place(width=86, height=14)

                godeformation_btn.place(x = sub_btn_x-8, y = sub_btn_y+sub_btn_inter-3)
                godeformation_btn.place(width=116, height=16)

                radiomics_btn.place(x = sub_btn_x+2, y = sub_btn_y+sub_btn_inter*3-6)
                radiomics_btn.place(width=116, height=17)
            
                canvas_rad.itemconfig(kk, state='normal')
                canvas_rad.itemconfig(l1, state='normal')
                canvas_rad.itemconfig(l2, state='normal')
                canvas_rad.itemconfig(l3, state='normal')
                canvas_rad.itemconfig(l4, state='normal')
                treeview.place_forget()
           
                
                switcher_.set(val*-1)

            else:
                gofair_btn.place_forget()
                gobreast_btn.place_forget()
                godeformation_btn.place_forget()
                arrow_label.place_forget()
                radiomics_btn.place_forget()
                switcher_.set(val*-1)
                canvas_rad.itemconfig(kk, state='hidden')
                canvas_rad.itemconfig(l1, state='hidden')
                canvas_rad.itemconfig(l2, state='hidden')
                canvas_rad.itemconfig(l3, state='hidden')
                canvas_rad.itemconfig(l4, state='hidden')

                treeview.place(x=info_x + 550, y=info_y - 20)
                treeview.place(width=540, height=tree_height / 2 + 50)

        functions=canvas_rad.create_text(start_x + label_inter*2+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='functions')
        canvas_rad.tag_bind(functions, '<ButtonPress-1>', show_test)   
        canvas_rad.insert(functions,1,"软件功能")


        # -------------- 选择待处理的数据路径 ----------------        

        choose_path_txt_x = 120
        choose_path_txt_y = 90

        choose_path_text = tk.Label(self,
            text=label_txt1, bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(23.0)))
        choose_path_text.place(x=choose_path_txt_x+30, y=choose_path_txt_y)

        thickness = 1
        length = 373
        rec_x = choose_path_txt_x-65
        rec_y = choose_path_txt_y+38
        canvas_rad.create_rectangle(rec_x, rec_y, rec_x + length, rec_y + thickness, fill="#339999", outline="")


        # ------------------ 选择输入按钮 ------------------
        fair_btn_width = 366
        fair_btn_height = 74
        fair_btn_x = choose_path_txt_x - 60
        fair_btn_y = choose_path_txt_y + 45
        fair_btn_inter = 80
        
        
        Img_path = tkinter.StringVar()
        Img_path.set(default_input1)

        def Img_choose_path():
            file_path = tkinter.filedialog.askdirectory(title=u'Choose data path',
                                                        initialdir=(os.path.expanduser(Img_path.get())))
            Img_path.set(file_path)
            print('Current chosen file path is: ', file_path)
            message = '已选择图像文件路径: ' + str(file_path)
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)

            # display patients info
            style = ttk.Style(self)
            style.theme_use("alt")
            style.configure("Treeview", background=bg_color,fieldbackground=bg_color, foreground="white")

            info_x = 480
            info_y = 120
            c1_txt = 'Patient ID'
            c2_txt = 'Sex'
            c3_txt = 'Modality'
            c4_txt = 'Study Date'
            c5_txt = 'Study Description'
            c6_txt = 'Count'
            c7_txt = 'Size'

            columns = (c1_txt, c2_txt, c3_txt, c4_txt, c5_txt, c7_txt,c6_txt)

            # -----metadata表格 2 更新处------
            treeview = ttk.Treeview(self, show="headings", columns=columns)  # 表格
                
            treeview.column(c1_txt, width=100, anchor='center')
            treeview.column(c2_txt, width=100, anchor='center')
            treeview.column(c3_txt, width=50, anchor='center')
            treeview.column(c4_txt, width=100, anchor='center')
            treeview.column(c5_txt, width=100, anchor='center')
            treeview.column(c7_txt, width=200, anchor='center')
            treeview.column(c6_txt, width=50, anchor='center')
                
            treeview.heading(c1_txt, text=c1_txt) # 显示表头
            treeview.heading(c2_txt, text=c2_txt)
            treeview.heading(c3_txt, text=c3_txt)
            treeview.heading(c4_txt, text=c4_txt)
            treeview.heading(c5_txt, text=c5_txt)
            treeview.heading(c7_txt, text=c7_txt)
            treeview.heading(c6_txt, text=c6_txt)

            treeview.place(x=info_x, y=info_y)
            treeview.place(width=600, height=tree_height)

            # 横纵两个scroll bar
            vbar = ttk.Scrollbar(self, orient=VERTICAL, command=treeview.yview)
            treeview.configure(yscrollcommand=vbar.set)

            hbar = ttk.Scrollbar(self, orient=HORIZONTAL, command=treeview.xview)
            treeview.configure(xscrollcommand=hbar.set)

            fc = Functions(file_path)
            patients_dcm_path = fc.batch_collect_patients_info(Img_path.get())
            
            patid, sex_, modality_, studydate, description, count_, size_, warning = fc.get_patients_info(patients_dcm_path)
            for i in range((len(patid))): # 写入数据
                treeview.insert('', i, values=(patid[i], sex_[i],modality_[i], studydate[i], description[i],size_[i],count_[i]))

        # 按钮 字体大小
        font_size = int(23)

        global choose_img_btn_img
        choose_img_btn_img = tk.PhotoImage(file="../GUI_material/empty.png")

        # 选择图像文件
        choose_img_btn = tk.Button(self,
                             image=choose_img_btn_img, borderwidth=0, highlightthickness=0,
                             command=Img_choose_path, relief="flat", text=btn_txt1,
                              fg = 'white',compound="center",font=("Arial-BoldMT", int(font_size)))
        choose_img_btn.place(x=fair_btn_x, y=fair_btn_y)
        choose_img_btn.place(width=fair_btn_width, height=fair_btn_height)


        # 选择标注文件
        Mask_path = tkinter.StringVar()
        Mask_path.set(default_input2)

        def Mask_choose_path():
            file_path = tkinter.filedialog.askdirectory(title=u'Choose SEG path',
                                                        initialdir=(os.path.expanduser(Mask_path.get())))
            Mask_path.set(file_path)
            print('Current chosen file path is: ', file_path)
            message = '已选择SEG文件路径: ' + str(file_path)
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)

        global choose_mask_btn_img
        choose_mask_btn_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        choose_mask_btn = tk.Button(self,
                             image=choose_mask_btn_img, borderwidth=0, highlightthickness=0,
                             command=Mask_choose_path, relief="flat", text=btn_txt2, 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(font_size)))
        choose_mask_btn.place(x=fair_btn_x, y=fair_btn_y + fair_btn_inter)
        choose_mask_btn.place(width=fair_btn_width, height=fair_btn_height)


        # 选择CSV文件
        Csv_path = tkinter.StringVar()
        Csv_path.set(default_input3)

        def Csv_choose_path():
            file_path = tkinter.filedialog.askopenfilename(title=u'Choose Metadata path',
                                                           initialdir=(os.path.expanduser(Csv_path.get())))
            Csv_path.set(file_path)
            print('Current chosen file path is: ', Csv_path.get())
            message = '已选择metadata文件路径: ' + str(file_path)
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)

        global choose_csv_btn_img
        choose_csv_btn_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        choose_csv_btn = tk.Button(self,
                             image=choose_csv_btn_img, borderwidth=0, highlightthickness=0,
                             command=Csv_choose_path, relief="flat", text=btn_txt3, 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(font_size)))
        choose_csv_btn.place(x=fair_btn_x, y=fair_btn_y + fair_btn_inter*2)
        choose_csv_btn.place(width=fair_btn_width, height=fair_btn_height)


        # -------------- 选择输出结果路径 ----------------     
        thickness = 1
        length = 300   

        metadata_txt_x = 140
        metadata_txt_y = 430

        metadata_text = tk.Label(self,
            text=label_txt2, bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(23.0)))
        metadata_text.place(x=metadata_txt_x-15, y=metadata_txt_y)

        thickness = 1
        length = 373
        rec_y = metadata_txt_y+38
        canvas_rad.create_rectangle(rec_x, rec_y, rec_x + length, rec_y + thickness, fill="#339999", outline="")

        # 选择 腺体标注 存放文件夹

        FCM_output_path = tkinter.StringVar()
        FCM_output_path.set(default_output1)
    
        def Gland_choose_path():
            file_path = tkinter.filedialog.askdirectory(title=u'Choose segmentation output directory',
                                                        initialdir=(os.path.expanduser(FCM_output_path.get())))
            FCM_output_path.set(file_path)
            print('Current chosen file path is: ', file_path)
            message = '已选择Seg存放文件夹: ' + str(file_path)
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)

        global choose_gland_output_btn_img
        choose_gland_output_btn_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        choose_gland_btn = tk.Button(self,
                             image=choose_gland_output_btn_img, borderwidth=0, highlightthickness=0,
                             command=Gland_choose_path, relief="flat", text=btn_txt4,
                              fg = 'white',compound="center",font=("Arial-BoldMT", int(font_size)))
        choose_gland_btn.place(x=fair_btn_x, y=rec_y + 7)
        choose_gland_btn.place(width=fair_btn_width, height=fair_btn_height)

        # 选择 BPE结果 存放文件夹
        BPE_output_path = tkinter.StringVar()
        BPE_output_path.set(default_output2)
    
        def BPE_save_choose_path():
            file_path = tkinter.filedialog.askdirectory(title=u'Choose ITK output directory',
                                                        initialdir=(os.path.expanduser(BPE_output_path.get())))
            BPE_output_path.set(file_path)
            print('Current chosen file path is: ', BPE_output_path.get())
            message = '已选择标注文件存放文件夹: ' + str(file_path)
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)

        global choose_bpe_btn_img
        choose_bpe_btn_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        choose_bpe_btn = tk.Button(self,
                             image=choose_bpe_btn_img, borderwidth=0, highlightthickness=0,
                             command=BPE_save_choose_path, relief="flat", text=btn_txt5, 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(font_size)))
        choose_bpe_btn.place(x=fair_btn_x, y=rec_y + 7 + fair_btn_inter)
        choose_bpe_btn.place(width=fair_btn_width, height=fair_btn_height)

        
        # ------------------ 病人信息 -------------------------

        style = ttk.Style(self)
        style.theme_use("alt")
        style.configure("Treeview", background=bg_color,fieldbackground=bg_color, foreground="white",highlightbackground='#8FBEDF')

        info_x = 480
        info_y = 120
        c1_txt = 'Patient ID'
        c2_txt = 'Sex'
        c3_txt = 'Modality'
        c4_txt = 'Study Date'
        c5_txt = 'Study Description'
        c6_txt = 'Count'
        c7_txt = 'Size'

        columns = (c1_txt, c2_txt, c3_txt, c4_txt, c5_txt, c7_txt,c6_txt)
        treeview = ttk.Treeview(self, show="headings", columns=columns)  # 表格
            
        treeview.column(c1_txt, width=100, anchor='center')
        treeview.column(c2_txt, width=100, anchor='center')
        treeview.column(c3_txt, width=50, anchor='center')
        treeview.column(c4_txt, width=100, anchor='center')
        treeview.column(c5_txt, width=100, anchor='center')
        treeview.column(c7_txt, width=120, anchor='center')
        treeview.column(c6_txt, width=50, anchor='center')
            
        treeview.heading(c1_txt, text=c1_txt) # 显示表头
        treeview.heading(c2_txt, text=c2_txt)
        treeview.heading(c3_txt, text=c3_txt)
        treeview.heading(c4_txt, text=c4_txt)
        treeview.heading(c5_txt, text=c5_txt)
        treeview.heading(c7_txt, text=c7_txt)
        treeview.heading(c6_txt, text=c6_txt)

        

        # -----图像周围蓝色边框------
        tree_height = 430
        start_x = info_x-1
        start_y = info_y-1
        width_tree = 602
        height_tree = tree_height+2
        # canvas_rad.create_line(start_x, start_y, start_x, start_y+height_tree, fill='#8FBEDF')
        # canvas_rad.create_line(start_x, start_y, start_x+width_tree, start_y, fill='#8FBEDF')
        # canvas_rad.create_line(start_x, start_y+height_tree, start_x+width_tree, start_y+height_tree, fill='#8FBEDF')
        # canvas_rad.create_line(start_x+width_tree, start_y, start_x+width_tree, start_y+height_tree, fill='#8FBEDF')
        
        # -----metadata表格 1 ------
        treeview.place(x=info_x + 550, y=info_y - 20)
        treeview.place(width=540, height=tree_height / 2 + 50)

        patientId = ['Example1','Example2','Example3','Example4','Example5','Example6','Example1','Example2','Example3','Example4','Example5','Example6','Example1','Example2','Example3','Example4','Example5','Example6','Example2','Example3','Example4','Example5','Example6','Example1','Example2','Example3','Example4','Example5','Example6','Example1','Example2','Example3','Example4','Example5','Example6']
        sex = ['M','F','M','M','F','M','M','F','M','M','F','M','M','F','M','M','F','M','F','M','M','F','M','M','F','M','M','F','M','M','F','M','M','F','M']
        modality = ['CT','CT','MR','CT','CT','MR','CT','CT','MR','CT','CT','MR','CT','CT','MR','CT','CT','MR','CT','MR','CT','CT','MR','CT','CT','MR','CT','CT','MR','CT','CT','MR','CT','CT','MR']
        studyDate = ['2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021','2021']
        studyDescription = ['Breast','Lung','Breast','Lung','Lung','Breast','Breast','Lung','Breast','Lung','Lung','Breast','Breast','Lung','Breast','Lung','Lung','Breast','Lung','Breast','Lung','Lung','Breast','Breast','Lung','Breast','Lung','Lung','Breast','Breast','Lung','Breast','Lung','Lung','Breast']
        count = ['300','213','87','98','142','184','300','213','87','98','142','184','300','213','87','98','142','184','213','87','98','142','184','300','213','87','98','142','184','300','213','87','98','142','184']
        size = ['512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512','512*512']
        for i in range(min(len(sex),len(modality),len(patientId))): # 写入数据
            treeview.insert('', i, values=(patientId[i], sex[i],modality[i], studyDate[i], studyDescription[i],size[i],count[i]))

        # 横纵两个scroll bar
        vbar = ttk.Scrollbar(self, orient=VERTICAL, command=treeview.yview)
        treeview.configure(yscrollcommand=vbar.set)

        hbar = ttk.Scrollbar(self, orient=HORIZONTAL, command=treeview.xview)
        treeview.configure(xscrollcommand=hbar.set)
 


        # ------------------ 功能选择 -------------------------

        radio_x = 550
        radio_y = 580

        type_ = IntVar()
        bpe_radio = Radiobutton(self, text=radio_btn_txt2, variable=type_, 
        value = 0, bg=bg_color, fg="white",font=("Arial-BoldMT", int(17)))
        #bpe_radio.place(x = radio_x + 170, y = radio_y+5)

        gland_seg_radio = Radiobutton(self, text=radio_btn_txt1, variable=type_, 
        value = 1, bg=bg_color, fg="white",font=("Arial-BoldMT", int(17)))
        #gland_seg_radio.place(x = radio_x, y = radio_y + 5)

        
        def start_SEG():
            message = 'Start to converting dcm images to SEG'
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)
            output_blank.insert('insert',"\n")

        def BPE_cal():
            message = '开始BPE计算'
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)
            output_blank.insert('insert',"\n")
        def gland_seg():
            message = '开始腺体分割'
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)
            output_blank.insert('insert',"\n")

        def convert():
            Root_Unenhances_Dirs = os.path.join(str(Img_path.get()),'Unenhanced')
            Root_Enhanced_Dirs = os.path.join(str(Img_path.get()),'Enhanced')
            Origin_Breast_Mask_Dirs = str(Mask_path.get())
            LESION_INFO_CSV_PATH = str(Csv_path.get())
            FCM_OUTPUT_DIR = str(FCM_output_path.get()) 
            BPE_OUTPUT_DIR = str(BPE_output_path.get())
            CSV_file_name = 'BreastBPE_testcase.csv' # set your file name


            Patient_list = os.listdir(Root_Unenhances_Dirs)
            Patient_list = [x for x in Patient_list if not x.startswith('.')] # remove files start with '.', especially for Mac machine
            Patient_list.sort()
                
            ARGS_ = ARGS()
            args = ARGS_.get_args()

            bpe_func = BPE_functions(Root_Unenhances_Dirs,Root_Enhanced_Dirs,Origin_Breast_Mask_Dirs,
            LESION_INFO_CSV_PATH,FCM_OUTPUT_DIR,BPE_OUTPUT_DIR,CSV_file_name,Patient_list,args)

            if type_.get() == 0:
                bpe_func.start_cal(1)
                message = 'BPE Calculation Done!'
                output_blank.insert('insert',"\n")
                output_blank.insert('insert',message)
                output_blank.insert('insert',"\n")
            elif type_.get() == 1:
                bpe_func.start_cal(0)
                message = 'Glands Segmentation Done!'
                output_blank.insert('insert',"\n")
                output_blank.insert('insert',message)
                output_blank.insert('insert',"\n")
                

        # start convert button
        global convert_btn_img
        convert_btn_img = tk.PhotoImage(file="../GUI_material/empty_func.png")
        
        convert_btn = tk.Button(self,
                             image=convert_btn_img, borderwidth=0, highlightthickness=0,
                             command=convert, relief="flat", text="开始处理", 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(17)))
        # convert_btn.place(x=880, y=580)
        # convert_btn.place(width=124, height=38)

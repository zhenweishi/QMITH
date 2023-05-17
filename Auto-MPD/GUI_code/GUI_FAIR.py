'''
# -*- coding: utf-8 -*-
@author: Tianchen Luo: ltc8498@gmail.com

'''
import tkinter as tk
import json
import SimpleITK as sitk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import sys
import shutil
import os
#import SimpleITK as sitk
#import matplotlib.pyplot as plt
import pydicom
import numpy as np
import glob
from tkinter import filedialog
from tkinter import font as tkFont
from subprocess import call
import GUI_Main as main
from GUI_Functions import Functions

from PIL import Image, ImageTk


class FAIR(tk.Frame):

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


        # ------------------ Background -------------------------
        #设置背景颜色
        bg_color = "#181A27" 

        canvas_fair = tk.Canvas(
            self, bg=bg_color, height=main.height, width=main.width,
            bd=0, highlightthickness=0)

        canvas_fair.place(x=0, y=0)

        thickness = 60
        length = main.width
        rec_x_ = 0
        rec_y_ = 0
        canvas_fair.create_rectangle(rec_x_, rec_y_, rec_x_ + length, rec_y_ + thickness, fill="#FFFFFF", outline="")

        # logo图像
        global logo_fair
        logo_fair = tk.PhotoImage(file="../GUI_material/icon6.png")
        logo_img = canvas_fair.create_image(200, 32, image=logo_fair)

        metamedai=canvas_fair.create_text(163, 17,font=("Arial-BoldMT", 24),anchor="nw",fill = 'white',tags='home_page')   
        canvas_fair.insert(metamedai,1,"MetaMedAI")

        def enter_bpe():
            controller.show_frame('BPE')

        def enter_rad():
            controller.show_frame('Radiomics')

        def enter_home_page(event):                  
            controller.show_frame('Welcome_Page')
        
        def enter_about_us(event):                  
            controller.show_frame('About_Us')

        def enter_contact(event):                  
            controller.show_frame('Contact')

        def enter_instruction(event):                  
            controller.show_frame('Instruction')

        def no():
            print('Stay here')
        
        def enter_deformation():                  
            controller.show_frame('Deformation')


        label_inter = 70
        start_x = 1050
        bar_y = 29
        text_color = '#000000'

        home_page=canvas_fair.create_text(start_x, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='home_page')
        canvas_fair.tag_bind(home_page, '<ButtonPress-1>', enter_home_page)   
        canvas_fair.insert(home_page,1,"首页")

        about_us=canvas_fair.create_text(start_x + label_inter, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='about_us_')
        canvas_fair.tag_bind(about_us, '<ButtonPress-1>', enter_about_us)   
        canvas_fair.insert(about_us,1,"关于我们")

        instruction=canvas_fair.create_text(start_x + label_inter*4, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='instruction')
        canvas_fair.tag_bind(instruction, '<ButtonPress-1>', enter_instruction)   
        canvas_fair.insert(instruction,1,"软件介绍")

        contact=canvas_fair.create_text(start_x + label_inter*5+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='contact')
        canvas_fair.tag_bind(contact, '<ButtonPress-1>', enter_contact)   
        canvas_fair.insert(contact,1,"联系方式")

        global box_img5
        box_img5 = ImageTk.PhotoImage(Image.open('../GUI_material/box2.png'))
        kk = canvas_fair.create_image(main.box_x, main.box_y, image=box_img5)
        l1 = canvas_fair.create_line(1230, 102, 1350, 102, fill='#E0E0E0')
        l2 = canvas_fair.create_line(1230, 131, 1350, 131, fill='#E0E0E0')
        l3 = canvas_fair.create_line(1230, 138+23, 1350, 138+23, fill='#E0E0E0')
        l4 = canvas_fair.create_line(1230, 138+23*2+5, 1350, 138+23*2+5, fill='#E0E0E0')
    
        canvas_fair.itemconfig(kk, state='hidden')
        canvas_fair.itemconfig(l1, state='hidden')
        canvas_fair.itemconfig(l2, state='hidden')
        canvas_fair.itemconfig(l3, state='hidden')
        canvas_fair.itemconfig(l4, state='hidden')

        progress_txt_x = 1300
        progress_txt_y = 85

        progress_text = tk.Label(self,
            text="处理进度", bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(23.0)))
        progress_text.place(x=progress_txt_x, y=progress_txt_y)

        # 下拉按钮
        global blank_img15
        blank_img15 = tk.PhotoImage(file="../GUI_material/blank.png")
        
        gofair_btn = tk.Button(self,
                             image=blank_img15, borderwidth=0, highlightthickness=0,
                             command=no, relief="flat", text="MMA-FAIR Image", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))
        
        global blank_img25
        blank_img25 = tk.PhotoImage(file="../GUI_material/blank.png")
        
        gobreast_btn = tk.Button(self,
                             image=blank_img25, borderwidth=0, highlightthickness=0,
                             command=enter_bpe, relief="flat", text="MMA-Breast", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))

        global blank_img35
        blank_img35 = tk.PhotoImage(file="../GUI_material/blank.png")
        
        godeformation_btn = tk.Button(self,
                             image=blank_img35, borderwidth=0, highlightthickness=0,
                             command=enter_deformation, relief="flat", text="MMA-Deform", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))

        global blank_img45
        blank_img45 = tk.PhotoImage(file="../GUI_material/blank.png")
        radiomics_btn = tk.Button(self,
                             image=blank_img45, borderwidth=0, highlightthickness=0,
                             command=enter_rad, relief="flat", text="MMA-Radiomics", 
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

                canvas_fair.itemconfig(kk, state='normal')
                canvas_fair.itemconfig(l1, state='normal')
                canvas_fair.itemconfig(l2, state='normal')
                canvas_fair.itemconfig(l3, state='normal')
                canvas_fair.itemconfig(l4, state='normal')
                output_blank.place_forget()
                progress_text.place_forget()
                switcher_.set(val*-1)

            else:
                gofair_btn.place_forget()
                gobreast_btn.place_forget()
                godeformation_btn.place_forget()
                arrow_label.place_forget()
                switcher_.set(val*-1)

                output_blank.place(x = 1120, y = 120)
                output_blank.place(width = 450, height = 510)

                progress_text.place(x=progress_txt_x, y=progress_txt_y)

                canvas_fair.itemconfig(kk, state='hidden')
                canvas_fair.itemconfig(l1, state='hidden')
                canvas_fair.itemconfig(l2, state='hidden')
                canvas_fair.itemconfig(l3, state='hidden')
                canvas_fair.itemconfig(l4, state='hidden')

        functions=canvas_fair.create_text(start_x + label_inter*2+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='functions')
        canvas_fair.tag_bind(functions, '<ButtonPress-1>', show_test)   
        canvas_fair.insert(functions,1,"软件功能")

        

        # ------------------ 右侧信息输出框 ------------------------

        

        text_scroll = Scrollbar()
        output_blank = Text(self, bg=bg_color, fg = 'white',font=("Helvetica", 20))

        
        output_blank.config(yscrollcommand=text_scroll.set) 
        output_blank.place(x = 1120, y = 120)
        output_blank.place(width = 450, height = 510)
        output_blank.configure(highlightbackground='#8FBEDF')
        output_blank.configure(highlightthickness = 2)
        text_scroll.config(command=output_blank.yview) 
        
        # ------------------ 返回按钮 ----------------------
        def enter_welcome():
            controller.show_frame('Welcome_Page')

        global back_btn_img
        back_btn_img = tk.PhotoImage(file="../GUI_material/arrow2.png")
        back_btn = tk.Button(self,
            image=back_btn_img, borderwidth=0, highlightthickness=0,
            command=enter_welcome, relief="flat")
        #back_btn.place(x=5, y=7, width=48, height=36)

        # ------------------ 介绍功能文字 ------------------
        title_x_result = 650
        title_y_result = 10
        title_result = tk.Label(self,
            text="FAIR 数据处理", bg=bg_color,
            fg="#339999", font=("Arial-BoldMT", int(45.0)))
        #title_result.place(x=title_x_result, y=title_y_result)

        # -------------- 选择待处理的数据路径 ----------------        

        choose_path_txt_x = 120
        choose_path_txt_y = 90

        choose_path_text = tk.Label(self,
            text="选择待处理的数据路径", bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(23.0)))
        choose_path_text.place(x=choose_path_txt_x, y=choose_path_txt_y)

        thickness = 1
        length = 373
        rec_x = choose_path_txt_x-65
        rec_y = choose_path_txt_y+38
        canvas_fair.create_rectangle(rec_x, rec_y, rec_x + length, rec_y + thickness, fill="#339999", outline="")


        # ------------------ 选择输入按钮 ------------------
        fair_btn_width = 366
        fair_btn_height = 74
        fair_btn_x = choose_path_txt_x - 60
        fair_btn_y = choose_path_txt_y + 45
        fair_btn_inter = 80
        txt_x = 140
        txt_y = 150
        
        Img_path = tkinter.StringVar()
        Img_path.set('../Data')

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
            treeview.column(c3_txt, width=80, anchor='center')
            treeview.column(c4_txt, width=120, anchor='center')
            treeview.column(c5_txt, width=100, anchor='center')
            treeview.column(c7_txt, width=150, anchor='center')
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

        font_size = int(23)

        global choose_img_btn_img
        choose_img_btn_img = tk.PhotoImage(file="../GUI_material/empty.png")

        # 选择图像文件
        choose_img_btn = tk.Button(self,
                             image=choose_img_btn_img, borderwidth=0, highlightthickness=0,
                             command=Img_choose_path, relief="flat", text="选择图像文件",
                              fg = 'white',compound="center",font=("Arial-BoldMT", int(font_size)))
        choose_img_btn.place(x=fair_btn_x, y=fair_btn_y)
        choose_img_btn.place(width=fair_btn_width, height=fair_btn_height)


        # 选择SEG文件

        SEG_path = tkinter.StringVar()
        SEG_path.set('../DCMSEG_Output/LUNG1-086_SEG.dcm')

        def Mask_choose_path():
            file_path = tkinter.filedialog.askopenfilename(title=u'Choose SEG path',
                                                        initialdir=(os.path.expanduser(SEG_path.get())))
            SEG_path.set(file_path)
            print('Current chosen file path is: ', file_path)
            message = '已选择SEG文件路径: ' + str(file_path)
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)

        global choose_seg_btn_img
        choose_seg_btn_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        choose_seg_btn = tk.Button(self,
                             image=choose_seg_btn_img, borderwidth=0, highlightthickness=0,
                             command=Mask_choose_path, relief="flat", text="选择SEG文件", 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(font_size)))
        choose_seg_btn.place(x=fair_btn_x, y=fair_btn_y + fair_btn_inter)
        choose_seg_btn.place(width=fair_btn_width, height=fair_btn_height)


        # 选择metadata文件

        Meta_path = tkinter.StringVar()
        Meta_path.set('../metadata/metadata.json')

        def Meta_choose_path():
            file_path = tkinter.filedialog.askopenfilename(title=u'Choose Metadata path',
                                                           initialdir=(os.path.expanduser(Meta_path.get())))
            Meta_path.set(file_path)
            print('Current chosen file path is: ', Meta_path.get())
            message = '已选择metadata文件路径: ' + str(file_path)
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)

        global choose_metadata_btn_img
        choose_metadata_btn_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        choose_metadata_btn = tk.Button(self,
                             image=choose_metadata_btn_img, borderwidth=0, highlightthickness=0,
                             command=Meta_choose_path, relief="flat", text="选择metadata文件", 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(font_size)))
        choose_metadata_btn.place(x=fair_btn_x, y=fair_btn_y + fair_btn_inter*2)
        choose_metadata_btn.place(width=fair_btn_width, height=fair_btn_height)


        # -------------- metadata ----------------        

        metadata_txt_x = 80
        metadata_txt_y = 300

        metadata_text = tk.Label(self,
            text="自定义制作metadata", bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(18.0)))
        #metadata_text.place(x=metadata_txt_x, y=metadata_txt_y)

        thickness = 1
        length = 300
        #rec_x = metadata_txt_x-65
        #rec_y = metadata_txt_y+28
        #canvas_fair.create_rectangle(rec_x, rec_y, rec_x + length, rec_y + thickness, fill="#339999", outline="")

        def enter_generator():
            controller.show_frame('MG')

        # 自定义制作metadata
        global diy_metadata_btn_img
        diy_metadata_btn_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        diy_metadata_btn = tk.Button(self,
                             image=diy_metadata_btn_img, borderwidth=0, highlightthickness=0,
                             command=enter_generator, relief="flat", text="自定义制作metadata", 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(font_size)))
        #diy_metadata_btn.place(x=fair_btn_x, y=rec_y + 7)
        #diy_metadata_btn.place(width=fair_btn_width, height=fair_btn_height)

        # -------------- 选择输出结果路径 ----------------        

        metadata_txt_x = 140
        metadata_txt_y = 430

        metadata_text = tk.Label(self,
            text="选择输出结果路径", bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(23.0)))
        metadata_text.place(x=metadata_txt_x, y=metadata_txt_y)

        thickness = 1
        length = 373

        #rec_x = choose_path_txt_x-65
        rec_y = metadata_txt_y+38
        canvas_fair.create_rectangle(rec_x, rec_y, rec_x + length, rec_y + thickness, fill="#339999", outline="")

        # 选择seg存放文件夹

        Seg_path = tkinter.StringVar()
        Seg_path.set('../DCMSEG_Output')
    
        def Seg_choose_path():
            file_path = tkinter.filedialog.askdirectory(title=u'Choose segmentation output directory',
                                                        initialdir=(os.path.expanduser(Seg_path.get())))
            Seg_path.set(file_path)
            print('Current chosen file path is: ', file_path)
            message = '已选择Seg存放文件夹: ' + str(file_path)
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)

        global choose_seg_output_btn_img
        choose_seg_output_btn_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        choose_seg_btn = tk.Button(self,
                             image=choose_seg_output_btn_img, borderwidth=0, highlightthickness=0,
                             command=Seg_choose_path, relief="flat", text="选择Seg存放文件夹",
                              fg = 'white',compound="center",font=("Arial-BoldMT", int(font_size)))
        choose_seg_btn.place(x=fair_btn_x, y=rec_y + 7)
        choose_seg_btn.place(width=fair_btn_width, height=fair_btn_height)

        # 选择ITK存放文件夹
        ITK_save_path = tkinter.StringVar()
        ITK_save_path.set('../ITK_Output')
    
        def ITK_save_choose_path():
            file_path = tkinter.filedialog.askdirectory(title=u'Choose ITK output directory',
                                                        initialdir=(os.path.expanduser(ITK_save_path.get())))
            ITK_save_path.set(file_path)
            print('Current chosen file path is: ', ITK_save_path.get())
            message = '已选择标注文件存放文件夹: ' + str(file_path)
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)

        global choose_itk_btn_img
        choose_itk_btn_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        choose_itk_btn = tk.Button(self,
                             image=choose_itk_btn_img, borderwidth=0, highlightthickness=0,
                             command=ITK_save_choose_path, relief="flat", text="选择标注文件存放文件夹", 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(font_size)))
        choose_itk_btn.place(x=fair_btn_x, y=rec_y + 7 + fair_btn_inter)
        choose_itk_btn.place(width=fair_btn_width, height=fair_btn_height)

        
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
        treeview.column(c3_txt, width=80, anchor='center')
        treeview.column(c4_txt, width=120, anchor='center')
        treeview.column(c5_txt, width=100, anchor='center')
        treeview.column(c7_txt, width=150, anchor='center')
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
        canvas_fair.create_line(start_x, start_y, start_x, start_y+height_tree, fill='#8FBEDF')
        canvas_fair.create_line(start_x, start_y, start_x+width_tree, start_y, fill='#8FBEDF')
        canvas_fair.create_line(start_x, start_y+height_tree, start_x+width_tree, start_y+height_tree, fill='#8FBEDF')
        canvas_fair.create_line(start_x+width_tree, start_y, start_x+width_tree, start_y+height_tree, fill='#8FBEDF')
        
        # -----metadata表格 1 ------
        treeview.place(x=info_x, y=info_y)
        treeview.place(width=600, height=tree_height)

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
        #vbar.place(x = 1080, y = 100)


        # ------------------ 功能选择 -------------------------

        radio_x = 550
        radio_y = 580

        type_ = IntVar()
        seg2itk_radio = Radiobutton(self, text="   SEG2ITK", variable=type_, 
        value = 1, bg=bg_color, fg="white",font=("Arial-BoldMT", int(17)))
        seg2itk_radio.place(x = radio_x, y = radio_y + 5)

        itk2seg_radio = Radiobutton(self, text="   ITK2SEG", variable=type_, 
        value = 0, bg=bg_color, fg="white",font=("Arial-BoldMT", int(17)))
        itk2seg_radio.place(x = radio_x + 170, y = radio_y+5)


        global seg2itk_btn_img
        seg2itk_btn_img = tk.PhotoImage(file="../GUI_material/empty_func.png")
        
        seg2itk_btn = tk.Button(self,
                             image=seg2itk_btn_img, borderwidth=0, highlightthickness=0,
                             command=Meta_choose_path, relief="flat", text="SEG2ITK", 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(17)))
        #seg2itk_btn.place(x=radio_x-10, y=radio_y)
        #seg2itk_btn.place(width=124, height=38)

        global itk2seg_btn_img
        itk2seg_btn_img = tk.PhotoImage(file="../GUI_material/empty_func.png")
        
        itk2seg_btn = tk.Button(self,
                             image=itk2seg_btn_img, borderwidth=0, highlightthickness=0,
                             command=Meta_choose_path, relief="flat", text="ITK2SEG", 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(17)))
        #itk2seg_btn.place(x=radio_x+200, y=radio_y)
        #itk2seg_btn.place(width=124, height=38)
        
        def _DCMNFITI2SEG(inputlabelList, inputDICOMDirectory, inputMetadata, outputSEGfile, outputDir, patientID):
            outputDICOM = os.path.join(outputDir, outputSEGfile)
            try:
                call(['itkimage2segimage', '--inputImageList', inputlabelList, '--inputDICOMDirectory',
                      inputDICOMDirectory, \
                      '--inputMetadata', inputMetadata, '--outputDICOM', outputDICOM])
                message = 'Successfully generated ' + patientID + '_SEG.dcm '
                output_blank.insert('insert',"\n")
                output_blank.insert('insert',message)
                
            except:
                message = 'Error: failed to pack dcm image to SEG.dcm'
                print('Error: failed to pack dcm image to SEG.dcm')
                output_blank.insert('insert',"\n")
                output_blank.insert('insert',message)

        # convert SEG objects to ITK nrrd images
        def SEG2ITKimage(SEG_file_name):
            
            try:
                call(['segimage2itkimage', '--outputType','nii','--prefix',SEG_file_name,'--inputDICOM', str(SEG_path.get()), '--outputDirectory', str(ITK_save_path.get())])
                message = 'Successfully converted ' + SEG_file_name + ' to ITK mask'
                output_blank.insert('insert',"\n")
                output_blank.insert('insert',message)
                output_blank.insert('insert',"\n")
            except:
                message = 'Error: Failed to pack ' + SEG_file_name + ' to ITK mask'
                output_blank.insert('insert',"\n")
                output_blank.insert('insert',message)
                print('Error: Failed to pack SEG to nrrd image')

        # convert ITK objects to SEG
        def DCMNFITI2SEG():  

            CTWorkingDir = '../tmp_CTFolder/'
            ITKWorkingDir = '../tmp_ITKFolder/'
            if not os.path.exists(CTWorkingDir):
                os.makedirs(CTWorkingDir)
            if not os.path.exists(ITKWorkingDir):
                os.makedirs(ITKWorkingDir)

            Data_path = str(Img_path.get())
            fc = Functions(Data_path)

            patients = fc.get_patients(Data_path)

            debug = True

            for patient in patients:
                print("Patient is: ---- ",patient)
                # Move single patient data to the temp working directories
                fc.move_CTScans(patient,CTWorkingDir,ITKWorkingDir)
                
                patid = fc.get_patientsID(patient)

                inputITKList_ = fc.get_ITKList(ITKWorkingDir)
                inputITKList = ','.join(map(str,inputITKList_))

                inputImageDir = CTWorkingDir
                metadata= str(Meta_path.get())
                output_seg_name = patid + '_' + 'SEG.dcm'
                output_seg_dir =str(Seg_path.get())

                if debug:
                    print('ITK list is: ------------', inputITKList)
                    print('Image list is:', inputImageDir)
                    print('metadata is: ', metadata)
                    #print('output_seg_name is: ', output_seg_name)
                    #print('output_seg_dir is: ', output_seg_dir)

                message = 'Packing ' + patid + ' dcm images to Seg.dcm'
                output_blank.insert('insert',"\n")
                #output_blank.insert('insert',message)
                

                _DCMNFITI2SEG(inputITKList,inputImageDir,metadata,output_seg_name,output_seg_dir,patid)

        def start_SEG():
            message = 'Start to converting dcm images to SEG'
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',"\n")
            output_blank.insert('insert',message)
            output_blank.insert('insert',"\n")

        def convert():
            #start_SEG()
            Data_path = str(Img_path.get())
            fc = Functions(Data_path)
            SEG_file_name = fc.get_files_name(str(SEG_path.get()))

            if type_.get() == 0:
                # start_SEG()
                DCMNFITI2SEG()
            elif type_.get() == 1:
                message = 'Converting ' + SEG_file_name + ' to ITK mask'
                output_blank.insert('insert',"\n")
                output_blank.insert('insert',message)
                SEG2ITKimage(SEG_file_name)   

        # start convert button
        global convert_btn_img
        convert_btn_img = tk.PhotoImage(file="../GUI_material/empty_func.png")
        
        convert_btn = tk.Button(self,
                             image=convert_btn_img, borderwidth=0, highlightthickness=0,
                             command=convert, relief="flat", text="开始处理", 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(17)))
        convert_btn.place(x=880, y=580)
        convert_btn.place(width=124, height=38)


        
        


'''
# -*- coding: utf-8 -*-
@author: Tianchen Luo: ltc8498@gmail.com
'''
from matplotlib.figure import Figure
from matplotlib.colors import colorConverter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import tkinter as tk
import matplotlib as mpl
from scipy.ndimage import rotate
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
import GUI_Main as main
from GUI_Functions import Functions
from GUI_BPEFUNCTION import FCM, BPE_functions, ARGS
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import erosion, dilation
import skimage.transform as skTrans
import nibabel as nib
import os
import numpy as np
import copy
import random
from skimage.measure import label
from scipy import ndimage
from skimage import draw
from skimage.io import imread, imshow
import GUI_Erosion_Dilation as ed


class Deformation(tk.Frame):

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

        canvas_deformation = tk.Canvas(
            self, bg=bg_color, height=main.height, width=main.width,
            bd=0, highlightthickness=0)

        canvas_deformation.place(x=0, y=0)

        thickness = 60
        length = main.width
        rec_x_ = 0
        rec_y_ = 0
        canvas_deformation.create_rectangle(rec_x_, rec_y_, rec_x_ + length, rec_y_ + thickness, fill="#FFFFFF", outline="")

        # ------------------------ 图像位置大小 ----------------------------
        img_x = 540
        img_y = 130
        img_size = 520

        
        # logo图像
        global logo_fair1
        logo_fair1 = tk.PhotoImage(file="../GUI_material/icon6.png")
        logo_img = canvas_deformation.create_image(200, 32, image=logo_fair1)

        metamedai=canvas_deformation.create_text(163, 17,font=("Arial-BoldMT", 24),anchor="nw",fill = 'white',tags='home_page')   
        canvas_deformation.insert(metamedai,1,"MetaMedAI")


        text_color = '#000000'

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

        def enter_deformation():                  
            print('Already here ...')
            
        global box_img
        box_img = ImageTk.PhotoImage(Image.open('../GUI_material/box2.png'))
        kk = canvas_deformation.create_image(main.box_x, main.box_y, image=box_img)
        l1 = canvas_deformation.create_line(1230, 102, 1350, 102, fill='#E0E0E0')
        l2 = canvas_deformation.create_line(1230, 131, 1350, 131, fill='#E0E0E0')
        l3 = canvas_deformation.create_line(1230, 138+23, 1350, 138+23, fill='#E0E0E0')
        l4 = canvas_deformation.create_line(1230, 138+23*2+5, 1350, 138+23*2+5, fill='#E0E0E0')
        # #E0E0E0
        canvas_deformation.itemconfig(kk, state='hidden')
        canvas_deformation.itemconfig(l1, state='hidden')
        canvas_deformation.itemconfig(l2, state='hidden')
        canvas_deformation.itemconfig(l3, state='hidden')
        canvas_deformation.itemconfig(l4, state='hidden')

        def enter_fair():
            controller.show_frame('FAIR')
        

        # 下拉按钮
        global blank_img1
        blank_img1 = tk.PhotoImage(file="../GUI_material/blank.png")
        gofair_btn = tk.Button(self,
                             image=blank_img1, borderwidth=0, highlightthickness=0,
                             command=enter_fair, relief="flat", text="MMA-FAIR Image", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))
        
        global blank_img2
        blank_img2 = tk.PhotoImage(file="../GUI_material/blank.png")
        gobreast_btn = tk.Button(self,
                             image=blank_img2, borderwidth=0, highlightthickness=0,
                             command=enter_bpe, relief="flat", text="MMA-Breast", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))

        global blank_img3
        blank_img3 = tk.PhotoImage(file="../GUI_material/blank.png")
        godeformation_btn = tk.Button(self,
                             image=blank_img3, borderwidth=0, highlightthickness=0,
                             command=enter_deformation, relief="flat", text="MMA-Deform", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))

        global blank_img4
        blank_img4 = tk.PhotoImage(file="../GUI_material/blank.png")
        radiomics_btn = tk.Button(self,
                             image=blank_img4, borderwidth=0, highlightthickness=0,
                             command=enter_rad, relief="flat", text="MMA-Radiomics", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))


        
        switcher_ = tk.StringVar()
        switcher_.set(-1)

        sub_btn_x = 1230
        sub_btn_y = 82
        sub_btn_inter = 30

        label_txt1 = '选择超参数搜索范围'
        choose_path_txt_x = 110
        choose_path_txt_y = 90

        choose_path_text = tk.Label(self,
            text=label_txt1, bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(23.0)))

        choose_path_text.place(x=choose_path_txt_x+30, y=choose_path_txt_y)

        thickness = 1
        length = 420
        rec_x = choose_path_txt_x-65
        rec_y = choose_path_txt_y+38
        rec1 = canvas_deformation.create_rectangle(rec_x, rec_y, rec_x + length, rec_y + thickness, fill="#339999", outline="")

        
        # -------------- Initialization and set the default value of each entry --------------
        prob_from = tkinter.IntVar()
        prob_from.set(0.7)
        prob_to = tkinter.IntVar()
        prob_to.set(0.8)
        prob_step = tkinter.IntVar()
        prob_step.set(0.1)

        iter_from = tkinter.IntVar()
        iter_from.set(15)
        iter_to = tkinter.IntVar()
        iter_to.set(15)
        iter_step = tkinter.IntVar()
        iter_step.set(5)

        expand_from = tkinter.IntVar()
        expand_from.set(100)
        expand_to = tkinter.IntVar()
        expand_to.set(200)
        expand_step = tkinter.IntVar()
        expand_step.set(50)

        patch_from = tkinter.IntVar()
        patch_from.set(10)
        patch_to = tkinter.IntVar()
        patch_to.set(20)
        patch_step = tkinter.IntVar()
        patch_step.set(5)

        kernel_from = tkinter.IntVar()
        kernel_from.set(3)
        kernel_to = tkinter.IntVar()
        kernel_to.set(9)
        kernel_step = tkinter.IntVar()
        kernel_step.set(3)

        dice_from = tkinter.IntVar()
        dice_from.set(0.8)
        dice_to = tkinter.IntVar()
        dice_to.set(0.9)

        iou_from = tkinter.IntVar()
        iou_from.set(0.8)
        iou_to = tkinter.IntVar()
        iou_to.set(0.9)

        hd_from = tkinter.IntVar()
        hd_from.set(0.8)
        hd_to = tkinter.IntVar()
        hd_to.set(0.9)

        mask_num_int = tkinter.IntVar()
        mask_num_int.set(5)


        label_x = 50
        label_y = 170
        label_inter = 70
        label_font_size = 22

        step_x = label_x + 290
        step_font = 20

        prob_label = tk.Label(self,
            text='Probability', bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(label_font_size)))
        prob_label.place(x=label_x, y=label_y+0*label_inter)

        prob_step_label = tk.Label(self,
            text='Step:', bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(step_font)))
        prob_step_label.place(x=step_x, y=label_y+0*label_inter)

        iter_label = tk.Label(self,
            text='Iteration', bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(label_font_size)))
        iter_label.place(x=label_x, y=label_y+1*label_inter)

        iter_step_label = tk.Label(self,
            text='Step:', bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(step_font)))
        iter_step_label.place(x=step_x, y=label_y+1*label_inter)

        expand_label = tk.Label(self,
            text='Expand Size', bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(label_font_size)))
        expand_label.place(x=label_x, y=label_y+2*label_inter)

        exp_step_label = tk.Label(self,
            text='Step:', bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(step_font)))
        exp_step_label.place(x=step_x, y=label_y+2*label_inter)

        patch_label = tk.Label(self,
            text='Patch Size', bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(label_font_size)))
        patch_label.place(x=label_x, y=label_y+3*label_inter)

        patch_step_label = tk.Label(self,
            text='Step:', bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(step_font)))
        patch_step_label.place(x=step_x, y=label_y+3*label_inter)

        kernel_label = tk.Label(self,
            text='Kernel Size', bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(label_font_size)))
        kernel_label.place(x=label_x, y=label_y+4*label_inter)

        kernel_step_label = tk.Label(self,
            text='Step:', bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(step_font)))
        kernel_step_label.place(x=step_x, y=label_y+4*label_inter)

        Dice_label = tk.Label(self,
            text='Dice range', bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(step_font)))
        Dice_label.place(x=label_x, y=label_y+5*label_inter)

        # IOU_label = tk.Label(self,
        #     text='IOU range', bg=bg_color,
        #     fg="#8FBEDF", font=("Arial-BoldMT", int(label_font_size)))
        # IOU_label.place(x=label_x, y=label_y+6*label_inter)

        # HD_label = tk.Label(self,
        #     text='HD range', bg=bg_color,
        #     fg="#8FBEDF", font=("Arial-BoldMT", int(label_font_size)))
        # HD_label.place(x=label_x, y=label_y+7*label_inter)


        mask_num_label = tk.Label(self,
            text='Mnum:', bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(step_font-5)))
        mask_num_label.place(x=step_x, y=label_y+5*label_inter)


        entry_width_ = 3
        entry_x = label_x + 150
        entry_y = label_y
        entry_between = 70
        entry_step_x = step_x+70
        
        prob_from_entry = tk.Entry(self, width=entry_width_, textvariable=prob_from, validate='key')
        prob_from_entry.place(x=entry_x, y=entry_y)
        

        prob_to_entry = tk.Entry(self, width=entry_width_, textvariable=prob_to, validate='key')
        prob_to_entry.place(x=entry_x+entry_between, y=entry_y)

        prob_step_entry = tk.Entry(self, width=entry_width_, textvariable=prob_step, validate='key')
        prob_step_entry.place(x=entry_step_x, y=entry_y)

        iter_from_entry = tk.Entry(self, width=entry_width_, textvariable=iter_from, validate='key')
        iter_from_entry.place(x=entry_x, y=entry_y + label_inter)

        iter_to_entry = tk.Entry(self, width=entry_width_, textvariable=iter_to, validate='key')
        iter_to_entry.place(x=entry_x+entry_between, y=entry_y + label_inter)

        iter_step_entry = tk.Entry(self, width=entry_width_, textvariable=iter_step, validate='key')
        iter_step_entry.place(x=entry_step_x, y=entry_y + label_inter)

        expand_from_entry = tk.Entry(self, width=entry_width_, textvariable=expand_from, validate='key')
        expand_from_entry.place(x=entry_x, y=entry_y + label_inter*2)

        expand_to_entry = tk.Entry(self, width=entry_width_, textvariable=expand_to, validate='key')
        expand_to_entry.place(x=entry_x+entry_between, y=entry_y + label_inter*2)

        expand_step_entry = tk.Entry(self, width=entry_width_, textvariable=expand_step, validate='key')
        expand_step_entry.place(x=entry_step_x, y=entry_y + label_inter*2)

        patch_from_entry = tk.Entry(self, width=entry_width_, textvariable=patch_from, validate='key')
        patch_from_entry.place(x=entry_x, y=entry_y + label_inter*3)

        patch_to_entry = tk.Entry(self, width=entry_width_, textvariable=patch_to, validate='key')
        patch_to_entry.place(x=entry_x+entry_between, y=entry_y + label_inter*3)

        patch_step_entry = tk.Entry(self, width=entry_width_, textvariable=patch_step, validate='key')
        patch_step_entry.place(x=entry_step_x, y=entry_y + label_inter*3)

        kernel_from_entry = tk.Entry(self, width=entry_width_, textvariable=kernel_from, validate='key')
        kernel_from_entry.place(x=entry_x, y=entry_y + label_inter*4)

        kernel_to_entry = tk.Entry(self, width=entry_width_, textvariable=kernel_to, validate='key')
        kernel_to_entry.place(x=entry_x+entry_between, y=entry_y + label_inter*4)

        kernel_step_entry = tk.Entry(self, width=entry_width_, textvariable=kernel_step, validate='key')
        kernel_step_entry.place(x=entry_step_x, y=entry_y + label_inter*4)

        dice_from_entry = tk.Entry(self, width=entry_width_, textvariable=dice_from, validate='key')
        dice_from_entry.place(x=entry_x, y=entry_y + label_inter*5)

        dice_to_entry = tk.Entry(self, width=entry_width_, textvariable=dice_to, validate='key')
        dice_to_entry.place(x=entry_x+entry_between, y=entry_y + label_inter*5)

        # iou_from_entry = tk.Entry(self, width=entry_width_, textvariable=iou_from, validate='key')
        # iou_from_entry.place(x=entry_x, y=entry_y + label_inter*6)

        # iou_to_entry = tk.Entry(self, width=entry_width_, textvariable=iou_to, validate='key')
        # iou_to_entry.place(x=entry_x+entry_between, y=entry_y + label_inter*6)

        # hd_from_entry = tk.Entry(self, width=entry_width_, textvariable=hd_from, validate='key')
        # hd_from_entry.place(x=entry_x, y=entry_y + label_inter*7)

        # hd_to_entry = tk.Entry(self, width=entry_width_, textvariable=hd_to, validate='key')
        # hd_to_entry.place(x=entry_x+entry_between, y=entry_y + label_inter*7)

        

        mask_num_entry = tk.Entry(self, width=entry_width_, textvariable=mask_num_int, validate='key')
        mask_num_entry.place(x=entry_step_x, y=entry_y + label_inter*5)

        btn_width = 366
        btn_height = 74

        

        # 确认超参数范围 以及 生成超参数candidate

        def confirm():
            probability_from = float(prob_from_entry.get())
            probability_to = float(prob_to_entry.get())

            exp_from = int(expand_from_entry.get())
            exp_to = int(expand_to_entry.get())

            pat_from = int(patch_from_entry.get())
            pat_to = int(patch_to_entry.get())

            iteration_from = int(iter_from_entry.get())
            iteration_to = int(iter_to_entry.get())

            ker_from = int(kernel_from_entry.get())
            ker_to = int(kernel_to_entry.get())

            global prob_list
            prob_list = ed.get_float_list(probability_from, probability_to, 0.1)

            global iter_list
            iter_list = ed.get_int_list(iteration_from, iteration_to, 5)

            global patch_list
            patch_list = ed.get_int_list(pat_from, pat_to, 5)

            global exp_list
            exp_list = ed.get_int_list(exp_from, exp_to, 50)

            global kernel_list
            kernel_list = ed.get_int_list(ker_from, ker_to, 3)

            see_hyper_list()
        
        def see_hyper_list():
            
            print('Prob: ',prob_list)
            print('Iteration: ',iter_list)
            print('Patch: ',patch_list)
            print('Expand: ',exp_list)
            print('Kernel: ',kernel_list)
        

        def separate_output():
            output_blank.insert('insert',"\n")
            message = '------------------------------------------------------'
            output_blank.insert('insert',message)

        def start():
            message = '开始处理， 请耐心等待'
            print(message)

            mask_path = '../Mask_folder'
            mask_list = ed.clean_list(os.listdir(mask_path)) # remove DS.Store
            for path in mask_list:

                path = os.path.join(mask_path, path)
                ed.patch_erosion_and_dilation_3D_grid_search(path, prob_list, iter_list, 2, 
                    exp_list, patch_list, kernel_list, str(mask_output_path.get()),
                    int(mask_num_entry.get()), float(dice_from_entry.get()), float(dice_to_entry.get()))
            
        
        global start_img
        start_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        start_btn = tk.Button(self,
                             image=start_img, borderwidth=0, highlightthickness=0,
                             command=start, relief="flat", text='开始处理', 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(23)))
        

        thickness_ = 3
        length_ = 20
        minus_x = entry_x + 45
        minus_y = label_y + 12
        canvas_deformation.create_rectangle(minus_x, minus_y, minus_x + length_, minus_y + thickness_, fill="#FFFFFF", outline="")
        canvas_deformation.create_rectangle(minus_x, minus_y+label_inter, minus_x + length_, minus_y+label_inter + thickness_, fill="#FFFFFF", outline="")
        canvas_deformation.create_rectangle(minus_x, minus_y+label_inter*2, minus_x + length_, minus_y+label_inter*2 + thickness_, fill="#FFFFFF", outline="")
        canvas_deformation.create_rectangle(minus_x, minus_y+label_inter*3, minus_x + length_, minus_y+label_inter*3+ thickness_, fill="#FFFFFF", outline="")
        canvas_deformation.create_rectangle(minus_x, minus_y+label_inter*4, minus_x + length_, minus_y+label_inter*4 + thickness_, fill="#FFFFFF", outline="")
        canvas_deformation.create_rectangle(minus_x, minus_y+label_inter*5, minus_x + length_, minus_y+label_inter*5 + thickness_, fill="#FFFFFF", outline="")
        # canvas_deformation.create_rectangle(minus_x, minus_y+label_inter*6, minus_x + length_, minus_y+label_inter*6 + thickness_, fill="#FFFFFF", outline="")
        # canvas_deformation.create_rectangle(minus_x, minus_y+label_inter*7, minus_x + length_, minus_y+label_inter*7 + thickness_, fill="#FFFFFF", outline="")


        # -------------------    右侧输出框   --------------------------------------------

        text_scroll = Scrollbar()
        output_blank = Text(self, bg=bg_color, fg = 'white',font=("Helvetica", 20))

        output_x = 1100
        output_y = 400
        output_width = 500
        output_height = 210

        output_blank.config(yscrollcommand=text_scroll.set) 
        # output_blank.place(x = output_x, y = output_y)
        # output_blank.place(width = output_width, height = output_height)

        output_blank.configure(highlightbackground='#8FBEDF')
        output_blank.configure(highlightthickness = 2)
        text_scroll.config(command=output_blank.yview)


        # -----------------------------右侧按钮和标签---------------------------------------------

        label_txt2 = '选择存放路径与配置文件'
        choose_path_txt_x = output_x + 120
        choose_path_txt_y = choose_path_txt_y

        choose_config_text = tk.Label(self,
            text=label_txt2, bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(23.0)))

        choose_config_text.place(x=choose_path_txt_x, y=choose_path_txt_y)
       
        thickness = 1
        length = 373
        rec_x = choose_path_txt_x-65
        rec_y = choose_path_txt_y+38
        rec_config = canvas_deformation.create_rectangle(rec_x, rec_y, rec_x + length, rec_y + thickness, fill="#339999", outline="")

        # --------------------------------------------------------------------------
        btn_font_size = 23
        fair_btn_x = choose_path_txt_x - 60
        fair_btn_y = choose_path_txt_y + 50
        fair_btn_inter = 80
        btn_width = 366
        btn_height = 74


        config_path = tkinter.StringVar()
        config_path.set('../config/config_easy.yml')

        def choose_config_path():
            file_path = tkinter.filedialog.askopenfilename(title=u'Choose Metadata path',
                                                           initialdir=(os.path.expanduser(config_path.get())))
            config_path.set(file_path)
            print('Current chosen config path is: ', config_path.get())
            

            config_dict = ed.read_config2dict(file_path)

            prob_from.set(config_dict['probability_from'])
            prob_to.set(config_dict['probability_to'])
            prob_step.set(config_dict['probability_step'])

            iter_from.set(config_dict['iteration_from'])
            iter_to.set(config_dict['iteration_to'])
            iter_step.set(config_dict['iteration_step'])

            expand_from.set(config_dict['expand_size_from'])
            expand_to.set(config_dict['expand_size_to'])
            expand_step.set(config_dict['expand_size_step'])

            patch_from.set(config_dict['patch_size_from'])
            patch_to.set(config_dict['patch_size_to'])
            patch_step.set(config_dict['patch_size_step'])

            kernel_from.set(config_dict['kernel_size_from'])
            kernel_to.set(config_dict['kernel_size_to'])
            kernel_step.set(config_dict['kernel_size_step'])

            dice_from.set(config_dict['dice_range_from'])
            dice_to.set(config_dict['dice_range_to'])

            mask_num_int.set(config_dict['mask_num'])

            # iou_from.set(0.8)
            # iou_to.set(0.9)

            # hd_from.set(0.8)
            # hd_to.set(0.9)

        #  ------ 选择标注文件寸放文件夹 -------
        global choose_config_img
        choose_config_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        choose_config_btn = tk.Button(self,
                             image=choose_config_img, borderwidth=0, highlightthickness=0,
                             command=choose_config_path, relief="flat", text='选择已有超参数配置文件', 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(btn_font_size)))
        choose_config_btn.place(x=fair_btn_x, y=fair_btn_y + fair_btn_inter)
        choose_config_btn.place(width=btn_width, height=btn_height)

        
        mask_output_path = tkinter.StringVar()
        mask_output_path.set('../outputs')

        def mask_output_choose_path():
            file_path = tkinter.filedialog.askdirectory(title=u'Choose Metadata path',
                                                           initialdir=(os.path.expanduser(mask_output_path.get())))
            mask_output_path.set(file_path)
            print('Current chosen mask output path is: ', mask_input_path.get())

            output_blank.insert('insert',"\n")
            message = '已选择mask存放文件路径: ' + str(file_path)
            output_blank.insert('insert',message)
            separate_output()
            

        global choose_mask_output_img
        choose_mask_output_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        choose_mask_output_btn = tk.Button(self,
                             image=choose_mask_output_img, borderwidth=0, highlightthickness=0,
                             command=mask_output_choose_path, relief="flat", text='选择标注文件存放路径', 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(btn_font_size)))
        choose_mask_output_btn.place(x=fair_btn_x, y=fair_btn_y)
        choose_mask_output_btn.place(width=btn_width, height=btn_height)

        # ---------------------------------load mask----------------------------------------------------

        load_label_text = '查看文件'
        load_label_txt_x = output_x + 120 
        load_label_txt_x_ = load_label_txt_x +47
        load_label_txt_y = 310

        load_label_text = tk.Label(self,
            text=load_label_text, bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(23.0)))

        load_label_text.place(x=load_label_txt_x_+30, y=load_label_txt_y)

        thickness = 1
        length = 373
        rec_x = load_label_txt_x-65
        rec_y = load_label_txt_y+38
        canvas_deformation.create_rectangle(rec_x, rec_y, rec_x + length, rec_y + thickness, fill="#339999", outline="")
        
        
        mask_input_path = tkinter.StringVar()
        mask_input_path.set('../outputs/first')

        def load_mask():
            '''
            逻辑: 
            选择已产生结果的文件夹
            整体展示
            '''
            
            file_path = tkinter.filedialog.askdirectory(title=u'Choose mask path',
                                                           initialdir=(os.path.expanduser(mask_input_path.get())))
            mask_input_path.set(file_path)
            print('Current chosen mask output path is: ', mask_input_path.get())
            
        
        image_input_path = tkinter.StringVar()
        image_input_path.set('../images/BBox4Tumor_PreT_Raw_10099473.nii.gz')

        def load_image():
            '''
            逻辑: 
            选择MRI图像文件
            '''
            file_path = tkinter.filedialog.askopenfilename(title=u'Choose mask path',
                                                           initialdir=(os.path.expanduser(image_input_path.get())))
            image_input_path.set(file_path)

            print('Current chosen mask output path is: ', mask_input_path.get())
            mask_path = str(mask_input_path.get())
            image_path = str(image_input_path.get())

            dummy_list = ed.clean_list(os.listdir(mask_path))

            mask = nib.load(os.path.join(mask_path, dummy_list[0])).get_fdata()
            image = nib.load(image_path).get_fdata()

            tumor_index = ed.find_tumor_index(mask)
            rotate_angle = 90
            scale.set(tumor_index)
            if int(mask_num_entry.get()) == 5:
                mask1 = nib.load(os.path.join(mask_path, dummy_list[0])).get_fdata()
                mask2 = nib.load(os.path.join(mask_path, dummy_list[1])).get_fdata()
                mask3 = nib.load(os.path.join(mask_path, dummy_list[2])).get_fdata()
                mask4 = nib.load(os.path.join(mask_path, dummy_list[3])).get_fdata()
                mask5 = nib.load(os.path.join(mask_path, dummy_list[4])).get_fdata()

                image_vals = np.fliplr(rotate(image[:,:,tumor_index], rotate_angle))
                mask_vals1 = np.fliplr(rotate(mask1[:,:,tumor_index], rotate_angle))
                mask_vals2 = np.fliplr(rotate(mask2[:,:,tumor_index], rotate_angle))
                mask_vals3 = np.fliplr(rotate(mask3[:,:,tumor_index], rotate_angle))
                mask_vals4 = np.fliplr(rotate(mask4[:,:,tumor_index], rotate_angle))
                mask_vals5 = np.fliplr(rotate(mask5[:,:,tumor_index], rotate_angle))

                color1 = colorConverter.to_rgba('white',alpha=0.0)
                color2 = colorConverter.to_rgba('black',alpha=1)
                color3 = colorConverter.to_rgba('red',alpha=0.6)
                color4 = colorConverter.to_rgba('yellow',alpha=0.7)
                color5 = colorConverter.to_rgba('blue',alpha=0.9)
                color6 = colorConverter.to_rgba('green',alpha=0.8)
                color7 = colorConverter.to_rgba('orange',alpha=0.85)

                cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap1',[color2,color5],256)
                cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap2',[color1,color3],256)
                cmap3 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap3',[color1,color4],256)
                cmap4 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap4',[color1,color6],256)
                cmap5 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap5',[color1,color7],256)

                image_map = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',[color1,color2],256)

                fig = Figure()
                plot1 = fig.subplots()
                
                img1 = plot1.imshow(mask_vals1,interpolation='nearest',cmap=cmap1,origin='lower')
                img2 = plot1.imshow(mask_vals2,interpolation='nearest',cmap=cmap2,origin='lower')
                img3 = plot1.imshow(mask_vals3,interpolation='nearest',cmap=cmap3,origin='lower')
                img4 = plot1.imshow(mask_vals4,interpolation='nearest',cmap=cmap4,origin='lower')
                img5 = plot1.imshow(mask_vals5,interpolation='nearest',cmap=cmap5,origin='lower')
                img = plot1.imshow(image_vals,interpolation='nearest',cmap=image_map,origin='lower')

                canvas = FigureCanvasTkAgg(fig,master = self)
                fig.patch.set_facecolor('black')
                canvas.draw()
                # canvas.get_tk_widget().place(width = 330,y = 120)
               
                canvas.get_tk_widget().place(x = img_x+41,y = img_y+80)
            
    
        global load_mask_img
        load_btn_y = load_label_txt_y + 50
        load_mask_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        load_mask_btn = tk.Button(self,
                             image=load_mask_img, borderwidth=0, highlightthickness=0,
                             command=load_mask, relief="flat", text='选择标注文件', 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(btn_font_size)))
        load_mask_btn.place(x=fair_btn_x, y=load_btn_y)
        load_mask_btn.place(width=btn_width, height=btn_height)

        global load_image_img
        load_image_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        load_image_btn = tk.Button(self,
                             image=load_image_img, borderwidth=0, highlightthickness=0,
                             command=load_image, relief="flat", text='选择MRI图像文件', 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(23)))

        load_image_btn.place(x=fair_btn_x, y= load_btn_y + fair_btn_inter)
        load_image_btn.place(width=btn_width, height=btn_height)
        # -------------------------------------------------------------------------------------
        start_text = '开始处理标注文件'
        start_text_x = output_x + 140
        start_text_y = 460+73

        start_label_text = tk.Label(self,
            text=start_text, bg=bg_color,
            fg="#8FBEDF", font=("Arial-BoldMT", int(23.0)))

        start_label_text.place(x=start_text_x+14, y=start_text_y)

        thickness = 1
        length = 373
        rec_x = start_text_x-85
        rec_y = start_text_y+38
        canvas_deformation.create_rectangle(rec_x, rec_y, rec_x + length, rec_y + thickness, fill="#339999", outline="")

        

        start_btn.place(x=fair_btn_x, y=start_text_y + 50)
        start_btn.place(width=btn_width, height=btn_height)


        global cfm_img
        cfm_img = tk.PhotoImage(file="../GUI_material/empty.png")
        
        cfm_btn = tk.Button(self,
                             image=cfm_img, borderwidth=0, highlightthickness=0,
                             command=confirm, relief="flat", text='确认参数', 
                             fg = 'white',compound="center",font=("Arial-BoldMT", int(btn_font_size)))
        cfm_btn.place(x=label_x+22, y=label_y+6*label_inter-10)
        cfm_btn.place(width=btn_width, height=btn_height)

        # ------------------------------------ plot图像 --------------------------------------
        start_x = img_x-2
        start_y = img_y-2
        width_img = img_size+4

        canvas_deformation.create_rectangle(start_x, start_y, start_x+width_img, start_y+width_img, fill="#000000", outline="")
        
        # -----图像边框------
        canvas_deformation.create_line(start_x, start_y, start_x, start_y+width_img, fill='#8FBEDF')
        canvas_deformation.create_line(start_x, start_y, start_x+width_img, start_y, fill='#8FBEDF')
        canvas_deformation.create_line(start_x, start_y+width_img, start_x+width_img, start_y+width_img, fill='#8FBEDF')
        canvas_deformation.create_line(start_x+width_img, start_y, start_x+width_img, start_y+width_img, fill='#8FBEDF')
        
        # 展示 图像与标注分割结果, 仅是demo
        mask_path = '../Mask_folder/BBox4Tumor_PreT_Label_10099473.nii.gz'
        image_path = '../images/BBox4Tumor_PreT_Raw_10099473.nii.gz'
        mask = nib.load(mask_path).get_fdata()
        image = nib.load(image_path).get_fdata()
        x,y,z = mask.shape
        zvals = np.fliplr(rotate(mask[:,:,61], 90))
        zvals2 = np.fliplr(rotate(image[:,:,61], 90))
        zvals3 = np.fliplr(rotate(mask[:,:,62], 90))
        zvals4 = np.fliplr(rotate(mask[:,:,60], 90))

        color1 = colorConverter.to_rgba('white',alpha=0.0)
        color2 = colorConverter.to_rgba('black',alpha=1)
        color3 = colorConverter.to_rgba('red',alpha=0.6)
        color4 = colorConverter.to_rgba('yellow',alpha=0.7)
        color5 = colorConverter.to_rgba('blue',alpha=0.9)

        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',[color2,color5],256)
        cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap3',[color1,color3],256)
        cmap3 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap4',[color1,color4],256)

        image_map = mpl.colors.LinearSegmentedColormap.from_list('my_cmap2',[color1,color2],256)
   
        fig = Figure()
        plot1 = fig.subplots()
        # plot1.imshow(np.fliplr(rotate(mask[:,:,61], -90)),cmap='gray')
        img2 = plot1.imshow(zvals,interpolation='nearest',cmap=cmap1,origin='lower')
        img3 = plot1.imshow(zvals3,interpolation='nearest',cmap=cmap2,origin='lower')
        img5 = plot1.imshow(zvals4,interpolation='nearest',cmap=cmap3,origin='lower')
        img4 = plot1.imshow(zvals2,interpolation='nearest',cmap=image_map,origin='lower')

        canvas = FigureCanvasTkAgg(fig,master = self)
        fig.patch.set_facecolor('black')
        canvas.draw()
        # canvas.get_tk_widget().place(width = 330,y = 120)
        canvas.get_tk_widget().place(x = img_x+41,y = img_y+80)
        # ------------------------------------------------------------------------------------

        global zoom_bol
        zoom_bol = False

        def gun(ev=None):
            
            if zoom_bol:
                zoom_in()
            else:
                zoom_out()

        # ------------------ 滚动条 -------------------------
        global scale  # changed
        scale = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL, command=gun,bg = "#181A27",
        fg = '#FFFFFF')
        scale.set(54)
        scale.place(x=img_x-1, y=img_y + 483)
        scale.place(width=width_img-1)
        scale.configure(highlightbackground='#8FBEDF')
        scale.configure(highlightthickness = 0)

        # --------------------------- zoom -------------------

        def zoom_in():
            global zoom_bol
            zoom_bol = True
            mask_out_folder = str(mask_input_path.get())
            
            dummy_list = ed.clean_list(os.listdir(mask_out_folder))
            index = scale.get()
            image = nib.load(str(image_input_path.get())).get_fdata()
            
            if int(mask_num_entry.get()) == 5:
                mask1 = nib.load(os.path.join(mask_out_folder, dummy_list[0])).get_fdata()
                mask2 = nib.load(os.path.join(mask_out_folder, dummy_list[1])).get_fdata()
                mask3 = nib.load(os.path.join(mask_out_folder, dummy_list[2])).get_fdata()
                mask4 = nib.load(os.path.join(mask_out_folder, dummy_list[3])).get_fdata()
                mask5 = nib.load(os.path.join(mask_out_folder, dummy_list[4])).get_fdata()

                top,bottom,left,right = ed.get_border_3D(mask1)

                image_vals = np.fliplr(rotate(image[:,:,index][top:bottom, left:right], 90))
                mask_vals1 = np.fliplr(rotate(mask1[:,:,index][top:bottom, left:right], 90))
                mask_vals2 = np.fliplr(rotate(mask2[:,:,index][top:bottom, left:right], 90))
                mask_vals3 = np.fliplr(rotate(mask3[:,:,index][top:bottom, left:right], 90))
                mask_vals4 = np.fliplr(rotate(mask4[:,:,index][top:bottom, left:right], 90))
                mask_vals5 = np.fliplr(rotate(mask5[:,:,index][top:bottom, left:right], 90))

                color1 = colorConverter.to_rgba('white',alpha=0.0)
                color2 = colorConverter.to_rgba('black',alpha=1)
                color3 = colorConverter.to_rgba('red',alpha=0.6)
                color4 = colorConverter.to_rgba('yellow',alpha=0.95)
                color5 = colorConverter.to_rgba('blue',alpha=0.9)
                color6 = colorConverter.to_rgba('green',alpha=0.8)
                color7 = colorConverter.to_rgba('orange',alpha=0.85)

                cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap1',[color2,color5],256)
                cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap2',[color1,color3],256)
                cmap3 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap3',[color1,color4],256)
                cmap4 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap4',[color1,color6],256)
                cmap5 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap5',[color1,color7],256)

                image_map = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',[color1,color2],256)

                fig = Figure()
                plot1 = fig.subplots()
                # plot1.imshow(np.fliplr(rotate(mask[:,:,61], -90)),cmap='gray')
                img1 = plot1.imshow(mask_vals1,interpolation='nearest',cmap=cmap1,origin='lower')
                img2 = plot1.imshow(mask_vals2,interpolation='nearest',cmap=cmap2,origin='lower')
                img3 = plot1.imshow(mask_vals3,interpolation='nearest',cmap=cmap3,origin='lower')
                img4 = plot1.imshow(mask_vals4,interpolation='nearest',cmap=cmap4,origin='lower')
                img5 = plot1.imshow(mask_vals5,interpolation='nearest',cmap=cmap5,origin='lower')
                img = plot1.imshow(image_vals,interpolation='nearest',cmap=image_map,origin='lower')

                canvas = FigureCanvasTkAgg(fig,master = self)
                fig.patch.set_facecolor('black')
                canvas.draw()
                # canvas.get_tk_widget().place(width = 330,y = 120)
                canvas.get_tk_widget().place(x = img_x+41,y = img_y+80)

                print('Current index is: ',scale.get())
            print('In')

        def zoom_out():
            global zoom_bol
            zoom_bol = False
            mask_out_folder = str(mask_input_path.get())
            
            dummy_list = ed.clean_list(os.listdir(mask_out_folder))
            index = scale.get()
            image = nib.load(str(image_input_path.get())).get_fdata()
            
            if int(mask_num_entry.get()) == 5:
                mask1 = nib.load(os.path.join(mask_out_folder, dummy_list[0])).get_fdata()
                mask2 = nib.load(os.path.join(mask_out_folder, dummy_list[1])).get_fdata()
                mask3 = nib.load(os.path.join(mask_out_folder, dummy_list[2])).get_fdata()
                mask4 = nib.load(os.path.join(mask_out_folder, dummy_list[3])).get_fdata()
                mask5 = nib.load(os.path.join(mask_out_folder, dummy_list[4])).get_fdata()

                image_vals = np.fliplr(rotate(image[:,:,index], 90))
                mask_vals1 = np.fliplr(rotate(mask1[:,:,index], 90))
                mask_vals2 = np.fliplr(rotate(mask2[:,:,index], 90))
                mask_vals3 = np.fliplr(rotate(mask3[:,:,index], 90))
                mask_vals4 = np.fliplr(rotate(mask4[:,:,index], 90))
                mask_vals5 = np.fliplr(rotate(mask5[:,:,index], 90))

                color1 = colorConverter.to_rgba('white',alpha=0.0)
                color2 = colorConverter.to_rgba('black',alpha=1)
                color3 = colorConverter.to_rgba('red',alpha=0.6)
                color4 = colorConverter.to_rgba('yellow',alpha=0.95)
                color5 = colorConverter.to_rgba('blue',alpha=0.9)
                color6 = colorConverter.to_rgba('green',alpha=0.8)
                color7 = colorConverter.to_rgba('orange',alpha=0.85)

                cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap1',[color2,color5],256)
                cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap2',[color1,color3],256)
                cmap3 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap3',[color1,color4],256)
                cmap4 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap4',[color1,color6],256)
                cmap5 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap5',[color1,color7],256)

                image_map = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',[color1,color2],256)

                fig = Figure()
                plot1 = fig.subplots()
                # plot1.imshow(np.fliplr(rotate(mask[:,:,61], -90)),cmap='gray')
                img1 = plot1.imshow(mask_vals1,interpolation='nearest',cmap=cmap1,origin='lower')
                img2 = plot1.imshow(mask_vals2,interpolation='nearest',cmap=cmap2,origin='lower')
                img3 = plot1.imshow(mask_vals3,interpolation='nearest',cmap=cmap3,origin='lower')
                img4 = plot1.imshow(mask_vals4,interpolation='nearest',cmap=cmap4,origin='lower')
                img5 = plot1.imshow(mask_vals5,interpolation='nearest',cmap=cmap5,origin='lower')
                img = plot1.imshow(image_vals,interpolation='nearest',cmap=image_map,origin='lower')

                canvas = FigureCanvasTkAgg(fig,master = self)
                fig.patch.set_facecolor('black')
                canvas.draw()
                # canvas.get_tk_widget().place(width = 330,y = 120)
                canvas.get_tk_widget().place(x = img_x+41,y = img_y+80)

                print(scale.get())
            


        zoom_in_x = img_x+220
        zoom_in_y = img_y+445

        global zoom_in_img
        zoom_in_img = tk.PhotoImage(file="../GUI_material/in.png")
        
        in_btn = tk.Button(self,
                             image=zoom_in_img, borderwidth=0, highlightthickness=0,
                             command=zoom_in, relief="flat",
                             fg = 'white',compound="center")
        in_btn.place(x=zoom_in_x, y=zoom_in_y)
        in_btn.place(width=38, height=36)

        global zoom_out_img
        zoom_out_img = tk.PhotoImage(file="../GUI_material/out.png")
        
        out_btn = tk.Button(self,
                             image=zoom_out_img, borderwidth=0, highlightthickness=0,
                             command=zoom_out, relief="flat",
                             fg = 'white',compound="center")
        out_btn.place(x=zoom_in_x+50, y=zoom_in_y)
        out_btn.place(width=38, height=36)

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
            
                canvas_deformation.itemconfig(kk, state='normal')
                canvas_deformation.itemconfig(l1, state='normal')
                canvas_deformation.itemconfig(l2, state='normal')
                canvas_deformation.itemconfig(l3, state='normal')
                canvas_deformation.itemconfig(l4, state='normal')

                choose_config_text.place_forget()
                choose_mask_output_btn.place_forget()
                canvas_deformation.itemconfig(rec_config, state='hidden')
                
                switcher_.set(val*-1)

            else:
                gofair_btn.place_forget()
                gobreast_btn.place_forget()
                godeformation_btn.place_forget()
                radiomics_btn.place_forget()
                switcher_.set(val*-1)
                canvas_deformation.itemconfig(kk, state='hidden')
                canvas_deformation.itemconfig(l1, state='hidden')
                canvas_deformation.itemconfig(l2, state='hidden')
                canvas_deformation.itemconfig(l3, state='hidden')
                canvas_deformation.itemconfig(l4, state='hidden')
                canvas_deformation.itemconfig(rec_config, state='normal')

                choose_config_text.place(x=1220, y=90)
                choose_mask_output_btn.place(x=fair_btn_x, y=fair_btn_y)
                choose_mask_output_btn.place(width=btn_width, height=btn_height)

        label_inter = 70
        start_x = 1050
        bar_y = 29
        
        home_page=canvas_deformation.create_text(start_x, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='home_page')
        canvas_deformation.tag_bind(home_page, '<ButtonPress-1>', enter_home_page)   
        canvas_deformation.insert(home_page,1,"首页")

        about_us=canvas_deformation.create_text(start_x + label_inter, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='about_us_')
        canvas_deformation.tag_bind(about_us, '<ButtonPress-1>', enter_about_us)   
        canvas_deformation.insert(about_us,1,"关于我们")

        instruction=canvas_deformation.create_text(start_x + label_inter*4, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='instruction')
        canvas_deformation.tag_bind(instruction, '<ButtonPress-1>', enter_instruction)   
        canvas_deformation.insert(instruction,1,"软件介绍")

        contact=canvas_deformation.create_text(start_x + label_inter*5+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='contact')
        canvas_deformation.tag_bind(contact, '<ButtonPress-1>', enter_contact)   
        canvas_deformation.insert(contact,1,"联系方式")

        functions=canvas_deformation.create_text(start_x + label_inter*2+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='functions')
        canvas_deformation.tag_bind(functions, '<ButtonPress-1>', show_test)   
        canvas_deformation.insert(functions,1,"软件功能")

        
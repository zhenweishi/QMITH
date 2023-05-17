import tkinter as tk
import os
from PIL import Image, ImageTk
import GUI_Main as main



class Instruction(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller
        self.controller.title('MetaMedAI')
        self.controller.state('normal')
        

        self.controller.geometry('{}x{}'.format(main.width, main.height)) #页面大小
        self.controller.maxsize(1600,680)
        parent.pack_propagate(0)

        
        
        welcome_bg_color = "#2D2D2D"
        canvas_ins = tk.Canvas(
            self, bg=welcome_bg_color, height=main.height, width=main.width,
            bd=0, highlightthickness=0, relief="ridge")
        canvas_ins.place(x=0, y=0)


        global bg_img
        bg_img = ImageTk.PhotoImage(Image.open('../GUI_material/bg5.png'))
        #bg_img_resize = bg_img.subsample(1, 1)
        kk = canvas_ins.create_image(0, 0, image=bg_img)

        def enter_welcome():
            controller.show_frame('Welcome_Page')
        
        

        global back_btn_img4
        back_btn_img4 = tk.PhotoImage(file="../GUI_material/arrow2.png")
        back_btn4 = tk.Button(self,
            image=back_btn_img4, borderwidth=0, highlightthickness=0,
            command=enter_welcome, relief="flat")
        #back_btn4.place(x=5, y=7, width=48, height=36)


        thickness = 60
        length = main.width
        rec_x_ = 0
        rec_y_ = 0
        canvas_ins.create_rectangle(rec_x_, rec_y_, rec_x_ + length, rec_y_ + thickness, fill="#FFFFFF", outline="")

        # logo图像
        global logo_fair_ins
        logo_fair_ins = tk.PhotoImage(file="../GUI_material/icon6.png")
        logo_img = canvas_ins.create_image(200, 32, image=logo_fair_ins)

        metamedai=canvas_ins.create_text(163, 17,font=("Arial-BoldMT", 24),anchor="nw",fill = 'white',tags='home_page')   
        canvas_ins.insert(metamedai,1,"MetaMedAI")

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


        label_inter = 70
        start_x = 1050
        bar_y = 29
        text_color = '#000000'

        home_page=canvas_ins.create_text(start_x, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='home_page')
        canvas_ins.tag_bind(home_page, '<ButtonPress-1>', enter_home_page)   
        canvas_ins.insert(home_page,1,"首页")

        about_us=canvas_ins.create_text(start_x + label_inter, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='about_us_')
        canvas_ins.tag_bind(about_us, '<ButtonPress-1>', enter_about_us)   
        canvas_ins.insert(about_us,1,"关于我们")

        

        instruction=canvas_ins.create_text(start_x + label_inter*4, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='instruction')
        canvas_ins.tag_bind(instruction, '<ButtonPress-1>', enter_instruction)   
        canvas_ins.insert(instruction,1,"软件介绍")

        contact=canvas_ins.create_text(start_x + label_inter*5+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='contact')
        canvas_ins.tag_bind(contact, '<ButtonPress-1>', enter_contact)   
        canvas_ins.insert(contact,1,"联系方式")

        font_size = 22

        word_x = 150
        word_y = 140
        inter = 50

        line_x = 50
        line_length = main.width - line_x*2
        line_y = 615
        
        canvas_ins.create_line(line_x, line_y, line_x+line_length, line_y, fill='#C1C1C1')
        txtid9=canvas_ins.create_text(560, line_y + 15,font=("Arial-BoldMT", 14),anchor="nw",fill = '#C1C1C1')
        canvas_ins.insert(txtid9,1,"Copyright © 2021   广东省医学影像智能分析与应用重点实验室   All Rights Reserved. \n")


        line1=canvas_ins.create_text(word_x, word_y,font=("Arial-BoldMT", font_size),anchor="nw",fill = 'white')
        canvas_ins.insert(line1,1,"MetaMedAI (MMA)旨在利用医学和人工智能知识来描述、解释、指导和开发医学人工智能系统，尤为关注医疗保健领域。\n")
        line2=canvas_ins.create_text(word_x, word_y + inter*1,font=("Arial-BoldMT", font_size),anchor="nw",fill = 'white')
        canvas_ins.insert(line2,1,"MMA是一款集成软件，涉及以下功能模块: \n")
        txtid3=canvas_ins.create_text(word_x, word_y + inter*2,font=("Arial-BoldMT", font_size),anchor="nw",fill = 'white')
        canvas_ins.insert(txtid3,1,"     1. MMA-FAIR Image: 基于FAIR数据准则，可实现医学影像数据标准化。为科学化医学数据管理提供技术支持，为多中心研究提供数据保障。\n")
        txtid4=canvas_ins.create_text(word_x, word_y + inter*3,font=("Arial-BoldMT", font_size),anchor="nw",fill = 'white')
        canvas_ins.insert(txtid4,1,"     2. MMA-Breast: 针对于乳腺癌预防、筛查、诊断、分级以及预后预测缺乏易用、精准量化工具，MMA-Breast可实现:\n")
        txtid5=canvas_ins.create_text(word_x, word_y + inter*4,font=("Arial-BoldMT", font_size),anchor="nw",fill = 'white')
        canvas_ins.insert(txtid5,1,"          （1）乳腺癌DCE-MRI图像的自动结构化解析，包括乳腺分割、腺体分割、肿瘤分割和瘤周定位。\n")
        txtid10=canvas_ins.create_text(word_x, word_y + inter*5,font=("Arial-BoldMT", font_size),anchor="nw",fill = 'white')
        canvas_ins.insert(txtid10,1,"          （2）自动化BPE、SER、FTV等定量计算。\n")
        txtid6=canvas_ins.create_text(word_x, word_y + inter*6,font=("Arial-BoldMT", font_size),anchor="nw",fill = 'white')
        canvas_ins.insert(txtid6,1,"     3. MMA-Lung: 可实现肺癌结构化解析，包括肺部分割、肿瘤分割等。\n")
        txtid7=canvas_ins.create_text(word_x, word_y + inter*7,font=("Arial-BoldMT", font_size),anchor="nw",fill = 'white')
        canvas_ins.insert(txtid7,1,"     4. MMA-Radiomics: 可实现（1）影像组学手工特征提取；（2）影像组学深度特征提取；\n")
        txtid8=canvas_ins.create_text(word_x, word_y + inter*8,font=("Arial-BoldMT", font_size),anchor="nw",fill = 'white')
        canvas_ins.insert(txtid8,1,"MetaMedAI支持常用操作系统（Windows，Mac OS，Linux)。MetaMedAI 仅用于非商业用途。\n")

        
      
        global box_img4
        box_img4 = ImageTk.PhotoImage(Image.open('../GUI_material/box2.png'))
        kk = canvas_ins.create_image(main.box_x, main.box_y, image=box_img4)
        l1 = canvas_ins.create_line(1230, 102, 1350, 102, fill='#E0E0E0')
        l2 = canvas_ins.create_line(1230, 131, 1350, 131, fill='#E0E0E0')
        l3 = canvas_ins.create_line(1230, 138+23, 1350, 138+23, fill='#E0E0E0')
        l4 = canvas_ins.create_line(1230, 138+23*2+5, 1350, 138+23*2+5, fill='#E0E0E0')
        # #E0E0E0
        canvas_ins.itemconfig(kk, state='hidden')
        canvas_ins.itemconfig(l1, state='hidden')
        canvas_ins.itemconfig(l2, state='hidden')
        canvas_ins.itemconfig(l3, state='hidden')
        canvas_ins.itemconfig(l4, state='hidden')
        
        

        def no():
            print('Worked!!!!')

        def enter_fair():
            controller.show_frame('FAIR')

        def enter_rad():
            controller.show_frame('Radiomics')
        
        def enter_deformation():                  
            controller.show_frame('Deformation')

        # 下拉按钮
        global blank_img14
        blank_img14 = tk.PhotoImage(file="../GUI_material/blank.png")
        
        gofair_btn = tk.Button(self,
                             image=blank_img14, borderwidth=0, highlightthickness=0,
                             command=enter_fair, relief="flat", text="MMA-FAIR Image", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))
        
        global blank_img24
        blank_img24 = tk.PhotoImage(file="../GUI_material/blank.png")
        
        gobreast_btn = tk.Button(self,
                             image=blank_img24, borderwidth=0, highlightthickness=0,
                             command=enter_bpe, relief="flat", text="MMA-Breast", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))

        global blank_img34
        blank_img34 = tk.PhotoImage(file="../GUI_material/blank.png")
        
        godeformation_btn = tk.Button(self,
                             image=blank_img34, borderwidth=0, highlightthickness=0,
                             command=enter_deformation, relief="flat", text="MMA-Deform", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))

        global blank_img44
        blank_img44 = tk.PhotoImage(file="../GUI_material/blank.png")
        radiomics_btn = tk.Button(self,
                             image=blank_img44, borderwidth=0, highlightthickness=0,
                             command=enter_rad, relief="flat", text="MMA-Radiomics", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))

        
        switcher_ = tk.StringVar()
        switcher_.set(-1)

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
                
                canvas_ins.itemconfig(kk, state='normal')
                canvas_ins.itemconfig(l1, state='normal')
                canvas_ins.itemconfig(l2, state='normal')
                canvas_ins.itemconfig(l3, state='normal')
                canvas_ins.itemconfig(l4, state='normal')
                
                switcher_.set(val*-1)

            else:
                gofair_btn.place_forget()
                gobreast_btn.place_forget()
                godeformation_btn.place_forget()
                radiomics_btn.place_forget()
                
                switcher_.set(val*-1)
                canvas_ins.itemconfig(kk, state='hidden')
                canvas_ins.itemconfig(l1, state='hidden')
                canvas_ins.itemconfig(l2, state='hidden')
                canvas_ins.itemconfig(l3, state='hidden')
                canvas_ins.itemconfig(l4, state='hidden')

        functions=canvas_ins.create_text(start_x + label_inter*2+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='functions')
        canvas_ins.tag_bind(functions, '<ButtonPress-1>', show_test)   
        canvas_ins.insert(functions,1,"软件功能")
import tkinter as tk
import os
from PIL import Image, ImageTk
import GUI_Main as main



class About_Us(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller
        self.controller.title('MetaMedAI')
        self.controller.state('normal')
        

        self.controller.geometry('{}x{}'.format(main.width, main.height)) #页面大小
        self.controller.maxsize(1600,680)
        parent.pack_propagate(0)

        def enter_welcome():
            controller.show_frame('Welcome_Page')
        
        
        welcome_bg_color = "#2D2D2D"
        canvas_about = tk.Canvas(
            self, bg=welcome_bg_color, height=main.height, width=main.width,
            bd=0, highlightthickness=0, relief="ridge")
        canvas_about.place(x=0, y=0)

        

        global bg_img
        bg_img = ImageTk.PhotoImage(Image.open('../GUI_material/bg5.png'))
        #bg_img_resize = bg_img.subsample(1, 1)
        kk = canvas_about.create_image(0, 0, image=bg_img)


        thickness = 60
        length = main.width
        rec_x_ = 0
        rec_y_ = 0
        canvas_about.create_rectangle(rec_x_, rec_y_, rec_x_ + length, rec_y_ + thickness, fill="#FFFFFF", outline="")

        # logo图像
        global logo_fair
        logo_fair = tk.PhotoImage(file="../GUI_material/icon6.png")
        logo_img = canvas_about.create_image(200, 32, image=logo_fair)

        metamedai=canvas_about.create_text(163, 17,font=("Arial-BoldMT", 24),anchor="nw",fill = 'white',tags='home_page')   
        canvas_about.insert(metamedai,1,"MetaMedAI")

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
        

        home_page=canvas_about.create_text(start_x, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='home_page')
        canvas_about.tag_bind(home_page, '<ButtonPress-1>', enter_home_page)   
        canvas_about.insert(home_page,1,"首页")

        about_us=canvas_about.create_text(start_x + label_inter, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='about_us_')
        canvas_about.tag_bind(about_us, '<ButtonPress-1>', enter_about_us)   
        canvas_about.insert(about_us,1,"关于我们")

        instruction=canvas_about.create_text(start_x + label_inter*4, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='instruction')
        canvas_about.tag_bind(instruction, '<ButtonPress-1>', enter_instruction)   
        canvas_about.insert(instruction,1,"软件介绍")

        contact=canvas_about.create_text(start_x + label_inter*5+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='contact')
        canvas_about.tag_bind(contact, '<ButtonPress-1>', enter_contact)   
        canvas_about.insert(contact,1,"联系方式")
        
        output_x = 540
        output_y = 180

        # canvas_about.create_rectangle(output_x, output_y, output_x + 1030, output_y + 450, fill='#747474', outline="")
        
        
        t1_f = '广东省人民医院'
        t1_b = '是一所三级甲等医院,作为华南地区最大的综合性医院之一,项目依托单位创建于'
        t2 = '1946年,是广东省最大的综合性医院,是国内规模最大、综合实力最强的医院之一。广东省人民'
        t3 = '医院放射科配置有双源CT、256层CT、128层CT、64层CT扫描仪多套。'
        t4_f = '广东省医学影像智能分析与应用重点实验室'
        t4_b = '是一支具有鲜明医工交叉特色的研究队伍, 有分别来'
        t5 = '自于影像学、病理学、肿瘤学、计算机科学与技术、生物医学工程等专业的人才。其中, 团队有'
        t6 = '工科博士后5名、工科博士3名、工科硕士10余名,为团队提供全面的算法支撑; 医学博士后3名'
        t7 = '医学博士5名, 医学硕士20余名, 为团队提供临床的支持。实验室配备高性能计算集群; 另有高端'
        t8 = '图像处理工作站50套, Nvidia高端型号显卡 RTX3090、RTX3080数十张。以上工作条件为实验'
        t9 = '室科研项目的数据获取、处理以及为深度学习提供了强大的计算力支持。'
        t1_x = output_x + 50
        t1_y = output_y+35
        ty_inter = 40
        up = 15
        canvas_about.create_text(t1_x, t1_y - up, anchor='w',text=t1_f,font=('Arial-BoldMT', 22),fill = '#FFFFFF')
        canvas_about.create_text(t1_x+155, t1_y- up, anchor='w',text=t1_b,font=('bold', 22),fill = '#FFFFFF')
        canvas_about.create_text(t1_x, t1_y+ty_inter- up, anchor='w',text=t2,font=('bold', 22),fill = '#FFFFFF')
        canvas_about.create_text(t1_x, t1_y+2*ty_inter- up, anchor='w',text=t3,font=('bold', 22),fill = '#FFFFFF')
        canvas_about.create_text(t1_x, t1_y+5*ty_inter- up*2, anchor='w',text=t4_f,font=('Arial-BoldMT', 22),fill = '#FFFFFF')
        canvas_about.create_text(t1_x+419, t1_y+5*ty_inter- up*2, anchor='w',text=t4_b,font=('bold', 22),fill = '#FFFFFF')
        canvas_about.create_text(t1_x, t1_y+6*ty_inter- up*2, anchor='w',text=t5,font=('bold', 22),fill = '#FFFFFF')
        canvas_about.create_text(t1_x, t1_y+7*ty_inter- up*2, anchor='w',text=t6,font=('bold', 22),fill = '#FFFFFF')
        canvas_about.create_text(t1_x, t1_y+8*ty_inter- up*2, anchor='w',text=t7,font=('bold', 22),fill = '#FFFFFF')
        canvas_about.create_text(t1_x, t1_y+9*ty_inter- up*2, anchor='w',text=t8,font=('bold', 22),fill = '#FFFFFF')
        canvas_about.create_text(t1_x, t1_y+10*ty_inter- up*2, anchor='w',text=t9,font=('bold', 22),fill = '#FFFFFF')

        

        txt_y = 100
        line_txt_y_inter = 50

        workers_x = 140
        move_right = 30

        workers_txt=canvas_about.create_text(workers_x + move_right, txt_y,font=("Arial-BoldMT", int(35.0)),anchor="nw",fill = '#6FACB5')
        canvas_about.insert(workers_txt,1,"软件开发人员\n")

        canvas_about.create_line(workers_x-5+ move_right, txt_y + line_txt_y_inter, 353+ move_right, txt_y + line_txt_y_inter, fill='#6FACB5')

        company_txt = canvas_about.create_text(950, txt_y,font=("Arial-BoldMT", int(35.0)),anchor="nw",fill = '#6FACB5')
        canvas_about.insert(company_txt,1,"软件开发单位\n")

        canvas_about.create_line(945, txt_y + line_txt_y_inter, 1162, txt_y + line_txt_y_inter, fill='#6FACB5')

        photo_width = 120
        photo_height = 160

        row1_x = 130
        row1_y = 255
        row2_y = 500
        x_inter = 220

        szw = '石镇维'
        lzy = '刘再毅'
        lch = '梁长虹'
        ltc = '罗天琛'
        canvas_about.create_text(100+ move_right, 365, anchor='w',text=szw,font=("Arial-BoldMT", 21),fill = '#FFFFFF')
        canvas_about.create_text(320+ move_right, 365, anchor='w',text=lzy,font=('Arial-BoldMT', 21),fill = '#FFFFFF')
        canvas_about.create_text(100+ move_right, 610, anchor='w',text=lch,font=('Arial-BoldMT', 21),fill = '#FFFFFF')
        canvas_about.create_text(320+ move_right, 610, anchor='w',text=ltc,font=('Arial-BoldMT', 21),fill = '#FFFFFF')
        

        global szw_img
        szw_img = ImageTk.PhotoImage(Image.open('../GUI_material/szw.png').resize((photo_width,photo_height)))
        canvas_about.create_image(row1_x+ move_right, row1_y, image=szw_img)

        global lzy_img
        lzy_img = ImageTk.PhotoImage(Image.open('../GUI_material/lzy.png').resize((photo_width,photo_height)))
        canvas_about.create_image(row1_x + x_inter+ move_right, row1_y, image=lzy_img)

        global lch_img
        lch_img = ImageTk.PhotoImage(Image.open('../GUI_material/lch.png').resize((photo_width,photo_height)))
        canvas_about.create_image(row1_x+ move_right, row2_y, image=lch_img)

        global ltc_img
        ltc_img = ImageTk.PhotoImage(Image.open('../GUI_material/ltc.png').resize((photo_width,photo_height)))
        canvas_about.create_image(row1_x + x_inter+ move_right, row2_y, image=ltc_img)

        

        

        global box_img2
        box_img2 = ImageTk.PhotoImage(Image.open('../GUI_material/box2.png'))
        kk = canvas_about.create_image(main.box_x, main.box_y, image=box_img2)
        l1 = canvas_about.create_line(1230, 102, 1350, 102, fill='#E0E0E0')
        l2 = canvas_about.create_line(1230, 131, 1350, 131, fill='#E0E0E0')
        l3 = canvas_about.create_line(1230, 138+23, 1350, 138+23, fill='#E0E0E0')
        l4 = canvas_about.create_line(1230, 138+23*2+5, 1350, 138+23*2+5, fill='#E0E0E0')
        # #E0E0E0
        canvas_about.itemconfig(kk, state='hidden')
        canvas_about.itemconfig(l1, state='hidden')
        canvas_about.itemconfig(l2, state='hidden')
        canvas_about.itemconfig(l3, state='hidden')
        canvas_about.itemconfig(l4, state='hidden')

        
        

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

                canvas_about.itemconfig(kk, state='normal')
                canvas_about.itemconfig(l1, state='normal')
                canvas_about.itemconfig(l2, state='normal')
                canvas_about.itemconfig(l3, state='normal')
                canvas_about.itemconfig(l4, state='normal')
                
                switcher_.set(val*-1)

            else:
                gofair_btn.place_forget()
                gobreast_btn.place_forget()
                godeformation_btn.place_forget()
                arrow_label.place_forget()
                radiomics_btn.place_forget()
                switcher_.set(val*-1)
                canvas_about.itemconfig(kk, state='hidden')
                canvas_about.itemconfig(l1, state='hidden')
                canvas_about.itemconfig(l2, state='hidden')
                canvas_about.itemconfig(l3, state='hidden')
                canvas_about.itemconfig(l4, state='hidden')

        functions=canvas_about.create_text(start_x + label_inter*2+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='functions')
        canvas_about.tag_bind(functions, '<ButtonPress-1>', show_test)   
        canvas_about.insert(functions,1,"软件功能")
        

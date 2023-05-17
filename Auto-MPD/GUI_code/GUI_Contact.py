import tkinter as tk
import os
from PIL import Image, ImageTk
import GUI_Main as main
import webbrowser



class Contact(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller
        self.controller.title('MetaMedAI')
        self.controller.state('normal')
        

        self.controller.geometry('{}x{}'.format(main.width, main.height)) #页面大小
        self.controller.maxsize(1600,680)
        parent.pack_propagate(0)

        
        
        welcome_bg_color = "#2D2D2D"
        canvas_contact = tk.Canvas(
            self, bg=welcome_bg_color, height=main.height, width=main.width,
            bd=0, highlightthickness=0, relief="ridge")
        canvas_contact.place(x=0, y=0)


        global bg_img
        bg_img = ImageTk.PhotoImage(Image.open('../GUI_material/bg5.png'))
        #bg_img_resize = bg_img.subsample(1, 1)
        kk = canvas_contact.create_image(0, 0, image=bg_img)

        thickness = 60
        length = main.width
        rec_x_ = 0
        rec_y_ = 0
        canvas_contact.create_rectangle(rec_x_, rec_y_, rec_x_ + length, rec_y_ + thickness, fill="#FFFFFF", outline="")

        # logo图像
        global logo_fair
        logo_fair = tk.PhotoImage(file="../GUI_material/icon6.png")
        logo_img = canvas_contact.create_image(200, 32, image=logo_fair)

        metamedai=canvas_contact.create_text(163, 17,font=("Arial-BoldMT", 24),anchor="nw",fill = 'white',tags='home_page')   
        canvas_contact.insert(metamedai,1,"MetaMedAI")

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

        home_page=canvas_contact.create_text(start_x, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='home_page')
        canvas_contact.tag_bind(home_page, '<ButtonPress-1>', enter_home_page)   
        canvas_contact.insert(home_page,1,"首页")

        about_us=canvas_contact.create_text(start_x + label_inter, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='about_us_')
        canvas_contact.tag_bind(about_us, '<ButtonPress-1>', enter_about_us)   
        canvas_contact.insert(about_us,1,"关于我们")


        instruction=canvas_contact.create_text(start_x + label_inter*4, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='instruction')
        canvas_contact.tag_bind(instruction, '<ButtonPress-1>', enter_instruction)   
        canvas_contact.insert(instruction,1,"软件介绍")

        contact=canvas_contact.create_text(start_x + label_inter*5+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='contact')
        canvas_contact.tag_bind(contact, '<ButtonPress-1>', enter_contact)   
        canvas_contact.insert(contact,1,"联系方式")

        global box_img3
        box_img3 = ImageTk.PhotoImage(Image.open('../GUI_material/box2.png'))
        kk = canvas_contact.create_image(main.box_x, main.box_y, image=box_img3)
        l1 = canvas_contact.create_line(1230, 102, 1350, 102, fill='#E0E0E0')
        l2 = canvas_contact.create_line(1230, 131, 1350, 131, fill='#E0E0E0')
        l3 = canvas_contact.create_line(1230, 138+23, 1350, 138+23, fill='#E0E0E0')
        l4 = canvas_contact.create_line(1230, 138+23*2+5, 1350, 138+23*2+5, fill='#E0E0E0')
        # #E0E0E0
        canvas_contact.itemconfig(kk, state='hidden')
        canvas_contact.itemconfig(l1, state='hidden')
        canvas_contact.itemconfig(l2, state='hidden')
        canvas_contact.itemconfig(l3, state='hidden')
        canvas_contact.itemconfig(l4, state='hidden')


        word_x = 750
        word_y = 250
        inter = 50

        move_right = 80

        szw = '联系人: 石镇维'
        company1 = '单位: 广东省人民医院'
        company2 = '             广东省医学影像智能分析与应用重点实验室'
        mail = '邮件: zhenwei_shi88@163.com'
        font_size = 23
        canvas_contact.create_text(word_x+move_right, word_y, anchor='w',text=szw,font=('bold', font_size),fill = '#FFFFFF')
        canvas_contact.create_text(word_x+move_right, word_y+inter, anchor='w',text=company1,font=('bold', font_size),fill = '#FFFFFF')
        canvas_contact.create_text(word_x+move_right, word_y+inter*2, anchor='w',text=company2,font=('bold', font_size),fill = '#FFFFFF')
        canvas_contact.create_text(word_x+move_right, word_y+inter*3, anchor='w',text=mail,font=('bold', font_size),fill = '#FFFFFF')
        
        global szw_img1
        szw_img1 = ImageTk.PhotoImage(Image.open('../GUI_material/szw1.png'))
        canvas_contact.create_image(600+move_right, 350, image=szw_img1)

        def callback(url):
            webbrowser.open_new(url)

        icon_x = 765+move_right
        icon_x_inter = 40

        global gh
        gh = ImageTk.PhotoImage(Image.open('../GUI_material/gh.png').resize((30,30)))
        github_icon = canvas_contact.create_image(icon_x, 450, image=gh,tags='gh')
        canvas_contact.tag_bind(github_icon, "<Button-1>", lambda e: callback("https://github.com/zhenweishi/MetaMedAI"))

        global rg
        rg = ImageTk.PhotoImage(Image.open('../GUI_material/rg.png').resize((30,30)))
        research_icon = canvas_contact.create_image(icon_x + icon_x_inter, 450, image=rg,tags='gh')
        canvas_contact.tag_bind(research_icon, "<Button-1>", lambda e: callback("https://www.researchgate.net/profile/Z-Shi-5"))

        global gs
        gs = ImageTk.PhotoImage(Image.open('../GUI_material/gs.png').resize((30,30)))
        google_icon = canvas_contact.create_image(icon_x + icon_x_inter*2, 450, image=gs,tags='gs')
        canvas_contact.tag_bind(google_icon, "<Button-1>", lambda e: callback("https://scholar.google.com/citations?user=aeK2yRsAAAAJ&hl=en"))

        def enter_rad():
            controller.show_frame('Radiomics')
        
        def no():
            print('Worked!!!!')

        def enter_fair():
            controller.show_frame('FAIR')

        def enter_deformation():                  
            controller.show_frame('Deformation')
        

        # 下拉按钮
        global blank_img13
        blank_img13 = tk.PhotoImage(file="../GUI_material/blank.png")
        
        gofair_btn = tk.Button(self,
                             image=blank_img13, borderwidth=0, highlightthickness=0,
                             command=enter_fair, relief="flat", text="MMA-FAIR Image", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))
        
        global blank_img23
        blank_img23 = tk.PhotoImage(file="../GUI_material/blank.png")
        
        gobreast_btn = tk.Button(self,
                             image=blank_img23, borderwidth=0, highlightthickness=0,
                             command=enter_bpe, relief="flat", text="MMA-Breast", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))

        global blank_img33
        blank_img33 = tk.PhotoImage(file="../GUI_material/blank.png")
        
        godeformation_btn = tk.Button(self,
                             image=blank_img33, borderwidth=0, highlightthickness=0,
                             command=enter_deformation, relief="flat", text="MMA-Deform", 
                             fg = '#000000',compound="center",font=("Arial-BoldMT", int(13)))

        global blank_img43
        blank_img43 = tk.PhotoImage(file="../GUI_material/blank.png")
        radiomics_btn = tk.Button(self,
                             image=blank_img43, borderwidth=0, highlightthickness=0,
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

                
                canvas_contact.itemconfig(kk, state='normal')
                canvas_contact.itemconfig(l1, state='normal')
                canvas_contact.itemconfig(l2, state='normal')
                canvas_contact.itemconfig(l3, state='normal')
                canvas_contact.itemconfig(l4, state='normal')
                
                switcher_.set(val*-1)

            else:
                gofair_btn.place_forget()
                gobreast_btn.place_forget()
                godeformation_btn.place_forget()
                radiomics_btn.place_forget()
                switcher_.set(val*-1)
                canvas_contact.itemconfig(kk, state='hidden')
                canvas_contact.itemconfig(l1, state='hidden')
                canvas_contact.itemconfig(l2, state='hidden')
                canvas_contact.itemconfig(l3, state='hidden')
                canvas_contact.itemconfig(l4, state='hidden')

        functions=canvas_contact.create_text(start_x + label_inter*2+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='functions')
        canvas_contact.tag_bind(functions, '<ButtonPress-1>', show_test)   
        canvas_contact.insert(functions,1,"软件功能")

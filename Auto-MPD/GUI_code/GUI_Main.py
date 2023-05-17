'''
# -*- coding: utf-8 -*-
@author: Tianchen Luo: ltc8498@gmail.com
"export PATH="$(pwd)/dcmqi_mac/bin":$PATH"
'''
import tkinter as tk
from tkinter import *
import GUI_FAIR as fair
import GUI_AboutUs as us
import GUI_Instruction as ins
import GUI_Contact as contact
import GUI_BPE as bpe
import GUI_Radiomics as rad
import GUI_Deformation as df
import os
from PIL import Image, ImageTk

# 页面画布，同尺寸
width = 1600
height = 680
box_x = 1290
box_y = 127

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self, width=500, height=250)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_propagate(0)
        container.pack_propagate(0)
        self.frames = {}

        # 在下面添加新的页面
        for F in (Welcome_Page,rad.Radiomics,fair.FAIR, us.About_Us,ins.Instruction,contact.Contact,bpe.BPE, df.Deformation):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid_propagate(0) 
            frame.grid(row=0, column=0, sticky="nsew")
            

        self.show_frame("Welcome_Page")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Welcome_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller
        self.controller.title('MetaMedAI')
        self.controller.state('normal')
        

        self.controller.geometry('{}x{}'.format(width, height)) #页面大小
        self.controller.maxsize(1600,700)
        parent.pack_propagate(0)
        
        
        welcome_bg_color = "#2D2D2D"
        canvas = tk.Canvas(
            self, bg=welcome_bg_color, height=height, width=width,
            bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        left_x = 100
        left_welcome_y = 200
        left_word = left_welcome_y + 100
        left_inter = 40

        global bg_img
        bg_img = ImageTk.PhotoImage(Image.open('../GUI_material/bg5.png'))
        #bg_img_resize = bg_img.subsample(1, 1)
        kk = canvas.create_image(0, 0, image=bg_img)

        thickness = 60
        length = width
        rec_x = 0
        rec_y = 0
        canvas.create_rectangle(rec_x, rec_y, rec_x + length, rec_y + thickness, fill="#FFFFFF", outline="")

        # ------------ 右上角功能栏 -----------
        

        # logo图像
        global logo
        logo = tk.PhotoImage(file="../GUI_material/icon6.png")
        logo_img = canvas.create_image(200, 32, image=logo)
        
        metamedai=canvas.create_text(163, 17,font=("Arial-BoldMT", 24),anchor="nw",fill = 'white',tags='home_page')   
        canvas.insert(metamedai,1,"MetaMedAI")

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
            controller.show_frame('Deformation')


        label_inter = 70
        start_x = 1050
        bar_y = 29
        
        text_color = '#000000'
        
        home_page=canvas.create_text(start_x, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='home_page')
        canvas.tag_bind(home_page, '<ButtonPress-1>', enter_home_page)   
        canvas.insert(home_page,1,"首页")

        about_us=canvas.create_text(start_x + label_inter, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='about_us_')
        canvas.tag_bind(about_us, '<ButtonPress-1>', enter_about_us)   
        canvas.insert(about_us,1,"关于我们")

        

        instruction=canvas.create_text(start_x + label_inter*4, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='instruction')
        canvas.tag_bind(instruction, '<ButtonPress-1>', enter_instruction)   
        canvas.insert(instruction,1,"软件介绍")

        contact=canvas.create_text(start_x + label_inter*5+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='contact')
        canvas.tag_bind(contact, '<ButtonPress-1>', enter_contact)   
        canvas.insert(contact,1,"联系方式")


        txtid=canvas.create_text(left_x+30+30, left_word,font=("Arial-BoldMT", 35),anchor="nw",fill = 'white')
        canvas.insert(txtid,1,"医学影像人工智能改善生命健康 \n\n")
        txtid3=canvas.create_text(left_x-50+30, left_word + 2* left_inter,font=("Arial-BoldMT", 35),anchor="nw",fill = 'white')
        canvas.insert(txtid3,1,"赋能医疗健康 赋能科学研究 赋能临床应用 \n\n")
        txtid5=canvas.create_text(left_x+35+30, left_word + 4* left_inter,font=("Arial-BoldMT", 35),anchor="nw",fill = 'white')
        canvas.insert(txtid5,1,"MetaMedAI源自临床回归临床\n\n")
        txtid6=canvas.create_text(left_x-5+30, left_welcome_y-3,font=("Arial-BoldMT", int(50.0)),anchor="nw",fill = '#6FACB5')
        canvas.insert(txtid6,1,"欢迎使用MetaMedAI软件\n")

        spot=canvas.create_text(1130, 200,font=("Arial-BoldMT", 35),anchor="nw",fill = '#6FACB5')  
        canvas.insert(spot,1,"三大亮点")

        canvas.create_line(1150, 255, 1250, 255, fill='#6FACB5')

        
        # logo图像
        global charac_resize
        charac = tk.PhotoImage(file="../GUI_material/charac.png")
        charac_resize = charac.subsample(1,1)
        canvas.create_image(1200, 400, image=charac_resize)

        global box_img
        box_img = ImageTk.PhotoImage(Image.open('../GUI_material/box2.png'))
        kk = canvas.create_image(box_x, box_y, image=box_img)
        l1 = canvas.create_line(1230, 102, 1350, 102, fill='#E0E0E0')
        l2 = canvas.create_line(1230, 131, 1350, 131, fill='#E0E0E0')
        l3 = canvas.create_line(1230, 138+23, 1350, 138+23, fill='#E0E0E0')
        l4 = canvas.create_line(1230, 138+23*2+5, 1350, 138+23*2+5, fill='#E0E0E0')
        # #E0E0E0
        canvas.itemconfig(kk, state='hidden')
        canvas.itemconfig(l1, state='hidden')
        canvas.itemconfig(l2, state='hidden')
        canvas.itemconfig(l3, state='hidden')
        canvas.itemconfig(l4, state='hidden')

        def no():
            print('Worked!!!!')

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
            
                canvas.itemconfig(kk, state='normal')
                canvas.itemconfig(l1, state='normal')
                canvas.itemconfig(l2, state='normal')
                canvas.itemconfig(l3, state='normal')
                canvas.itemconfig(l4, state='normal')
                
                switcher_.set(val*-1)

            else:
                gofair_btn.place_forget()
                gobreast_btn.place_forget()
                godeformation_btn.place_forget()
                radiomics_btn.place_forget()
                switcher_.set(val*-1)
                canvas.itemconfig(kk, state='hidden')
                canvas.itemconfig(l1, state='hidden')
                canvas.itemconfig(l2, state='hidden')
                canvas.itemconfig(l3, state='hidden')
                canvas.itemconfig(l4, state='hidden')

        functions=canvas.create_text(start_x + label_inter*2+35, bar_y,font=("Arial-BoldMT", 17),anchor="nw",fill = text_color,tags='functions')
        canvas.tag_bind(functions, '<ButtonPress-1>', show_test)   
        canvas.insert(functions,1,"软件功能")

       


        


if __name__ == "__main__":
    print('-------------欢迎使用MetaMedAI实验版本---------------')
    app = SampleApp()
    app.mainloop()

    
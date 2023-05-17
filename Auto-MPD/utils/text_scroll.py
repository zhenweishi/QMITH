import tkinter

wuya = tkinter.Tk()
wuya.title("wuya")
wuya.geometry("300x50+10+20")

# 创建滚动条
scroll = tkinter.Scrollbar()
# 创建文本框text，设置宽度100，high不是高度，是文本显示的行数设置为3行
text = tkinter.Text(wuya)
# 将滚动条填充
scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y) # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
text.pack(side=tkinter.LEFT,fill=tkinter.Y) # 将文本框填充进wuya窗口的左侧，
# 将滚动条与文本框关联
scroll.config(command=text.yview) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
text.config(yscrollcommand=scroll.set) # 将滚动条关联到文本框

# 设置文本框内容
txt = 'China urges the U.S. to abide by the one-China principle and the principles of the three Sino-U.S.' \
      ' Joint Communiques, and stop all forms of military contact with Taiwan including arms sales, Wu said.'
# 将文本内容插入文本框
text.insert('insert',txt)



wuya.mainloop()
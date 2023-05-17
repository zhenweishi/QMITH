from tkinter import *  # 导入窗口控件
from tkinter import ttk
root=Tk () #创建窗口
root.title("label-test")
root.geometry("800x900+300+100") #小写x代表乘号500x400为窗口大小，+500+300窗口显示位置
root.columnconfigure(0, weight=1)
tree = ttk.Treeview(root, show="headings") #表格第一列不显示
tree.grid(row=1, columnspan=1)
tree["columns"] = ("序号", "企业名称", "详细信息","aa")
# 设置列，不显示
tree.column("序号", width=100)
tree.column("企业名称", width=100)
tree.column("详细信息", width=300)
tree.column("aa", width=300)
# 显示表头
tree.heading("序号", text="序号")
tree.heading("企业名称", text="企业名称")
tree.heading("详细信息", text="详细信息")
tree.heading("aa", text="aa")



i = 0
ii = 0
name = "辽宁忠旺集团"
addurl = "辽宁省沈阳市铁西区22号"
aa = ".........................................................."
tree.insert("", i, text="", values=(i, name, addurl, aa))
tree.insert("", i, text="", values=(ii, "1", addurl, aa))
tree.insert("", i, text="", values=(ii, "2", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
tree.insert("", i, text="", values=(ii, "3", addurl, aa))
"""
    定义滚动条控件
    orient为滚动条的方向，vertical--纵向，horizontal--横向
    command=tree.yview 将滚动条绑定到treeview控件的Y轴
"""
#scroll_ty = Scrollbar(root, orient=VERTICAL, command=tree.yview)
#scroll_ty.grid(row=1, column=1, sticky=N+S)
#tree['yscrollcommand']=scroll_ty.set

# ----vertical scrollbar------------
vbar = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=vbar.set)
#tree.grid(row=0, column=0, sticky=NSEW)
vbar.grid(row=1, column=1, sticky=NS)

# ----horizontal scrollbar----------
hbar = ttk.Scrollbar(root, orient=HORIZONTAL, command=tree.xview)
tree.configure(xscrollcommand=hbar.set)
hbar.grid(row=3, column=0, sticky=EW)


root.mainloop() #显示窗口  mainloop 消息循环








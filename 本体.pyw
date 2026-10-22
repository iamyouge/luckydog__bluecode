# 抽奖程序· v11.1(2024-11-29)
import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog, messagebox
import winsound
try:
    import chardet
except:
    print("NOCHARDET")
import os

'''
NameList = ['彭祖海', '陈春日','覃贤', '许云飞', '黄允','张逸', '关雨萱', '吴梓馨', '张诚', '张声冠', '刘子涵', '钟可馨', '吴金明', '莫盟君', '周冠颖', '刘钦梅', '杨怡宁', '章宝峰', '李颢光', '张丽蕊', '覃晓杨', '黄德晟',
            '许峻源', '张世怡', '黄显璐', '彭业拓', '姚凯膑', '李光铭', '丁世洪', '刘星冉', '何晓饶', '张晓慧', '许智慧', '谭滢', '苏祈荣', '包基材', '梁馨月',
            '赵益雯', '刘子添', '郑富艺', '李芳漩', '马佳宜', '梁祥鑫', '刘喜', '梁皓云', '吴文祥', '周琳钧', '黄俊祥', '吕继杰', '林英韬', '韦惜', '陈子铃', '卜凡', '罗伟雄',
            '朱春晓', '冯晨曦', '梁孪萍', '黄河锦','黄允' ,'苏禄万', '何秋静', '邱丽桦', '胡永盛', '陆渝龙', '吴泓佑', '揭世洲', '杨洁榕', '杨萧亦', '曹东岳', '黄裕贵']

'''
NameList = []
abc = []
dxcq_name = ''
selected = []
localnamelist = []
list_namelist = []
win3 = None
label = None
focus_names = ''
dxcq_ky = False
# 创建一部字典来保存复选框的状态
selected_names = {}
#悬浮框
drag_x = 0
drag_y = 0


def a():  # 随机名字的方法
    global click_count
    global dxcq_ky
    if len(abc) >= 6:
        b()
    if dxcq_ky:
        namechu = focus_names
        dxcq_ky = False
    elif selected:
        namechu = selected[random.randint(0, len(selected) - 1)]
    else:
        namechu = NameList[random.randint(0, len(NameList) - 1)]
    txt1 = Label(box1, text=namechu, font='华文中宋 30 bold', bg='#a5e8fb', width=18, height=1, compound='center',
                 relief='raised')
    txt1.pack()
    abc.append(txt1)


def b():  # 清除结果的方法
    while abc:
        txt1 = abc.pop()
        txt1.destroy()


def dxcq(name):
    global dxcq_name, dxcqsfky
    dxcq_name = NameList[name]
    dxcqsfky = True
def focus_name():#定向抽取
    def dxcq1():
        global focus_names
        global dxcq_ky
        focus_names = NameList[dxchoose.get()]
        dxcq_ky = True
    def dxcq2():
        global dxcq_ky
        global focus_names
        focus_names = NameList[dxchoose.get()]
        focus_name.destroy()
        dxcq_ky = True
    focus_name = Toplevel()
    focus_name.iconbitmap("幸运方块.ico")
    focus_name.title('定向抽取')  # 窗体标题
    focus_name.resizable(False, False)

    fn_txt = Label(focus_name, text='点击一个LuckyDog', font='微软雅黑 25 bold', width=33)
    fn_txt.grid(row=0, column=0, columnspan=10)
    xx = 1
    yy = 1
    dxchoose = IntVar()
    for i in range(0, len(NameList)):
        Radiobutton(focus_name, variable = dxchoose, value = i, text = NameList[i]).grid(row=xx,column=yy)
        if xx >= 10:
            xx = 0
            yy += 1
        xx += 1
    choose_qd1 = ttk.Button(focus_name, text='确定', command=dxcq1)
    choose_qd1.grid(row=11,column=0,columnspan=5)
    choose_qd2 = ttk.Button(focus_name, text='确定并退出', command=dxcq2)
    choose_qd2.grid(row=11,column=3,columnspan=5)
def names():#范围抽取
    global focus_names, NameList, selected_names
    focus_names = tk.Toplevel(Main)
    focus_names.iconbitmap("幸运方块.ico")
    focus_names.title('范围抽取')
    focus_names.resizable(False, False)
    fn_txt = Label(focus_names, text='点击选择LuckyDogs（可以多选）', font='微软雅黑 25 bold', width=33)
    fn_txt.grid(row=0, column=0, columnspan=10)
    xx = 1
    yy = 1
    for i, name in enumerate(NameList):
        # 创建复选框
        var = tk.IntVar()
        checkbutton = tk.Checkbutton(focus_names, text=name, variable=var)
        checkbutton.grid(row=xx, column=yy, padx=5, pady=5)
        selected_names[name] = var
        if xx >= 8:
            xx = 0
            yy += 1
        xx += 1

    # 创建一个Frame来放置按钮
    button_frame = tk.Frame(focus_names)
    button_frame.grid(row=xx + 2, column=0, columnspan=10, pady=20)

    # 添加确定按钮
    confirm_button = tk.Button(button_frame, text='确定', command=lambda: confirm_selection(selected_names))
    confirm_button.pack(side=tk.LEFT,padx=(10))


    # 添加退出按钮
    exit_button = tk.Button(
        button_frame, text='反选', command=fx)
    exit_button.pack(side=tk.LEFT,padx=(10))

    allchose = tk.Button(
        button_frame, text='全选',  command=qx)
    allchose.pack(side=tk.LEFT,padx=(10))
    
    # 添加退出按钮
    exit_button = tk.Button(
        button_frame, text='确定并退出',  command=lambda: confirm_selections1(selected_names))
    exit_button.pack(side=tk.LEFT, padx=(10))
def confirm_selection(selected_names):
    global selected
    # 获取选中的复选框的值
    selected = [name for name, var in selected_names.items() if var.get() == 1]
    if selected:
        pass
    else:
        messagebox.showinfo("提示", "请至少选择一个学生")
def qx():#全选
    global selected_names
    for a, b in selected_names.items():
        b.set(1)
def fx():#反选
    global selected_names
    for a, b in selected_names.items():
        if b.get() == 1:
            b.set(0)
        else:
            b.set(1)
def confirm_selections1(selected_names):
    global selected
    # 获取选中的复选框的值
    selected = [name for name, var in selected_names.items() if var.get() == 1]
    if selected:
        focus_names.destroy()
    else:
        messagebox.showinfo("提示", "请至少选择一个学生")



def import_students(a):#导入名单
    global NameList,file_object,list_namelist,Main
    mingdan = []
    fileType = [('txt文件','*.txt')]
    file = filedialog.askopenfilename(title='选择名单',filetypes=fileType)
    try:
        with open(file,'rb') as file_o:
            result = chardet.detect(file_o.read())
            encod = result['encoding']
    except:
        pass
    try:
        with open(file,encoding='utf-8') as file_o:
            for line in file_o:
                mingdan.append(line.rstrip())
    except:
        pass

    abcd = "a" #默认名
    if len(mingdan) == 0:
        messagebox.showerror('警告','导入失败')
    else:
        NameList = mingdan
        def show_input():
            global abcd
            text = entry.get()
            if text or text in list_namelist:
                abcd = text
                with open(abcd, 'a') as file_object:
                    file_object.truncate(0)
                    for i in mingdan:
                        if i == mingdan[len(NameList) - 1]:
                            file_object.write(i)
                        else:
                            file_object.write(i + ',')
                with open("luckdata.dat", "a") as file_object:
                    if 0 == a:
                        file_object.truncate(0)
                        file_object.write(abcd)
                        list_namelist.append(abcd)
                    else:
                        file_object.write(",")
                        file_object.write(abcd)
                        list_namelist.append(abcd)
                messagebox.showinfo('提示', '导入已完成！\n 已切换至新导入的名单')
                # os.system("attrib +h luckydog.txt")
                root5.destroy()
            else:
                messagebox.showinfo("请输入内容！", "请输入内容！")
        root5 = Toplevel(Main)
        # # 标签
        tk.Label(root5, text="请输入内容：").pack(pady=5)
        # 创建输入框
        entry = tk.Entry(root5, width=30, font=("Arial", 12), bg="#f0f0f0")
        entry.pack(pady=10)
        tk.Button(root5, text="提交", command=show_input, bg="#4CAF50", fg="white").pack()


        if 0 == a:
            with open(abcd,'a') as file_object:
                file_object.truncate(0)
                for i in mingdan:
                    if i==mingdan[len(NameList) - 1]:
                        file_object.write(i)
                    else:
                        file_object.write(i+',')
            with open("luckdata.dat","a") as file_object:
                if 0 == a:
                    file_object.truncate(0)
                    file_object.write(abcd)
                    list_namelist.append(abcd)
                else:
                    file_object.write(",")
                    file_object.write(abcd)
                    list_namelist.append(abcd)
            messagebox.showinfo('提示','导入已完成！')
            os.system("attrib +s +a +h luckydog.txt")


def student_out():
    with open("studentslist.txt","w") as file:
        for i in NameList:
            file.write(i + "\n")
    #os.command()
    messagebox.showinfo("提示", "已导出到桌面")

def namelist_check():
    win = Toplevel()
    name_count={}
    for i in NameList:
        if i in name_count.keys():
            #user_chose = messagebox.askyesno('警告','检测到重复名字，是否删除？\n (',icon="warning")
            name_count[i] += 1
        else:
            name_count[i] = 1
        box = Frame(win)
        Label(box,text=i).pack()
        Label(box,text=name_count[i]).pack()
        box.pack()

'''

def file():
    root4 = Toplevel()
    root4.geometry('400x450+600+100')
    Label(root4,text="请选择要使用的名单",font='微软雅黑 25 bold').pack()
    for i in range(0,cixu):
        Radiobutton(root4).pack()
    
'''

def about_us():
    info_window = tk.Toplevel(Main)
    info_window.iconbitmap("蓝图编码.ico")
    info_window.title('关于蓝图编码')
    info_window.geometry('300x200+517+360')
    info_window.resizable(False, False)

    # 使用Text小部件来显示多行文本
    text = tk.Text(info_window, height=10, width=40)
    text.pack(padx=10, pady=10)

    # 插入关于我们的内容
    text.insert(tk.END, "关于我们：\n")
    text.insert(tk.END, "蓝图编码是由一群热爱编程和开源项目的工程师和开发者组成的团队。\n")
    text.insert(tk.END, "我们专注于使用Python语言来解决实际问题，\n")
    text.insert(tk.END, "并致力于提供高效、可靠和创新的解决方案。\n")
    text.insert(tk.END, "团队愿景：通过我们的技术和服务，为客户和社会创造真正的价值。\n")
    text.insert(tk.END, "并建立一个开放、协作和互助的工作环境，激发团队成员的潜力。\n")
    text.insert(tk.END, "持续探索和采用最新的技术，以保持我们的竞争力\n")
    text.insert(tk.END, "创建一个开放、协作和互助的环境，\n")
    text.insert(tk.END, "让每个成员都能发挥自己的潜力，\n")
    text.insert(tk.END, "共同推动技术的进步和社会的发展。\n\n")
    text.insert(tk.END, "我们的目标是：'让我们的程序在龙湾初中部 ⚡随 处 可 见⚡ '\n\n")
    text.insert(tk.END, "联系方式1：400-888-888\n")
    text.insert(tk.END, "联系方式2：400-114-12530\n")
    text.insert(tk.END, "联系方式3：H—303-305-306\n")
    text.insert(tk.END, "电子邮件: contact@blueprintcode.com\n")
    text.insert(tk.END, "官方网站: www.blueprint_code.com\n")

    # 禁止文本编辑
    text.config(state=tk.DISABLED)

    # 关闭按钮
    close_button = tk.Button(info_window, text="关闭", command=info_window.destroy)
    close_button.pack(pady=10)

def reset():
    global dxcq_ky,selected
    selected = []
    dxcq_ky = False
    messagebox.showinfo('提示','     已重置!    ')

def on_minisize(evnet):
    def start_drag(event):
        global drag_x,drag_y
        drag_x = event.x
        drag_y = event.y
    def on_enter(event):
        x = float_win.winfo_x()
        y = float_win.winfo_y()
        w = win_w
        h = win_h
            # 从右侧弹出
        if x >= sw - w - 1:
            float_win.geometry(f"+{self.sw - w}+{y}")
            # 从左侧弹出
        elif x <= 0:
            float_win.geometry(f"+0+{y}")
            # 从底部弹出
        if y >= sh - h - 1:
            float_win.geometry(f"+{x}+{self.sh - h}")
    def do_drag(event):
        x = float_win.winfo_x() + event.x - drag_x
        y = float_win.winfo_y() + event.y - drag_y
        float_win.geometry(f"+{x}+{y}")
    def restore_main_window(event):
        float_win.destroy()
        Main.deiconify()
        Main.lift()
    if Main.state() == "iconic":
        print("a")
        Main.withdraw()
        float_win = tk.Toplevel()
        float_win.overrideredirect(True)
        float_win.attributes("-alpha", 0.6)
        float_win.attributes("-topmost", True)
        float_win.config(bg="#cccccc")
        float_win.geometry("120x50+200+200")
        label = tk.Label(
            float_win,
            text="双击恢复窗口",
            bg="#cccccc",
            font=("微软雅黑", 10)
        )
        label.pack(expand=True, fill=tk.BOTH)
        sw = float_win.winfo_screenwidth()
        sh = float_win.winfo_screenheight()
        # 拖动事件
        float_win.bind("<ButtonPress-1>", start_drag)
        float_win.bind("<B1-Motion>", do_drag)
        # 双击恢复
        float_win.bind("<Double-1>", restore_main_window)
        #float_win.bind("<ButtonRelease-1>", on_release)
        float_win.bind("<Enter>", on_enter)

try:
    with open('luckdata.dat','r') as file_object:
         luckdata = file_object.readlines()
         for i in luckdata:
             list_namelist.append(i)
         namelist = list_namelist[0]
         result = namelist.split(",")
         try:
            with open(result[0],"r") as file_object:
                # 此处result为选用名单序号
                localnamelist = file_object.readlines()
                result = localnamelist[0]
                result = result.split(",")
                NameList = result
         except Exception as e:
             messagebox.showinfo("错误","名单文件出错，请尝试重新导入名单")
             import_students(0)
except:
    with open('luckdata.dat','w') as file_object:
        messagebox.showinfo('提示','     快点去导入新名单    ')
        import_students(0)
        os.system("attrib +h luckdata.dat")

if __name__ == "__main__":
    Main = Tk()
    Main.iconbitmap("幸运方块.ico")
    Main.title('抽奖程序v10.20最新版')  # print窗体标题
    Main.bind("<Unmap>", on_minisize)
    screenwidth = Main.winfo_screenwidth()
    screenheight = Main.winfo_screenheight()
    geometry = '%dx%d+%d+%d' % (400,495, (screenwidth - 400) / 2, (screenheight - 495) / 2)
    Main.geometry(geometry)  # 窗体初始生成大小、位置
    Main.resizable(False, False)  # 设置窗体大小可更改参数（宽，高）
    top_menu = Menu(Main)
    menu1 = Menu(top_menu, tearoff=False)
    top_menu.add_cascade(label="软件功能", menu=menu1)
    top_menu.add_command(label="关于我们", command=about_us)
    top_menu.add_command(label="抽取重置", command=reset)
    Main.config(menu=top_menu)
    menu1.add_command(label='定向抽取', command=focus_name)
    menu1.add_command(label='范围抽取', command=names)
    menu1.add_command(label='名单导出', command=student_out)
    #menu1.add_command(label='名单管理', command=file)
    menu1.add_command(label="名单检查", command=namelist_check)
    menu1.add_command(label='名单更改', command=lambda:import_students(1))
    box1 = Frame(Main)
    box1.pack()
    txt = Label(box1, text='今天的LuckyDog是：', font='微软雅黑 25 bold')
    txt.pack()
    start = Button(
        box1, text='抽一个', bg='#43d2f9', width=20, height=1, anchor='center', font='等线 25', command=lambda:
        a())
    start.pack()
    update = Button(box1, text='归零', bg='#43d2f9', width=20, height=1, anchor='center', font='等线 25', command=b)
    update.pack()
    Main.attributes("-topmost", True)
    Main.quit()
    print(list_namelist)
    print(NameList)
    Main.mainloop()

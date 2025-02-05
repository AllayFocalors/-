import random as r
import tkinter as tk
import time as t
import WeightChoice as wc
import os
import threading
import time
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter.ttk import Style, Progressbar
from ffpyplayer.player import MediaPlayer

win = tk.Tk()
NumberList = []
Chosen = []
os.environ['FFMPEG_HWACCEL'] = 'auto'
# 定义视频播放器类
class VideoPlayTk:
    # 初始化函数
    def __init__(self, root,filepath):
        self.root = root
        self.root.title('视频播放器')  # 设置窗口标题
 
        # 创建一个画布用于显示视频帧
        self.canvas = tk.Canvas(root, bg='black')
        self.canvas.place(x=0, y=0, width=root.winfo_width(), height=root.winfo_height())
        self.player = MediaPlayer(filepath, ff_opts={'hwaccel': 'auto'})

        # 初始化播放器和播放状态标
        self.player = MediaPlayer(filepath)  # 创建一个MediaPlayer对象
        self.is_stopped = False
        self.is_paused = False
        self.thread = threading.Thread(target=self.play_video_thread)

        self.thread.daemon = True
        self.thread.start()
    
    def play_video_thread(self):
        while not self.is_stopped:
            frame, val = self.player.get_frame()
            if val == 'eof':
                self.StopAnimation()
                break
            elif frame is not None:
                image, pts = frame
                self.update_canvas(image)

            if not self.is_paused and val is not None:
                time.sleep(val)
    def StopAnimation(self):
        self.is_stopped = True
        self.canvas.place_forget()
        if self.player:
            self.player.close_player()
            self.player = None  # 如果停止播放，则释放播放器资源


    def update_canvas(self, image):
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        img = Image.frombytes("RGB", image.get_size(), bytes(image.to_bytearray()[0]))
        img = img.resize((canvas_width, canvas_height), Image.NEAREST)  # 使用最近邻插值
        photo = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.image = photo

def PlayAnimation(filepath):
    app=VideoPlayTk(win,filepath)
    win.after(6200,app.StopAnimation)

def ShowAbout():
    abt = tk.Toplevel(win)
    abt.title('悦灵云工作室·AllayCloud-Studio')
    Img_StudioLogo = ImageTk.PhotoImage(Image.open("StudioLogo.png").resize((512,200),Image.LANCZOS))
    Lab_StudioLogoShow = tk.Label(abt,image=Img_StudioLogo)
    Img_AppLogo = ImageTk.PhotoImage(Image.open("SeeWangLogo-new.png").resize((512,256),Image.LANCZOS))
    Lab_AppLogoShow = tk.Label(abt,image=Img_AppLogo)
    Lab_StudioLogoShow.image = Img_StudioLogo
    Lab_AppLogoShow.image = Img_AppLogo
    Lab_StudioLogoShow.pack()
    Lab_AppLogoShow.pack()
    abt.mainloop()

def RefreshWeight():
    global config
    config = wc.GetConfig()
    
def reset():
    global NumberList,Chosen,config,stu_Quantity
    NumberList = []
    Chosen = []
    for i in config:
        NumberList.append(i.split(' ')[0])
    stu_Quantity = len(NumberList)

RefreshWeight()
reset()

win.geometry("1700x900+0+5")
win.title('希王点名系统')

animation=False

MainTitle_color = '#5982ff'

def changeAnimation():
    global animation
    if animation:
        animation=False
        But_AnimationOn.config(text='已禁用动画')
    else:
        animation=True
        But_AnimationOn.config(text='已启用动画')

def ShowWeightSettings():
    print('config.txt')
    os.system(f'start notepad ./config.txt')

def ChooseOne():
    global config,animation
    if animation:
        PlayAnimation('V1lower.mp4')
    if r.randint(1,200)==1:
        Lab_Number.config(text='666666666666666666666666666666666',fg='black',font=("MiSans VF Bold",160))
    else:
        if len(Chosen) < stu_Quantity:
            Tar = wc.Choice(config,Chosen,stu_Quantity)
            NumberList.remove(Tar)
            Chosen.append(Tar)
            Lab_Number.config(text=str(Tar),fg=MainTitle_color)
            Lab_Chosen.config(text=str(f'已抽{len(Chosen)}个学生：\n{str(Chosen)}'))   
        else:
            Lab_Number.config(text='已抽完,请重置',font=("MiSans VF Bold",100),fg='red')

def ChooseN():
    global stu_Quantity
    if animation:
        PlayAnimation('V2low.mp4')
    if r.randint(1,200)==1:
        Lab_Number.config(text='666666666666666666666666666666666',fg='black',font=("MiSans VF Bold",160))
    elif int(Ent_N.get())>=10:
        Lab_Number.config(text=f'你脑子是不是有问题，搁着周处除{Ent_N.get()}害呢',font=("MiSans VF Bold",100),fg='red')
    else:
        if len(Chosen) < stu_Quantity-int(Ent_N.get())+1:
            res=''
            for i in range(int(Ent_N.get())):
                Tar = wc.Choice(config,Chosen,stu_Quantity)
                print(f'Tar={Tar}')
                NumberList.remove(Tar)
                Chosen.append(Tar)
                Lab_Chosen.config(text=str(f'已抽{len(Chosen)}个学生：\n{str(Chosen)}'))
                res+=str(Tar)+' '
            Lab_Number.config(text=str(res),fg=MainTitle_color)
        else:
            Lab_Number.config(text='剩下的人不够抽了:)',font=("MiSans VF Bold",100),fg='red')

def ChooseThree():
    global stu_Quantity
    if animation:
        PlayAnimation('V2low.mp4')
    if r.randint(1,200)==1:
        Lab_Number.config(text='666666666666666666666666666666666',fg='black',font=("MiSans VF Bold",160))    # 彩蛋
    else:
        if len(Chosen) < stu_Quantity-2:
            res=''
            for i in range(3):
                Tar = wc.Choice(config,Chosen,stu_Quantity)
                print(f'Tar={Tar}')
                NumberList.remove(Tar)
                Chosen.append(Tar)
                Lab_Chosen.config(text=str(f'已抽{len(Chosen)}个学生：\n{str(Chosen)}'))
                res+=str(Tar)+' '
            Lab_Number.config(text=str(res),fg=MainTitle_color)
        else:
            Lab_Number.config(text='剩下的人不够抽了:)',font=("MiSans VF Bold",100),fg='red')

def update_Lab_Number_wraplength(event):
    Lab_Number.config(wraplength=win.winfo_width(),font=("MiSans VF",int(win.winfo_width()/10-40)))

win.bind('<Configure>', update_Lab_Number_wraplength)

Lab_Number = tk.Label(win,text="快抽我等不及了",font=("MiSans VF Bold",160),wraplength=int(win.winfo_width()))
But_ChoiseOne = tk.Button(win,text="单抽",font=("MiSans VF",20),height=2,width=30,border=5,command=ChooseOne)
But_ChooseThree = tk.Button(win,text="三抽",font=("MiSans VF",20),height=2,width=30,border=5,command=ChooseThree)
But_ChooseN = tk.Button(win,text="N抽",font=("MiSans VF",20),height=2,width=30,border=5,command=ChooseN)
Lab_N = tk.Label(win,text='N = ',font=("MiSans VF",15))
Ent_N = tk.Entry(win,width=5,font=("MiSans VF",15))
Lab_Chosen = tk.Label(win,text="已抽学生：",font=("MiSans VF",15),wraplength=800)
def resetAll():
    reset()
    Lab_Chosen.config(text=str(f'已抽{len(Chosen)}个学生：{str(Chosen)}'))
But_Reset = tk.Button(win,text="重置已抽学生",font=("MiSans VF",15),command=resetAll)
But_EditWeight = tk.Button(win,text="编辑权重",font=("MiSans VF",15),command=ShowWeightSettings)
But_RefreshWeight = tk.Button(win,text="刷新权重",font=("MiSans VF",15),command=RefreshWeight)
But_AnimationOn = tk.Button(win,text="已禁用动画",font=("MiSans VF",15),command=changeAnimation)
But_About = tk.Button(win,text="关于",font=("MiSans VF",15),command=ShowAbout)
Lab_A = tk.Label(win,text='Allay',font=("MiSans VF Medium",20))

Lab_Number.pack()
But_ChoiseOne.pack()
But_ChooseThree.pack()
But_ChooseN.pack()
Lab_N.place(x=100,y=350)
Ent_N.place(x=150,y=350)
But_Reset.place(x=100,y=400)   
But_EditWeight.place(x=100,y=450)
But_RefreshWeight.place(x=100,y=500)
But_AnimationOn.place(x=100,y=550)
But_About.place(x=100,y=600)
Lab_Chosen.pack()

win.mainloop()

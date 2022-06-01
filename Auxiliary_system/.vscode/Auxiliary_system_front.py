from tkinter import *
import tkinter as tk
import sys
class Auxiliary_system_front():
    def __init__(self):
        self.lifelinelist=[]#记录生命线的列表，用于判断后面的数据线是否重复以及画图，这个列表的元素是一个字符串(表示生命线名字)
        self.messagelist=[]#记录消息的列表，用于画图以及判断不同生命线间的相同消息(根据相同的消息会将现在描述的数据线的消息上移来达到叙述者的需求)，这个列表的元素是一个包含三个字符串(消息首部、消息尾部、消息名)和一个整数(高度值，用于得到后面画图的高度)的列表
        self.fragmentlist=[]#记录片段的列表，用于画图，这个列表的元素是一个包含一个字符串()和七个整数(左上x坐标、左上y坐标、右下x坐标、右下y坐标、片段处于第几层、片段外那层片段在列表中的位置、分区数)的列表
        self.heightnum=0#记录高度值的参数，用于得到后面画图的高度
        self.lifeline_index=0#记录上一条生命线合并后消息列表的位置，用于判断消息列表中的哪些消息是这个生命线上的
        self.cen=-1#记录片段处于第几层片段，因为片段层数越高片段的宽度越小
        self.nowfragment=0#记录当前片段在片段列表中的位置
        self.beforefragment=-1#记录上一个片段在片段列表中的位置
        self.x_lifeline=238#记录生命线的x坐标
        self.fenqu=[]#记录分区虚线的高度值
        self.nowtime=["",0]#记录当前处理的事务，它的第一个元素记录处理事务的类型(是消息还是片段),它的第二个元素记录这个事务在相应列表中的位置，这个当前事务在画图时会用红线画出给用户更好的反馈
        self.Str=""#用于将异步消息的各种传递可能列在最后界面上的字符串，它的值由Auxiliary_system来赋

    def work(self,mark):#Auxiliary_system调用的主要函数，用于创建可视化界面以及实现人机交互，mark是Auxiliary_system传过来的用来通知应该显示哪个界面的值
        self.send=""#记录要回馈给Auxiliary_system的内容的参数
        root= Tk()
        root.title('顺序图辅助系统')
        root.geometry('720x720') 
        
        def run0():#退出系统事件
            sys.exit()


        def run1():#输入消息事件
            self.send = str(inp1.get())#记录输入的消息
            U=self.send.split(",")#将输入的消息以,为分隔符分割成一个列表的不同元素
            for i in range(len(self.messagelist)):#遍历消息列表，看是否有和输入消息相同的消息，有则将当前生命线的消息的高度值移到这个相同消息的高度值前
                if self.messagelist[i][0]==U[0] and self.messagelist[i][1]==U[1] and self.messagelist[i][2]==U[2]:#判断是否是相同的消息
                    num_i=self.messagelist[i][3]
                    move_num=0#记录一共上移了多少个消息，这也是后面非当前生命线但高度值高于这个相同消息的消息的高度的后移值
                    for i1 in range(len(self.messagelist)):#将当前生命线的消息的高度值移到这个相同消息的高度值前，用的是将当前生命线的消息的高度值前移而这个相同消息的高度值下移的方式
                        if i1>self.lifeline_index:
                            self.messagelist[i1][3]=self.messagelist[i][3]
                            self.messagelist[i][3]=self.messagelist[i][3]+1
                            move_num=move_num+1
                    for i2 in range(len(self.messagelist)):#将非当前生命线但高度值高于这个相同消息的消息的高度值后移来确保不会有两个消息高度值一样的情况
                        if self.messagelist[i2][3]>num_i and i2!=i and i2<=self.lifeline_index:
                            self.messagelist[i2][3]=self.messagelist[i2][3]+move_num
                    self.lifeline_index=len(self.messagelist)-1#更新上一个生命线的位置为现在消息列表的长度减一，实际上上个生命线的位置不应该变化，这里只是为了移动的正确性
                    self.nowtime[0]="mes"#当前输入的事务类型为消息
                    self.nowtime[1]=i#当前输入的事务在对应列表的位置为i
                    root.destroy()#关闭这个界面
                    return
            self.heightnum=self.heightnum+1
            U.append(self.heightnum)
            self.messagelist.append(U)
            fragment=self.fragmentlist[self.nowfragment]#得到当前所处的片段
            while fragment[6]!=-1:#一层层向上找片段，为每个片段的右下y坐标加1,因为加了一条消息，这个片段的高度也理应变大
                fragment[4]=fragment[4]+1
                fragment=self.fragmentlist[fragment[6]]
            self.nowtime[0]="mes"#当前输入的事务类型为消息
            self.nowtime[1]=len(self.messagelist)-1#当前输入的事务在对应列表的最后
            root.destroy()#关闭这个界面
            return

        def run2():#最外层框架为seq事件
            self.send = "1"#记录要反馈的用户选择
            self.cen=self.cen+1
            self.fragmentlist.append(["seq",0,0,0,0,self.cen,self.beforefragment,0])
            self.nowtime[0]="fra"#当前输入的事务类型为片段
            self.nowtime[1]=self.nowfragment#记录当前输入的事务在对应列表的位置
            root.destroy()
            return

        def run3():#最外层框架为strict事件
            self.send = "2"
            self.cen=self.cen+1
            self.fragmentlist.append(["strict",0,0,0,0,self.cen,self.beforefragment,0])
            self.nowtime[0]="fra"
            self.nowtime[1]=self.nowfragment
            root.destroy()
            return

        def run4():#最外层框架为par事件
            self.send = "3"
            self.cen=self.cen+1
            self.fragmentlist.append(["par",0,0,0,0,self.cen,self.beforefragment,0])
            self.nowtime[0]="fra"
            self.nowtime[1]=self.nowfragment
            root.destroy()
            return

        def run5():#最外层框架为critical事件
            self.send = "4"
            self.cen=self.cen+1
            self.fragmentlist.append(["critical",0,0,0,0,self.cen,self.beforefragment,0])
            self.nowtime[0]="fra"
            self.nowtime[1]=self.nowfragment
            root.destroy()
            return

        def run6():#再次测试事件，要将属性都转化为初值
            self.send = "5"
            self.lifelinelist=[]
            self.messagelist=[]
            self.fragmentlist=[]
            self.heightnum=0
            self.lifeline_index=0
            self.cen=-1
            self.nowfragment=0
            self.beforefragment=-1
            self.x_lifeline=238
            self.fenqu=[]
            self.nowtime=["",0]
            self.Str=""
            root.destroy()
            return
        
        def run7():#关闭程序事件
            self.send = "6"
            root.destroy()
            return

        def run8():#开始输入一条生命线上的消息事件
            self.lifeline_index=len(self.messagelist)-1#记录上一条生命线合并后消息列表的位置，用于判断消息列表中的哪些消息是这个生命线上的
            self.send = "1"
            root.destroy()
            return

        def run9():#退出seq片段或其他片段的区域事件
            self.send = "2"
            self.nowtime[0]="fra"
            self.nowtime[1]=self.nowfragment
            root.destroy()
            return

        def run10():#接下来有一个critical片段事件
            self.send = "3"
            self.cen=self.cen+1
            self.heightnum=self.heightnum+1
            self.beforefragment=self.nowfragment
            self.nowfragment=len(self.fragmentlist)
            self.fragmentlist.append(["critical",0,self.heightnum,0,self.heightnum+1,self.cen,self.beforefragment,0])
            fragment=self.fragmentlist[self.beforefragment]#得到当前所处的片段
            while fragment[6]!=-1:#一层层向上找片段，为每个片段的右下y坐标加2,因为加了一条片段，外层片段的高度也理应变大
                fragment[4]=fragment[4]+2
                fragment=self.fragmentlist[fragment[6]]
            self.nowtime[0]="fra"
            self.nowtime[1]=self.nowfragment
            root.destroy()
            return

        def run11():#输入一条消息事件
            self.send = "1"
            root.destroy()
            return

        def run12():#结束输入消息事件
            self.send = "2"
            root.destroy()
            return

        def run13():#为片段创建一个区域事件
            self.send = "1"
            fragment=self.fragmentlist[self.nowfragment]
            if fragment[7]!=0:
                self.fenqu.append([self.heightnum+0.5,self.cen])#记录分区虚线的高度值
            self.fragmentlist[self.nowfragment][7]=fragment[7]+1
            root.destroy()
            return


        def run15():#退出strict/par/critical片段事件
            self.send = "3"
            fragment=self.fragmentlist[self.nowfragment]
            self.nowfragment=fragment[6]
            self.cen=self.cen-1
            self.heightnum=self.heightnum+1
            self.nowtime[0]="fra"
            self.nowtime[1]=self.nowfragment
            root.destroy()
            return


        def run23():#接下来有一个strict片段事件
            self.send = "4"
            self.cen=self.cen+1
            self.heightnum=self.heightnum+1
            self.beforefragment=self.nowfragment
            self.nowfragment=len(self.fragmentlist)
            self.fragmentlist.append(["strict",0,self.heightnum,0,self.heightnum+1,self.cen,self.beforefragment,0])
            fragment=self.fragmentlist[self.beforefragment]#得到当前所处的片段
            while fragment[6]!=-1:#一层层向上找片段，为每个片段的右下y坐标加2,因为加了一条片段，外层片段的高度也理应变大
                fragment[4]=fragment[4]+2
                fragment=self.fragmentlist[fragment[6]]
            self.nowtime[0]="fra"
            self.nowtime[1]=self.nowfragment
            root.destroy()
            return

        def run24():#接下来有一个par片段事件
            self.send = "5"
            self.cen=self.cen+1
            self.heightnum=self.heightnum+1
            self.beforefragment=self.nowfragment
            self.nowfragment=len(self.fragmentlist)
            self.fragmentlist.append(["par",0,self.heightnum,0,self.heightnum+1,self.cen,self.beforefragment,0])
            fragment=self.fragmentlist[self.beforefragment]#得到当前所处的片段
            while fragment[6]!=-1:#一层层向上找片段，为每个片段的右下y坐标加2,因为加了一条片段，外层片段的高度也理应变大
                fragment[4]=fragment[4]+2
                fragment=self.fragmentlist[fragment[6]]
            self.nowtime[0]="fra"
            self.nowtime[1]=self.nowfragment
            root.destroy()
            return





        


        msg1 = Message(root,text='''欢迎使用辅助系统。请将序列图从外到内、从上到下、从左到右地叙述顺序图(只用按顺序添加片段、区域、消息就能得到所有异步信息传输的可能性)。
        要按固定格式输入信息,例如,a:A->B请输入A,B,a\nPS:在这一区域的一条生命线上输入过一个信息的前提下再在另一条生命线上输入相同的信息，画布会自动调节位置。
        叙述位置在片段的区域中时，因为从上向下的叙述，叙述位置一定在最下方的区域中''',relief=GROOVE,width=600)
        msg1.place(relx=0.08,y=10,relheight=0.1,width=600)
        if mark=="enter_message":
            lb1 = Label(root, text='请输入这条消息')
            lb1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

            inp1 = Entry(root)
            inp1.place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.05)

            btn1 = Button(root, text='输入', command=run1)
            btn1.place(relx=0.4, rely=0.27, relwidth=0.2, relheight=0.05)

            btn25 = Button(root, text='退出程序', command=run0)
            btn25.place(relx=0.4, rely=0.33, relwidth=0.2, relheight=0.05)

        if mark=="list":
            btn2 = Button(root, text='1.最外层框架为seq', command=run2)
            btn2.place(relx=0.3, rely=0.12, relwidth=0.4, relheight=0.04)

            btn3 = Button(root, text='2.最外层框架为strict', command=run3)
            btn3.place(relx=0.3, rely=0.17, relwidth=0.4, relheight=0.04)

            btn4 = Button(root, text='3.最外层框架为par', command=run4)
            btn4.place(relx=0.3, rely=0.22, relwidth=0.4, relheight=0.04)

            btn5 = Button(root, text='4.最外层框架为critical', command=run5)
            btn5.place(relx=0.3, rely=0.27, relwidth=0.4, relheight=0.04)

            btn26 = Button(root, text='退出程序', command=run0)
            btn26.place(relx=0.3, rely=0.32, relwidth=0.4, relheight=0.04)
        
        if mark=="end":
            btn6 = Button(root, text='5.再次测试', command=run6)
            btn6.place(relx=0.5, rely=0.19, relwidth=0.4, relheight=0.05)

            btn7 = Button(root, text='6.退出', command=run7)
            btn7.place(relx=0.5, rely=0.26, relwidth=0.4, relheight=0.05)

            btn27 = Button(root, text='退出程序', command=run0)
            btn27.place(relx=0.5, rely=0.32, relwidth=0.4, relheight=0.05)

            txt=Text(root)
            txt.place(relx=0.1, rely=0.15, relwidth=0.35, relheight=0.2)
            txt.insert(END,self.Str)
        
        if mark=="seq":
            btn8 = Button(root, text='1.开始输入一条生命线上的消息', command=run8)
            btn8.place(relx=0.3, rely=0.12, relwidth=0.4, relheight=0.03)

            btn9 = Button(root, text='2.退出这个区域/片段', command=run9)
            btn9.place(relx=0.3, rely=0.16, relwidth=0.4, relheight=0.03)

            btn10 = Button(root, text='3.接下来有一个critical片段', command=run10)
            btn10.place(relx=0.3, rely=0.20, relwidth=0.4, relheight=0.03)

            btn23 = Button(root, text='4.接下来有一个strict片段', command=run23)
            btn23.place(relx=0.3, rely=0.24, relwidth=0.4, relheight=0.03)

            btn24 = Button(root, text='5.接下来有一个par片段', command=run24)
            btn24.place(relx=0.3, rely=0.28, relwidth=0.4, relheight=0.03)

            btn28 = Button(root, text='退出程序', command=run0)
            btn28.place(relx=0.3, rely=0.32, relwidth=0.4, relheight=0.03)

        if mark=="lifeline":
            btn11 = Button(root, text='1.输入一条消息', command=run11)
            btn11.place(relx=0.3, rely=0.15, relwidth=0.4, relheight=0.05)

            btn12= Button(root, text='2.结束输入消息', command=run12)
            btn12.place(relx=0.3, rely=0.22, relwidth=0.4, relheight=0.05)
            
            btn29= Button(root, text='退出程序', command=run0)
            btn29.place(relx=0.3, rely=0.29, relwidth=0.4, relheight=0.05)

        if mark=="strict":
            btn13= Button(root, text='1.创建一个区域', command=run13)
            btn13.place(relx=0.3, rely=0.15, relwidth=0.4, relheight=0.05)



            btn15 = Button(root, text='2.退出这个片段', command=run15)
            btn15.place(relx=0.3, rely=0.22, relwidth=0.4, relheight=0.05)

            btn30 = Button(root, text='退出程序', command=run0)
            btn30.place(relx=0.3, rely=0.29, relwidth=0.4, relheight=0.05)

        if mark=="par":
            btn16= Button(root, text='1.创建一个区域', command=run13)
            btn16.place(relx=0.3, rely=0.15, relwidth=0.4, relheight=0.05)


            btn18 = Button(root, text='2.退出这个片段', command=run15)
            btn18.place(relx=0.3, rely=0.22, relwidth=0.4, relheight=0.05)

            btn31 = Button(root, text='退出程序', command=run0)
            btn31.place(relx=0.3, rely=0.29, relwidth=0.4, relheight=0.05)
        
        if mark=="critical":
            btn19= Button(root, text='1.创建一个区域', command=run13)
            btn19.place(relx=0.3, rely=0.15, relwidth=0.4, relheight=0.05)


            btn22 = Button(root, text='2.退出这个片段', command=run15)
            btn22.place(relx=0.3, rely=0.22, relwidth=0.4, relheight=0.05)

            btn32 = Button(root, text='退出程序', command=run0)
            btn32.place(relx=0.3, rely=0.29, relwidth=0.4, relheight=0.05)

        

        self.canvas = tk.Canvas(root, width=576, height=396, bg="#fff")#创建画布，在画布上画出顺序图，让用户知道自己进行到了哪一步
        self.canvas.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.55)


        self.fondlifeline()
        self.draw()
        



        root.mainloop()

        return self.send
    def drawfragment(self,topleft_x,topleft_y,bottemright_x,bottemright_y,txt):#画片段的函数
        self.canvas.create_rectangle(topleft_x,topleft_y,bottemright_x,bottemright_y,width=1,outline="black")
        self.canvas.create_rectangle(topleft_x,topleft_y,topleft_x+40,topleft_y+20,width=1,outline="black")
        self.canvas.create_text(topleft_x+18,topleft_y+10, text = txt, fill="#000")

    def drawfragment1(self,topleft_x,topleft_y,bottemright_x,bottemright_y,txt):#当当前描述的事务是这个片段时画片段的函数
        self.canvas.create_rectangle(topleft_x,topleft_y,bottemright_x,bottemright_y,width=1,outline="red")
        self.canvas.create_rectangle(topleft_x,topleft_y,topleft_x+40,topleft_y+20,width=1,outline="red")
        self.canvas.create_text(topleft_x+18,topleft_y+10, text = txt, fill="#f00")

    def drawlifeline(self,x,txt):#画生命线的函数
        self.canvas.create_rectangle(x-20,10,x+20,50,width=1,outline="black")
        self.canvas.create_text(x,30, text =":"+ txt, fill="#000")
        self.canvas.create_line(x,50,x,396,fill="black",dash=(4,4))
    
    def drawmessage1(self,x1,y1,x2,y2,txt):#画消息的函数
        self.canvas.create_line(x1, y1, x2, y2, fill="#000")
        if x1<x2:
            self.canvas.create_line(x2-6, y2-3, x2, y2, fill="#000")
            self.canvas.create_line(x2-6, y2+3, x2, y2, fill="#000")
        else:
            self.canvas.create_line(x2, y2, x2+6, y2-3, fill="#000")
            self.canvas.create_line(x2, y2, x2+6, y2+3, fill="#000")
        self.canvas.create_text((x1+x2)/2,y2-10, text =txt, fill="#000")

    def drawmessage2(self,x1,y1,x2,y2,txt):#当当前描述的事务是这个消息时画消息的函数
        self.canvas.create_line(x1, y1, x2, y2, fill="#f00")
        if x1<x2:
            self.canvas.create_line(x2-6, y2-3, x2, y2, fill="#f00")
            self.canvas.create_line(x2-6, y2+3, x2, y2, fill="#f00")
        else:
            self.canvas.create_line(x2, y2, x2+6, y2-3, fill="#f00")
            self.canvas.create_line(x2, y2, x2+6, y2+3, fill="#f00")
        self.canvas.create_text((x1+x2)/2,y2-10, text =txt, fill="#f00")

    def fondlifeline(self):#找生命线的函数
        sum=len(self.messagelist)
        for i in range(sum):#通过遍历消息列表，将消息列表中出现过的消息首部和消息尾部作为生命线的名字记入生命线列表
            if self.messagelist[i][0] not in self.lifelinelist:#判断这个消息首部是否已经在生命线列表中，如果不在则将它加入
                self.lifelinelist.append(self.messagelist[i][0])
            if self.messagelist[i][1] not in self.lifelinelist:#判断这个消息尾部是否已经在生命线列表中，如果不在则将它加入
                self.lifelinelist.append(self.messagelist[i][1])
            
    def draw(self):#画布上画图的主函数，上面几个函数只是供它调用的工具函数
        sum_lifeline=len(self.lifelinelist)
        if sum_lifeline!=0:
            self.x_lifeline=556.0/(sum_lifeline+1)#因为画布大小是固定的所以每条生命线间的间距会随着生命线的增加而减小，从而达到可以一定程度无上限加生命线的目的，下面很多地方也用了这种思想，如每层片段x坐标的确定、片段和消息y坐标的确定
            for i in range(sum_lifeline):
                self.drawlifeline(10+(i+1)*self.x_lifeline,self.lifelinelist[i])
        sum_fragment=len(self.fragmentlist)#记录片段数量
        sum_message=len(self.messagelist)#记录消息数量
        if sum_fragment!=0:
            y_fragment_and_message=316.0/(sum_fragment*2+sum_message-1)#因为画布大小是固定的所以片段和消息的间距会随着片段和消息的增加而减小，从而达到可以一定程度无上限加消息和片段的目的，因为片段是两条线，所以这里片段的权重是2，消息的权重是1，且因为最外层片段不被记入所以总数减2

            maxcen=0#记录最大层数的参数
            for i in range(sum_fragment):#遍历片段列表得到最大层数
                if self.fragmentlist[i][5]>maxcen:
                    maxcen=self.fragmentlist[i][5]

            self.x_fragment=self.x_lifeline/(maxcen+1)#因为画布大小是固定的所以每层片段间的间距会随着最大层数的增加而减小，从而达到可以一定程度无上限加片段的目的
            
            x1=[int(i) for i in range(sum_fragment)]#记录片段右上角x坐标的参数
            y1=[int(i) for i in range(sum_fragment)]#记录片段右上角y坐标的参数
            x2=[int(i) for i in range(sum_fragment)]#记录片段左下角x坐标的参数
            y2=[int(i) for i in range(sum_fragment)]#记录片段左下角x坐标的参数
            
            
            for i in range(sum_fragment):#为每个片段算好右上角x坐标和左下角x坐标
                x1[i]=10+(self.fragmentlist[i][5])*self.x_fragment
                x2[i]=566-(self.fragmentlist[i][5])*self.x_fragment
            
            for i in range(sum_fragment):#为每个片段算好右上角y坐标和左下角y坐标
                y1[i]=70+self.fragmentlist[i][2]*y_fragment_and_message
                y2[i]=70+self.fragmentlist[i][4]*y_fragment_and_message
            
            for i in range(sum_fragment):
                if i==0:#如果是最外层框架则调用函数时输入固定值
                    if self.nowtime[0]=="fra" and self.nowtime[1]==i:#是当前描述的事务则调用可以把片段画红的函数
                        self.drawfragment1(10,70,566,386,self.fragmentlist[i][0])
                    else:
                        self.drawfragment(10,70,566,386,self.fragmentlist[i][0])
                else:#如果不是最外层框架则调用函数时根据片段自己的值来画大小
                    if self.nowtime[0]=="fra" and self.nowtime[1]==i:#是当前描述的事务则调用可以把片段画红的函数
                        self.drawfragment1(x1[i],y1[i],x2[i],y2[i],self.fragmentlist[i][0])
                    else:
                        self.drawfragment(x1[i],y1[i],x2[i],y2[i],self.fragmentlist[i][0])
        if sum_message!=0:
            y_fragment_and_message=316.0/(sum_fragment*2+sum_message-1)#因为画布大小是固定的所以片段和消息的间距会随着片段和消息的增加而减小，从而达到可以一定程度无上限加消息和片段的目的，因为片段是两条线，所以这里片段的权重是2，消息的权重是1，且因为最外层片段不被记入所以总数减2
            for i in range(sum_message):
                x1=0#记录消息首部x坐标的参数
                x2=0#记录消息尾部x坐标的参数
                y=0#记录消息y坐标的参数
                for i1 in range(sum_lifeline):
                    if self.messagelist[i][0]==self.lifelinelist[i1]:
                        x1=10+(i1+1)*self.x_lifeline#为每个消息计算消息首部的x坐标
                    if self.messagelist[i][1]==self.lifelinelist[i1]:
                        x2=10+(i1+1)*self.x_lifeline#为每个消息计算消息尾部的x坐标
                y=70+self.messagelist[i][3]*y_fragment_and_message#为每个消息计算y坐标
                if x1!=0 and x2!=0 and y!=0:
                    if self.nowtime[0]=="mes" and self.nowtime[1]==i:#是当前描述的事务则调用可以把消息画红的函数
                        self.drawmessage2(x1,y,x2,y,self.messagelist[i][2])
                    else:
                        self.drawmessage1(x1,y,x2,y,self.messagelist[i][2])
        if len(self.fenqu)!=0:
            y_fragment_and_message=316.0/(sum_fragment*2+sum_message-1)#分区虚线的y坐标会被消息和片段的数量影响但它的数量不会影响消息和片段的数量，因为分区虚线本身的高度值是一定高度值+0.5，不占权重
            for i in range(len(self.fenqu)):
                self.canvas.create_line(10+(self.fenqu[i][1])*self.x_fragment,70+self.fenqu[i][0]*y_fragment_and_message,566-(self.fenqu[i][1])*self.x_fragment,70+self.fenqu[i][0]*y_fragment_and_message,fill="black",dash=(4,4))

import Auxiliary_system_end
import Auxiliary_system_front
p=Auxiliary_system_front.Auxiliary_system_front()#创建picture的实例，picture是用以实现和用户人机交互的可视化界面类
def systemlist():#最初的菜单函数
    choice="0"
    str_end=""
    choice=p.work("list")#调用work方法并传入“list”这一当前状态值(当前处于哪个界面)，方法会反馈用户的选择
    if choice=="1":#当最外层框架为seq片段时
        str_end=seq_base()
    if choice=="2":#当最外层框架为strict片段时
        str_end=strict()
    if choice=="3":#当最外层框架为par片段时
        str_end=par()
    if choice=="4":#当最外层框架为critical片段时
        str_end=critical()

    Lab5=Auxiliary_system_end.Auxiliary_system_end()#创建lab5的实例，lab5是得到异步消息传递所以可能性的后端实现类
    Str=Lab5.work(str_end)#在从最外层框架退出后表示本次叙述结束，调用lab5的work函数，将通过用户描述产生的代码字符串传入，函数会反馈记录异步消息传递的所有可能性的字符串
    p.Str=Str#将记录异步消息传递的所有可能性的字符串传入picture的Str变量中，异步消息传递的所有可能性会在界面上显示

    choice=p.work("end")#调用work方法并传入“end”这一当前状态值(当前处于哪个界面)，方法会反馈用户的选择
    if choice=="5":#当用户要再次叙述时
        systemlist()
    if choice=="6":#当用户要退出时
        return
    return
    
    
def seq_base():#当处于seq片段或其他片段一个区域中时的函数
    choice=0
    index=-1#记录生命线应该插入在生命线列表中的位置的参数
    l=[]#生命线列表，存贮生命线的列表
    str_seq=""
    SUM=0#记录这个片段已经合并几个列表了，如果还没合并列表则只用加上这个列表而不用调用seq函数合并
    while choice!="2":#当choice为2时结束这一片段，所以要在choice不为2的前提下循环
        choice=p.work("seq")#调用work方法并传入“seq”这一当前状态值(当前处于哪个界面)，方法会反馈用户的选择
        if choice=="1":#当用户选择开始输入一条生命线上的消息时
            index=index+1
            l.append([])#在生命线列表中加一个新的列表来存储生命线上的消息
            choose="0"
            while choose!="2":#当用户选择2时会退出选择是否输入消息的界面，所以要在choose不为2的前提下循环
                choose=p.work("lifeline")#调用work方法并传入“lifeline”这一当前状态值(当前处于哪个界面)，方法会反馈用户的选择
                if choose=="1":#当用户选择输入消息时
                    u=p.work("enter_message")#调用work方法并传入“enter_message”这一当前状态值(当前处于哪个界面)，方法会反馈用户输入的消息
                    U=u.split(",")
                    l[index].append(U)#将消息存放在当前正在存储的生命线上
        if choice=="2":#当用户选择退出这个片段时
            sum_lifeline=len(l)
            for i in range(sum_lifeline):#遍历生命线列表将每条生命线以字符串代码的形式合并
                if SUM==0:
                    SUM=SUM+1
                    str_seq=str_seq+str(l[0])
                else:
                    SUM=SUM+1
                    str_seq="self.seq("+str_seq+","+str(l[i])+")"#将对生命线的合并先以字符串的形式记录
        if choice=="3":#当用户选择这个区域或seq片段接下来有critical片段时
            cr=critical()
            if SUM==0:
                    SUM=SUM+1
                    str_seq=str_seq+cr
            else:
                SUM=SUM+1
                str_seq="self.seq("+str_seq+","+cr+")"#将对critical片段的合并先以字符串的形式记录
        if choice=="4":#当用户选择这个区域或seq片段接下来有strict片段时
            cr=strict()
            if SUM==0:
                    SUM=SUM+1
                    str_seq=str_seq+cr
            else:
                SUM=SUM+1
                str_seq="self.seq("+str_seq+","+cr+")"#将对strict片段的合并先以字符串的形式记录
        if choice=="5":#当用户选择这个区域或seq片段接下来有par片段时
            cr=par()
            if SUM==0:
                    SUM=SUM+1
                    str_seq=str_seq+cr
            else:
                SUM=SUM+1
                str_seq="self.seq("+str_seq+","+cr+")"#将对par片段的合并先以字符串的形式记录
    return str_seq
def strict():#当处于strict片段时的函数
    choice="0"
    str_strict=""
    num_strict=0#记录合并的列表数，合并第一个不用调用strict函数
    while choice!="3":#choice为3表示要退出这个片段，所以循环要在choice不为3的前提下进行
        choice=p.work("strict")#调用work方法并传入“strict”这一当前状态值(当前处于哪个界面)，方法会反馈用户的选择
        v=""
        if choice=="3":#当用户选择退出这个片段时
            break
        if choice=="1":#当用户选择创建一个区域时
            v=seq_base()
        if choice=="2":#这个已经没有了，work方法不会反馈2
            v=par()
        num_strict=num_strict+1
        if num_strict==1:
            str_strict=str_strict+v
        else:
            str_strict="self.strict("+str_strict+","+v+")"#将对区域的合并先以字符串的形式记录
    return str_strict
def par():#当处于par片段时的函数
    choice="0"
    str_par=""
    num_par=0
    while choice!="3":#choice为3表示要退出这个片段，所以循环要在choice不为3的前提下进行
        choice=p.work("par")#调用work方法并传入“par”这一当前状态值(当前处于哪个界面)，方法会反馈用户的选择
        v=""
        if choice=="3":#当用户选择退出这个片段时
            break
        if choice=="1":#当用户选择创建一个区域时
            v=seq_base()
        if choice=="2":#这个已经没有了，work方法不会反馈2
            v=strict()
        num_par=num_par+1
        if num_par==1:
            str_par=str_par+v
        else:
            str_par="self.par("+str_par+","+v+")"#将对区域的合并先以字符串的形式记录
    return str_par
def critical():#当处于critical片段时的函数
    choice="0"
    str_critical=""
    num_critical=0
    while choice!="3":#choice为3表示要退出这个片段，所以循环要在choice不为3的前提下进行
        choice=p.work("critical")#调用work方法并传入“critical”这一当前状态值(当前处于哪个界面)，方法会反馈用户的选择
        v=""
        if choice=="3":#当用户选择退出这个片段时
            break
        if choice=="1":#当用户选择创建一个区域时
            v=seq_base()
        if choice=="2":#这个已经没有了，work方法不会反馈2
            v=strict()
        if choice=="4":#这个已经没有了，work方法不会反馈4
            v=par()
        num_critical=num_critical+1
        if num_critical==1:
            str_critical="self.critical("+v+")"
        else:
            str_critical="self.critical("+str_critical+","+v+")"#将对区域的合并先以字符串的形式记录
    return str_critical


systemlist()
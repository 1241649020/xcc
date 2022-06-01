import random
class Auxiliary_system_end():
    def seq(self,a,b):#对seq片段或其他片段一个区域中任意两条生命线的合并的函数
        same_number=0#记录两条生命线间相同消息的个数的参数
        for len_a in range(len(a)):#通过for循环遍历a,b两个列表，得到他们相同消息的个数
            for len_b in range(len(b)):
                if(a[len_a]==b[len_b]):
                    same_number=same_number+1
        num_list = [int(i) for i in range(len(a)+len(b)-same_number)]#创建列表，用于存储生命线合并后的结果，之后用结果列表指代，因为相同元素算一个，所以创建时要减去相同元素的数量
        index=0#记录结果列表进行到了哪个位置的参数
        index_a=0#记录生命线a进行到了哪个位置的参数
        index_b=0#记录生命线b进行到了哪个位置的参数
        same_number=0#将
        if len(a[0])>3 and len(a)==1:#在本程序的定义中正常生命线的每个元素都是长度为3的，而critical片段的元素长度大于3且长度为1，这里判断a是否为critical片段的列表
            num_list=[]#因为a是critical片段,将a,b必然没有相同元素，合并即可
            num_list.append(a[0])
            for x in range(len(b)):
                num_list.append(b[x])
            return num_list
        elif len(b[0])>3 and len(a)==1:#这里判断b是否为critical片段的列表
            num_list=[]#因为b是critical片段,将a,b必然没有相同元素，合并即可
            num_list.append(b[0])
            for x in range(len(a)):
                num_list.append(a[x])
            return num_list
        for len_a in range(len(a)):#遍历a,b两个列表
            for len_b in range(len(b)):
                if(a[len_a]==b[len_b]):#当找到a,b列表中相同的元素时确定结果列表要插入元素的的位置范围，这用buttom和top来限制
                    same_number=same_number+1
                    buttom=index#buttom为结果列表之前进行到的位置
                    top=len_a+len_b+1-same_number#top为结果列表之后要进行到的位置，因为相同元素算一个所以要减去相同元素的数量
                    num_list[top]=a[len_a]#这里也可以=b[len_b]效果是一样的
                    sum=top-buttom#要加入的元素总数
                    for num in range(sum):
                        if index_a==len_a:#当列表a的位置已经到达了相同元素的位置，a列表中已经没有元素可以取了，接下来只有从b中取元素加入结果列表即可
                            num_list[buttom+num]=b[index_b]
                            index_b=index_b+1
                            continue
                        if index_b==len_b:#当列表b的位置已经到达了相同元素的位置，b列表中已经没有元素可以取了，接下来只有从a中取元素加入结果列表即可
                            num_list[buttom+num]=a[index_a]
                            index_a=index_a+1
                            continue
                        if random.randint(0,1)==0:#因为两个生命线的相同元素间的元素是没有先后顺序的，所以通过random.randint(0,1)来随机从a，b列表中选择一个的元素插入结果列表，来达到没有先后顺序的效果，当随机到0则从a中取元素
                            num_list[buttom+num]=a[index_a]
                            index_a=index_a+1
                            continue
                        else:#当随机到1则从b中取元素
                            num_list[buttom+num]=b[index_b]
                            index_b=index_b+1
                            continue
                    index_a=len_a+1
                    index_b=len_b+1
                    index=top+1
        sum_a=len(a)-index_a#记录在a,b间最后一个相同元素之后a还有几个元素的参数
        sum_b=len(b)-index_b#记录在a,b间最后一个相同元素之后b还有几个元素的参数
        for num in range(sum_a+sum_b):#这个for循环和上面那个for循环同理，就是实现两个生命线间元素(除相同元素)没有先后顺序的效果
            if index_a==len(a):
                num_list[index+num]=b[index_b]
                index_b=index_b+1
                continue
            if index_b==len(b):
                num_list[index+num]=a[index_a]
                index_a=index_a+1
                continue
            if random.randint(0,1)==0:
                num_list[index+num]=a[index_a]
                index_a=index_a+1
                continue
            else:
                num_list[index+num]=b[index_b]
                index_b=index_b+1
                continue
        return num_list

    def strict(self,a,b):#将strict片段两个区域合并的函数
        return a+b
    def par(self,a,b):#将par片段两个区域合并的函数
        num_list = [int(i) for i in range(len(a)+len(b))]#创建列表，用于存储区域合并后的结果，和上面一样之后用结果列表指代
        index_a=0
        index_b=0
        for num in range(len(a)+len(b)):#和seq中for循环类似，只是这里实现的是并发的效果(实现过程是一致的)
            if index_a==len(a):
                num_list[num]=b[index_b]
                index_b=index_b+1
                continue
            if index_b==len(b):
                num_list[num]=a[index_a]
                index_a=index_a+1
                continue
            if random.randint(0,1)==0:
                num_list[num]=a[index_a]
                index_a=index_a+1
                continue
            else:
                num_list[num]=b[index_b]
                index_b=index_b+1
                continue
        return num_list
    def critical(self,a,b):#将critical片段中的两个区域合并的函数 ps：后面测试发现这个方法调用有问题，不过critical只有一个区域所以这个方法其实根本不用有
        c=self.seq(a, b)#将两个列表合并成一个列表
        s=[[]]
        for i in range(len(c)):
            s[0]=s[0]+c[i]#因为在本程序critical列表是用一个列表中只有一个元素且这个元素的大小大于3来表示的，因此要合并在一个元素中
        return s
    def critical(self,a):#将critical片段中只有一个区域情况下的函数
        s=[[]]
        for i in range(len(a)):
            s[0]=s[0]+a[i]
        return s
    def work(self,str_end):#正在的核心函数，前面的函数都是要调用的工具函数，str_end是Auxiliary_system传过来的根据用户描述创建的代码字符串
        Str=""#最后要输出的字符串，用于记录消息传递的一种种可能性
        s=[]#记录消息传递的列表，用来判断这种消息传递在之前有没有出现过
        for k in range(10000):#循环一万次来寻找消息传递的所以可能性，这个数量可以后期调控
            c=eval(str_end)#根据用户描述就可以反馈消息传递可能性的重要函数，能将代码字符串转化为代码运行，c为代码运行最终得到的消息列表
            if c not in s:#判断这个消息列表c是否已经出现过，没有出现过则记录并且将消息列表中的消息转化为可视形式记入字符串
                s.append(c)
                index=len(s)
                Str=Str+str(index)+". "
                for i in range(len(c)):#遍历消息列表c
                    if i!=(len(c)-1):#因为最后一个消息不用再加箭头所以要判断是否为最后一个消息
                        if len(c[i])==3:#这个消息不是critical片段时
                            Str=Str+c[i][2]+"->"
                            print(c[i][2]+"->",end="")
                        else:#这个消息是critical片段时
                            for z in range(int(len(c[i])/3)):
                                Str=Str+c[i][z*3+2]+"->"
                                print(c[i][z*3+2]+"->",end="")
                    else:
                        if len(c[i])==3:#这个消息不是critical片段时
                            Str=Str+c[i][2]
                            print(c[i][2],end="")
                        else:#这个消息是critical片段时
                            for z in range(int(len(c[i])/3)):
                                Str=Str+c[i][z*3+2]
                                print(c[i][z*3+2],end="")
                Str=Str+"\n"
                print("")
        return Str
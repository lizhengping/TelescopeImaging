import math

def diff_urad(destination,stateNow):
   twoPi_urad=2 * math.pi * 1000000
   Pi_urad=math.pi * 1000000
   diff=(destination-stateNow)
   if abs(diff)>Pi_urad:
       diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
   return  diff

def diff_deg(destination,stateNow):
    return  diff_urad(destination,stateNow)/5



def relatedDirection(xNum,yNum,step):
        xTarget = []
        yTarget = []
        x=[]
        V1 = 0
        V2 = 0

        for i in range(yNum):
            yTarget += [i * step] * xNum

        for j in range(xNum):
            x.append(step*j)

        r = [i for i in x]
        r.reverse()
        x2 =x + r

        if (yNum % 2) == 0:
             xTarget = x2 * int(yNum / 2)
        if (yNum % 2) == 1:
             xTarget = x2 * int(yNum / 2) + x
        xTarget=[-x+int((xNum-1)*step/2) for x in xTarget]
        yTarget=[-y+int((yNum-1)*step/2) for y in yTarget]
        return xTarget,yTarget

def Least_common_multiple(*args):
    Max_decimal_digits = count_float(args)
    # print(Max_decimal_digits)
    size = len(args)
    args = list(args)
    for i in range(size):
        args[i] =int( args[i] * int(math.pow(10, Max_decimal_digits)))
    # print(args)
    idx = 1
    i = int(args[0])
    # i = int(i * math.pow(10,Max_decimal_digits))
    while idx < size:
        j = args[idx]
        # j=int(j * math.pow(10,Max_decimal_digits))
        # print(j)
        # 用辗转相除法求i,j的最大公约数m
        b = i if i < j else j  # i，j中较小那个值
        a = i if i > j else j  # i,j中较大那个值
        r = b  # a除以b的余数
        while(r != 0):
            r = a % b
            if r != 0:
               a = b
               b = r
        f = i*j/b  # 两个数的最小公倍数
        i = f
        idx += 1
    return f/math.pow(10,Max_decimal_digits)

def count_float(args):
    Max=0
    size = len(args)
    idx = 0
    while idx < size:
        # print(idx)
        s=str(args[idx])
        if s.count('.') == 1: #小数有且仅有一个小数点
            left = s.split('.')[0]  #小数点左边（整数位，可为正或负）
            right = s.split('.')[1]  #小数点右边（小数位，一定为正）
            if Max<len(right):
                Max=len(right)
        idx += 1
    # print(Max)
    return Max

def get_range(T,n,t):
    range=T*n+t
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
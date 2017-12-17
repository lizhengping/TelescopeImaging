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
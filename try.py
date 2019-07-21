import math

abs_pos=10
count_per_uRad = 16777216/2/math.pi/1000000
judge = -1 if abs_pos<0 else 1
abs=int(count_per_uRad*abs_pos)%(judge* 16777216) ##youcuo
print(abs)
print(-1 %-10)
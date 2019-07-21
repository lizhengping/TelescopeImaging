from matplotlib import pyplot as plt
import sys
sys.path.append('../Plot')
import singlepicture  #直接全部引用了，注意
from scipy.optimize import curve_fit
import numpy as np

# definition
picture_fold='./photos/'
files=[]
Noise=0



binWidth=20 #0.5ns



def get_time_info(filename):
    #pixels_original_times = [[0 for x in range(0, xNum*xPicNum)] for y in range(0, yNum*yPicNum)]

    pixels_range= [[0 for x in range(0, xNum*xPicNum)] for y in range(0, yNum*yPicNum)]
    times=[]
    file = open(filename, 'r')

    #lines = file.readlines()
    line = file.readline()
    ProcessNum=0
    #for line in lines:
    while line!='':
        ProcessNum +=1
        print(ProcessNum)
        #t1 = time.time()
        line=line[:-1]
        line=line.split(',')

        for i in range(len(line)):
            if line[i] != '':
              line[i]=int(line[i])
            else:
              line[i]=0

        px=line[0]
        py=line[1]


        time_info = [x/100 for x in line[4:]]
        times.append(list(flatten(time_info)))


        #pixels_range[px][py] =get_accurate_range(find_ranges(time_info,binWidth)[0])
        line = file.readline()
    # print(len(times))
    times=list(flatten(times))
    plt.hist(times, 500, normed=0, facecolor='blue', alpha=0.5)
    plt.show()
    return pixels_range


def find_ranges(Pix_Data,L):
    Pix_Data.sort()
    sumMax = 0

    for i in range(len(Pix_Data)):
        D=Pix_Data[i]+L
        j=i
        Events=0
        rangeD = []

        while (j < len(Pix_Data)):

            if (Pix_Data[j] <= D):
                Events +=1
                rangeD.append(Pix_Data[j])
            j =j+1

        if (Events>sumMax):
            sumMax=Events
            Max_index=i
            rangeData=rangeD[:]

    #print(rangeData)
    return rangeData,Max_index,


def get_accurate_range(data):
    dataSum=0
    #print(data)
    for i in range(len(data)):
        dataSum +=data[i]
    data_range=dataSum/len(data)
    # print(data_range)
    return data_range


def plot_heatmap(pixel_Data,type="intensity"):

    xlabels=['' for i in range(xNum*xPicNum)]
    ylabels=['' for j in range(yNum*yPicNum)]

    for i in range(xPicNum):
        xlabels[i * xNum] = i
    for j in range(yPicNum):
        ylabels[j * yNum] = j

    if type=='intensity':
        singlepicture.draw_heatmap(pixel_Data, xlabels, ylabels)
    if type=='range':
        singlepicture.draw_heatmap(pixel_Data, xlabels, ylabels,user_defined=True,vmin=9502000,vmax=9506000)

    plt.show()
    plt.savefig('123.png')

# def auto_scale(Pixcel_Data)：
#     Data=[x/1000 for x in Pixcel_Data]
#     for i in range(12):
#         width=1
#
# def find_ranges(Pix_Data,L):
#     Pix_Data.sort()
#     sumMax = 0
#
#     for i in range(len(Pix_Data)):
#         D=Pix_Data[i]+L
#         j=i
#         Events=0
#         rangeD = []
#
#         while (j < len(Pix_Data)):
#
#             if (Pix_Data[j] <= D):
#                 Events +=1
#                 rangeD.append(Pix_Data[j])
#             j =j+1
#
#         if (Events>sumMax):
#             sumMax=Events
#             Max_index=i
#             rangeData=rangeD[:]
#
#     #print(rangeData)
#     return rangeData


def flatten(a):
    for each in a:
        if not isinstance(each, list):
            yield each
        else:
            yield from flatten(each)


def f_gauss(x, A, B, C, sigma):
    return A*np.exp(-(x-B)**2/(2*sigma**2)) + C

def fit(x,y):
    popt, pcov = curve_fit(f_gauss, x, y,p0=[9000,9000,1,1])
    # 获取popt里面是拟合系数
    a = popt[0]
    b = popt[1]
    c=  popt[2]
    d=  popt[3]

    return b,2*d

def threeD(filename):

    pixels_range=get_time_info(filename)
    His_range=list(flatten(pixels_range))

    binW=100
    n, bins, patches=plt.hist(His_range, binW, normed=0, facecolor='blue', alpha=0.5)

    # print(n)
    # x_1=[i for i in range(binW)]
    # fit(binW,n)
    plt.show()
    plot_heatmap(pixels_range, "intensity")
    plot_heatmap(pixels_range, "range")


xNum = 64
yNum = 64

xPicNum = 1
yPicNum = 1

if __name__ == '__main__':
    #Pix_Data = [1, 3, 2,49,45,23,2,34,45,6,5,6]
    filename = '/Users/Benli/projects/polt/pluseIndexs1_sub.csv'
    threeD(filename)


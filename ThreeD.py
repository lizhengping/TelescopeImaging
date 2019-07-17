import singlepicture  #直接全部引用了，注意
import os
import sys
import Tool
import time
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# definition
picture_fold='./photos/'
files=[]
Noise=0
xNum=64
yNum=64


binWidth=1 #1ns
period=int(10000*(1/binWidth))+1#（10us-ns）

def find_peak(pixel_data):
    maxSum=1
    maxNum=period-2

    for i in range(len(pixel_data)-1):
        pixel_data_Sum=pixel_data[i]+pixel_data[i+1]
        if (pixel_data_Sum>maxSum):
            maxSum=pixel_data_Sum
            maxNum=i
    #print(maxNum,maxSum)
    return maxNum,maxSum

def get_accurate_range(data):
    dataSum=0
    #print(data)
    for i in range(len(data)):
        dataSum +=data[i]
    data_range=dataSum/len(data)

    return data_range


def get_time_info(filename):
    pixels_original_times = [[0 for x in range(0, xNum*xPicNum)] for y in range(0, yNum*yPicNum)]
    pixels_counts =  [[0 for x in range(0, xNum*xPicNum)] for y in range(0, yNum*yPicNum)]
    pixels_range= [[0 for x in range(0, xNum*xPicNum)] for y in range(0, yNum*yPicNum)]

    counts_Histo = [0 for x in range(0, period)]
    count_Statistics=[[] for x in range(0, period)]

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



        #time_info=[x for x in line[3:]]  #ps [x/1000 for x in line[3:]]

        time_info = [x/1000 for x in line[4:]]

        pixels_original_times[px][py]=time_info
        #print(px,py)


        for k in time_info:
            binIndex=int(round(k/binWidth,0))
            #print(binIndex)
            counts_Histo[binIndex] +=1
            count_Statistics[binIndex].append(k)


        #t2 = time.time()
        maxIndex,pixels_counts[px][py]=find_peak(counts_Histo)
        #print(maxIndex,'    ',pixels_counts[px][py])


        #print(count_Statistics[maxIndex]+count_Statistics[maxIndex+1])
        if (maxIndex==period-2):
            pixels_range[px][py]=10000
        else:
            pixels_range[px][py]=get_accurate_range(count_Statistics[maxIndex]+count_Statistics[maxIndex+1])



        counts_Histo = [0 for x in range(period)]
        count_Statistics = [[] for x in range(period)]


        #print('time   ',t2 - t1)

        line = file.readline()

    return pixels_counts,pixels_range

def plot_heatmap(pixel_Data,type="intensity"):

    xlabels=['' for i in range(xNum*xPicNum)]
    ylabels=['' for j in range(yNum*yPicNum)]

    for i in range(xPicNum):
        xlabels[i * xNum] = i
    for j in range(yPicNum):
        ylabels[j * yNum] = j

    if type=='intensity':
      singlepicture.draw_heatmap(pixel_Data, xlabels, ylabels,user_defined=True,vmin=0,vmax=3000)

    if type=='range':
      singlepicture.draw_heatmap(pixel_Data, xlabels, ylabels,user_defined=True,vmin=9502,vmax=9506)
    #plt.show(block=False)
    plt.show()
    plt.savefig('123.png')

def plot_3D(data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(yNum*yPicNum):
        for j in range(xNum*xPicNum):

            # ax.scatter([i] * length, [j] * length, pixel[i * 32 + j], s=1, c='r', marker='.')
            # ax.scatter([i] * length, [j] * length, pixel[i * 32 + j][:length], s=0.1, c='r', marker='.')
            if (data[i][j]>=9500 and data[i][j]<=9505):
                ax.scatter(i, j, data[i][j], s=1, c='r', marker='o')
                print(i*xNum+j)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()
    plt.savefig('photos/' + foldname + '/' + '3D_Draw' + '.png')

def flatten(a):
    for each in a:
        if not isinstance(each, list):
            yield each
        else:
            yield from flatten(each)

if __name__ == '__main__' :

    # if len(sys.argv)==4:
    #     for i in range(1, len(sys.argv)):
    #         foldname=sys.argv[1]
    #         xPicNum=sys.argv[2]
    #         yPicNum=sys.argv[3]
    # else:
    #     print('parameters error')
    #     foldname = 'yancong'

    #     xPicNum = 5
    #     yPicNum = 5
    xPicNum=1
    yPicNum=1
    t1 = time.time()
    #wholepicture_info = [[0 for x in range(0, xNum * xPicNum)] for y in range(0, yNum * yPicNum)]
    #all_pixel_count = [[0 for x in range(0, xNum * xPicNum)] for y in range(0, yNum * yPxicNum)]
    #filename = 'photos/'+foldname+'/WholePicture'+foldname+'.csv'
    filename='pluseIndexs1_sub.csv'
    #filename='pixelsample.csv'
    pixels_counts,pixels_range=get_time_info(filename)
    t2 = time.time()
    print(t2 - t1)
    plot_heatmap(pixels_counts,"intensity")
    plot_heatmap(pixels_range,"range")

    His_range = list(flatten(pixels_range))
    binW = 100
    #n, bins, patches = plt.hist(His_range, binW, normed=0, facecolor='blue', alpha=0.5)
    plt.show()
    #plot_3D(pixels_range)

    Gx=range(64)
    Gy=pixels_range[30]
    plt.plot(Gx,Gy);
    plt.show()

    #out_put_Data(wholepicture_info)
    #out_put_Data(wholepicture_info)

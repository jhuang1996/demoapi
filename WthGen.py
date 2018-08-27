# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 11:18:00 2018

@author: SDLab- Jung Huang, Bing-Chen JHONG
"""
#Mean_MonRain=[13.760697674418617, 14.742602040816315, 14.850918635170624, 14.941964285714285, 19.22629969418961, 19.959523809523816, 23.06584158415842, 31.703846153846168, 43.295770392749304, 40.233509234828531, 26.63084577114423, 17.164878048780466]
Mean_MonTemp=[10.23951612903225, 10.416071428571406, 12.845806451612907, 16.225999999999992, 19.337741935483876, 21.728833333333334, 23.234032258064495, 22.918064516129, 20.969000000000005, 17.909032258064542, 15.227500000000003, 11.889677419354831]
#STD_MonRain=[16.984043523171138, 16.585851062706478, 17.240913935442574, 20.010919511931732, 28.460772607911331, 28.739217341094822, 47.388279993342032, 67.066261039530772, 68.792614786617236, 69.386170415589376, 43.675905487810937, 22.094143040463123]
STD_MonTemp=[3.5504206599560986, 3.7438605354878889, 3.9965144282790055, 3.5570199137292842, 2.5737812144497298, 1.9498252841957124, 0.93982832968686369, 0.93432542287881104, 1.9724956273715799, 2.3084240607220994, 3.0896807413280332, 3.5152556772711292]
Correl_MonTemp=[0.60092610659415169, 0.62072877064348075, 0.61162876255170517, 0.5949574148981881, 0.56811541025748646, 0.73937223937768715, 0.55300412139889932, 0.5103224821533372, 0.80360425053959528, 0.7391783120658294, 0.68144520828336907, 0.64295279475109124]
#alpha=[0.8516742252119287, 1.1714692031512575, 0.94393150137153525, 0.6639612917536224, 0.62553411913355128, 0.60206872944681789, 0.59407390542579008, 0.53009405677429278, 0.5754460967992443, 0.54708050950328224, 0.92759124503427259, 0.79626751164169207]
#beta=[9.6927439749512434, 12.862012745947267, 11.114036289121742, 16.583156649749576, 23.2423556635068, 25.366880857237653, 24.51513067237159, 26.826267817212759, 47.902518043262546, 20.799320613469519, 20.322806944907946, 12.63144795778085]
#Pw=[0.69354838709677424, 0.69999999999999996, 0.61451612903225805, 0.56000000000000005, 0.52741935483870972, 0.48999999999999999, 0.32580645161290323, 0.41935483870967744, 0.55166666666666664, 0.6112903225806452, 0.67000000000000004, 0.66129032258064513]
#Pww=[ 0.81860465116279069, 0.83673469387755106, 0.78740157480314965, 0.74404761904761907, 0.70948012232415902, 0.69047619047619047, 0.57425742574257421, 0.63846153846153841, 0.74320241691842903, 0.78364116094986802, 0.8159203980099502, 0.79756097560975614]
#Pwd=[0.38421052631578945, 0.40476190476190477, 0.33891213389121339, 0.34469696969696972, 0.32081911262798635, 0.30065359477124182, 0.20813397129186603, 0.26111111111111113, 0.2899628252788104, 0.34024896265560167, 0.37373737373737376, 0.40000000000000002]

import random
import math
import numpy
from scipy.stats import gamma
from sklearn import  linear_model
import json
import csv
#import matplotlib.pyplot as plt

def prec(para1,para2,method):
    RandNum2 = random.random()
    if method=='expon':
        #para1 is mean
        Prec = para1 * ( - math.log(1 - RandNum2) )
    elif method=='weibull':
        #para1 is mean
        Prec = (para1*(-math.log(1-RandNum2))**0.75)/1.191
    #elif method == 'dweibull':
        ##para1 is shape; para2 is scale
        #Prec=para2*((-math.log(1-RandNum2))**(1/para1))
    elif method=='gamma':
        #para1 is mean; para2 is std
        theta= (para2**2) / para1
        k= para1 / theta
        Prec= gamma.rvs(a=k,scale=theta)
    return Prec

def monthWG_prec(month, NumDay, Mean_MonRain,STD_MonRain, Pw, Pww, Pwd,method):
    RandNum1 = random.random()
    Jug_R = 0
    Prec = [0.0 for i in range(NumDay)]
    if RandNum1 < Pw[month]:    # The first day of a month
        Jug_R = 1           # rainy day
        Prec[0]=prec(Mean_MonRain[month],STD_MonRain[month],method)    
    for i in range(1,NumDay):
        RandNum3 = random.random()
        if (Jug_R == 1) and (RandNum3 < Pww[month]):
            Prec[i] = prec(Mean_MonRain[month],STD_MonRain[month],method)
            Jug_R == 1           # rainy day
        elif (Jug_R == 0) and (RandNum3 < Pwd[month]):
            Prec[i] = prec(Mean_MonRain[month],STD_MonRain[month],method)
            Jug_R == 1           # rainy day
        else:
            Prec[i] = 0
            Jug_R = 0
    return Prec

def monthWG_temp(month, NumDay, Mean_MonthTemp, STD_MonthTemp,Correl_MonthTemp):
    Temp = []
    preTemp=Mean_MonthTemp[month]   
    Temp.append(preTemp)
    for i in range(1,NumDay):
        RandNum=numpy.random.normal()
        Temp.append(Mean_MonthTemp[month]+Correl_MonthTemp[month]*(preTemp-Mean_MonthTemp[month])+RandNum*STD_MonthTemp[month]*(1-Correl_MonthTemp[month]**2)**0.5)
    return Temp

def YearWG_prec(Years,Mean_MonRain, STD_MonRain,Pw, Pww, Pwd,method):
    Month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    Output=[]
    for k in range(Years):
        for i in range(12):
            temp=monthWG_prec(i, Month[i], Mean_MonRain, STD_MonRain,Pw, Pww, Pwd,method)
            for j in range(len(temp)):
                Output.append(temp[j])
        #Output.append(monthWG(i, Month[i], Mean_MonRain, Pw, Pww, Pwd))
    return Output

def YearWG_temp(Years,Mean_MonTemp, STD_MonTemp,Correl_MonTemp):
    Month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    Output=[]
    for k in range(Years):
        for i in range(12):
            temp=monthWG_temp(i,Month[i],Mean_MonTemp, STD_MonTemp,Correl_MonTemp)
            for j in range(len(temp)):
                Output.append(temp[j])
        #Output.append(monthWG(i, Month[i], Mean_MonRain, Pw, Pww, Pwd))
    return Output

def exportToTXT(filename,result):
    info=[]
    info.append("* MH (Multifield Hourly Data Format)")
    info.append("* 以 '*' 字元開頭的文字為格式說明")
    info.append("* 以 '#' 字元開頭的文字為氣象資料欄位標題列7個字元一組")
    info.append("********************************************************************************")
    info.append("* 格式說明:")
    info.append("* 站碼(stno) 時間(rrr-yyyy-mm-dd)  氣象資料欄位")
    info.append("* 1~6       8~18              第19個字元開始每個氣象要素(欄位)7個字元")
    info.append("* rrr:執行次數")
    info.append("* yyyy:設計年")
    info.append("* mm:月")
    info.append("* dd:日")
    info.append("********************************************************************************")
    info.append("* 欄位標題說明:")
    info.append("* PP01 降水量(mm)")
    info.append("* TX01 氣溫(℃)")
    info.append("********************************************************************************")
    info.append("# stno\trrr-yyyy-mm-dd\tPP01\tTX01")
    for i in range(len(result)):
        r=result[i]
        info.append("{:6s}\t{:14s}\t{:.2f}\t{:.2f}".format(r['stno'],r['rrr-yyyy-mm-dd'],r['PP01'],r['TX01']))
    f = open(filename+'.txt', 'w')
    for i in range(1,len(info)):
        f.write(str(info[i])+'\n')
    f.close()

def exportToJSON(filename, result):
    with open(filename+'.json', 'w') as outfile:
        json.dump(result, outfile)
    outfile.close()

def exportToCSV(filename,result):
    fieldnames = ['stno', 'rrr-yyyy-mm-dd', 'PP01', 'TX01']
    f = open(filename+'.csv', 'w')
    csvCursor = csv.DictWriter(f, fieldnames=fieldnames)
    csvCursor.writeheader()
    for i in range(len(result)):
        csvCursor.writerow(result[i])
    f.close()
    
def return_nearest(value):
    value_s=math.floor(value*10)/10
    value_m=value_s+0.05
    value_l=value_s+0.1
    c_value=0
    if abs(value-value_s)<=abs(value-value_m) and abs(value-value_s)<=abs(value-value_l):
        c_value=value_s
    elif abs(value-value_m)<=abs(value-value_l):
        c_value=value_m
    else:
        c_value=value_l
    return c_value

def setAR5ClimateScenarios(lng,lat,Mean,RCP,GCM,time,wType):
    c_lng=return_nearest(lng)
    #print(c_lng)
    c_lat=return_nearest(lat)
    #print(c_lat)
    tmp=[]
    filename='ar5_'+RCP+'_'+wType+'_'+GCM+'_'+str(time)+str(time+19)+'_全臺.txt'
    #print(filename)
    f=open(filename,'r')
    for line in f:
        data=line.split()
        if float(data[0])==c_lng and float(data[1])==c_lat:
            tmp=data
    f.close()
    #print(Mean)
    #print(tmp)
    FutureMean=[]
    if wType=='temp':
        for i in range(12):
            FutureMean.append(Mean[i]+float(tmp[2+i]))
    elif wType=='rain':
        for i in range(12):
            FutureMean.append(Mean[i]*(100.0+float(tmp[2+i]))/100)
    return FutureMean

def generate(StationID,run,year,prec,temp):
    data=[]
    Totalmonth=12
    MonthofDate = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    count=0
    for y in range(1,year+1):
        for m in range(1,Totalmonth+1):
            month=MonthofDate[m-1]
            for d in range(1,month+1):
                time="{:03d}-{:04d}-{:02d}-{:02d}".format(run,y,m,d)
                p=round(prec[count],2)
                t=round(temp[count],2)
                wg_dict = {'stno':str(StationID), 'rrr-yyyy-mm-dd': time, 'PP01': p, 'TX01': t}
                data.append(wg_dict)
                count=count+1
    return data
 
def LR_STD(Mean,STD,FutureMean):
    X = numpy.asarray(Mean)
    Y = numpy.asarray(STD)
    X=X.reshape(len(X),1)
    Y=Y.reshape(len(Y),1) 
    # Plot outputs
    #plt.scatter(X, Y,  color='black')
    #plt.title('Data')
    #plt.xlabel('Mean_MonTemp')
    #plt.ylabel('STD_MonTemp')
    #plt.xticks(())
    #plt.yticks(())
    #plt.show()
    # Create linear regression object
    regr = linear_model.LinearRegression()
    #Train the model using the training sets
    regr.fit(X, Y)
    #print(regr.coef_[0][0])
    #print(regr.intercept_[0])
    FutureSTD=[]
    for i in range(len(STD)):
        FutureSTD.append(regr.coef_[0][0]*FutureMean[i]+regr.intercept_[0])
    #print(FutureSTD)
    return FutureSTD


         
